# Library: Mission Graph Merge (Bridging)

## Purpose
Merge a `mission_graph.json` (node/link graph) into a hypergraph and create `mission_ref` bridges so mission structure and code structure connect.

## Inputs
- Hypergraph JSON (code-oriented)
- Mission graph JSON (mission-oriented)

## Outputs
- Merged hypergraph JSON (with `mission_ref` edges)

## How To Run (Template)
```bash
CARGO_TARGET_DIR=target \
cargo run --manifest-path meta3-graph-core/Cargo.toml \
  --bin merge_mission_hypergraph -- \
  --hyper <hypergraph.json> \
  --mission <mission_graph.json> \
  --out <merged.json>
```

## Validation
- Use the eval harness in `scripts/graph_core_eval.sh`

