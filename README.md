# Canonical Repo (In-Tree Seed)

This directory is a **canonical seed** for standardizing Meta3’s reusable knowledge:

1. **Use-case libraries**: distilled “how-to” modules (inputs → process → outputs → evidence).
2. **Multi-agent role prompts**: stable agent roles that produce compatible artifacts.
3. **Canonical intellectual graph**: a minimal, regenerable hypergraph describing the system’s core concepts.

This is intentionally stored **in-tree** (not a separate Git repo) so it can evolve via PRs alongside the engine.

## Layout

- `canonical/libraries/` — use-case modules (Markdown)
- `canonical/agents/` — role prompts (Markdown)
- `canonical/graphs/` — canonical hypergraph seeds (JSON)
- `canonical/index.json` — machine-readable index

## Quality Bar

Each library module should include:
- Plain-English purpose
- Inputs + outputs
- “How to run” commands
- Evidence paths (graphs/reports/receipts)
- Failure modes and how to validate

