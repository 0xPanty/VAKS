---
record_kind: project_overlay
status: candidate
knowledge_status: candidate
processing_tier: heavy
overlay_state: confirmed
overlay_scope: project_sidecar_only
overlay_storage: confirmed_persistent_project_bucket
retrieval_scope: active_project_only
default_retrieval: false
retrieval_policy:
  policy_kind: project_context_only
  default_scope: project_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: overlay_not_authority
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
project_id: VAKS
target_ref: outputs/review/2026-06-11-safishamsi-graphify-candidate-distillation.md
target_selector: "candidate source: safishamsi/graphify"
target_hint:
  - type: workflow
    value: graph-retrieval
    status: conceptual
    anchor_version: 2026-06-11-source-review
  - type: workflow
    value: agent-context-orientation
    status: conceptual
    anchor_version: 2026-06-11-source-review
  - type: workspace
    value: outputs/review/vaks-retrieval-layer-design-2026-06-11
    status: active_candidate_workspace
    anchor_version: 2026-06-11-file-checked
project_borrow_scope: "Use Graphify as a P1 design reference for derived graph retrieval, AST-first anchors, community activation, and agent-facing query tools in the VAKS retrieval-layer design workspace."
project_non_borrow_scope: "Do not use Graphify as a VAKS truth store, reviewed relation engine, action-basis gate, default hook system, or mainline dependency before a bucket-first sandbox pilot."
project_reopen_trigger: "Reopen after VAKS has a small graph retrieval adapter that measures recall, source-anchor correctness, graph-cache staleness, query privacy, and bucket-boundary violations."
confirmation_basis: "GitHub/API/source snapshot/static source review captured 2026-06-11; no local runtime benchmark."
last_checked_at: 2026-06-11
expires_at: 2026-08-11
---

# Project Overlay: Graphify Graph Retrieval Layer

## Boundary

This is a VAKS project-scoped sidecar.

It does not rewrite the source card, candidate distillation, reviewed note,
decision, pattern, or action basis.

## Target

```yaml
target_ref: outputs/review/2026-06-11-safishamsi-graphify-candidate-distillation.md
target_selector: "candidate source: safishamsi/graphify"
target_hint:
  - graph-retrieval
  - agent-context-orientation
  - VAKS retrieval-layer design workspace
```

## Project Borrow Scope

For VAKS, borrow Graphify only as a design reference for:

```text
derived graph retrieval cache
AST-first source/symbol anchors
community-neighborhood activation
query/path/explain style agent commands
MCP-style read-only graph tools
incremental graph rebuild hygiene
graph-output security guardrails
```

## Project Non-Borrow Scope

For VAKS, do not borrow Graphify as:

```text
truth store
reviewed relation engine
evidence support checker
action-basis generator
default forced hook system
mainline dependency before pilot
single mixed graph of raw/candidate/reviewed/feedback without policy labels
```

## Why This Matters

Graphify is the strongest current reference for a practical “agent asks a graph
before reading raw files” workflow.

For VAKS, the winning translation is:

```text
authority bucket first
-> graph retrieval inside allowed bucket
-> anchor queue with source/chunk/status labels
-> context pack
-> evidence/action gate only when required
```

This keeps its efficiency while preventing graph rank or confidence tags from
turning into fake authority.

## Reopen Trigger

Reopen this overlay when there is a VAKS sandbox that can test:

- recall quality vs current file search / BM25 / vector candidates;
- source-anchor correctness;
- whether graph traversal crosses authority buckets;
- cache invalidation after source changes;
- prompt-injection and sensitive query leakage risk;
- whether agent-facing query tools improve or distract from real development.
