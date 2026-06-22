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
query_run_ref: query_runs/G3-15-rag-attribution-action-faithfulness-decoy-query-run.md
active_project: VAKS
query_mode: action
use_mode: action
risk_tier: high
policy_ref: qp-action-default-authority-first-local-lexical-v1
requested_authority_bucket: authority_first_readonly_bucket_plan
included_buckets:
- reviewed
- raw_anchor
- candidate
- overlay
- source_annotation
excluded_buckets:
- reviewed_write_path
- action_basis
- truth_mutation
query_policy:
  policy_id: qp-action-default-authority-first-local-lexical-v1
  policy_version: 2026-06-15-pro-retrieval-plane-step1
  use_mode: action
  risk_tier: high
  intent: 'Decoy: action mode must block faithfulness scoring as final support.'
  authority_filter_mode: bucket_first_before_ranking
  allowed_authority_buckets:
  - reviewed
  - raw_anchor
  - candidate
  - overlay
  - source_annotation
  support_candidate_authority_buckets: []
  allowed_roles:
  - orientation
  - review_input
  - diagnostic
  retrieval_channels:
  - local_lexical
  disabled_channels:
  - dense_vector
  - sparse_semantic
  - graph_overlay
  - rrf_hybrid_fusion
  - second_stage_rerank
  fusion_method: none_single_local_lexical_channel
  fusion_scope: within_authority_bucket_only_when_multiple_channels_exist
  rerank_method: none
  max_hops: 0
  enable_graph: false
  enable_expansion: false
  needs_claim_binding: true
  writeback_allowed: false
  promotion_allowed: false
  truth_mutation_allowed: false
retrieval_bucket_receipt:
  authority_filter_mode: bucket_first_before_ranking
  pre_filter_doc_count: 210
  post_filter_doc_count: 210
  excluded_doc_count: 0
  pre_filter_bucket_counts:
    candidate: 40
    overlay: 8
    source_annotation: 5
    raw_anchor: 156
    reviewed: 1
  post_filter_bucket_counts:
    candidate: 40
    overlay: 8
    source_annotation: 5
    raw_anchor: 156
    reviewed: 1
  excluded_bucket_counts: {}
  excluded_path_sample: []
  query_policy_id: qp-action-default-authority-first-local-lexical-v1
  retrieval_channels:
  - local_lexical
  fusion_method: none_single_local_lexical_channel
  rerank_method: none
  returned_hit_count: 12
items:
- ref: outputs/review/2026-06-11-AxDSan-mnemosyne-candidate-distillation.md
  record_kind: candidate_distillation
  knowledge_status: candidate
  authority_bucket: candidate
  pack_role: review_input
  retrieval_role: review_input
  support_eligibility: ineligible
  eligibility_basis:
  - candidate_distillation_is_review_input_not_support
  match_representation: raw_markdown_lexical_match
  support_representation: none
  retrieval_channels:
  - local_lexical
  warning_code: candidate_not_action_basis
  action_basis_allowed: false
  truth_mutation_allowed: false
  independent_anchor_ref: ''
  selected_by:
    lexical: true
    semantic: false
    graph: false
    metadata: false
    rank: true
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 1
  retrieval_score: 36.0
  matched_terms:
  - as
  - confidence
  - reviewed
  - score
  - truth
  - write
  source_hash: 95939bb236c67d7dba28e880c3cc280d0bb79d01f47706f1914f3aef5183496e
  excluded_reason: candidate_distillation_is_review_input_not_support
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: outputs/review/2026-06-14-google-open-knowledge-format-candidate-distillation.md
  record_kind: candidate_distillation
  knowledge_status: candidate
  authority_bucket: candidate
  pack_role: review_input
  retrieval_role: review_input
  support_eligibility: ineligible
  eligibility_basis:
  - candidate_distillation_is_review_input_not_support
  match_representation: raw_markdown_lexical_match
  support_representation: none
  retrieval_channels:
  - local_lexical
  warning_code: candidate_not_action_basis
  action_basis_allowed: false
  truth_mutation_allowed: false
  independent_anchor_ref: ''
  selected_by:
    lexical: true
    semantic: false
    graph: false
    metadata: false
    rank: true
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 2
  retrieval_score: 32.5
  matched_terms:
  - as
  - citation
  - confidence
  - reviewed
  - truth
  - write
  source_hash: a8ffe7a813e3d107dcb9b0c0bceb82f6f2b9bb0751fd77ccfaccde837a5f4f30
  excluded_reason: candidate_distillation_is_review_input_not_support
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: raw/repos/2026-06-14-rohitg00-agentmemory-source.md
  record_kind: source_card
  knowledge_status: raw
  authority_bucket: raw_anchor
  pack_role: orientation
  retrieval_role: orientation
  support_eligibility: ineligible
  eligibility_basis:
  - query_mode_not_readonly_support_mode
  match_representation: raw_markdown_lexical_match
  support_representation: none
  retrieval_channels:
  - local_lexical
  warning_code: raw_is_provenance_only
  action_basis_allowed: false
  truth_mutation_allowed: false
  independent_anchor_ref: ''
  selected_by:
    lexical: true
    semantic: false
    graph: false
    metadata: false
    rank: true
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 3
  retrieval_score: 31.0
  matched_terms:
  - as
  - citation
  - confidence
  - reviewed
  - score
  - truth
  - write
  source_hash: 28ba0a38756b80bd67732ad47ecd4e265455e116593f63620dc6442884e39d9c
  excluded_reason: query_mode_not_readonly_support_mode
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: raw/papers/2026-05-29-rag-attribution-faithfulness-source.md
  record_kind: source_card
  knowledge_status: raw
  authority_bucket: raw_anchor
  pack_role: orientation
  retrieval_role: orientation
  support_eligibility: ineligible
  eligibility_basis:
  - query_mode_not_readonly_support_mode
  match_representation: raw_markdown_lexical_match
  support_representation: none
  retrieval_channels:
  - local_lexical
  warning_code: raw_is_provenance_only
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
  retrieval_rank: 4
  retrieval_score: 29.5
  matched_terms:
  - as
  - citation
  - faithfulness
  - score
  source_hash: a95728112b9a8a80d61fd956290999e7e125c0cd2637f81c8a7e42ee5f12438a
  excluded_reason: query_mode_not_readonly_support_mode
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: outputs/review/2026-06-08-bilibili-claudian-obsidian-skill-workflow-candidate-distillation.md
  record_kind: candidate_distillation
  knowledge_status: candidate
  authority_bucket: candidate
  pack_role: review_input
  retrieval_role: review_input
  support_eligibility: ineligible
  eligibility_basis:
  - candidate_distillation_is_review_input_not_support
  match_representation: raw_markdown_lexical_match
  support_representation: none
  retrieval_channels:
  - local_lexical
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
  retrieval_rank: 5
  retrieval_score: 29.0
  matched_terms:
  - as
  - confidence
  - reviewed
  - score
  - truth
  - write
  source_hash: 769215c982a13c9bd434e5241b6f83a18e0fbdaaa6f9a518c0f447b127869cd0
  excluded_reason: candidate_distillation_is_review_input_not_support
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: outputs/review/2026-06-14-edochi-mdvs-candidate-distillation.md
  record_kind: candidate_distillation
  knowledge_status: candidate
  authority_bucket: candidate
  pack_role: review_input
  retrieval_role: review_input
  support_eligibility: ineligible
  eligibility_basis:
  - candidate_distillation_is_review_input_not_support
  match_representation: raw_markdown_lexical_match
  support_representation: none
  retrieval_channels:
  - local_lexical
  warning_code: candidate_not_action_basis
  action_basis_allowed: false
  truth_mutation_allowed: false
  independent_anchor_ref: ''
  selected_by:
    lexical: true
    semantic: false
    graph: false
    metadata: false
    rank: false
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 6
  retrieval_score: 28.0
  matched_terms:
  - as
  - confidence
  - reviewed
  - score
  - truth
  - write
  source_hash: 210bef25145cba4013a716374083098fa438568e19ad99a3e40324f2e854efe7
  excluded_reason: candidate_distillation_is_review_input_not_support
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: outputs/review/2026-06-14-kanna12580-kk-knowledge-agent-candidate-distillation.md
  record_kind: candidate_distillation
  knowledge_status: candidate
  authority_bucket: candidate
  pack_role: review_input
  retrieval_role: review_input
  support_eligibility: ineligible
  eligibility_basis:
  - candidate_distillation_is_review_input_not_support
  match_representation: raw_markdown_lexical_match
  support_representation: none
  retrieval_channels:
  - local_lexical
  warning_code: candidate_not_action_basis
  action_basis_allowed: false
  truth_mutation_allowed: false
  independent_anchor_ref: ''
  selected_by:
    lexical: true
    semantic: false
    graph: false
    metadata: false
    rank: false
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 7
  retrieval_score: 27.5
  matched_terms:
  - as
  - confidence
  - reviewed
  - score
  - truth
  - write
  source_hash: 19a685b5f8d9ae7d2e8c3ba0bb5fef04150d2cf8f2811174861397ebf3ae7dc8
  excluded_reason: candidate_distillation_is_review_input_not_support
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: outputs/review/2026-06-08-bilibili-ioto-obsidian-knowledge-production-system-candidate-distillation.md
  record_kind: candidate_distillation
  knowledge_status: candidate
  authority_bucket: candidate
  pack_role: review_input
  retrieval_role: review_input
  support_eligibility: ineligible
  eligibility_basis:
  - candidate_distillation_is_review_input_not_support
  match_representation: raw_markdown_lexical_match
  support_representation: none
  retrieval_channels:
  - local_lexical
  warning_code: candidate_not_action_basis
  action_basis_allowed: false
  truth_mutation_allowed: false
  independent_anchor_ref: ''
  selected_by:
    lexical: true
    semantic: false
    graph: false
    metadata: true
    rank: false
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 8
  retrieval_score: 26.5
  matched_terms:
  - as
  - confidence
  - reviewed
  - truth
  - write
  source_hash: 2acebe3ef58f6e9872e1e586aad46155e1291d5f747ba3765b247fc35407d7b5
  excluded_reason: candidate_distillation_is_review_input_not_support
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: outputs/review/2026-06-11-RyanCodrai-turbovec-candidate-distillation.md
  record_kind: candidate_distillation
  knowledge_status: candidate
  authority_bucket: candidate
  pack_role: review_input
  retrieval_role: review_input
  support_eligibility: ineligible
  eligibility_basis:
  - candidate_distillation_is_review_input_not_support
  match_representation: raw_markdown_lexical_match
  support_representation: none
  retrieval_channels:
  - local_lexical
  warning_code: candidate_not_action_basis
  action_basis_allowed: false
  truth_mutation_allowed: false
  independent_anchor_ref: ''
  selected_by:
    lexical: true
    semantic: false
    graph: false
    metadata: false
    rank: false
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 9
  retrieval_score: 26.0
  matched_terms:
  - as
  - confidence
  - now
  - reviewed
  - score
  - truth
  source_hash: 245c07226c481552e6ad7130f63ef1cfee8dcf0c1997096d737ba6a64913e719
  excluded_reason: candidate_distillation_is_review_input_not_support
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: outputs/review/2026-06-12-breferrari-obsidian-mind-candidate-distillation.md
  record_kind: candidate_distillation
  knowledge_status: candidate
  authority_bucket: candidate
  pack_role: review_input
  retrieval_role: review_input
  support_eligibility: ineligible
  eligibility_basis:
  - candidate_distillation_is_review_input_not_support
  match_representation: raw_markdown_lexical_match
  support_representation: none
  retrieval_channels:
  - local_lexical
  warning_code: candidate_not_action_basis
  action_basis_allowed: false
  truth_mutation_allowed: false
  independent_anchor_ref: ''
  selected_by:
    lexical: true
    semantic: false
    graph: false
    metadata: false
    rank: false
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 10
  retrieval_score: 26.0
  matched_terms:
  - as
  - confidence
  - now
  - reviewed
  - truth
  - write
  source_hash: a8fe634cba55b59c4348f056d0ba1052d7f0b3815cd1092429e1a944f3359b19
  excluded_reason: candidate_distillation_is_review_input_not_support
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: outputs/review/2026-06-14-rohitg00-agentmemory-candidate-distillation.md
  record_kind: candidate_distillation
  knowledge_status: candidate
  authority_bucket: candidate
  pack_role: review_input
  retrieval_role: review_input
  support_eligibility: ineligible
  eligibility_basis:
  - candidate_distillation_is_review_input_not_support
  match_representation: raw_markdown_lexical_match
  support_representation: none
  retrieval_channels:
  - local_lexical
  warning_code: candidate_not_action_basis
  action_basis_allowed: false
  truth_mutation_allowed: false
  independent_anchor_ref: ''
  selected_by:
    lexical: true
    semantic: false
    graph: false
    metadata: false
    rank: false
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 11
  retrieval_score: 26.0
  matched_terms:
  - as
  - confidence
  - reviewed
  - truth
  - write
  source_hash: fe8a82b3ff9a733c053cf38fa49e6ce3759cf051f04355ff994e164a269d1084
  excluded_reason: candidate_distillation_is_review_input_not_support
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: outputs/review/2026-06-13-bilibili-book-note-workflow-candidate-distillation.md
  record_kind: candidate_distillation
  knowledge_status: candidate
  authority_bucket: candidate
  pack_role: review_input
  retrieval_role: review_input
  support_eligibility: ineligible
  eligibility_basis:
  - candidate_distillation_is_review_input_not_support
  match_representation: raw_markdown_lexical_match
  support_representation: none
  retrieval_channels:
  - local_lexical
  warning_code: candidate_not_action_basis
  action_basis_allowed: false
  truth_mutation_allowed: false
  independent_anchor_ref: ''
  selected_by:
    lexical: true
    semantic: false
    graph: false
    metadata: false
    rank: false
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 12
  retrieval_score: 25.5
  matched_terms:
  - as
  - confidence
  - now
  - reviewed
  - truth
  source_hash: b4f0812941e2939688fb04ac05ff5078f3b47307f77a151238bb8e60300c7151
  excluded_reason: candidate_distillation_is_review_input_not_support
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
support_checks:
- claim_ref: no_final_support_selected
  independent_anchor_ref: ''
  result: not_ready
  resolution:
    status: not_checked
    reason: generic assembler selected no support items
  reason: retrieved_items_remain_review_input_or_orientation_only
  semantic_support_status: not_external_judged
human_confirmation_required: false
artifact_kind: live_readonly_test_artifact
retrieval_exclusion: true
default_retrieval: false
indexing_policy: exclude_from_default_retrieval_graph_pack_support
truth_mutation_allowed: false
action_basis_allowed: false
---

# Context Pack: G3-15-rag-attribution-action-faithfulness-decoy

## Boundary

This pack is a read-only attention surface. It is not action basis and does not write truth.

## Support Selection

- not_ready: `no_final_support_selected` anchor=``