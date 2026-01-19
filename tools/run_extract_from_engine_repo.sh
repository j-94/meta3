#!/usr/bin/env bash
set -euo pipefail

# Convenience wrapper to derive nomenclature/concepts from an engine repo checkout.
#
# Usage:
#   ENGINE_REPO=/path/to/meta3-engine-repo ./tools/run_extract_from_engine_repo.sh

ENGINE_REPO="${ENGINE_REPO:-}"
if [[ -z "$ENGINE_REPO" ]]; then
  echo "missing ENGINE_REPO" >&2
  exit 2
fi

python3 ./tools/extract_nomenclature.py --engine-repo "$ENGINE_REPO" --out-dir .

