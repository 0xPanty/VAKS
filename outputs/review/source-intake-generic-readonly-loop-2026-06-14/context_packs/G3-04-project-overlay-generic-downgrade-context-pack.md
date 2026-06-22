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
query_run_ref: query_runs/G3-04-project-overlay-generic-downgrade-query-run.md
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
  intent: Generic assembler should not let a project overlay become final support.
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
- ref: outputs/review/project_lens_overlays/2026-06-13-flexnote-vaks-visual-knowledge-workbench-overlay.md
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
  retrieval_rank: 1
  retrieval_score: 88.5
  matched_terms:
  - flexnote
  - overlay
  - project
  - support
  - visual
  - workbench
  source_hash: fcf83b091b5531a203dd1f236c0907abca47e29b9617a335cb5d7b1576676d54
  excluded_reason: project_overlay_is_project_context_not_support
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: outputs/review/project_lens_overlays/2026-06-14-agents365-ai-drawio-skill-vaks-visualization-overlay.md
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
  retrieval_score: 41.0
  matched_terms:
  - overlay
  - project
  - support
  - visual
  source_hash: 61fa61be313c54388fd9ff11283b4eb92d28018713c1067125a1d39efd59e6a3
  excluded_reason: project_overlay_is_project_context_not_support
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: outputs/review/2026-06-13-flexnote-docs-candidate-distillation.md
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
  retrieval_rank: 3
  retrieval_score: 40.5
  matched_terms:
  - flexnote
  - overlay
  - project
  - support
  - visual
  - workbench
  source_hash: 875108c0ae9d3a00c2e666d3cd4f04eb9475e1a6143fc19c3ec27c3d37928aaf
  excluded_reason: candidate_distillation_is_review_input_not_support
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: outputs/review/project_lens_overlays/2026-06-14-kanna12580-kk-knowledge-agent-misa-kb-memory-overlay.md
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
  retrieval_rank: 4
  retrieval_score: 39.0
  matched_terms:
  - overlay
  - project
  - support
  source_hash: 24cebf26e26cfd69186c5ee4a976c8bdd12bf60feaf6233c582f6ac7cdc13636
  excluded_reason: project_overlay_is_project_context_not_support
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
  retrieval_rank: 5
  retrieval_score: 38.5
  matched_terms:
  - overlay
  - project
  - support
  source_hash: 062b96779d75bc7e4dc572e309a16e9e023bc37e86f838ecc99d0039ebd710cb
  excluded_reason: project_overlay_is_project_context_not_support
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: outputs/review/project_lens_overlays/2026-06-14-adithya-s-k-omniparse-vaks-raw-intake-overlay.md
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
    rank: false
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 6
  retrieval_score: 34.5
  matched_terms:
  - overlay
  - project
  - support
  source_hash: 905b00fe0774cd7462b60709a27ccafa8d64f60b6fefbfafd5276b1aa1f05e7c
  excluded_reason: project_overlay_is_project_context_not_support
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
    metadata: true
    rank: false
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 7
  retrieval_score: 34.5
  matched_terms:
  - overlay
  - project
  source_hash: a3e9c37feba9649bbf312c9fd73fa0a0f1d65d27bea528294234f60ca1902cad
  excluded_reason: project_overlay_is_project_context_not_support
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: outputs/review/project_lens_overlays/2026-06-14-edochi-mdvs-vaks-validation-search-overlay.md
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
    rank: false
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 8
  retrieval_score: 33.5
  matched_terms:
  - overlay
  - project
  - support
  source_hash: 7d7f81930b0b1456aed7884921abb1e26656f52908651b67cceac47a7b9ad257
  excluded_reason: project_overlay_is_project_context_not_support
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: raw/articles/2026-06-13-flexnote-docs-source.md
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
    rank: false
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 9
  retrieval_score: 29.5
  matched_terms:
  - flexnote
  - overlay
  - project
  - visual
  - workbench
  source_hash: b60e969515a9f112f85797ac62a52c3536515147a64149353c824eeeb5127800
  excluded_reason: query_mode_not_readonly_support_mode
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: outputs/review/2026-06-13-bilibili-obsidian-homepage-plugin-workbench-candidate-distillation.md
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
  retrieval_rank: 10
  retrieval_score: 28.0
  matched_terms:
  - project
  - support
  - workbench
  source_hash: 42c844a6c02cd25e7c3c4f87d4ab0d39490569bfccffc75b1b7292966ff3da85
  excluded_reason: candidate_distillation_is_review_input_not_support
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: outputs/review/project_lens_overlays/2026-06-13-bilibili-book-note-workflow-vaks-reading-intake-overlay.md
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
    rank: false
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 11
  retrieval_score: 25.5
  matched_terms:
  - overlay
  - project
  - support
  - workbench
  source_hash: cf36ab001550a571f98a148938562d4f88fe79600040a1d3754d14cd97bf1b64
  excluded_reason: project_overlay_is_project_context_not_support
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: raw/articles/2026-06-13-flexnote-docs-source/inspected-pages.md
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
    rank: false
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 12
  retrieval_score: 23.5
  matched_terms:
  - flexnote
  - support
  - visual
  source_hash: 888f6eac02467a688a294446106759e17a33f79640a8f00633f86211df7dc67d
  excluded_reason: query_mode_not_readonly_support_mode
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

# Context Pack: G3-04-project-overlay-generic-downgrade

## Boundary

This pack is a read-only attention surface. It is not action basis and does not write truth.

## Support Selection

- not_ready: `no_final_support_selected` anchor=``