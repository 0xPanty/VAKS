---
record_kind: retrieval_receipt
fixture_id: valid-orientation-receipt
expected_contract_status: valid_orientation_trace
query_id: q-orientation-001
query_time: 2026-06-15T00:00:00+08:00
question_summary: "What prior materials should be inspected for retrieval receipt design?"
query_mode: orientation
requested_authority_bucket: mixed_for_orientation
included_buckets:
  - reviewed
  - candidate
  - project_overlay
excluded_buckets:
  - feedback
rrf_scope: same_authority_bucket_only
retrieval_engines:
  - engine_id: rg-manual
    engine_type: lexical
    engine_scope: local_markdown
retrieval_filters:
  include_reviewed: true
  include_raw_anchors: false
  include_candidates: true
  include_project_overlays: active_project_only
  include_feedback: false
  exclude_runtime_artifacts: true
  exclude_legacy_raw_metadata: true
selected_items:
  - ref: SOURCE_INTAKE.md#retrieval-bucket-policy
    record_kind: implementation_note
    knowledge_status: reviewed
    authority_bucket: reviewed
    pack_role: orientation
    action_basis_allowed: false
    warning_code:
    selected_by:
      lexical: "retrieval receipt"
      semantic:
      graph:
      metadata:
      manual:
      legacy_raw_metadata: false
    diagnostic_scores:
      lexical_score:
      semantic_score:
      graph_rank:
      rrf_rank:
      scores_are_support: false
  - ref: outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md#p0-01
    record_kind: upgrade_plan
    knowledge_status: candidate
    authority_bucket: candidate
    pack_role: review_input
    action_basis_allowed: false
    warning_code: candidate_not_action_basis
    selected_by:
      lexical: "P0-01 Retrieval Receipt Template"
      semantic:
      graph:
      metadata:
      manual:
      legacy_raw_metadata: false
    diagnostic_scores:
      lexical_score:
      semantic_score:
      graph_rank:
      rrf_rank:
      scores_are_support: false
excluded_items:
  - ref: outputs/feedback/events/example.jsonl
    record_kind: feedback_event
    authority_bucket: feedback
    excluded_reason: feedback_not_truth
support_checks: []
warnings:
  - orientation_mode_mixed_buckets_must_not_imply_support
gaps:
  - no_support_claim_made
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

# Valid Orientation Receipt

This fixture is valid because it uses mixed buckets only for orientation and
does not claim support.
