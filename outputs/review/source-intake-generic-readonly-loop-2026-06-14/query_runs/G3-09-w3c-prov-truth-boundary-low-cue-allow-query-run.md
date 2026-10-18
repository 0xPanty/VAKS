---
record_kind: query_run_trace
status: archived
query_id: G3-09-w3c-prov-truth-boundary-low-cue-allow
query_time: '2026-06-22T15:34:42+00:00'
question_summary: 'Low-cue allow: name the source family but not the boundary heading; rely on content overlap under the raw
  boundary section.'
verbatim_input: W3C PROV provenance traceability decide truth confidence citation support
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
  intent: 'Low-cue allow: name the source family but not the boundary heading; rely on content overlap under the raw boundary
    section.'
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
  independent_anchor_ref: raw/articles/2026-05-29-w3c-prov-source.md#边界
  selected_by:
    lexical: true
    semantic: false
    graph: false
    metadata: true
    rank: true
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 1
  retrieval_score: 55.0
  matched_terms:
  - citation
  - confidence
  - decide
  - prov
  - provenance
  - support
  - traceability
  - truth
  - w3c
  source_hash: d02636005e119966eb13a08c98a2416f0c99844e72f1740e44901535175e152f
  excluded_reason: resolved_stable_anchor_section_content_overlap
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
  retrieval_score: 30.0
  matched_terms:
  - citation
  - confidence
  - decide
  - provenance
  - support
  - traceability
  - truth
  source_hash: a8ffe7a813e3d107dcb9b0c0bceb82f6f2b9bb0751fd77ccfaccde837a5f4f30
  excluded_reason: candidate_distillation_is_review_input_not_support
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: raw/papers/2026-05-29-prove-provenance-verification-source.md
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
  independent_anchor_ref: raw/papers/2026-05-29-prove-provenance-verification-source.md#边界
  selected_by:
    lexical: true
    semantic: false
    graph: false
    metadata: true
    rank: true
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 3
  retrieval_score: 24.0
  matched_terms:
  - decide
  - provenance
  - support
  - truth
  source_hash: 0babaa8a6d48949250c0415a23e7aa0a60fd5322e57749fbdfee10ec89b1d9c7
  excluded_reason: additional_resolved_anchor_kept_for_drilldown
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
  retrieval_score: 22.0
  matched_terms:
  - confidence
  - decide
  - support
  - truth
  source_hash: a8fe634cba55b59c4348f056d0ba1052d7f0b3815cd1092429e1a944f3359b19
  excluded_reason: candidate_distillation_is_review_input_not_support
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: outputs/review/2026-06-08-cbrain-knowledge-system-mindmap-candidate-distillation.md
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
  retrieval_score: 21.5
  matched_terms:
  - confidence
  - provenance
  - support
  - truth
  source_hash: 0ea68c875f42774bd5bb85e20583eeee6a02dee15d065d4a88d1a9387601c307
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
  retrieval_rank: 6
  retrieval_score: 20.5
  matched_terms:
  - confidence
  - support
  - truth
  source_hash: 2acebe3ef58f6e9872e1e586aad46155e1291d5f747ba3765b247fc35407d7b5
  excluded_reason: candidate_distillation_is_review_input_not_support
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
support_checks:
- claim_ref: raw/articles/2026-05-29-w3c-prov-source.md
  independent_anchor_ref: raw/articles/2026-05-29-w3c-prov-source.md#边界
  result: supported
  resolution:
    status: resolved
    path: raw/articles/2026-05-29-w3c-prov-source.md
    selector: 边界
    source_hash: d02636005e119966eb13a08c98a2416f0c99844e72f1740e44901535175e152f
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

# Query Run: G3-09-w3c-prov-truth-boundary-low-cue-allow

## Live Retrieval Boundary

This artifact was built from a local Markdown corpus scan. It is still read-only sandbox evidence, not Source Intake P0 approval.

## Query Policy

- policy: `qp-review-default-authority-first-local-lexical-v1`
- allowed authority buckets: `reviewed, raw_anchor, candidate, overlay, source_annotation`
- support candidate buckets: `raw_anchor`
- retrieval channels: `local_lexical`

## Top Retrieved Results

- rank 1: `raw/articles/2026-05-29-w3c-prov-source.md` score=55.00 bucket=raw_anchor kind=source_card status=raw
- rank 2: `outputs/review/2026-06-14-google-open-knowledge-format-candidate-distillation.md` score=30.00 bucket=candidate kind=candidate_distillation status=candidate
- rank 3: `raw/papers/2026-05-29-prove-provenance-verification-source.md` score=24.00 bucket=raw_anchor kind=source_card status=raw
- rank 4: `outputs/review/2026-06-12-breferrari-obsidian-mind-candidate-distillation.md` score=22.00 bucket=candidate kind=candidate_distillation status=candidate
- rank 5: `outputs/review/2026-06-08-cbrain-knowledge-system-mindmap-candidate-distillation.md` score=21.50 bucket=candidate kind=candidate_distillation status=candidate
- rank 6: `outputs/review/2026-06-08-bilibili-ioto-obsidian-knowledge-production-system-candidate-distillation.md` score=20.50 bucket=candidate kind=candidate_distillation status=candidate
- rank 7: `outputs/review/2026-06-12-uthvah-sync-embeds-candidate-distillation.md` score=20.00 bucket=candidate kind=candidate_distillation status=candidate
- rank 8: `raw/repos/2026-06-14-rohitg00-agentmemory-source.md` score=20.00 bucket=raw_anchor kind=source_card status=raw
- rank 9: `outputs/review/2026-06-13-bilibili-book-note-workflow-candidate-distillation.md` score=18.50 bucket=candidate kind=candidate_distillation status=candidate
- rank 10: `raw/articles/2026-05-30-w3c-web-annotation-source.md` score=18.50 bucket=raw_anchor kind=source_card status=raw
- rank 11: `outputs/review/2026-06-08-Yaozhuwa-easy-typing-obsidian-candidate-distillation.md` score=17.50 bucket=candidate kind=candidate_distillation status=candidate
- rank 12: `outputs/review/2026-06-11-AxDSan-mnemosyne-candidate-distillation.md` score=17.50 bucket=candidate kind=candidate_distillation status=candidate

## Selected Pack Items

- `raw/articles/2026-05-29-w3c-prov-source.md` -> support / raw_is_provenance_only
- `outputs/review/2026-06-14-google-open-knowledge-format-candidate-distillation.md` -> review_input / candidate_not_action_basis
- `raw/papers/2026-05-29-prove-provenance-verification-source.md` -> anchor / raw_is_provenance_only
- `outputs/review/2026-06-12-breferrari-obsidian-mind-candidate-distillation.md` -> review_input / candidate_not_action_basis
- `outputs/review/2026-06-08-cbrain-knowledge-system-mindmap-candidate-distillation.md` -> review_input / candidate_not_action_basis
- `outputs/review/2026-06-08-bilibili-ioto-obsidian-knowledge-production-system-candidate-distillation.md` -> review_input / candidate_not_action_basis