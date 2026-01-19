#!/usr/bin/env bash
set -euo pipefail

# Sync canonical content from a Meta3 engine repo into this standalone canonical repo.
#
# Usage:
#   ENGINE_REPO=/path/to/tmp-meta3-engine-test ./tools/sync_from_engine_repo.sh

ENGINE_REPO="${ENGINE_REPO:-}"
if [[ -z "$ENGINE_REPO" ]]; then
  echo "missing ENGINE_REPO (path to meta3 engine repo root)" >&2
  exit 2
fi

if [[ ! -d "$ENGINE_REPO/canonical" ]]; then
  echo "ENGINE_REPO does not contain canonical/: $ENGINE_REPO" >&2
  exit 2
fi

rsync -a --exclude='.DS_Store' "$ENGINE_REPO/canonical/" .
echo "sync_ok=1 engine_repo=$ENGINE_REPO"

