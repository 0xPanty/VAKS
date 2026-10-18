---
record_kind: query_run_trace
status: archived
query_id: G3-17-w3c-prov-full-ontology-decoy
query_time: '2026-06-22T15:34:42+00:00'
question_summary: 'Decoy: full ontology/runtime terms should not pass as final support through the narrow anchor vocabulary.'
verbatim_input: PROV ontology RDF OWL validator query protocol graph implementation
active_project: VAKS
query_mode: review
use_mode: review
risk_tier: medium
policy_ref: qp-review-default-authority-first-local-lexical-v1
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
  policy_id: qp-review-default-authority-first-local-lexical-v1
  policy_version: 2026-06-15-pro-retrieval-plane-step1
  use_mode: review
  risk_tier: medium
  intent: 'Decoy: full ontology/runtime terms should not pass as final support through the narrow anchor vocabulary.'
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
  query_policy_id: qp-review-default-authority-first-local-lexical-v1
  retrieval_channels:
  - local_lexical
  fusion_method: none_single_local_lexical_channel
  rerank_method: none
  returned_hit_count: 12
retrieval_filters:
  authority_bucket_filter_applied_before_ranking: true
  include_candidates: true
  include_overlays: active_project_only
  include_source_annotations: true
  include_runtime_test_artifacts: false
  writeback_allowed: false
  promotion_allowed: false
  truth_mutation_allowed: false
selected_items:
- ref: raw/articles/2026-05-29-w3c-prov-source.md
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
  retrieval_score: 25.5
  matched_terms:
  - graph
  - ontology
  - owl
  - protocol
  - prov
  - query
  - rdf
  - validator
  source_hash: d02636005e119966eb13a08c98a2416f0c99844e72f1740e44901535175e152f
  excluded_reason: no_generic_resolved_source_fact_anchor
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: outputs/review/project_lens_overlays/2026-06-14-benmaster82-Kwipu-vaks-local-graph-rag-overlay.md
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
    metadata: true
    rank: true
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 2
  retrieval_score: 22.5
  matched_terms:
  - graph
  - query
  source_hash: 062b96779d75bc7e4dc572e309a16e9e023bc37e86f838ecc99d0039ebd710cb
  excluded_reason: project_overlay_is_project_context_not_support
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
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
  retrieval_rank: 3
  retrieval_score: 14.5
  matched_terms:
  - graph
  - implementation
  - query
  source_hash: 95939bb236c67d7dba28e880c3cc280d0bb79d01f47706f1914f3aef5183496e
  excluded_reason: candidate_distillation_is_review_input_not_support
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: outputs/review/2026-06-11-safishamsi-graphify-candidate-distillation.md
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
  - graph
  - query
  source_hash: 570fdd61549384443adf42d624180f9f10473a7ae831daf1c0b8bc8548917ab4
  excluded_reason: candidate_distillation_is_review_input_not_support
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: outputs/review/2026-06-11-guoxun-onefeed-candidate-distillation.md
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
  retrieval_rank: 5
  retrieval_score: 13.0
  matched_terms:
  - graph
  - query
  source_hash: 190687de48f1046fbe077626f70a48509e547a2ea0f0e507d3779f7bb5c53347
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
  retrieval_rank: 6
  retrieval_score: 13.0
  matched_terms:
  - graph
  - implementation
  - query
  source_hash: 926ccda1a8089c5b4ad43e98677a176ef16f4f7e388883ba9c7ad151257aa215
  excluded_reason: no_generic_resolved_source_fact_anchor
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: outputs/review/2026-06-08-bilibili-obsidian-outlinks-graph-candidate-distillation.md
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
  retrieval_rank: 7
  retrieval_score: 12.0
  matched_terms:
  - graph
  - implementation
  source_hash: a67dc11ca4083d17f7da2ad356cfb84109bfe48c72f5f218b6646c3e5708f750
  excluded_reason: candidate_distillation_is_review_input_not_support
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: raw/papers/2026-06-11-guoxun-onefeed-source.md
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
    rank: false
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 8
  retrieval_score: 12.0
  matched_terms:
  - protocol
  - query
  source_hash: 042595fa848562f552dcf6bce1bcfdcb020391cef53e3c01515b0a4216f3df9c
  excluded_reason: no_generic_resolved_source_fact_anchor
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: raw/videos/2026-06-08-bilibili-obsidian-outlinks-graph-source.md
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
    rank: false
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 9
  retrieval_score: 12.0
  matched_terms:
  - graph
  source_hash: 3e279bec2240c0d925ac1281a1b7bd8e0d693dd0b4b28410289ea1f613cbadbe
  excluded_reason: no_generic_resolved_source_fact_anchor
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: raw/repos/2026-06-11-safishamsi-graphify-source.md
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
  retrieval_rank: 10
  retrieval_score: 11.0
  matched_terms:
  - graph
  - implementation
  - query
  source_hash: d8b2b00bf782010353fcdeef45d51338bc503af9c81fb5194125e7d6f23785dc
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
    metadata: false
    rank: false
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 11
  retrieval_score: 10.5
  matched_terms:
  - graph
  - implementation
  - query
  source_hash: be138c5b99e6351f444f8aee37e9000b7821b89e8f357e8a11911ba9e245853c
  excluded_reason: no_generic_resolved_source_fact_anchor
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: raw/papers/2026-05-29-graphfc-source.md
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
    rank: false
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 12
  retrieval_score: 10.0
  matched_terms:
  - graph
  source_hash: 54df60e15d56d99a7e84f282e927f5627808f15128517503d27e33eaea728697
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

# Query Run: G3-17-w3c-prov-full-ontology-decoy

## Live Retrieval Boundary

This artifact was built from a local Markdown corpus scan. It is still read-only sandbox evidence, not Source Intake P0 approval.

## Query Policy

- policy: `qp-review-default-authority-first-local-lexical-v1`
- allowed authority buckets: `reviewed, raw_anchor, candidate, overlay, source_annotation`
- support candidate buckets: `raw_anchor`
- retrieval channels: `local_lexical`

## Top Retrieved Results

- rank 1: `raw/articles/2026-05-29-w3c-prov-source.md` score=25.50 bucket=raw_anchor kind=source_card status=raw
- rank 2: `outputs/review/project_lens_overlays/2026-06-14-benmaster82-Kwipu-vaks-local-graph-rag-overlay.md` score=22.50 bucket=overlay kind=project_overlay status=candidate
- rank 3: `outputs/review/2026-06-11-AxDSan-mnemosyne-candidate-distillation.md` score=14.50 bucket=candidate kind=candidate_distillation status=candidate
- rank 4: `outputs/review/2026-06-11-safishamsi-graphify-candidate-distillation.md` score=14.50 bucket=candidate kind=candidate_distillation status=candidate
- rank 5: `outputs/review/2026-06-11-guoxun-onefeed-candidate-distillation.md` score=13.00 bucket=candidate kind=candidate_distillation status=candidate
- rank 6: `raw/repos/2026-06-14-benmaster82-Kwipu-source.md` score=13.00 bucket=raw_anchor kind=source_card status=raw
- rank 7: `outputs/review/2026-06-08-bilibili-obsidian-outlinks-graph-candidate-distillation.md` score=12.00 bucket=candidate kind=candidate_distillation status=candidate
- rank 8: `raw/papers/2026-06-11-guoxun-onefeed-source.md` score=12.00 bucket=raw_anchor kind=source_card status=raw
- rank 9: `raw/videos/2026-06-08-bilibili-obsidian-outlinks-graph-source.md` score=12.00 bucket=raw_anchor kind=source_card status=raw
- rank 10: `raw/repos/2026-06-11-safishamsi-graphify-source.md` score=11.00 bucket=raw_anchor kind=source_card status=raw
- rank 11: `raw/repos/2026-05-27-knowledge-base-server-source.md` score=10.50 bucket=raw_anchor kind=source_card status=raw
- rank 12: `raw/papers/2026-05-29-graphfc-source.md` score=10.00 bucket=raw_anchor kind=source_card status=raw

## Selected Pack Items

- `raw/articles/2026-05-29-w3c-prov-source.md` -> orientation / raw_is_provenance_only
- `outputs/review/project_lens_overlays/2026-06-14-benmaster82-Kwipu-vaks-local-graph-rag-overlay.md` -> review_input / overlay_not_authority
- `outputs/review/2026-06-11-AxDSan-mnemosyne-candidate-distillation.md` -> review_input / candidate_not_action_basis
- `outputs/review/2026-06-11-safishamsi-graphify-candidate-distillation.md` -> review_input / candidate_not_action_basis
- `outputs/review/2026-06-11-guoxun-onefeed-candidate-distillation.md` -> review_input / candidate_not_action_basis
- `raw/repos/2026-06-14-benmaster82-Kwipu-source.md` -> orientation / raw_is_provenance_only
- `outputs/review/2026-06-08-bilibili-obsidian-outlinks-graph-candidate-distillation.md` -> review_input / candidate_not_action_basis
- `raw/papers/2026-06-11-guoxun-onefeed-source.md` -> orientation / raw_is_provenance_only
- `raw/videos/2026-06-08-bilibili-obsidian-outlinks-graph-source.md` -> orientation / raw_is_provenance_only
- `raw/repos/2026-06-11-safishamsi-graphify-source.md` -> orientation / raw_is_provenance_only
- `raw/repos/2026-05-27-knowledge-base-server-source.md` -> orientation / raw_is_provenance_only
- `raw/papers/2026-05-29-graphfc-source.md` -> orientation / raw_is_provenance_only