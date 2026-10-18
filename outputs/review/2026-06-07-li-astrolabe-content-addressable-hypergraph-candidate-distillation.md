---
record_kind: candidate_distillation
type: review-candidate
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: confirmed
review_pressure: none
derived_from:
  - raw/papers/2026-06-07-li-astrolabe-content-addressable-hypergraph-source.md
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
v0_2_13_trigger: no
project: verified-action-knowledge-system
scope: li-astrolabe-content-addressable-hypergraph-distillation
source_checked_at: 2026-06-07
borrow_value: strong
borrow_order:
  - "P1: relation as first-class record with its own content"
  - "P1: content-addressed atomic entries"
  - "P1: hyperedge can reference atoms or other edges"
  - "P1: plugin-interpreted record conventions"
  - "P2: width/depth decomposition for relation complexity"
  - "P2: semantic propagation after change"
  - "P2: statement-proof separation"
  - "P3: Lean/math bridge as domain demo"
avoid:
  - "Do not make hypergraph runtime VAKS truth core now."
  - "Do not treat hash identity as truth confidence."
  - "Do not treat plugin record conventions as reviewed relations."
  - "Do not treat graph metrics as trust."
  - "Do not migrate from Markdown/YAML to graph runtime."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "Designing future complex relation objects or graph-runtime experiments."
  support_when: "Discussing reviewed relations, candidate graph fragments, semantic edge records, or relation provenance."
  risk_when: "Any proposal replaces VAKS Markdown/YAML truth layer with graph runtime or hash identity."
  cold_references:
    - raw/papers/2026-06-07-li-astrolabe-content-addressable-hypergraph-source.md
routing_hint:
  - semantic-relations
  - graph-runtime
  - candidate-graph-fragment
  - relation-provenance
tags:
  - candidate
  - provisional
  - paper-distillation
  - hypergraph
  - semantic-relations
borrow_tags:
  - P1/relation_as_first_class_record
  - P1/content_addressed_atomic_entries
  - P1/hyperedge_can_reference_edges
  - P1/plugin_interpreted_record_conventions
  - P2/width_depth_decomposition_for_relation_complexity
  - P2/semantic_propagation_after_change
  - P2/statement_proof_separation
  - P3/lean_math_bridge_as_domain_demo
do_not_borrow_tags:
  - avoid/hypergraph_as_vaks_truth_core_now
  - avoid/hash_identity_as_truth_confidence
  - avoid/plugin_record_as_reviewed_relation
  - avoid/graph_metric_as_trust
  - avoid/full_migration_from_markdown_to_graph_runtime
---

# Astrolabe Content-Addressable Hypergraph Candidate Distillation

## Boundary

Candidate-only future graph/relation reference. It does not replace VAKS Markdown/YAML records or reviewed relation rules.

## Plain-Language Takeaway

说人话：这篇提醒我们，复杂关系可以不是一条边，而是一个“有自己内容的对象”。这对 VAKS 未来的 candidate_relation / reviewed_relation 设计很有启发，但现在不能直接把系统改成超图数据库。

## Candidate Points

### 1. Relations can be records

A relation may need its own record, source, note, status, and interpretation, not just `A -> B`.

### 2. Hyperedges can represent higher-order meaning

An edge can reference other edges, allowing structures like "this argument connects these two claims through this evidence".

### 3. Content addressing helps identity and dedupe

Hashing record content can support stable identity and dedupe, but it does not prove truth.

### 4. Plugin-interpreted records keep core generic

The core can store generic records while plugins define domain conventions, but plugin output must remain governed.

### 5. Semantic propagation is separate from hash identity

If a dependency changes, affected nodes should be flagged through semantic graph traversal, not assumed from hash changes alone.

## Open Questions

- Should VAKS candidate graph fragments treat relation notes as first-class records?
- What is the smallest relation object that improves review without graph-runtime bloat?
- Can content hashes help dedupe source/candidate records without implying authority?
