---
record_kind: context_pack_manifest
status: archived
knowledge_status: candidate
processing_tier: medium
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: review_input_only
  action_basis_allowed: false
  warning_code: context_pack_not_action_basis
query_run_ref: query_runs/V2-04-adversarial-candidate-mislabeled-support-query-run.md
active_project: VAKS
query_mode: action
requested_authority_bucket: read_only_source_and_review_input
included_buckets:
- raw
- candidate
excluded_buckets:
- reviewed_write_path
- action_basis
- truth_mutation
items:
- ref: outputs/review/2026-06-11-AxDSan-mnemosyne-candidate-distillation.md
  record_kind: candidate_distillation
  knowledge_status: candidate
  pack_role: support
  warning_code: candidate_not_action_basis
  action_basis_allowed: false
  truth_mutation_allowed: false
  independent_anchor_ref: ''
  selected_by:
    lexical: true
    semantic: false
    graph: false
    metadata: true
    rank: true
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 1
  retrieval_score: 85.0
  matched_terms:
  - action
  - basis
  - candidate
  - memory
  - mnemosyne
  - support
  - vector
  source_hash: 95939bb236c67d7dba28e880c3cc280d0bb79d01f47706f1914f3aef5183496e
  excluded_reason: adversarial_mislabel_expected_to_be_blocked
support_checks:
- claim_ref: outputs/review/2026-06-11-AxDSan-mnemosyne-candidate-distillation.md
  independent_anchor_ref: ''
  result: not_ready
  resolution:
    status: not_checked
    reason: anchor ref has no selector
    method: path_selector_heading_or_string_resolution
  reason: non_raw_source_item_cannot_be_final_support
human_confirmation_required: false
artifact_kind: live_readonly_test_artifact
retrieval_exclusion: true
default_retrieval: false
indexing_policy: exclude_from_default_retrieval_graph_pack_support
truth_mutation_allowed: false
action_basis_allowed: false
---

# Context Pack: V2-04-adversarial-candidate-mislabeled-support

## Boundary

This pack is a read-only attention surface. It is not action basis and does not write truth.

## Support Selection

- not_ready: `outputs/review/2026-06-11-AxDSan-mnemosyne-candidate-distillation.md` anchor=``