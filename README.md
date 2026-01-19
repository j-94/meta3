# Meta3 (Canonical)

This repo is the canonical home for **Meta3 nomenclature & concepts**, derived from engine repo data (catalogs + system docs) and then curated.

It contains:
- **Nomenclature pipeline**: deterministic extraction + curation.
- **Use-case libraries**: distilled “how-to” modules (inputs → process → outputs → evidence).
- **Multi-agent role prompts**: stable agent roles that exchange artifacts.
- **Concept graphs**: distilled hypergraphs (not filesystem scans).

This is intended to be used alongside the main engine repo, but lives as a standalone GitHub repo.

## Layout

- `concepts/` — generated concepts + curated overrides
- `libraries/` — use-case modules (Markdown)
- `agents/` — role prompts (Markdown)
- `graphs/` — distilled hypergraph outputs (JSON)
- `index.json` — machine-readable index

## Run End-to-End (Derive Concepts)

From a checkout of this repo:

```bash
ENGINE_REPO=/path/to/meta3-engine-repo \
./tools/run_extract_from_engine_repo.sh
```

Outputs:
- `concepts/concepts.json`
- `concepts/glossary.md`
- `graphs/nomenclature.hypergraph.json`

## Showcases (Impressive Outputs)

- `showcases/README.md` — what to look at
- `showcases/nomenclature/index.html` — explorable concept hypergraph viewer (local file)
- `showcases/capability-graph/index.html` — explorable capability graph viewer (local file)

If you enable GitHub Pages (Settings → Pages → “Deploy from a branch” → `/docs`):
- `/docs/index.html` becomes a landing page with links to the two viewers.

## Quality Bar

Each library module should include:
- Plain-English purpose
- Inputs + outputs
- “How to run” commands
- Evidence paths (graphs/reports/receipts)
- Failure modes and how to validate
