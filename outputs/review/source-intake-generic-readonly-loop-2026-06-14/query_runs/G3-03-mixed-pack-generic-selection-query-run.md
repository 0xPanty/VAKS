---
record_kind: query_run_trace
status: archived
query_id: G3-03-mixed-pack-generic-selection
query_time: '2026-06-22T15:34:42+00:00'
question_summary: Generic assembler should keep candidate/overlay as review input while selecting resolved raw support.
verbatim_input: FlexNote Extracted Source Facts visual workbench candidate overlay source anchor tag database context pack
  inspected pages
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
  intent: Generic assembler should keep candidate/overlay as review input while selecting resolved raw support.
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
  retrieval_rank: 1
  retrieval_score: 92.5
  matched_terms:
  - anchor
  - candidate
  - context
  - database
  - extracted
  - flexnote
  - inspected
  - overlay
  - pack
  - pages
  - source
  - tag
  - visual
  - workbench
  source_hash: 875108c0ae9d3a00c2e666d3cd4f04eb9475e1a6143fc19c3ec27c3d37928aaf
  excluded_reason: candidate_distillation_is_review_input_not_support
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
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
  retrieval_rank: 2
  retrieval_score: 91.0
  matched_terms:
  - database
  - extracted
  - facts
  - flexnote
  - inspected
  - pages
  - source
  - tag
  - visual
  source_hash: 888f6eac02467a688a294446106759e17a33f79640a8f00633f86211df7dc67d
  excluded_reason: resolved_named_stable_anchor_heading
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
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
  retrieval_rank: 3
  retrieval_score: 87.0
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
  source_hash: fcf83b091b5531a203dd1f236c0907abca47e29b9617a335cb5d7b1576676d54
  excluded_reason: project_overlay_is_project_context_not_support
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
    metadata: true
    rank: true
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 4
  retrieval_score: 74.0
  matched_terms:
  - anchor
  - candidate
  - context
  - pack
  - source
  - tag
  - workbench
  source_hash: b4f0812941e2939688fb04ac05ff5078f3b47307f77a151238bb8e60300c7151
  excluded_reason: candidate_distillation_is_review_input_not_support
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
    metadata: true
    rank: true
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 5
  retrieval_score: 66.5
  matched_terms:
  - candidate
  - context
  - database
  - inspected
  - overlay
  - pack
  - source
  - tag
  source_hash: 95939bb236c67d7dba28e880c3cc280d0bb79d01f47706f1914f3aef5183496e
  excluded_reason: candidate_distillation_is_review_input_not_support
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: outputs/review/2026-06-13-bilibili-edge-recall-contextual-active-recall-candidate-distillation.md
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
  retrieval_rank: 6
  retrieval_score: 65.5
  matched_terms:
  - anchor
  - candidate
  - context
  - overlay
  - pack
  - source
  - workbench
  source_hash: 8242851f349003dcde33540994edbd9a0018f57092e747634485f264091d5913
  excluded_reason: candidate_distillation_is_review_input_not_support
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

# Query Run: G3-03-mixed-pack-generic-selection

## Live Retrieval Boundary

This artifact was built from a local Markdown corpus scan. It is still read-only sandbox evidence, not Source Intake P0 approval.

## Query Policy

- policy: `qp-review-default-authority-first-local-lexical-v1`
- allowed authority buckets: `reviewed, raw_anchor, candidate, overlay, source_annotation`
- support candidate buckets: `raw_anchor`
- retrieval channels: `local_lexical`

## Top Retrieved Results

- rank 1: `outputs/review/2026-06-13-flexnote-docs-candidate-distillation.md` score=92.50 bucket=candidate kind=candidate_distillation status=candidate
- rank 2: `raw/articles/2026-06-13-flexnote-docs-source/inspected-pages.md` score=91.00 bucket=raw_anchor kind=source_card status=raw
- rank 3: `outputs/review/project_lens_overlays/2026-06-13-flexnote-vaks-visual-knowledge-workbench-overlay.md` score=87.00 bucket=overlay kind=project_overlay status=candidate
- rank 4: `outputs/review/2026-06-13-bilibili-book-note-workflow-candidate-distillation.md` score=74.00 bucket=candidate kind=candidate_distillation status=candidate
- rank 5: `outputs/review/2026-06-11-AxDSan-mnemosyne-candidate-distillation.md` score=66.50 bucket=candidate kind=candidate_distillation status=candidate
- rank 6: `outputs/review/2026-06-13-bilibili-edge-recall-contextual-active-recall-candidate-distillation.md` score=65.50 bucket=candidate kind=candidate_distillation status=candidate
- rank 7: `outputs/review/2026-06-11-zhizhuodemao-ai-reverse-toolkit-candidate-distillation.md` score=64.00 bucket=candidate kind=candidate_distillation status=candidate
- rank 8: `outputs/review/2026-06-13-bilibili-obsidian-homepage-plugin-workbench-candidate-distillation.md` score=61.00 bucket=candidate kind=candidate_distillation status=candidate
- rank 9: `outputs/review/2026-06-14-agents365-ai-drawio-skill-candidate-distillation.md` score=58.00 bucket=candidate kind=candidate_distillation status=candidate
- rank 10: `outputs/review/2026-06-14-kanna12580-kk-knowledge-agent-candidate-distillation.md` score=57.00 bucket=candidate kind=candidate_distillation status=candidate
- rank 11: `raw/repos/2026-05-27-dusk-obsidian-vault-source.md` score=56.00 bucket=raw_anchor kind=source_card status=raw
- rank 12: `outputs/review/2026-06-11-cyrilxbt-n8n-obsidian-business-brain-candidate-distillation.md` score=54.50 bucket=candidate kind=candidate_distillation status=candidate

## Selected Pack Items

- `outputs/review/2026-06-13-flexnote-docs-candidate-distillation.md` -> review_input / candidate_not_action_basis
- `raw/articles/2026-06-13-flexnote-docs-source/inspected-pages.md` -> support / raw_is_provenance_only
- `outputs/review/project_lens_overlays/2026-06-13-flexnote-vaks-visual-knowledge-workbench-overlay.md` -> review_input / overlay_not_authority
- `outputs/review/2026-06-13-bilibili-book-note-workflow-candidate-distillation.md` -> review_input / candidate_not_action_basis
- `outputs/review/2026-06-11-AxDSan-mnemosyne-candidate-distillation.md` -> review_input / candidate_not_action_basis
- `outputs/review/2026-06-13-bilibili-edge-recall-contextual-active-recall-candidate-distillation.md` -> review_input / candidate_not_action_basis