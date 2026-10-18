---
record_kind: query_run_trace
status: archived
query_id: G3-13-web-annotation-action-basis-decoy
query_time: '2026-06-22T15:34:42+00:00'
question_summary: 'Decoy: action mode must not produce final support even when anchor-like terms are present.'
verbatim_input: Use W3C Web Annotation exact prefix suffix as an action basis now
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
  intent: 'Decoy: action mode must not produce final support even when anchor-like terms are present.'
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
- ref: raw/articles/2026-05-30-w3c-web-annotation-source.md
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
  retrieval_rank: 1
  retrieval_score: 65.5
  matched_terms:
  - annotation
  - as
  - exact
  - prefix
  - suffix
  - w3c
  - web
  source_hash: e16be8aa931cc46d912429b26446ad7efb8ed49ba7a653512e63e37b14fb28c0
  excluded_reason: query_mode_not_readonly_support_mode
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
  retrieval_score: 30.5
  matched_terms:
  - action
  - an
  - as
  - basis
  - use
  source_hash: a8ffe7a813e3d107dcb9b0c0bceb82f6f2b9bb0751fd77ccfaccde837a5f4f30
  excluded_reason: candidate_distillation_is_review_input_not_support
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
    metadata: false
    rank: true
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 3
  retrieval_score: 30.0
  matched_terms:
  - action
  - as
  - basis
  - now
  - use
  source_hash: 42c844a6c02cd25e7c3c4f87d4ab0d39490569bfccffc75b1b7292966ff3da85
  excluded_reason: candidate_distillation_is_review_input_not_support
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: raw/videos/2026-06-04-youtube-hermes-obsidian-source.md
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
  retrieval_rank: 4
  retrieval_score: 29.0
  matched_terms:
  - action
  - an
  - as
  - basis
  - exact
  - now
  - use
  source_hash: 4d58e7a6f9d936d58756152801e2b12b588d5440c331730b7d3bc5621d83e65b
  excluded_reason: query_mode_not_readonly_support_mode
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
  retrieval_score: 25.5
  matched_terms:
  - action
  - an
  - as
  - basis
  - use
  source_hash: 19a685b5f8d9ae7d2e8c3ba0bb5fef04150d2cf8f2811174861397ebf3ae7dc8
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
  retrieval_rank: 6
  retrieval_score: 25.0
  matched_terms:
  - action
  - an
  - as
  - basis
  - now
  - use
  source_hash: a8fe634cba55b59c4348f056d0ba1052d7f0b3815cd1092429e1a944f3359b19
  excluded_reason: candidate_distillation_is_review_input_not_support
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: outputs/review/2026-06-12-uthvah-sync-embeds-candidate-distillation.md
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
  retrieval_score: 24.0
  matched_terms:
  - action
  - an
  - as
  - basis
  - use
  source_hash: 8bb5069adbbb370ca51bdc002455e8e08fbfd78bfd22dc4c0f30c9f76f8230ce
  excluded_reason: candidate_distillation_is_review_input_not_support
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: raw/articles/2026-05-29-w3c-prov-source.md
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
  retrieval_rank: 8
  retrieval_score: 23.5
  matched_terms:
  - use
  - w3c
  source_hash: d02636005e119966eb13a08c98a2416f0c99844e72f1740e44901535175e152f
  excluded_reason: query_mode_not_readonly_support_mode
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
    metadata: false
    rank: false
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 9
  retrieval_score: 23.0
  matched_terms:
  - action
  - annotation
  - as
  - basis
  - web
  source_hash: 875108c0ae9d3a00c2e666d3cd4f04eb9475e1a6143fc19c3ec27c3d37928aaf
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
  retrieval_rank: 10
  retrieval_score: 23.0
  matched_terms:
  - action
  - as
  - basis
  - use
  source_hash: 210bef25145cba4013a716374083098fa438568e19ad99a3e40324f2e854efe7
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
    metadata: false
    rank: false
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 11
  retrieval_score: 22.5
  matched_terms:
  - action
  - an
  - as
  - basis
  - exact
  source_hash: 95939bb236c67d7dba28e880c3cc280d0bb79d01f47706f1914f3aef5183496e
  excluded_reason: candidate_distillation_is_review_input_not_support
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: outputs/review/2026-06-14-agents365-ai-drawio-skill-candidate-distillation.md
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
  retrieval_score: 21.0
  matched_terms:
  - action
  - an
  - as
  - basis
  - exact
  - use
  source_hash: 7784ff211228cdcbc6c0b96081f8371fc83a27d71bb355843854d7eb0b2f6eda
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

# Query Run: G3-13-web-annotation-action-basis-decoy

## Live Retrieval Boundary

This artifact was built from a local Markdown corpus scan. It is still read-only sandbox evidence, not Source Intake P0 approval.

## Query Policy

- policy: `qp-action-default-authority-first-local-lexical-v1`
- allowed authority buckets: `reviewed, raw_anchor, candidate, overlay, source_annotation`
- support candidate buckets: ``
- retrieval channels: `local_lexical`

## Top Retrieved Results

- rank 1: `raw/articles/2026-05-30-w3c-web-annotation-source.md` score=65.50 bucket=raw_anchor kind=source_card status=raw
- rank 2: `outputs/review/2026-06-14-google-open-knowledge-format-candidate-distillation.md` score=30.50 bucket=candidate kind=candidate_distillation status=candidate
- rank 3: `outputs/review/2026-06-13-bilibili-obsidian-homepage-plugin-workbench-candidate-distillation.md` score=30.00 bucket=candidate kind=candidate_distillation status=candidate
- rank 4: `raw/videos/2026-06-04-youtube-hermes-obsidian-source.md` score=29.00 bucket=raw_anchor kind=source_card status=raw
- rank 5: `outputs/review/2026-06-14-kanna12580-kk-knowledge-agent-candidate-distillation.md` score=25.50 bucket=candidate kind=candidate_distillation status=candidate
- rank 6: `outputs/review/2026-06-12-breferrari-obsidian-mind-candidate-distillation.md` score=25.00 bucket=candidate kind=candidate_distillation status=candidate
- rank 7: `outputs/review/2026-06-12-uthvah-sync-embeds-candidate-distillation.md` score=24.00 bucket=candidate kind=candidate_distillation status=candidate
- rank 8: `raw/articles/2026-05-29-w3c-prov-source.md` score=23.50 bucket=raw_anchor kind=source_card status=raw
- rank 9: `outputs/review/2026-06-13-flexnote-docs-candidate-distillation.md` score=23.00 bucket=candidate kind=candidate_distillation status=candidate
- rank 10: `outputs/review/2026-06-14-edochi-mdvs-candidate-distillation.md` score=23.00 bucket=candidate kind=candidate_distillation status=candidate
- rank 11: `outputs/review/2026-06-11-AxDSan-mnemosyne-candidate-distillation.md` score=22.50 bucket=candidate kind=candidate_distillation status=candidate
- rank 12: `outputs/review/2026-06-14-agents365-ai-drawio-skill-candidate-distillation.md` score=21.00 bucket=candidate kind=candidate_distillation status=candidate

## Selected Pack Items

- `raw/articles/2026-05-30-w3c-web-annotation-source.md` -> orientation / raw_is_provenance_only
- `outputs/review/2026-06-14-google-open-knowledge-format-candidate-distillation.md` -> review_input / candidate_not_action_basis
- `outputs/review/2026-06-13-bilibili-obsidian-homepage-plugin-workbench-candidate-distillation.md` -> review_input / candidate_not_action_basis
- `raw/videos/2026-06-04-youtube-hermes-obsidian-source.md` -> orientation / raw_is_provenance_only
- `outputs/review/2026-06-14-kanna12580-kk-knowledge-agent-candidate-distillation.md` -> review_input / candidate_not_action_basis
- `outputs/review/2026-06-12-breferrari-obsidian-mind-candidate-distillation.md` -> review_input / candidate_not_action_basis
- `outputs/review/2026-06-12-uthvah-sync-embeds-candidate-distillation.md` -> review_input / candidate_not_action_basis
- `raw/articles/2026-05-29-w3c-prov-source.md` -> orientation / raw_is_provenance_only
- `outputs/review/2026-06-13-flexnote-docs-candidate-distillation.md` -> review_input / candidate_not_action_basis
- `outputs/review/2026-06-14-edochi-mdvs-candidate-distillation.md` -> review_input / candidate_not_action_basis
- `outputs/review/2026-06-11-AxDSan-mnemosyne-candidate-distillation.md` -> review_input / candidate_not_action_basis
- `outputs/review/2026-06-14-agents365-ai-drawio-skill-candidate-distillation.md` -> review_input / candidate_not_action_basis