#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Set


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--inputs", nargs="+", required=True)
    args = ap.parse_args()

    nodes: List[dict] = []
    hyperedges: List[dict] = []
    seen_nodes: Set[str] = set()
    seen_edges: Set[str] = set()

    root_id = f"RUN:{args.run_id}"
    nodes.append({"id": root_id, "kind": "run", "label": args.run_id, "data": None})
    seen_nodes.add(root_id)

    edge_i = 0
    for p in args.inputs:
        g = load(Path(p))
        gid = g.get("id") or Path(p).stem
        sub_id = f"SUBGRAPH:{gid}"
        if sub_id not in seen_nodes:
            nodes.append({"id": sub_id, "kind": "subgraph", "label": str(gid), "data": {"path": p}})
            seen_nodes.add(sub_id)
        hid = f"edge:run_has_subgraph:{edge_i}"
        hyperedges.append({"id": hid, "kind": "run_has_subgraph", "causes": [root_id], "effects": [sub_id], "data": None})
        edge_i += 1

        for n in g.get("nodes", []):
            nid = n.get("id")
            if not nid or nid in seen_nodes:
                continue
            nodes.append(n)
            seen_nodes.add(nid)

        for e in g.get("hyperedges", []):
            eid = e.get("id")
            if not eid:
                continue
            # Avoid collisions by prefixing duplicates.
            if eid in seen_edges:
                eid = f"{gid}:{eid}"
                e = dict(e)
                e["id"] = eid
            if eid in seen_edges:
                continue
            seen_edges.add(eid)
            hyperedges.append(e)

    out = {
        "id": "tribench",
        "nodes": nodes,
        "hyperedges": hyperedges,
        "metadata": {"run_id": args.run_id, "generated_at": "", "source": "tribench_merge"},
    }
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

