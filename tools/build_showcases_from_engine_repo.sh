#!/usr/bin/env bash
set -euo pipefail

# Build/refresh the showcase artifacts in this repo using an engine repo checkout.
#
# Usage:
#   ENGINE_REPO=/path/to/meta3-engine-repo ./tools/build_showcases_from_engine_repo.sh
#
# Requirements:
# - python3
# - rust toolchain (for the engine's meta3-graph-core binaries)

ENGINE_REPO="${ENGINE_REPO:-}"
if [[ -z "$ENGINE_REPO" ]]; then
  echo "missing ENGINE_REPO" >&2
  exit 2
fi

if [[ ! -d "$ENGINE_REPO/meta3-graph-core" ]]; then
  echo "ENGINE_REPO missing meta3-graph-core/: $ENGINE_REPO" >&2
  exit 2
fi

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT_NOM="$ROOT/showcases/nomenclature"
OUT_CAP="$ROOT/showcases/capability-graph"
OUT_MIS="$ROOT/showcases/mission-bridge"
DOCS_NOM="$ROOT/docs/nomenclature"
DOCS_CAP="$ROOT/docs/capability-graph"
DOCS_MIS="$ROOT/docs/mission-bridge"
TMP="$ROOT/tmp/_showcase_tmp"

mkdir -p "$OUT_NOM" "$OUT_CAP" "$OUT_MIS" "$DOCS_NOM" "$DOCS_CAP" "$DOCS_MIS" "$TMP"

echo "[1/3] Extract curated nomenclature"
python3 "$ROOT/tools/extract_nomenclature.py" --engine-repo "$ENGINE_REPO" --out-dir "$ROOT" >/dev/null

cp -f "$ROOT/concepts/concepts.json" "$OUT_NOM/concepts.json"
cp -f "$ROOT/concepts/glossary.md" "$OUT_NOM/glossary.md"
cp -f "$ROOT/graphs/nomenclature.hypergraph.json" "$OUT_NOM/hypergraph.json"

echo "[2/3] Build capability graph + report (engine)"
CARGO_TARGET_DIR="$ENGINE_REPO/target" \
cargo run --quiet --manifest-path "$ENGINE_REPO/meta3-graph-core/Cargo.toml" \
  --bin graph_capability_graph -- \
  --catalog "$ENGINE_REPO/dist/meta3-engine-v0.5.0/config/capabilities.json" \
  --out "$TMP/capability.hypergraph.json" \
  --run-id showcase-capability-graph

CARGO_TARGET_DIR="$ENGINE_REPO/target" \
cargo run --quiet --manifest-path "$ENGINE_REPO/meta3-graph-core/Cargo.toml" \
  --bin capability_report -- \
  --catalog "$ENGINE_REPO/dist/meta3-engine-v0.5.0/config/capabilities.json" \
  --out "$TMP/capability_report.md" \
  --root "$ENGINE_REPO"

cp -f "$TMP/capability.hypergraph.json" "$OUT_CAP/hypergraph.json"
cp -f "$TMP/capability_report.md" "$OUT_CAP/capability_report.md"

echo "[3/4] Mission → Code bridge (measured)"
cp -f "$ENGINE_REPO/tests/graph_core/fixtures/hyper_small.json" "$OUT_MIS/hypergraph.json"
cp -f "$ENGINE_REPO/tests/graph_core/fixtures/mission_small.json" "$OUT_MIS/mission_graph.json"

CARGO_TARGET_DIR="$ENGINE_REPO/target" \
cargo run --quiet --manifest-path "$ENGINE_REPO/meta3-graph-core/Cargo.toml" \
  --bin merge_mission_hypergraph -- \
  --hyper "$OUT_MIS/hypergraph.json" \
  --mission "$OUT_MIS/mission_graph.json" \
  --out "$OUT_MIS/merged.hypergraph.json" \
  --scope full

python3 "$ENGINE_REPO/scripts/graph_core_eval.py" \
  --hyper "$OUT_MIS/hypergraph.json" \
  --mission "$OUT_MIS/mission_graph.json" \
  --merged "$OUT_MIS/merged.hypergraph.json" \
  --scope full \
  --min-precision 1.0 \
  --min-recall 1.0 \
  --out "$OUT_MIS/eval.json"

echo "[4/4] Render viewers (engine)"
CARGO_TARGET_DIR="$ENGINE_REPO/target" \
cargo run --quiet --manifest-path "$ENGINE_REPO/meta3-graph-core/Cargo.toml" \
  --bin render_hypergraph -- \
  --in "$OUT_NOM/hypergraph.json" --out "$TMP/nomenclature_view"

cp -f "$TMP/nomenclature_view/index.html" "$OUT_NOM/index.html"
cp -f "$TMP/nomenclature_view/hypergraph.dot" "$OUT_NOM/hypergraph.dot"
cp -f "$TMP/nomenclature_view/index.html" "$DOCS_NOM/index.html"

CARGO_TARGET_DIR="$ENGINE_REPO/target" \
cargo run --quiet --manifest-path "$ENGINE_REPO/meta3-graph-core/Cargo.toml" \
  --bin render_hypergraph -- \
  --in "$OUT_CAP/hypergraph.json" --out "$TMP/capability_view"

cp -f "$TMP/capability_view/index.html" "$OUT_CAP/index.html"
cp -f "$TMP/capability_view/hypergraph.dot" "$OUT_CAP/hypergraph.dot"
cp -f "$TMP/capability_view/index.html" "$DOCS_CAP/index.html"

CARGO_TARGET_DIR="$ENGINE_REPO/target" \
cargo run --quiet --manifest-path "$ENGINE_REPO/meta3-graph-core/Cargo.toml" \
  --bin render_hypergraph -- \
  --in "$OUT_MIS/merged.hypergraph.json" --out "$TMP/mission_view"

cp -f "$TMP/mission_view/index.html" "$OUT_MIS/index.html"
cp -f "$TMP/mission_view/hypergraph.dot" "$OUT_MIS/hypergraph.dot"
cp -f "$TMP/mission_view/index.html" "$DOCS_MIS/index.html"

echo "showcases_ok=1"
