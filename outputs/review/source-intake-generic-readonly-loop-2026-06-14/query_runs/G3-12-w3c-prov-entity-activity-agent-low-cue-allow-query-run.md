---
record_kind: query_run_trace
status: archived
query_id: G3-12-w3c-prov-entity-activity-agent-low-cue-allow
query_time: '2026-06-22T15:34:42+00:00'
question_summary: 'Low-cue allow: name the source family but not the source heading; test PROV entity/activity/agent content.'
verbatim_input: W3C PROV entities activities agents lightweight provenance skeleton source records
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
  intent: 'Low-cue allow: name the source family but not the source heading; test PROV entity/activity/agent content.'
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
  independent_anchor_ref: raw/articles/2026-05-29-w3c-prov-source.md#初步看点
  selected_by:
    lexical: true
    semantic: false
    graph: false
    metadata: true
    rank: true
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 1
  retrieval_score: 69.5
  matched_terms:
  - activities
  - agents
  - entities
  - lightweight
  - prov
  - provenance
  - records
  - skeleton
  - source
  - w3c
  source_hash: d02636005e119966eb13a08c98a2416f0c99844e72f1740e44901535175e152f
  excluded_reason: resolved_stable_anchor_section_content_overlap
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: raw/articles/2026-05-30-w3c-web-annotation-source.md
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
  independent_anchor_ref: raw/articles/2026-05-30-w3c-web-annotation-source.md#Source Anchor
  selected_by:
    lexical: true
    semantic: false
    graph: false
    metadata: true
    rank: true
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 2
  retrieval_score: 38.5
  matched_terms:
  - provenance
  - source
  - w3c
  source_hash: e16be8aa931cc46d912429b26446ad7efb8ed49ba7a653512e63e37b14fb28c0
  excluded_reason: additional_resolved_anchor_kept_for_drilldown
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
  retrieval_score: 33.5
  matched_terms:
  - agents
  - lightweight
  - records
  - source
  source_hash: be138c5b99e6351f444f8aee37e9000b7821b89e8f357e8a11911ba9e245853c
  excluded_reason: no_generic_resolved_source_fact_anchor
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
- ref: raw/papers/2026-05-29-prove-provenance-verification-source.md
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
  retrieval_rank: 4
  retrieval_score: 29.5
  matched_terms:
  - provenance
  - source
  source_hash: 0babaa8a6d48949250c0415a23e7aa0a60fd5322e57749fbdfee10ec89b1d9c7
  excluded_reason: no_generic_resolved_source_fact_anchor
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
  retrieval_score: 29.5
  matched_terms:
  - agents
  - lightweight
  - source
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
  retrieval_score: 27.5
  matched_terms:
  - source
  source_hash: fda2831fec735c8e20c8c2cf28875629d3ae8256d73b527be2fa3c75ad5b50a1
  excluded_reason: no_generic_resolved_source_fact_anchor
  assembler_rule: generic_record_kind_status_anchor_rule
  case_scripted_selection: false
support_checks:
- claim_ref: raw/articles/2026-05-29-w3c-prov-source.md
  independent_anchor_ref: raw/articles/2026-05-29-w3c-prov-source.md#初步看点
  result: supported
  resolution:
    status: resolved
    path: raw/articles/2026-05-29-w3c-prov-source.md
    selector: 初步看点
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

# Query Run: G3-12-w3c-prov-entity-activity-agent-low-cue-allow

## Live Retrieval Boundary

This artifact was built from a local Markdown corpus scan. It is still read-only sandbox evidence, not Source Intake P0 approval.

## Query Policy

- policy: `qp-review-default-authority-first-local-lexical-v1`
- allowed authority buckets: `reviewed, raw_anchor, candidate, overlay, source_annotation`
- support candidate buckets: `raw_anchor`
- retrieval channels: `local_lexical`

## Top Retrieved Results

- rank 1: `raw/articles/2026-05-29-w3c-prov-source.md` score=69.50 bucket=raw_anchor kind=source_card status=raw
- rank 2: `raw/articles/2026-05-30-w3c-web-annotation-source.md` score=38.50 bucket=raw_anchor kind=source_card status=raw
- rank 3: `raw/repos/2026-05-27-knowledge-base-server-source.md` score=33.50 bucket=raw_anchor kind=source_card status=raw
- rank 4: `raw/papers/2026-05-29-prove-provenance-verification-source.md` score=29.50 bucket=raw_anchor kind=source_card status=raw
- rank 5: `raw/repos/2026-05-27-kagantic-vault-structure-source.md` score=29.50 bucket=raw_anchor kind=source_card status=raw
- rank 6: `raw/repos/2026-05-27-dusk-obsidian-vault-source.md` score=27.50 bucket=raw_anchor kind=source_card status=raw
- rank 7: `raw/repos/2026-06-11-awesome-obsidian-vault/alexiachen-my-notes-source.md` score=27.00 bucket=raw_anchor kind=source_card status=raw
- rank 8: `raw/repos/2026-06-12-breferrari-obsidian-mind-source.md` score=24.50 bucket=raw_anchor kind=source_card status=raw
- rank 9: `raw/videos/2026-06-08-xhs-ai-knowledge-base-source.md` score=24.50 bucket=raw_anchor kind=source_card status=raw
- rank 10: `raw/repos/2026-05-27-kepano-obsidian-source.md` score=24.00 bucket=raw_anchor kind=source_card status=raw
- rank 11: `raw/repos/2026-06-14-rohitg00-agentmemory-source.md` score=23.50 bucket=raw_anchor kind=source_card status=raw
- rank 12: `raw/papers/2026-06-11-guoxun-onefeed-source.md` score=23.00 bucket=raw_anchor kind=source_card status=raw

## Selected Pack Items

- `raw/articles/2026-05-29-w3c-prov-source.md` -> support / raw_is_provenance_only
- `raw/articles/2026-05-30-w3c-web-annotation-source.md` -> anchor / raw_is_provenance_only
- `raw/repos/2026-05-27-knowledge-base-server-source.md` -> orientation / raw_is_provenance_only
- `raw/papers/2026-05-29-prove-provenance-verification-source.md` -> orientation / raw_is_provenance_only
- `raw/repos/2026-05-27-kagantic-vault-structure-source.md` -> orientation / raw_is_provenance_only
- `raw/repos/2026-05-27-dusk-obsidian-vault-source.md` -> orientation / raw_is_provenance_only