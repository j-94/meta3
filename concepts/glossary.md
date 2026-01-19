# Meta3 Nomenclature & Concepts

Generated: `2026-01-19T18:58:03Z`
Run: `nomenclature-20260119T185803Z`
Engine repo: `/Users/jobs/Desktop/tmp-meta3-engine-test`

This glossary is generated from engine repo data (capability catalogs + system docs).

## AGI Solver

Optimal Path Finding

- Sources:
  - `dist/meta3-engine-v0.5.0/config/capabilities.json` (capability_catalog)

## amplify_signal

Standalone Utility: amplify_signal

- Sources:
  - `dist/meta3-engine-v0.5.0/config/capabilities.json` (capability_catalog)

## antigravity_history_explorer

Standalone Utility: antigravity_history_explorer

- Sources:
  - `dist/meta3-engine-v0.5.0/config/capabilities.json` (capability_catalog)

## binary

A capability classification used in the catalog.

- Sources:
  - `dist/meta3-engine-v0.5.0/config/capabilities.json` (capability_catalog)

## Capability Catalog

A machine-readable list of what the system can do (capabilities), including triggers, types, and source modules.

- Aliases: `catalog`
- Sources:
  - `(curation)` (curation)

## Capability Graph

A hypergraph derived from the capability catalog that links capabilities to triggers, types, and source modules (not a filesystem 'contains' graph).

- Aliases: `graph_capability_graph`
- Sources:
  - `(curation)` (curation)

## capability_report

generate English capability/module report (`meta3-graph-core/src/bin/capability_report.rs`)

- Sources:
  - `meta3-graph-core/SYSTEM_PROMPT.md` (graph_core_prompt)

## Capability Report (English)

A human-readable report explaining what each capability/module does, how to invoke it, and where it is implemented.

- Aliases: `capability_report`
- Sources:
  - `(curation)` (curation)

## flux

Standalone Utility: flux

- Sources:
  - `dist/meta3-engine-v0.5.0/config/capabilities.json` (capability_catalog)

## graph_capability_graph

build **catalog-focused** capability hypergraph (`meta3-graph-core/src/bin/graph_capability_graph.rs`)

- Sources:
  - `meta3-graph-core/SYSTEM_PROMPT.md` (graph_core_prompt)

## graph_context_bundle

create context + tasks from a hypergraph (`meta3-graph-core/src/bin/graph_context_bundle.rs`)

- Sources:
  - `meta3-graph-core/SYSTEM_PROMPT.md` (graph_core_prompt)

## graph_harness_emit

append harness/loop nodes for auditability (`meta3-graph-core/src/bin/graph_harness_emit.rs`)

- Sources:
  - `meta3-graph-core/SYSTEM_PROMPT.md` (graph_core_prompt)

## graph_probe

summarize a hypergraph (`meta3-graph-core/src/bin/graph_probe.rs`)

- Sources:
  - `meta3-graph-core/SYSTEM_PROMPT.md` (graph_core_prompt)

## Graph Transducer Runtime

A runtime that consumes events, evaluates state transitions as graph deltas, validates them against invariants, and applies them while emitting durable evidence (receipts).

- Sources:
  - `(curation)` (curation)

## Graph.Mutate

Propose graph update

- Sources:
  - `meta3-causal-kernel/SYSTEM_PROMPT.md` (system_prompt)

## Graph.Query

Query the State Hypergraph

- Sources:
  - `meta3-causal-kernel/SYSTEM_PROMPT.md` (system_prompt)

## Hybrid Chat

LLM + Graph Tracking

- Sources:
  - `dist/meta3-engine-v0.5.0/config/capabilities.json` (capability_catalog)

## HyperGraph

Meta6 Abstract Machine

- Aliases: `State Hypergraph`, `hypergraph`
- Sources:
  - `dist/meta3-engine-v0.5.0/config/capabilities.json` (capability_catalog)
  - `(curation)` (curation)

## interaction_hypergraph

Standalone Utility: interaction_hypergraph

- Sources:
  - `dist/meta3-engine-v0.5.0/config/capabilities.json` (capability_catalog)
  - `meta3-graph-core/SYSTEM_REPORT.md` (system_report)

## JIT Verification

Just-in-time verification: validate proposed actions/deltas against invariants before execution, producing accept/reject decisions with evidence.

- Aliases: `Just-In-Time verification`, `LeJIT`
- Sources:
  - `(curation)` (curation)

## kernel_interception

A capability classification used in the catalog.

- Sources:
  - `dist/meta3-engine-v0.5.0/config/capabilities.json` (capability_catalog)

## LEARNING SOLVER

Heuristic + Multiway Verification

- Sources:
  - `dist/meta3-engine-v0.5.0/config/capabilities.json` (capability_catalog)

## LeJIT

Just-in-time verification layer that validates proposed actions/deltas against invariants before they are executed.

- Aliases: `JIT Verification`, `Just-In-Time verification`
- Sources:
  - `(curation)` (curation)

## merge_mission_hypergraph

merge `mission_graph.json` into a hypergraph (`meta3-graph-core/src/bin/merge_mission_hypergraph.rs`)

- Sources:
  - `meta3-graph-core/SYSTEM_PROMPT.md` (graph_core_prompt)

## Meta3 Graph Core

Deterministic Rust kernel that reads ops packets / graph deltas and reifies them into reality with auditable receipts.

- Sources:
  - `(curation)` (curation)

## negentropy

Standalone Utility: negentropy

- Sources:
  - `dist/meta3-engine-v0.5.0/config/capabilities.json` (capability_catalog)

## oracle

Standalone Utility: oracle

- Sources:
  - `dist/meta3-engine-v0.5.0/config/capabilities.json` (capability_catalog)

## Receipts Beat Recollection

Operational rule: don’t rely on memory. Every claim and state change should be backed by an artifact (receipt, graph packet, report).

- Aliases: `immutable evidence`, `receipts`
- Sources:
  - `(curation)` (curation)

## render_hypergraph

render a hypergraph to self-contained HTML (`meta3-graph-core/src/bin/render_hypergraph.rs`)

- Sources:
  - `meta3-graph-core/SYSTEM_PROMPT.md` (graph_core_prompt)

## Ruliad

Formal Rewrite System - Wolfram Physics

- Sources:
  - `dist/meta3-engine-v0.5.0/config/capabilities.json` (capability_catalog)

## State Hypergraph

The state model of the system: nodes represent entities (files, concepts, artifacts, tasks) and hyperedges represent causal relationships that can connect multiple entities at once.

- Sources:
  - `(curation)` (curation)

## Task Graph

LLM-based Task Decomposition

- Sources:
  - `dist/meta3-engine-v0.5.0/config/capabilities.json` (capability_catalog)

## Thought Tree

ASCII Hierarchical Render

- Sources:
  - `dist/meta3-engine-v0.5.0/config/capabilities.json` (capability_catalog)

## ToolHub

The capability scanner/catalog generator (ToolHub) used to enumerate available capabilities and tools.

- Sources:
  - `(curation)` (curation)

## TSP

Traveling Salesman Problem - Ruliad Way

- Sources:
  - `dist/meta3-engine-v0.5.0/config/capabilities.json` (capability_catalog)

## UTIR

Universal Tool Invocation Receipt: a structured evidence stream used to audit and reproduce actions (writes/execs) performed by the system.

- Aliases: `artifact stream`, `receipts`
- Sources:
  - `(curation)` (curation)
