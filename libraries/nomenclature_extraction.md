# Library: Nomenclature & Concepts Extraction

## Purpose
Derive the project’s **nomenclature** (terms) and **concepts** (definitions + evidence) from engine repo data.

This is the canonical way to avoid hand-writing terminology: you ingest the system’s own catalogs and system docs, then curate.

## Inputs
From an engine repo checkout:
- Capability catalog (default):
  - `dist/meta3-engine-v0.5.0/config/capabilities.json`
- System docs (default set):
  - `meta3-causal-kernel/SYSTEM_PROMPT.md`
  - `meta3-graph-core/SYSTEM_REPORT.md`
  - `meta3-graph-core/SYSTEM_PROMPT.md`

## Outputs (in this repo)
- `concepts/concepts.json`
- `concepts/glossary.md`
- `graphs/nomenclature.hypergraph.json`

## How To Run
```bash
ENGINE_REPO=/path/to/engine-repo \
./tools/run_extract_from_engine_repo.sh
```

## Curation Loop
The extractor is conservative and deterministic. You should:
- prune noisy terms
- add missing definitions for important concepts
- add alias links for synonymous terms

