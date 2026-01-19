#!/usr/bin/env python3
"""
Deterministic nomenclature & concept extractor for Meta3.

Inputs (from an ENGINE_REPO):
  - dist/.../capabilities.json (capability catalog)
  - meta3-causal-kernel/SYSTEM_PROMPT.md (conceptual manifesto)
  - meta3-graph-core/SYSTEM_REPORT.md (capability matrix + core terms)
  - meta3-graph-core/SYSTEM_PROMPT.md (graph-core operational prompt)

Outputs (into this canonical repo):
  - concepts/concepts.json
  - concepts/glossary.md
  - graphs/nomenclature.hypergraph.json  (Meta3 hypergraph schema)
"""

from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set, Tuple, Any


STOP_TERMS = {
    "meta3",
    "meta",
    "json",
    "yaml",
    "http",
    "https",
    "api",
    "cli",
    "github",
    "rust",
    "python",
}

DEFAULT_DENY_TERMS = {
    "constraints",
    "constraint",
    "content",
    "contains",
    "edges",
    "entities",
    "inputs",
    "outputs",
    "notes",
    "usage",
    "examples",
    "testing",
    "development",
    "quick start",
    "installation",
    "response protocol",
    "available capabilities",
    "critical reminders",
}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def slugify(text: str) -> str:
    s = text.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-{2,}", "-", s)
    return s.strip("-")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def first_sentence(text: str) -> str:
    t = " ".join(text.strip().split())
    if not t:
        return ""
    m = re.split(r"(?<=[.!?])\s+", t, maxsplit=1)
    return m[0].strip()


def extract_markdown_headings(md: str) -> List[str]:
    out: List[str] = []
    for line in md.splitlines():
        line = line.strip()
        if not line.startswith("#"):
            continue
        title = line.lstrip("#").strip()
        # Drop emoji / punctuation-only headings
        title = re.sub(r"[^\w\s\-\(\):/]+", "", title).strip()
        title = re.sub(r"\s+", " ", title).strip()
        if len(title) < 3:
            continue
        # Drop obvious section headings (too noisy for nomenclature)
        if re.match(r"^\d+(\.\d+)?\s+", title):
            continue
        if re.match(r"^[A-Z]\)\s+", title):
            continue
        if title.lower() in {
            "overview",
            "architecture",
            "usage",
            "notes",
            "examples",
            "constraints",
            "response protocol",
            "outputs",
            "inputs",
            "testing",
            "development",
            "advanced features",
            "quick start",
            "installation",
        }:
            continue
        if any(
            kw in title.lower()
            for kw in (
                "how to run",
                "how to",
                "template",
                "example",
                "quick",
                "usage",
                "outputs",
                "inputs",
                "testing",
                "validation",
            )
        ):
            continue
        out.append(title)
    return out


def extract_backticked_terms(md: str) -> List[str]:
    # Extract `like_this` and `Tool.Name` and `graph_capability_graph`
    return [m.group(1).strip() for m in re.finditer(r"`([^`]{2,80})`", md)]

def extract_inline_definitions(md: str) -> List[Tuple[str, str]]:
    """
    Extract simple Markdown list definitions of the form:
      - `term` — description
      - `term` - description
    """
    out: List[Tuple[str, str]] = []
    for line in md.splitlines():
        l = line.strip()
        m = re.match(r"^[-*]\s+`([^`]{2,80})`\s*[—-]\s*(.+)$", l)
        if not m:
            continue
        term = m.group(1).strip()
        desc = m.group(2).strip()
        if term and desc:
            out.append((term, desc))
    return out


def extract_markdown_table_terms(md: str) -> List[Tuple[str, str]]:
    """
    Extract 2-column (term, description) pairs from Markdown tables.
    Intended for sections like "Available Capabilities".
    """
    out: List[Tuple[str, str]] = []
    for line in md.splitlines():
        l = line.strip()
        if not (l.startswith("|") and "`" in l):
            continue
        # | `FileSystem.Write` | Write content to file | ...
        m = re.match(r"^\|\s*`([^`]{2,80})`\s*\|\s*([^|]{2,200})\|", l)
        if not m:
            continue
        term = m.group(1).strip()
        desc = m.group(2).strip()
        # Skip header rows
        if term.lower() in {"capability", "tool id", "id"}:
            continue
        if term and desc and not set(desc) <= {"-", " "}:
            out.append((term, desc))
    return out


def normalize_term(term: str) -> Optional[str]:
    t = term.strip()
    # Trim common markdown/list prefixes that may appear in backticked strings.
    t = re.sub(r"^[#>\-\*\s]+", "", t).strip()
    t = re.sub(r"^\d+(\.\d+)?\s+", "", t).strip()
    t = re.sub(r"^[A-Z]\)\s+", "", t).strip()
    t = t.replace("\u2014", "-").replace("\u2013", "-")
    t = re.sub(r"\s+", " ", t)
    if len(t) < 3 or len(t) > 80:
        return None
    if re.match(r"^\d", t):
        return None
    if re.match(r"^[A-Z]\)\s+", t):
        return None
    # Drop obvious paths
    if "/" in t or t.endswith(".rs") or t.endswith(".md") or t.endswith(".json"):
        return None
    # Drop raw commands (too noisy)
    if t.startswith("cargo ") or t.startswith("git ") or t.startswith("gh "):
        return None
    # Drop purely numeric
    if re.fullmatch(r"\d+(\.\d+)*", t):
        return None
    # Reduce stopwords
    if t.lower() in STOP_TERMS:
        return None
    return t


@dataclass(frozen=True)
class SourceRef:
    path: str
    kind: str


@dataclass
class Concept:
    id: str
    term: str
    definition: str
    category: str
    aliases: List[str]
    sources: List[SourceRef]


def load_curation(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def apply_curation(concepts: List[Concept], curation: Dict[str, Any]) -> List[Concept]:
    allow_raw = curation.get("allow_terms") or []
    deny_raw = curation.get("deny_terms") or []
    definitions = curation.get("definitions") or {}
    aliases = curation.get("aliases") or {}

    allow: Set[str] = {str(t).strip() for t in allow_raw if str(t).strip()}
    deny: Set[str] = {str(t).strip().lower() for t in deny_raw if str(t).strip()}
    deny |= DEFAULT_DENY_TERMS

    out: List[Concept] = []
    for c in concepts:
        term = c.term.strip()
        term_l = term.lower()

        # Always keep catalog-derived terms (capability names/types) unless explicitly denied.
        from_catalog = any(s.kind == "capability_catalog" for s in c.sources)
        if term_l in deny and not from_catalog:
            continue

        if allow and not from_catalog and term not in allow:
            continue

        # Apply definition overrides by exact term.
        if isinstance(definitions, dict) and term in definitions:
            c.definition = str(definitions[term]).strip()

        # Apply alias overrides by exact term.
        if isinstance(aliases, dict) and term in aliases:
            extra = [str(a).strip() for a in (aliases[term] or []) if str(a).strip()]
            c.aliases = sorted(set(c.aliases) | set(extra))

        out.append(c)

    return out


def ensure_seed_terms(concepts: List[Concept], curation: Dict[str, Any]) -> List[Concept]:
    allow_raw = curation.get("allow_terms") or []
    definitions = curation.get("definitions") or {}
    aliases = curation.get("aliases") or {}

    want: List[str] = [str(t).strip() for t in allow_raw if str(t).strip()]
    have: Set[str] = {c.term for c in concepts}

    out = list(concepts)
    for term in want:
        if term in have:
            continue
        c = Concept(
            id=f"concept:{slugify(term)}",
            term=term,
            definition=str(definitions.get(term, "")).strip() if isinstance(definitions, dict) else "",
            category="concept",
            aliases=sorted({str(a).strip() for a in (aliases.get(term, []) if isinstance(aliases, dict) else []) if str(a).strip()}),
            sources=[SourceRef(path="(curation)", kind="curation")],
        )
        out.append(c)
        have.add(term)
    return sorted(out, key=lambda c: c.id)

def apply_taxonomy(concepts: List[Concept], catalog_types: Set[str]) -> List[Concept]:
    # Mark known catalog type labels as taxonomy, plus any concept whose definition
    # is the catalog-type placeholder.
    for c in concepts:
        if c.term in catalog_types:
            c.category = "taxonomy"
        if c.definition.strip() == "A capability classification used in the catalog.":
            c.category = "taxonomy"
    return concepts


def merge_concept(
    concepts: Dict[str, Concept],
    term: str,
    definition: str,
    source: SourceRef,
    aliases: Optional[Iterable[str]] = None,
) -> None:
    cid = f"concept:{slugify(term)}"
    if cid not in concepts:
        concepts[cid] = Concept(
            id=cid,
            term=term,
            definition=definition.strip(),
            category="concept",
            aliases=sorted({a for a in (aliases or []) if a and a != term}),
            sources=[source],
        )
        return

    c = concepts[cid]
    if not c.definition and definition.strip():
        c.definition = definition.strip()
    if aliases:
        c.aliases = sorted(set(c.aliases) | {a for a in aliases if a and a != term})
    if source not in c.sources:
        c.sources.append(source)


def extract_from_capabilities_catalog(path: Path) -> List[Tuple[str, str]]:
    data = load_json(path)
    caps = data.get("capabilities") if isinstance(data, dict) else data
    if not isinstance(caps, list):
        return []
    out: List[Tuple[str, str]] = []
    for cap in caps:
        if not isinstance(cap, dict):
            continue
        name = cap.get("name") or cap.get("id")
        desc = cap.get("description") or ""
        if isinstance(name, str) and name.strip():
            out.append((name.strip(), first_sentence(str(desc))))
        cap_type = cap.get("type")
        if isinstance(cap_type, str) and cap_type.strip():
            out.append((cap_type.strip(), "A capability classification used in the catalog."))
    return out


def extract_catalog_types(path: Path) -> Set[str]:
    data = load_json(path)
    caps = data.get("capabilities") if isinstance(data, dict) else data
    if not isinstance(caps, list):
        return set()
    out: Set[str] = set()
    for cap in caps:
        if not isinstance(cap, dict):
            continue
        cap_type = cap.get("type")
        if isinstance(cap_type, str) and cap_type.strip():
            out.add(cap_type.strip())
    return out


def build_hypergraph(concepts: List[Concept], run_id: str) -> dict:
    nodes = []
    for c in concepts:
        nodes.append(
            {
                "id": c.id,
                "kind": "concept",
                "label": c.term,
                "data": {
                    "definition": c.definition,
                    "aliases": c.aliases,
                    "sources": [asdict(s) for s in c.sources],
                },
            }
        )

    # Very light structure: group by source kind.
    kinds = sorted({s.kind for c in concepts for s in c.sources})
    for k in kinds:
        nodes.append(
            {
                "id": f"source_kind:{k}",
                "kind": "source_kind",
                "label": k,
                "data": None,
            }
        )

    edges = []
    edge_i = 0
    for c in concepts:
        for s in c.sources:
            edges.append(
                {
                    "id": f"edge:derived_from:{edge_i}",
                    "kind": "derived_from",
                    "causes": [f"source_kind:{s.kind}"],
                    "effects": [c.id],
                    "data": {"path": s.path},
                }
            )
            edge_i += 1

    return {
        "id": "nomenclature",
        "nodes": nodes,
        "hyperedges": edges,
        "metadata": {
            "run_id": run_id,
            "generated_at": utc_now_iso(),
            "source": "nomenclature_extractor",
        },
    }


def render_glossary(concepts: List[Concept], run_id: str, engine_repo: str) -> str:
    lines: List[str] = []
    lines.append("# Meta3 Nomenclature & Concepts")
    lines.append("")
    lines.append(f"Generated: `{utc_now_iso()}`")
    lines.append(f"Run: `{run_id}`")
    lines.append(f"Engine repo: `{engine_repo}`")
    lines.append("")
    lines.append("This glossary is generated from engine repo data (capability catalogs + system docs).")
    lines.append("")

    taxonomy = [c for c in concepts if getattr(c, "category", "") == "taxonomy"]
    core = [c for c in concepts if getattr(c, "category", "") != "taxonomy"]

    if core:
        lines.append("## Concepts")
        lines.append("")
        lines.append("Core concepts and capabilities (curated + derived).")
        lines.append("")
        for c in core:
            lines.append(f"### {c.term}")
            lines.append("")
            if c.definition:
                lines.append(c.definition)
            else:
                lines.append("_Definition pending (add/curate)._")
            lines.append("")
            if c.aliases:
                lines.append(f"- Aliases: {', '.join(f'`{a}`' for a in c.aliases)}")
            lines.append("- Sources:")
            for s in sorted(c.sources, key=lambda x: (x.kind, x.path)):
                lines.append(f"  - `{s.path}` ({s.kind})")
            lines.append("")

    if taxonomy:
        lines.append("## Taxonomy")
        lines.append("")
        lines.append("System vocabulary that is primarily categorical/typing information (kept separate from concepts).")
        lines.append("")
        for c in taxonomy:
            lines.append(f"### {c.term}")
            lines.append("")
            if c.definition:
                lines.append(c.definition)
            else:
                lines.append("_Definition pending (add/curate)._")
            lines.append("")
            if c.aliases:
                lines.append(f"- Aliases: {', '.join(f'`{a}`' for a in c.aliases)}")
            lines.append("- Sources:")
            for s in sorted(c.sources, key=lambda x: (x.kind, x.path)):
                lines.append(f"  - `{s.path}` ({s.kind})")
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--engine-repo", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--catalog", default="dist/meta3-engine-v0.5.0/config/capabilities.json")
    ap.add_argument("--curation", default="concepts/curation.json")
    args = ap.parse_args()

    engine_repo = Path(args.engine_repo)
    out_dir = Path(args.out_dir)
    out_concepts = out_dir / "concepts" / "concepts.json"
    out_glossary = out_dir / "concepts" / "glossary.md"
    out_graph = out_dir / "graphs" / "nomenclature.hypergraph.json"

    sources: List[Tuple[Path, str]] = []
    sources.append((engine_repo / args.catalog, "capability_catalog"))
    sources.append((engine_repo / "meta3-causal-kernel" / "SYSTEM_PROMPT.md", "system_prompt"))
    sources.append((engine_repo / "meta3-graph-core" / "SYSTEM_REPORT.md", "system_report"))
    sources.append((engine_repo / "meta3-graph-core" / "SYSTEM_PROMPT.md", "graph_core_prompt"))

    concepts: Dict[str, Concept] = {}
    catalog_types: Set[str] = set()

    # 1) Capabilities catalog -> capability names and types as concepts
    cat_path = engine_repo / args.catalog
    if cat_path.exists():
        catalog_types = extract_catalog_types(cat_path)
        for term, desc in extract_from_capabilities_catalog(cat_path):
            t = normalize_term(term)
            if not t:
                continue
            merge_concept(
                concepts,
                t,
                desc,
                SourceRef(path=str(Path(args.catalog)), kind="capability_catalog"),
            )

    # 2) System docs -> headings + backticked terms
    for p, kind in sources:
        if not p.exists():
            continue
        txt = read_text(p)
        # Prefer direct "term — description" patterns when present.
        for term, desc in extract_inline_definitions(txt):
            t = normalize_term(term)
            if not t:
                continue
            merge_concept(concepts, t, first_sentence(desc), SourceRef(path=str(p.relative_to(engine_repo)), kind=kind))
        # Pull terminology from tables (e.g., semantic capability interface).
        for term, desc in extract_markdown_table_terms(txt):
            t = normalize_term(term)
            if not t:
                continue
            merge_concept(concepts, t, first_sentence(desc), SourceRef(path=str(p.relative_to(engine_repo)), kind=kind))
        for h in extract_markdown_headings(txt):
            t = normalize_term(h)
            if not t:
                continue
            merge_concept(concepts, t, "", SourceRef(path=str(p.relative_to(engine_repo)), kind=kind))
        for bt in extract_backticked_terms(txt):
            t = normalize_term(bt)
            if not t:
                continue
            merge_concept(concepts, t, "", SourceRef(path=str(p.relative_to(engine_repo)), kind=kind))

    # 3) Minimal curation rules: unify some common aliases
    alias_map = {
        "Hypergraph": ["State Hypergraph", "hypergraph"],
        "Receipts": ["receipt", "UTIR", "immutable evidence"],
        "UTIR": ["receipts", "artifact stream"],
        "LeJIT": ["JIT Verification", "Just-In-Time verification"],
    }
    for term, aliases in alias_map.items():
        t = normalize_term(term)
        if not t:
            continue
        merge_concept(
            concepts,
            t,
            "",
            SourceRef(path="(curation)", kind="curation"),
            aliases=aliases,
        )

    # Deterministic order
    concept_list = sorted(concepts.values(), key=lambda c: c.id)

    run_id = f"nomenclature-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"

    out_concepts.parent.mkdir(parents=True, exist_ok=True)
    out_glossary.parent.mkdir(parents=True, exist_ok=True)
    out_graph.parent.mkdir(parents=True, exist_ok=True)

    curation_path = out_dir / args.curation
    curation = load_curation(curation_path)
    concept_list = apply_curation(concept_list, curation)
    if curation:
        concept_list = ensure_seed_terms(concept_list, curation)
    concept_list = apply_taxonomy(concept_list, catalog_types)

    payload = {
        "version": "v1",
        "run_id": run_id,
        "generated_at": utc_now_iso(),
        "engine_repo": str(engine_repo),
        "curation": {
            "path": str(Path(args.curation)),
            "applied": bool(curation),
        },
        "inputs": [
            {"path": str(p.relative_to(engine_repo)) if p.exists() else str(p), "kind": kind, "exists": p.exists()}
            for (p, kind) in sources
        ],
        "concepts": [
            {
                "id": c.id,
                "term": c.term,
                "definition": c.definition,
                "category": getattr(c, "category", "concept"),
                "aliases": c.aliases,
                "sources": [asdict(s) for s in c.sources],
            }
            for c in concept_list
        ],
    }
    out_concepts.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    out_glossary.write_text(render_glossary(concept_list, run_id, str(engine_repo)), encoding="utf-8")
    out_graph.write_text(json.dumps(build_hypergraph(concept_list, run_id), indent=2) + "\n", encoding="utf-8")

    print(
        f"nomenclature_ok=1 concepts={len(concept_list)} out_concepts={out_concepts} out_glossary={out_glossary} out_graph={out_graph}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
