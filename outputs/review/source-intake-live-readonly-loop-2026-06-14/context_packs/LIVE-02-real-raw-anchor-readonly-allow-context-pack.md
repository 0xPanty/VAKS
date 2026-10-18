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
query_run_ref: query_runs/LIVE-02-real-raw-anchor-readonly-allow-query-run.md
active_project: VAKS
query_mode: source_inspection
requested_authority_bucket: read_only_source_and_review_input
included_buckets:
- raw
- candidate
excluded_buckets:
- reviewed_write_path
- action_basis
- truth_mutation
items:
- ref: raw/articles/2026-06-13-flexnote-docs-source/inspected-pages.md
  record_kind: source_card
  knowledge_status: raw
  pack_role: support
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
  retrieval_score: 67.0
  matched_terms:
  - card
  - database
  - extracted
  - facts
  - first
  - flexnote
  - local
  - source
  - tag
  source_hash: 888f6eac02467a688a294446106759e17a33f79640a8f00633f86211df7dc67d
  excluded_reason: ''
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
  reason: resolved_raw_stable_anchor
human_confirmation_required: false
artifact_kind: live_readonly_test_artifact
retrieval_exclusion: true
default_retrieval: false
indexing_policy: exclude_from_default_retrieval_graph_pack_support
truth_mutation_allowed: false
action_basis_allowed: false
---

# Context Pack: LIVE-02-real-raw-anchor-readonly-allow

## Boundary

This pack is a read-only attention surface. It is not action basis and does not write truth.

## Support Selection

- supported: `raw/articles/2026-06-13-flexnote-docs-source/inspected-pages.md` anchor=`raw/articles/2026-06-13-flexnote-docs-source/inspected-pages.md#Extracted Source Facts`