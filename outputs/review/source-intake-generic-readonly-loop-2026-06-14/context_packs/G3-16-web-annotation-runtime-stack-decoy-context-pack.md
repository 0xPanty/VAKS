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
query_run_ref: query_runs/G3-16-web-annotation-runtime-stack-decoy-query-run.md
active_project: VAKS
query_mode: source_inspection
use_mode: source_inspection
risk_tier: low
policy_ref: qp-source_inspection-default-authority-first-local-lexical-v1
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
  policy_id: qp-source_inspection-default-authority-first-local-lexical-v1
  policy_version: 2026-06-15-pro-retrieval-plane-step1
  use_mode: source_inspection
  risk_tier: low
  intent: 'Decoy: non-support implementation/runtime terms should not become final support through stable-anchor headings.'
  authority_filter_mode: bucket_first_before_ranking
  allowed_authority_buckets:
  - reviewed
  - raw_anchor
  - candidate
  - overlay
  - source_annotation
  support_candidate_authority_buckets:
  - raw_anchor
  allowed_roles:
  - orientation
  - review_input
  - diagnostic
  - support_candidate
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
  needs_claim_binding: false
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
  query_policy_id: qp-source_inspection-default-authority-first-local-lexical-v1
  retrieval_channels:
  - local_lexical
  fusion_method: none_single_local_lexical_channel
  rerank_method: none
  returned_hit_count: 12
items:
- ref: raw/articles/2026-05-30-w3c-web-annotation-source.md
  record_kind: source_card
  knowledge_status: raw
  authority_bucket: raw_anchor
  pack_role: orientation
  retrieval_role: orientation
  support_eligibility: ineligible
  eligibility_basis:
  - no_generic_resolved_source_fact_anchor
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
  retrieval_rank: 1
  retrieval_score: 24.5
  matched_terms:
  - annotation
  - browser
  - json
  - ld
  - rdf
  - runtime
  - server
  source_hash: e16be8aa931cc46d912429b26446ad7efb8ed49ba7a653512e63e37b14fb28c0
  excluded_reason: no_generic_resolved_source_fact_anchor
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: raw/repos/2026-05-27-knowledge-base-server-source.md
  record_kind: source_card
  knowledge_status: raw
  authority_bucket: raw_anchor
  pack_role: orientation
  retrieval_role: orientation
  support_eligibility: ineligible
  eligibility_basis:
  - no_generic_resolved_source_fact_anchor
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
  retrieval_rank: 2
  retrieval_score: 23.5
  matched_terms:
  - json
  - runtime
  - server
  source_hash: be138c5b99e6351f444f8aee37e9000b7821b89e8f357e8a11911ba9e245853c
  excluded_reason: no_generic_resolved_source_fact_anchor
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: raw/repos/2026-06-11-awesome-obsidian-vault/dpapathanasiou-recipes-source.md
  record_kind: source_card
  knowledge_status: raw
  authority_bucket: raw_anchor
  pack_role: orientation
  retrieval_role: orientation
  support_eligibility: ineligible
  eligibility_basis:
  - no_generic_resolved_source_fact_anchor
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
  retrieval_rank: 3
  retrieval_score: 15.5
  matched_terms:
  - json
  source_hash: bd241a41dbae509a75e64b78db828dcd0b49d853d2eee50c7e16b9ca907b810f
  excluded_reason: no_generic_resolved_source_fact_anchor
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
    rank: true
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 4
  retrieval_score: 14.5
  matched_terms:
  - json
  - runtime
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
    metadata: true
    rank: true
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 5
  retrieval_score: 12.5
  matched_terms:
  - runtime
  source_hash: fe8a82b3ff9a733c053cf38fa49e6ce3759cf051f04355ff994e164a269d1084
  excluded_reason: candidate_distillation_is_review_input_not_support
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: raw/repos/2026-06-11-PaddlePaddle-PaddleOCR-source.md
  record_kind: source_card
  knowledge_status: raw
  authority_bucket: raw_anchor
  pack_role: orientation
  retrieval_role: orientation
  support_eligibility: ineligible
  eligibility_basis:
  - no_generic_resolved_source_fact_anchor
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
    rank: false
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 6
  retrieval_score: 11.0
  matched_terms:
  - json
  - runtime
  - server
  source_hash: ce8543a925ea709c235815ac4017e1b569df19aa5ad0a038be53c30899496433
  excluded_reason: no_generic_resolved_source_fact_anchor
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
  retrieval_score: 10.0
  matched_terms:
  - runtime
  - server
  source_hash: 19a685b5f8d9ae7d2e8c3ba0bb5fef04150d2cf8f2811174861397ebf3ae7dc8
  excluded_reason: candidate_distillation_is_review_input_not_support
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: outputs/review/2026-06-11-PaddlePaddle-PaddleOCR-candidate-distillation.md
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
  retrieval_rank: 8
  retrieval_score: 9.0
  matched_terms:
  - json
  - runtime
  source_hash: bdf0f9045aae266725831616c10e88ba7adc2718df5ce927a597a2ad3062308e
  excluded_reason: candidate_distillation_is_review_input_not_support
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: raw/repos/2026-06-14-benmaster82-Kwipu-source.md
  record_kind: source_card
  knowledge_status: raw
  authority_bucket: raw_anchor
  pack_role: orientation
  retrieval_role: orientation
  support_eligibility: ineligible
  eligibility_basis:
  - no_generic_resolved_source_fact_anchor
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
    rank: false
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 9
  retrieval_score: 9.0
  matched_terms:
  - runtime
  - server
  source_hash: 926ccda1a8089c5b4ad43e98677a176ef16f4f7e388883ba9c7ad151257aa215
  excluded_reason: no_generic_resolved_source_fact_anchor
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: outputs/review/2026-06-12-bilibili-apex-knowledge-schema-rag-candidate-distillation.md
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
  retrieval_score: 8.5
  matched_terms:
  - json
  source_hash: 540154444469d9087008dc25db570e7fc72afc40043226fad4801eabb22d1798
  excluded_reason: candidate_distillation_is_review_input_not_support
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: outputs/review/project_lens_overlays/2026-06-14-rohitg00-agentmemory-misa-vaks-bridge-overlay.md
  record_kind: project_overlay
  knowledge_status: candidate
  authority_bucket: overlay
  pack_role: review_input
  retrieval_role: review_input
  support_eligibility: ineligible
  eligibility_basis:
  - project_overlay_is_project_context_not_support
  match_representation: raw_markdown_lexical_match
  support_representation: none
  retrieval_channels:
  - local_lexical
  warning_code: overlay_not_authority
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
  retrieval_score: 8.5
  matched_terms:
  - runtime
  source_hash: a3e9c37feba9649bbf312c9fd73fa0a0f1d65d27bea528294234f60ca1902cad
  excluded_reason: project_overlay_is_project_context_not_support
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: raw/repos/2026-06-12-breferrari-obsidian-mind-source.md
  record_kind: source_card
  knowledge_status: raw
  authority_bucket: raw_anchor
  pack_role: orientation
  retrieval_role: orientation
  support_eligibility: ineligible
  eligibility_basis:
  - no_generic_resolved_source_fact_anchor
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
    rank: false
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 12
  retrieval_score: 8.0
  matched_terms:
  - json
  - runtime
  source_hash: f3a16afdd0e9f060c68674c59cb3719a536710f185d19a3d7b9095d945557f4b
  excluded_reason: no_generic_resolved_source_fact_anchor
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

# Context Pack: G3-16-web-annotation-runtime-stack-decoy

## Boundary

This pack is a read-only attention surface. It is not action basis and does not write truth.

## Support Selection

- not_ready: `no_final_support_selected` anchor=``