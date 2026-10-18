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
query_run_ref: query_runs/V2-06-adversarial-rank-diagnostic-mislabeled-support-query-run.md
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
- ref: outputs/review/2026-06-13-flexnote-docs-candidate-distillation.md
  record_kind: candidate_distillation
  knowledge_status: candidate
  pack_role: support
  warning_code: candidate_not_action_basis
  action_basis_allowed: false
  truth_mutation_allowed: false
  independent_anchor_ref: retrieval_rank:1:score:89.5000
  selected_by:
    lexical: true
    semantic: false
    graph: false
    metadata: true
    rank: true
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 1
  retrieval_score: 89.5
  matched_terms:
  - anchor
  - candidate
  - context
  - database
  - flexnote
  - overlay
  - pack
  - source
  - tag
  - visual
  - workbench
  source_hash: 875108c0ae9d3a00c2e666d3cd4f04eb9475e1a6143fc19c3ec27c3d37928aaf
  excluded_reason: adversarial_rank_anchor_expected_to_be_blocked
support_checks:
- claim_ref: outputs/review/2026-06-13-flexnote-docs-candidate-distillation.md
  independent_anchor_ref: retrieval_rank:1:score:89.5000
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

# Context Pack: V2-06-adversarial-rank-diagnostic-mislabeled-support

## Boundary

This pack is a read-only attention surface. It is not action basis and does not write truth.

## Support Selection

- not_ready: `outputs/review/2026-06-13-flexnote-docs-candidate-distillation.md` anchor=`retrieval_rank:1:score:89.5000`