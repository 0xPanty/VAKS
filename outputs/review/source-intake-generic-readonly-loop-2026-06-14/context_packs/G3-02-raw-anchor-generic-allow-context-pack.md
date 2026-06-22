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
query_run_ref: query_runs/G3-02-raw-anchor-generic-allow-query-run.md
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
  intent: Generic assembler may allow a naturally retrieved raw/stable anchor in read-only mode.
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
- ref: raw/articles/2026-06-13-flexnote-docs-source/inspected-pages.md
  record_kind: source_card
  knowledge_status: raw
  authority_bucket: raw_anchor
  pack_role: support
  retrieval_role: support_candidate
  support_eligibility: eligible
  eligibility_basis:
  - resolved_named_stable_anchor_heading
  match_representation: raw_markdown_lexical_match
  support_representation: raw_excerpt
  retrieval_channels:
  - local_lexical
  warning_code: raw_is_provenance_only
  action_basis_allowed: false
  truth_mutation_allowed: false
  independent_anchor_ref: raw/articles/2026-06-13-flexnote-docs-source/inspected-pages.md#Extracted Source Facts
  selected_by:
    lexical: true
    semantic: false
    graph: false
    metadata: true
    rank: true
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 1
  retrieval_score: 104.0
  matched_terms:
  - card
  - database
  - extracted
  - facts
  - first
  - flexnote
  - inspected
  - local
  - pages
  - source
  - tag
  source_hash: 888f6eac02467a688a294446106759e17a33f79640a8f00633f86211df7dc67d
  excluded_reason: resolved_named_stable_anchor_heading
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
  retrieval_rank: 2
  retrieval_score: 56.0
  matched_terms:
  - card
  - database
  - extracted
  - first
  - flexnote
  - inspected
  - local
  - pages
  - source
  - tag
  source_hash: 875108c0ae9d3a00c2e666d3cd4f04eb9475e1a6143fc19c3ec27c3d37928aaf
  excluded_reason: candidate_distillation_is_review_input_not_support
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
  retrieval_rank: 3
  retrieval_score: 41.5
  matched_terms:
  - database
  - extracted
  - first
  - local
  - source
  - tag
  source_hash: be138c5b99e6351f444f8aee37e9000b7821b89e8f357e8a11911ba9e245853c
  excluded_reason: no_generic_resolved_source_fact_anchor
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: raw/articles/2026-06-13-flexnote-docs-source.md
  record_kind: source_card
  knowledge_status: raw
  authority_bucket: raw_anchor
  pack_role: anchor
  retrieval_role: support_candidate
  support_eligibility: eligible
  eligibility_basis:
  - additional_resolved_anchor_kept_for_drilldown
  match_representation: raw_markdown_lexical_match
  support_representation: raw_excerpt
  retrieval_channels:
  - local_lexical
  warning_code: raw_is_provenance_only
  action_basis_allowed: false
  truth_mutation_allowed: false
  independent_anchor_ref: raw/articles/2026-06-13-flexnote-docs-source.md#初步看点
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
  - card
  - database
  - first
  - flexnote
  - inspected
  - local
  - pages
  - source
  - tag
  source_hash: b60e969515a9f112f85797ac62a52c3536515147a64149353c824eeeb5127800
  excluded_reason: additional_resolved_anchor_kept_for_drilldown
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: raw/repos/2026-05-27-kagantic-vault-structure-source.md
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
  retrieval_rank: 5
  retrieval_score: 37.5
  matched_terms:
  - first
  - inspected
  - local
  - pages
  - source
  - tag
  source_hash: be1fc4bd29ef877afa5c5a1e289f1eff1b1efc5afc26c9eb549bacf13d647833
  excluded_reason: no_generic_resolved_source_fact_anchor
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: raw/repos/2026-05-27-dusk-obsidian-vault-source.md
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
  retrieval_rank: 6
  retrieval_score: 35.5
  matched_terms:
  - inspected
  - local
  - source
  - tag
  source_hash: fda2831fec735c8e20c8c2cf28875629d3ae8256d73b527be2fa3c75ad5b50a1
  excluded_reason: no_generic_resolved_source_fact_anchor
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
support_checks:
- claim_ref: raw/articles/2026-06-13-flexnote-docs-source/inspected-pages.md
  independent_anchor_ref: raw/articles/2026-06-13-flexnote-docs-source/inspected-pages.md#Extracted Source Facts
  result: supported
  resolution:
    status: resolved
    path: raw/articles/2026-06-13-flexnote-docs-source/inspected-pages.md
    selector: Extracted Source Facts
    source_hash: 888f6eac02467a688a294446106759e17a33f79640a8f00633f86211df7dc67d
    heading_match: true
    string_match: true
    method: path_selector_heading_or_string_resolution
    semantic_support_status: not_external_judged
    freshness_or_drift_status: source_hash_captured_no_remote_drift_check
  reason: resolved_raw_stable_anchor_structural_only
  semantic_support_status: not_external_judged
human_confirmation_required: false
artifact_kind: live_readonly_test_artifact
retrieval_exclusion: true
default_retrieval: false
indexing_policy: exclude_from_default_retrieval_graph_pack_support
truth_mutation_allowed: false
action_basis_allowed: false
---

# Context Pack: G3-02-raw-anchor-generic-allow

## Boundary

This pack is a read-only attention surface. It is not action basis and does not write truth.

## Support Selection

- supported: `raw/articles/2026-06-13-flexnote-docs-source/inspected-pages.md` anchor=`raw/articles/2026-06-13-flexnote-docs-source/inspected-pages.md#Extracted Source Facts`