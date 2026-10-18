---
record_kind: project_overlay
status: candidate
knowledge_status: candidate
processing_tier: medium
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
project_id: verified-action-knowledge-system
target_ref: outputs/review/2026-06-07-li-astrolabe-content-addressable-hypergraph-candidate-distillation.md
source_card: raw/papers/2026-06-07-li-astrolabe-content-addressable-hypergraph-source.md
target_selector: semantic_relation_hypergraph_runtime
target_hint: "Use for future complex relation-object and graph-runtime experiments only."
borrow_tags:
  - P1/relation_as_first_class_record
  - P1/content_addressed_atomic_entries
  - P1/hyperedge_can_reference_edges
  - P1/plugin_interpreted_record_conventions
  - P2/width_depth_decomposition_for_relation_complexity
  - P2/semantic_propagation_after_change
  - P2/statement_proof_separation
do_not_borrow_tags:
  - avoid/hypergraph_as_vaks_truth_core_now
  - avoid/hash_identity_as_truth_confidence
  - avoid/plugin_record_as_reviewed_relation
  - avoid/graph_metric_as_trust
  - avoid/full_migration_from_markdown_to_graph_runtime
project_reopen_trigger:
  - "When designing first-class relation records or candidate graph fragments."
  - "When experimenting with graph runtime separate from Markdown source of truth."
confirmation_basis: "arXiv abstract/PDF observed on 2026-06-07; PDF hash recorded."
last_checked_at: 2026-06-07
expires_at:
---

# VAKS Overlay: Astrolabe

## Boundary

Future graph/relation reference only. It cannot replace Markdown/YAML, reviewed relation gates, or evidence-aware review.

## Project Borrow Scope

- Relation as first-class record.
- Content-addressed atomic entries for identity/dedupe exploration.
- Hyperedges referencing edges.
- Plugin-interpreted record conventions.
- Width/depth decomposition for complex relation analysis.
- Semantic propagation after dependency changes.

## Project Non-Borrow Scope

- No hypergraph runtime as VAKS core now.
- No hash identity as truth confidence.
- No plugin record as reviewed relation.
- No graph metric as trust.
- No full migration away from Markdown/YAML truth layer.
