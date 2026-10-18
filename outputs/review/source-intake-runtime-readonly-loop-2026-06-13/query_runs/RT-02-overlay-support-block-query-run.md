---
record_kind: query_run_trace
artifact_kind: runtime_test_artifact
status: runtime_fixture
knowledge_status: candidate
retrieval_exclusion: true
default_retrieval: false
indexing_policy: exclude_from_default_retrieval_graph_pack_support
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: none
  action_basis_allowed: false
  warning_code: context_pack_not_action_basis
query_id: RT-02-overlay-support-block
query_time: '2026-06-14T01:37:48+00:00'
question_summary: Can a project overlay become final support?
verbatim_input: Can a project overlay become final support?
query_mode: action
active_project: vaks-source-intake-runtime-readonly
requested_authority_bucket: reviewed_support_or_raw_anchor_only
included_buckets:
- raw_anchor
- candidate_context
excluded_buckets:
- reviewed_writeback
- promotion
retrieval_filters:
  include_candidates: true
  include_overlays: active_project_only
  read_only: true
  writeback_allowed: false
  promotion_allowed: false
selected_items:
- ref: outputs/review/project_overlays/vaks/example-confirmed-overlay.md#borrow-scope
  record_kind: project_overlay
  knowledge_status: candidate
  pack_role: support
  warning_code: overlay_not_authority
  action_basis_allowed: false
  independent_anchor_ref: raw/articles/example-source.md#L12-L18
  selected_by:
    lexical: false
    semantic: false
    graph: false
    metadata: true
    rank: false
    dashboard: false
    legacy_raw_metadata: false
support_checks:
- claim_ref: overlay-local borrow scope
  independent_anchor_ref: raw/articles/example-source.md#L12-L18
  support_check_stage: pre_validation_fixture_input
  result_semantics: proposed_fixture_input_not_evaluated_verdict
  proposed_support_result: supported
human_confirmation_required: false
runtime_boundary:
  read_only: true
  writeback_attempted: false
  promotion_attempted: false
  truth_mutation_attempted: false
---

# Query Run Trace

Read-only runtime boundary fixture. This trace is not a reviewed record.

