# Library: Capability Graph (Catalog-Focused)

## Purpose
Build a capability hypergraph that reflects **what the system can do**, not the entire filesystem tree.

## Inputs
- Capability catalog JSON (ToolHub output or dist config):
  - `dist/meta3-engine-v0.5.0/config/capabilities.json`

## Outputs
- Hypergraph JSON:
  - `tmp/capability_graph.hypergraph.json`

## How To Run
```bash
CARGO_TARGET_DIR=target \
cargo run --manifest-path meta3-graph-core/Cargo.toml \
  --bin graph_capability_graph -- \
  --catalog dist/meta3-engine-v0.5.0/config/capabilities.json \
  --out tmp/capability_graph.hypergraph.json
```

## What It Contains (English)
- Capabilities as instances (handles duplicate catalog IDs)
- Grouping nodes (`capability_key`)
- Links to triggers, types, and source modules

## Evidence
- Generator: `meta3-graph-core/src/bin/graph_capability_graph.rs`
- Builder: `meta3-graph-core/src/capability_graph.rs`

