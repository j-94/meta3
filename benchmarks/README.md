# Benchmarks (Reality-Checked)

We track three external benchmark families (not reimplemented here):

1) **SWE-bench Verified (coding)** — real repos, real tests, patch quality.
2) **AgentBench (general agent)** — multi-step tool use in interactive environments.
3) **Agent-SafetyBench (safety)** — unsafe tool actions and policy adherence.

This repo’s purpose is not to claim SOTA on them by default.
Instead, we build an **engine-native composite** (“TriBench”) that captures the core *mechanics* of all three, with receipts and graphs.

## Meta3 TriBench (composite)

TriBench is a reproducible run that:
- executes **three tracks in parallel** via the engine (UTIR)
- produces **receipts** for everything
- emits **graphs + HTML viewers** for inspection

Tracks:
- **Code (SWE-like):** capability catalog → capability graph + English report + viewer
- **Agent (AgentBench-like):** mission graph → code hypergraph bridge + measured precision/recall + viewer
- **Safety (SafetyBench-like):** sandbox/path traversal block is attempted and recorded (expected failure)

Run it (from a checkout of this repo):
```bash
ENGINE_REPO=/path/to/meta3-engine-repo ./tools/run_tribench_via_engine.sh
```

Outputs:
- `showcases/tribench/utir/receipts/` (evidence)
- `showcases/tribench/tribench/index.html` (merged viewer)

