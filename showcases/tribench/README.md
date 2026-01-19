# Showcase: TriBench (Code + Agent + Safety) — Engine End-to-End

This showcase runs **three tracks in parallel** using the Meta3 engine, and produces receipts + merged graphs.

Tracks:
1) **Code (SWE-like)**: capability catalog → capability graph + English report + viewer
2) **Agent (AgentBench-like)**: mission graph → code hypergraph bridge (precision/recall) + viewer
3) **Safety (SafetyBench-like)**: sandbox/path traversal block is attempted and recorded as expected evidence

Outputs:
- `showcases/tribench/utir.json` — the UTIR document executed by `meta3-graph-core`
- `showcases/tribench/utir/receipts/` — receipt.json evidence (deterministic mode)
- Per-track artifacts:
  - `showcases/tribench/nomenclature/`
  - `showcases/tribench/capability/`
  - `showcases/tribench/mission-bridge/`
- Merged graph:
  - `showcases/tribench/tribench.hypergraph.json`
  - `showcases/tribench/tribench/index.html`

Regenerate:
```bash
ENGINE_REPO=/path/to/meta3-engine-repo ./tools/run_tribench_via_engine.sh
```

