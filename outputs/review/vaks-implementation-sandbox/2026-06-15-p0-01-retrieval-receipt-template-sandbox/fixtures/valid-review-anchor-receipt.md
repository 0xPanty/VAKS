---
record_kind: retrieval_receipt
fixture_id: valid-review-anchor-receipt
expected_contract_status: valid_review_anchor_trace
query_id: q-review-001
query_time: 2026-06-15T00:00:00+08:00
question_summary: "Can this specific target use an inspected raw anchor as support input?"
query_mode: review
requested_authority_bucket: raw_anchor
included_buckets:
  - raw_anchor
excluded_buckets:
  - candidate
  - project_overlay
  - feedback
rrf_scope: same_authority_bucket_only
retrieval_engines:
  - engine_id: manual-anchor-check
    engine_type: manual
    engine_scope: inspected_source_span
retrieval_filters:
  include_reviewed: false
  include_raw_anchors: true
  include_candidates: false
  include_project_overlays: false
  include_feedback: false
  exclude_runtime_artifacts: true
  exclude_legacy_raw_metadata: true
selected_items:
  - ref: raw/repos/example-source.md#L10
    title: Example source span
    record_kind: source_card
    knowledge_status: raw
    authority_bucket: raw_anchor
    pack_role: anchor
    action_basis_allowed: false
    warning_code: raw_requires_support_check
    source_anchor:
      source_ref: raw/repos/example-source.md
      selector: "#L10"
      source_hash: sha256:example-source-hash
      chunk_hash: sha256:example-chunk-hash
      evidence_granularity: table_or_code_anchor
    selected_by:
      lexical:
      semantic:
      graph:
      metadata:
      manual: "explicit reviewer source-span inspection"
      legacy_raw_metadata: false
    diagnostic_scores:
      lexical_score:
      semantic_score:
      graph_rank:
      rrf_rank:
      scores_are_support: false
excluded_items:
  - ref: outputs/review/example-candidate.md
    record_kind: candidate_distillation
    authority_bucket: candidate
    excluded_reason: candidate_cannot_be_final_support
support_checks:
  - target_ref: review-candidate:example-target
    proposed_support_item_ref: raw/repos/example-source.md#L10
    independent_anchor_ref: raw/repos/example-source.md#L10
    evidence_role: direct_support
    result: supported
    reviewer_note: "Fixture demonstrates shape only; real support requires reviewer inspection."
warnings:
  - supported_does_not_mean_truth
  - receipt_does_not_mean_reviewer_approval
gaps:
  - action_readiness_not_checked
support_boundary:
  selected_by_is_not_support: true
  same_bucket_rrf_only: true
  cross_bucket_rank_not_authority: true
  legacy_raw_metadata_excluded: true
  candidate_overlay_feedback_not_support: true
  url_only_not_direct_support: true
  graph_rank_not_trust: true
  receipt_not_review_approval: true
  receipt_not_action_basis: true
  receipt_not_reviewed_knowledge: true
---

# Valid Review Anchor Receipt

This fixture is valid because the support check points at a raw independent
anchor and still preserves the boundary that support is not truth or action
readiness.
