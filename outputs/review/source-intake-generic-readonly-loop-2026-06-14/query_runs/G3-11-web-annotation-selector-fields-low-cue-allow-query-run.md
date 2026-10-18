---
record_kind: query_run_trace
status: archived
query_id: G3-11-web-annotation-selector-fields-low-cue-allow
query_time: '2026-06-22T15:34:42+00:00'
question_summary: 'Low-cue allow: test exact/prefix/suffix content without naming the Source Anchor heading.'
verbatim_input: Which selector fields preserve the quote and surrounding snippets so a reviewer can re-find a span?
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
  intent: 'Low-cue allow: test exact/prefix/suffix content without naming the Source Anchor heading.'
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
- ref: raw/repos/2026-06-11-awesome-obsidian-vault/maggieappleton-digital-gardeners-source.md
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
    rank: true
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 1
  retrieval_score: 42.0
  matched_terms:
  - and
  - can
  - re
  - the
  source_hash: 36273939b6ddb5cc4fa89945675a28139eda408b3c54c516a59a10b33fc13668
  excluded_reason: no_generic_resolved_source_fact_anchor
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: raw/repos/2026-06-11-awesome-obsidian-vault/cyanvoxel-obsidian-vault-template-source.md
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
    rank: true
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 2
  retrieval_score: 36.0
  matched_terms:
  - and
  - can
  - find
  - snippets
  - the
  - which
  source_hash: b7dce1d2b1d283c4f77c3a24fbb6dc14aaf8a1c52e57a298deaf7eecb8026b13
  excluded_reason: no_generic_resolved_source_fact_anchor
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: raw/repos/2026-06-11-awesome-obsidian-vault/dotnet-dotnet-api-docs-source.md
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
    rank: true
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 3
  retrieval_score: 35.0
  matched_terms:
  - and
  - snippets
  - the
  source_hash: bcad764c012d956a4b083e8d55bc74d1e9c7058d31da44e5538446fe24d1cd26
  excluded_reason: no_generic_resolved_source_fact_anchor
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: raw/articles/2026-05-30-w3c-web-annotation-source.md
  record_kind: source_card
  knowledge_status: raw
  authority_bucket: raw_anchor
  pack_role: support
  retrieval_role: support_candidate
  support_eligibility: eligible
  eligibility_basis:
  - resolved_stable_anchor_section_content_overlap
  match_representation: raw_markdown_lexical_match
  support_representation: raw_excerpt
  retrieval_channels:
  - local_lexical
  warning_code: raw_is_provenance_only
  action_basis_allowed: false
  truth_mutation_allowed: false
  independent_anchor_ref: raw/articles/2026-05-30-w3c-web-annotation-source.md#Source Anchor
  selected_by:
    lexical: true
    semantic: false
    graph: false
    metadata: false
    rank: true
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 4
  retrieval_score: 31.0
  matched_terms:
  - and
  - can
  - fields
  - find
  - preserve
  - quote
  - re
  - reviewer
  - selector
  - snippets
  - so
  - span
  - surrounding
  - the
  source_hash: e16be8aa931cc46d912429b26446ad7efb8ed49ba7a653512e63e37b14fb28c0
  excluded_reason: resolved_stable_anchor_section_content_overlap
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
    rank: true
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 5
  retrieval_score: 30.5
  matched_terms:
  - and
  - can
  - selector
  - so
  - the
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
  retrieval_rank: 6
  retrieval_score: 30.0
  matched_terms:
  - and
  - can
  - preserve
  - reviewer
  - the
  - which
  source_hash: bdf0f9045aae266725831616c10e88ba7adc2718df5ce927a597a2ad3062308e
  excluded_reason: candidate_distillation_is_review_input_not_support
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
support_checks:
- claim_ref: raw/articles/2026-05-30-w3c-web-annotation-source.md
  independent_anchor_ref: raw/articles/2026-05-30-w3c-web-annotation-source.md#Source Anchor
  result: supported
  resolution:
    status: resolved
    path: raw/articles/2026-05-30-w3c-web-annotation-source.md
    selector: Source Anchor
    source_hash: e16be8aa931cc46d912429b26446ad7efb8ed49ba7a653512e63e37b14fb28c0
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

# Query Run: G3-11-web-annotation-selector-fields-low-cue-allow

## Live Retrieval Boundary

This artifact was built from a local Markdown corpus scan. It is still read-only sandbox evidence, not Source Intake P0 approval.

## Query Policy

- policy: `qp-source_inspection-default-authority-first-local-lexical-v1`
- allowed authority buckets: `reviewed, raw_anchor, candidate, overlay, source_annotation`
- support candidate buckets: `raw_anchor`
- retrieval channels: `local_lexical`

## Top Retrieved Results

- rank 1: `raw/repos/2026-06-11-awesome-obsidian-vault/maggieappleton-digital-gardeners-source.md` score=42.00 bucket=raw_anchor kind=source_card status=raw
- rank 2: `raw/repos/2026-06-11-awesome-obsidian-vault/cyanvoxel-obsidian-vault-template-source.md` score=36.00 bucket=raw_anchor kind=source_card status=raw
- rank 3: `raw/repos/2026-06-11-awesome-obsidian-vault/dotnet-dotnet-api-docs-source.md` score=35.00 bucket=raw_anchor kind=source_card status=raw
- rank 4: `raw/articles/2026-05-30-w3c-web-annotation-source.md` score=31.00 bucket=raw_anchor kind=source_card status=raw
- rank 5: `outputs/review/2026-06-14-kanna12580-kk-knowledge-agent-candidate-distillation.md` score=30.50 bucket=candidate kind=candidate_distillation status=candidate
- rank 6: `outputs/review/2026-06-11-PaddlePaddle-PaddleOCR-candidate-distillation.md` score=30.00 bucket=candidate kind=candidate_distillation status=candidate
- rank 7: `raw/repos/2026-06-11-awesome-obsidian-vault/mayfrost-guides-source.md` score=29.00 bucket=raw_anchor kind=source_card status=raw
- rank 8: `raw/repos/2026-06-11-awesome-obsidian-vault/xxiivv-oscean-source.md` score=28.00 bucket=raw_anchor kind=source_card status=raw
- rank 9: `outputs/review/2026-06-14-agents365-ai-drawio-skill-candidate-distillation.md` score=26.00 bucket=candidate kind=candidate_distillation status=candidate
- rank 10: `raw/articles/2026-06-13-flexnote-docs-source/inspected-pages.md` score=26.00 bucket=raw_anchor kind=source_card status=raw
- rank 11: `raw/repos/2026-06-11-awesome-obsidian-vault/hundredrabbits-grimgrains-source.md` score=25.50 bucket=raw_anchor kind=source_card status=raw
- rank 12: `raw/repos/2026-06-11-trimstray-the-book-of-secret-knowledge-source.md` score=25.50 bucket=raw_anchor kind=source_card status=raw

## Selected Pack Items

- `raw/repos/2026-06-11-awesome-obsidian-vault/maggieappleton-digital-gardeners-source.md` -> orientation / raw_is_provenance_only
- `raw/repos/2026-06-11-awesome-obsidian-vault/cyanvoxel-obsidian-vault-template-source.md` -> orientation / raw_is_provenance_only
- `raw/repos/2026-06-11-awesome-obsidian-vault/dotnet-dotnet-api-docs-source.md` -> orientation / raw_is_provenance_only
- `raw/articles/2026-05-30-w3c-web-annotation-source.md` -> support / raw_is_provenance_only
- `outputs/review/2026-06-14-kanna12580-kk-knowledge-agent-candidate-distillation.md` -> review_input / candidate_not_action_basis
- `outputs/review/2026-06-11-PaddlePaddle-PaddleOCR-candidate-distillation.md` -> review_input / candidate_not_action_basis