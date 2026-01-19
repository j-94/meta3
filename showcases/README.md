# Showcases

These are “muscle flex” demos: they produce **real artifacts** (English + graphs + viewers), not just claims.

## 1) Nomenclature → Concepts → Hypergraph → Viewer

- Purpose: derive project nomenclature from engine data, then render a navigable concept graph.
- Artifacts:
  - `showcases/nomenclature/glossary.md`
  - `showcases/nomenclature/concepts.json`
  - `showcases/nomenclature/hypergraph.json`
  - `showcases/nomenclature/index.html` (self-contained viewer)

## 2) Capability Catalog → Capability Graph + English Report

- Purpose: show what the system can do and where it lives, in both graph form and plain English.
- Artifacts:
  - `showcases/capability-graph/hypergraph.json`
  - `showcases/capability-graph/index.html` (self-contained viewer)
  - `showcases/capability-graph/capability_report.md`

## 3) Mission → Code Bridge (Measured)

- Purpose: merge a mission graph into a hypergraph and **measure** bridge correctness (precision/recall).
- Artifacts:
  - `showcases/mission-bridge/merged.hypergraph.json`
  - `showcases/mission-bridge/eval.json`
  - `showcases/mission-bridge/index.html` (self-contained viewer)

## 4) TriBench (Engine End-to-End)

- Purpose: run **code + agent + safety** tracks *in parallel* through the engine, producing receipts and a merged hypergraph viewer.
- Artifacts:
  - `showcases/tribench/utir.json`
  - `showcases/tribench/utir/receipts/`
  - `showcases/tribench/tribench.hypergraph.json`
  - `showcases/tribench/tribench/index.html`
