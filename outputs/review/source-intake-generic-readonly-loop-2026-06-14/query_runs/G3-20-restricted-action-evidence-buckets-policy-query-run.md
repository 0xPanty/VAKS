---
record_kind: query_run_trace
status: archived
query_id: G3-20-restricted-action-evidence-buckets-policy
query_time: '2026-06-22T15:34:42+00:00'
question_summary: 'Default restricted action case: only reviewed/raw_anchor buckets may enter retrieval; no support candidate
  bucket is allowed.'
verbatim_input: Use PROV traceability as truth confidence and action basis now
active_project: VAKS
query_mode: action
use_mode: action
risk_tier: high
policy_ref: qp-action-default-restricted-action-evidence-authority-first-local-lexical-v1
requested_authority_bucket: authority_first_readonly_bucket_plan
included_buckets:
- reviewed
- raw_anchor
excluded_buckets:
- reviewed_write_path
- action_basis
- truth_mutation
query_policy:
  policy_id: qp-action-default-restricted-action-evidence-authority-first-local-lexical-v1
  policy_version: 2026-06-15-pro-retrieval-plane-step1
  use_mode: action
  risk_tier: high
  intent: 'Default restricted action case: only reviewed/raw_anchor buckets may enter retrieval; no support candidate bucket
    is allowed.'
  authority_filter_mode: bucket_first_before_ranking
  allowed_authority_buckets:
  - reviewed
  - raw_anchor
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
  post_filter_doc_count: 157
  excluded_doc_count: 53
  pre_filter_bucket_counts:
    candidate: 40
    overlay: 8
    source_annotation: 5
    raw_anchor: 156
    reviewed: 1
  post_filter_bucket_counts:
    raw_anchor: 156
    reviewed: 1
  excluded_bucket_counts:
    candidate: 40
    overlay: 8
    source_annotation: 5
  excluded_path_sample:
  - outputs/review/2026-06-07-aal-ruller-pkm-second-brain-ai-companian-candidate-distillation.md
  - outputs/review/2026-06-08-bilibili-claudian-obsidian-skill-workflow-candidate-distillation.md
  - outputs/review/2026-06-08-bilibili-codex-obsidian-minimal-loop-candidate-distillation.md
  - outputs/review/2026-06-08-bilibili-ioto-obsidian-knowledge-production-system-candidate-distillation.md
  - outputs/review/2026-06-08-bilibili-modular-obsidian-official-site-candidate-distillation.md
  - outputs/review/2026-06-08-bilibili-obsidian-outlinks-graph-candidate-distillation.md
  - outputs/review/2026-06-08-bilibili-pdf-to-obsidian-paper-intake-candidate-distillation.md
  - outputs/review/2026-06-08-cbrain-knowledge-system-mindmap-candidate-distillation.md
  - outputs/review/2026-06-08-Momoyu404-geminese-candidate-distillation.md
  - outputs/review/2026-06-08-sumruler-typora-theme-phycat-candidate-distillation.md
  query_policy_id: qp-action-default-restricted-action-evidence-authority-first-local-lexical-v1
  retrieval_channels:
  - local_lexical
  fusion_method: none_single_local_lexical_channel
  rerank_method: none
  returned_hit_count: 12
retrieval_filters:
  authority_bucket_filter_applied_before_ranking: true
  include_candidates: false
  include_overlays: false
  include_source_annotations: false
  include_runtime_test_artifacts: false
  writeback_allowed: false
  promotion_allowed: false
  truth_mutation_allowed: false
selected_items:
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
  retrieval_rank: 1
  retrieval_score: 36.0
  matched_terms:
  - action
  - and
  - as
  - basis
  - confidence
  - now
  - truth
  - use
  source_hash: 4d58e7a6f9d936d58756152801e2b12b588d5440c331730b7d3bc5621d83e65b
  excluded_reason: query_mode_not_readonly_support_mode
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
  retrieval_rank: 2
  retrieval_score: 35.0
  matched_terms:
  - action
  - and
  - as
  - basis
  - confidence
  - truth
  source_hash: 28ba0a38756b80bd67732ad47ecd4e265455e116593f63620dc6442884e39d9c
  excluded_reason: query_mode_not_readonly_support_mode
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
    rank: true
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 3
  retrieval_score: 34.5
  matched_terms:
  - and
  - confidence
  - prov
  - traceability
  - truth
  - use
  source_hash: d02636005e119966eb13a08c98a2416f0c99844e72f1740e44901535175e152f
  excluded_reason: query_mode_not_readonly_support_mode
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
  retrieval_score: 31.0
  matched_terms:
  - action
  - and
  - as
  - confidence
  - truth
  - use
  source_hash: be138c5b99e6351f444f8aee37e9000b7821b89e8f357e8a11911ba9e245853c
  excluded_reason: query_mode_not_readonly_support_mode
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: raw/videos/2026-06-08-xhs-knowledge-base-not-use-source.md
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
  retrieval_rank: 5
  retrieval_score: 31.0
  matched_terms:
  - action
  - and
  - basis
  - confidence
  - truth
  - use
  source_hash: 70f4303e60d8b5e7a132c61725d01cad48dd11e45959497d752744885843b639
  excluded_reason: query_mode_not_readonly_support_mode
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: raw/repos/2026-06-11-awesome-obsidian-vault/maggieappleton-digital-gardeners-source.md
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
    rank: false
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 6
  retrieval_score: 29.5
  matched_terms:
  - action
  - and
  - as
  - basis
  - confidence
  - truth
  source_hash: 36273939b6ddb5cc4fa89945675a28139eda408b3c54c516a59a10b33fc13668
  excluded_reason: query_mode_not_readonly_support_mode
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: raw/repos/2026-06-14-kanna12580-kk-knowledge-agent-source.md
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
    rank: false
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 7
  retrieval_score: 29.0
  matched_terms:
  - action
  - and
  - as
  - basis
  - truth
  - use
  source_hash: d4a4a4000279e566189c2a2b651fcd7ef96c1dbbc3bd30cc735ad0245c21921f
  excluded_reason: query_mode_not_readonly_support_mode
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
    rank: false
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 8
  retrieval_score: 28.0
  matched_terms:
  - action
  - and
  - as
  - basis
  - now
  - truth
  - use
  source_hash: f3a16afdd0e9f060c68674c59cb3719a536710f185d19a3d7b9095d945557f4b
  excluded_reason: query_mode_not_readonly_support_mode
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: raw/repos/2026-06-14-agents365-ai-drawio-skill-source.md
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
    rank: false
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 9
  retrieval_score: 28.0
  matched_terms:
  - action
  - and
  - as
  - basis
  - truth
  - use
  source_hash: 78315218d16aa9eb7ae11f03b5abb9b373be5a43b771ff24892dec6e14159298
  excluded_reason: query_mode_not_readonly_support_mode
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: raw/repos/2026-06-08-Yaozhuwa-easy-typing-obsidian-source.md
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
    rank: false
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 10
  retrieval_score: 27.0
  matched_terms:
  - action
  - and
  - as
  - basis
  - confidence
  - truth
  - use
  source_hash: b7abe7b06abbb6a6d3db1e6cf010587f0b44f948985bf2ab69e43757a1d82d88
  excluded_reason: query_mode_not_readonly_support_mode
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: raw/repos/2026-05-27-kepano-obsidian-source.md
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
    rank: false
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 11
  retrieval_score: 26.0
  matched_terms:
  - action
  - and
  - as
  - confidence
  - truth
  - use
  source_hash: 927127052d181b160c23ee65e8704191efd53bc3473467a3e8fdc098cfdc2527
  excluded_reason: query_mode_not_readonly_support_mode
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: raw/repos/2026-06-08-sumruler-typora-theme-phycat-source.md
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
    rank: false
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 12
  retrieval_score: 26.0
  matched_terms:
  - action
  - and
  - as
  - basis
  - confidence
  - truth
  - use
  source_hash: f15a19a3295e00581daa675b3bc33e1baa133bac713ee3782b652e0eee1f2dba
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

# Query Run: G3-20-restricted-action-evidence-buckets-policy

## Live Retrieval Boundary

This artifact was built from a local Markdown corpus scan. It is still read-only sandbox evidence, not Source Intake P0 approval.

## Query Policy

- policy: `qp-action-default-restricted-action-evidence-authority-first-local-lexical-v1`
- allowed authority buckets: `reviewed, raw_anchor`
- support candidate buckets: ``
- retrieval channels: `local_lexical`

## Top Retrieved Results

- rank 1: `raw/videos/2026-06-04-youtube-hermes-obsidian-source.md` score=36.00 bucket=raw_anchor kind=source_card status=raw
- rank 2: `raw/repos/2026-06-14-rohitg00-agentmemory-source.md` score=35.00 bucket=raw_anchor kind=source_card status=raw
- rank 3: `raw/articles/2026-05-29-w3c-prov-source.md` score=34.50 bucket=raw_anchor kind=source_card status=raw
- rank 4: `raw/repos/2026-05-27-knowledge-base-server-source.md` score=31.00 bucket=raw_anchor kind=source_card status=raw
- rank 5: `raw/videos/2026-06-08-xhs-knowledge-base-not-use-source.md` score=31.00 bucket=raw_anchor kind=source_card status=raw
- rank 6: `raw/repos/2026-06-11-awesome-obsidian-vault/maggieappleton-digital-gardeners-source.md` score=29.50 bucket=raw_anchor kind=source_card status=raw
- rank 7: `raw/repos/2026-06-14-kanna12580-kk-knowledge-agent-source.md` score=29.00 bucket=raw_anchor kind=source_card status=raw
- rank 8: `raw/repos/2026-06-12-breferrari-obsidian-mind-source.md` score=28.00 bucket=raw_anchor kind=source_card status=raw
- rank 9: `raw/repos/2026-06-14-agents365-ai-drawio-skill-source.md` score=28.00 bucket=raw_anchor kind=source_card status=raw
- rank 10: `raw/repos/2026-06-08-Yaozhuwa-easy-typing-obsidian-source.md` score=27.00 bucket=raw_anchor kind=source_card status=raw
- rank 11: `raw/repos/2026-05-27-kepano-obsidian-source.md` score=26.00 bucket=raw_anchor kind=source_card status=raw
- rank 12: `raw/repos/2026-06-08-sumruler-typora-theme-phycat-source.md` score=26.00 bucket=raw_anchor kind=source_card status=raw

## Selected Pack Items

- `raw/videos/2026-06-04-youtube-hermes-obsidian-source.md` -> orientation / raw_is_provenance_only
- `raw/repos/2026-06-14-rohitg00-agentmemory-source.md` -> orientation / raw_is_provenance_only
- `raw/articles/2026-05-29-w3c-prov-source.md` -> orientation / raw_is_provenance_only
- `raw/repos/2026-05-27-knowledge-base-server-source.md` -> orientation / raw_is_provenance_only
- `raw/videos/2026-06-08-xhs-knowledge-base-not-use-source.md` -> orientation / raw_is_provenance_only
- `raw/repos/2026-06-11-awesome-obsidian-vault/maggieappleton-digital-gardeners-source.md` -> orientation / raw_is_provenance_only
- `raw/repos/2026-06-14-kanna12580-kk-knowledge-agent-source.md` -> orientation / raw_is_provenance_only
- `raw/repos/2026-06-12-breferrari-obsidian-mind-source.md` -> orientation / raw_is_provenance_only
- `raw/repos/2026-06-14-agents365-ai-drawio-skill-source.md` -> orientation / raw_is_provenance_only
- `raw/repos/2026-06-08-Yaozhuwa-easy-typing-obsidian-source.md` -> orientation / raw_is_provenance_only
- `raw/repos/2026-05-27-kepano-obsidian-source.md` -> orientation / raw_is_provenance_only
- `raw/repos/2026-06-08-sumruler-typora-theme-phycat-source.md` -> orientation / raw_is_provenance_only