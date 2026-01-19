# Capability & Module Report

Generated: `2026-01-19T19:56:42Z`

Catalog: `dist/meta3-engine-v0.5.0/config/capabilities.json`

## Overview

- Capability IDs: `11`
- Catalog entries: `14`
- Duplicate IDs: `3`

This is a human-readable view of the capability catalog: what each capability is, how it is triggered, and where it lives in the codebase.

## Capabilities (English)

### amplify_signal (`bin.amplify_signal`)

- What it does: Standalone Utility: amplify_signal
- How to invoke: `run amplify_signal [args]`
- Type: `binary`
- Source: `src/bin/amplify_signal.rs`

### antigravity_history_explorer (`bin.antigravity_history_explorer`)

- What it does: Standalone Utility: antigravity_history_explorer
- How to invoke: `run antigravity_history_explorer [args]`
- Type: `binary`
- Source: `src/bin/antigravity_history_explorer.rs`

### flux (`bin.flux`)

- What it does: Standalone Utility: flux
- How to invoke: `run flux [args]`
- Type: `binary`
- Source: `src/bin/flux.rs`

### interaction_hypergraph (`bin.interaction_hypergraph`)

- What it does: Standalone Utility: interaction_hypergraph
- How to invoke: `run interaction_hypergraph [args]`
- Type: `binary`
- Source: `src/bin/interaction_hypergraph.rs`

### negentropy (`bin.negentropy`)

- What it does: Standalone Utility: negentropy
- How to invoke: `run negentropy [args]`
- Type: `binary`
- Source: `src/bin/negentropy.rs`

### oracle (`bin.oracle`)

- What it does: Standalone Utility: oracle
- How to invoke: `run oracle [args]`
- Type: `binary`
- Source: `src/bin/oracle.rs`

### AGI Solver (`nstar.core.0`)

- What it does: Optimal Path Finding
- How to invoke: `'solve', 'agi', or 'optimal'`
- Type: `kernel_interception`
- Source: `src/nstar.rs`

### TSP (`nstar.core.0a`)

- What it does: Traveling Salesman Problem - Ruliad Way
- How to invoke: `'tsp', 'salesman', 'tour' / 'solve', 'learn', or 'optimize'`
- Type: `kernel_interception / kernel_interception`
- Source: `src/nstar.rs / src/nstar.rs`
- Variants:
  - 1. TSP (type `kernel_interception`, source `src/nstar.rs`)
  - 2. LEARNING SOLVER (type `kernel_interception`, source `src/nstar.rs`)

### Ruliad (`nstar.core.0b`)

- What it does: Formal Rewrite System - Wolfram Physics
- How to invoke: `'ruliad', 'rewrite', 'multiway' / 'tree', 'thought', 'hierarchy'`
- Type: `kernel_interception / kernel_interception`
- Source: `src/nstar.rs / src/nstar.rs`
- Variants:
  - 1. Ruliad (type `kernel_interception`, source `src/nstar.rs`)
  - 2. Thought Tree (type `kernel_interception`, source `src/nstar.rs`)

### Task Graph (`nstar.core.0c`)

- What it does: LLM-based Task Decomposition
- How to invoke: `'graph' or 'plan'  (for software engineering tasks) / 'chat' keyword - tracks conversation as a graph`
- Type: `kernel_interception / kernel_interception`
- Source: `src/nstar.rs / src/nstar.rs`
- Variants:
  - 1. Task Graph (type `kernel_interception`, source `src/nstar.rs`)
  - 2. Hybrid Chat (type `kernel_interception`, source `src/nstar.rs`)

### HyperGraph (`nstar.core.0d`)

- What it does: Meta6 Abstract Machine
- How to invoke: `'hyper', 'signal', or 'traverse'`
- Type: `kernel_interception`
- Source: `src/nstar.rs`

## Modules (Grouped by Source)

### `src/bin/amplify_signal.rs`

- Module summary: In a real scenario, we would call the LLM endpoint here with the file content.
- Capabilities:
  - `bin.amplify_signal` — amplify_signal (type `binary`)

### `src/bin/antigravity_history_explorer.rs`

- Module summary: Antigravity Conversation History State Explorer
- Capabilities:
  - `bin.antigravity_history_explorer` — antigravity_history_explorer (type `binary`)

### `src/bin/flux.rs`

- Module summary: FLUX: The Meta6 High-Fidelity Interface
- Capabilities:
  - `bin.flux` — flux (type `binary`)

### `src/bin/interaction_hypergraph.rs`

- Module summary: / --- DATA MODELS ---
- Capabilities:
  - `bin.interaction_hypergraph` — interaction_hypergraph (type `binary`)

### `src/bin/negentropy.rs`

- Module summary: / META3: OMNI-NEGENTROPY ENGINE (Recursive)
- Capabilities:
  - `bin.negentropy` — negentropy (type `binary`)

### `src/bin/oracle.rs`

- Module summary: / META3: THE ORACLE (Higher Mind Interface)
- Capabilities:
  - `bin.oracle` — oracle (type `binary`)

### `src/nstar.rs`

- Module summary: No module header comment found.
- Capabilities:
  - `nstar.core.0` — AGI Solver (type `kernel_interception`)
  - `nstar.core.0a` — TSP (type `kernel_interception`)
  - `nstar.core.0a` — LEARNING SOLVER (type `kernel_interception`)
  - `nstar.core.0b` — Ruliad (type `kernel_interception`)
  - `nstar.core.0b` — Thought Tree (type `kernel_interception`)
  - `nstar.core.0c` — Task Graph (type `kernel_interception`)
  - `nstar.core.0c` — Hybrid Chat (type `kernel_interception`)
  - `nstar.core.0d` — HyperGraph (type `kernel_interception`)

