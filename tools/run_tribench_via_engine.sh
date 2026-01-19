#!/usr/bin/env bash
set -euo pipefail

# Runs TriBench through the engine end-to-end (UTIR executed by meta3-graph-core),
# producing receipts + per-track artifacts + a merged hypergraph viewer.
#
# Usage:
#   ENGINE_REPO=/path/to/meta3-engine-repo ./tools/run_tribench_via_engine.sh

ENGINE_REPO="${ENGINE_REPO:-}"
if [[ -z "$ENGINE_REPO" ]]; then
  echo "missing ENGINE_REPO" >&2
  exit 2
fi

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/showcases/tribench"
mkdir -p "$OUT"

RUN_ID="tribench-demo"
UTIR_PATH="$OUT/utir.json"

cat >"$UTIR_PATH" <<'JSON'
{
  "task_id": "tribench-demo",
  "description": "TriBench: run code/agent/safety tracks in parallel with receipts and render merged graphs",
  "operations": [
    {
      "type": "parallel",
      "max_concurrency": 4,
      "steps": [
        {
          "type": "shell",
          "command": "python3 tools/extract_nomenclature.py --engine-repo ../.. --out-dir . >/dev/null",
          "timeout": "300s",
          "working_dir": "_export/meta3-canonical",
          "env": {},
          "allow_network": false,
          "capture_output": true
        },
        {
          "type": "shell",
          "command": "mkdir -p _export/meta3-canonical/showcases/tribench/nomenclature && cp -f _export/meta3-canonical/concepts/concepts.json _export/meta3-canonical/showcases/tribench/nomenclature/concepts.json && cp -f _export/meta3-canonical/concepts/glossary.md _export/meta3-canonical/showcases/tribench/nomenclature/glossary.md && cp -f _export/meta3-canonical/graphs/nomenclature.hypergraph.json _export/meta3-canonical/showcases/tribench/nomenclature/hypergraph.json",
          "timeout": "300s",
          "working_dir": ".",
          "env": {},
          "allow_network": false,
          "capture_output": true
        },
        {
          "type": "shell",
          "command": "mkdir -p _export/meta3-canonical/showcases/tribench/capability && cargo run --quiet --manifest-path meta3-graph-core/Cargo.toml --bin graph_capability_graph -- --catalog dist/meta3-engine-v0.5.0/config/capabilities.json --out _export/meta3-canonical/showcases/tribench/capability/hypergraph.json --run-id tribench-demo && cargo run --quiet --manifest-path meta3-graph-core/Cargo.toml --bin capability_report -- --catalog dist/meta3-engine-v0.5.0/config/capabilities.json --out _export/meta3-canonical/showcases/tribench/capability/capability_report.md --root .",
          "timeout": "600s",
          "working_dir": ".",
          "env": {},
          "allow_network": false,
          "capture_output": true
        },
        {
          "type": "shell",
          "command": "mkdir -p _export/meta3-canonical/showcases/tribench/mission-bridge && cp -f tests/graph_core/fixtures/hyper_small.json _export/meta3-canonical/showcases/tribench/mission-bridge/hypergraph.json && cp -f tests/graph_core/fixtures/mission_small.json _export/meta3-canonical/showcases/tribench/mission-bridge/mission_graph.json && cargo run --quiet --manifest-path meta3-graph-core/Cargo.toml --bin merge_mission_hypergraph -- --hyper _export/meta3-canonical/showcases/tribench/mission-bridge/hypergraph.json --mission _export/meta3-canonical/showcases/tribench/mission-bridge/mission_graph.json --out _export/meta3-canonical/showcases/tribench/mission-bridge/merged.hypergraph.json --scope full && python3 scripts/graph_core_eval.py --hyper _export/meta3-canonical/showcases/tribench/mission-bridge/hypergraph.json --mission _export/meta3-canonical/showcases/tribench/mission-bridge/mission_graph.json --merged _export/meta3-canonical/showcases/tribench/mission-bridge/merged.hypergraph.json --scope full --min-precision 1.0 --min-recall 1.0 --out _export/meta3-canonical/showcases/tribench/mission-bridge/eval.json",
          "timeout": "600s",
          "working_dir": ".",
          "env": {},
          "allow_network": false,
          "capture_output": true
        },
        {
          "type": "conditional",
          "condition": {
            "type": "fs.write",
            "path": "../OUTSIDE_SANDBOX.txt",
            "content": "should be blocked",
            "mode": "0644",
            "create_dirs": false
          },
          "then_op": {
            "type": "shell",
            "command": "echo unexpected: sandbox write succeeded",
            "timeout": "5s",
            "working_dir": ".",
            "env": {},
            "allow_network": false,
            "capture_output": true
          },
          "else_op": null
        }
      ]
    },
    {
      "type": "shell",
      "command": "python3 _export/meta3-canonical/tools/tribench/merge_hypergraphs.py --run-id tribench-demo --out _export/meta3-canonical/showcases/tribench/tribench.hypergraph.json --inputs _export/meta3-canonical/showcases/tribench/nomenclature/hypergraph.json _export/meta3-canonical/showcases/tribench/capability/hypergraph.json _export/meta3-canonical/showcases/tribench/mission-bridge/merged.hypergraph.json",
      "timeout": "60s",
      "working_dir": ".",
      "env": {},
      "allow_network": false,
      "capture_output": true
    },
    {
      "type": "shell",
      "command": "cargo run --quiet --manifest-path meta3-graph-core/Cargo.toml --bin render_hypergraph -- --in _export/meta3-canonical/showcases/tribench/tribench.hypergraph.json --out _export/meta3-canonical/showcases/tribench/tribench",
      "timeout": "300s",
      "working_dir": ".",
      "env": {},
      "allow_network": false,
      "capture_output": true
    }
  ]
}
JSON

cd "$ENGINE_REPO"

mkdir -p "$OUT/utir"

GRAPH_SANDBOX_ROOT="$ENGINE_REPO" \
CARGO_TARGET_DIR="$ENGINE_REPO/target" \
cargo run --quiet --manifest-path meta3-graph-core/Cargo.toml --bin meta3-graph-core -- \
  --receipt --deterministic --receipt-dir "_export/meta3-canonical/showcases/tribench/utir" \
  < <(python3 -c 'import json; import sys; print(json.dumps(json.load(open(sys.argv[1], "r", encoding="utf-8"))))' "$UTIR_PATH")

# Copy viewer entrypoints into docs for GitHub Pages.
mkdir -p "$ROOT/docs/tribench"
cp -f "$OUT/tribench/index.html" "$ROOT/docs/tribench/index.html"

echo "tribench_ok=1 out=$OUT"
