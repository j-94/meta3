# Library: Capability Report (English)

## Purpose
Generate a human-readable report describing capabilities/modules in plain English.

## Inputs
- Capability catalog JSON:
  - `dist/meta3-engine-v0.5.0/config/capabilities.json`

## Outputs
- Markdown report:
  - `tmp/capability_report.md`

## How To Run
```bash
CARGO_TARGET_DIR=target \
cargo run --manifest-path meta3-graph-core/Cargo.toml \
  --bin capability_report -- \
  --catalog dist/meta3-engine-v0.5.0/config/capabilities.json \
  --out tmp/capability_report.md \
  --root .
```

## Evidence
- Generator: `meta3-graph-core/src/bin/capability_report.rs`

