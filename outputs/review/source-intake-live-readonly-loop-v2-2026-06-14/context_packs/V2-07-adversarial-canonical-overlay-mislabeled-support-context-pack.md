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
query_run_ref: query_runs/V2-07-adversarial-canonical-overlay-mislabeled-support-query-run.md
active_project: VAKS
query_mode: action
requested_authority_bucket: read_only_source_and_review_input
included_buckets:
- raw
- candidate
excluded_buckets:
- reviewed_write_path
- action_basis
- truth_mutation
items:
- ref: outputs/review/project_overlays/_runtime_test_fixtures/2026-06-14-flexnote-canonical-overlay-runtime-fixture.md
  record_kind: project_overlay
  knowledge_status: candidate
  pack_role: support
  warning_code: overlay_not_authority
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
  retrieval_score: 90.5
  matched_terms:
  - canonical
  - fixture
  - flexnote
  - overlay
  - project
  - runtime
  - support
  source_hash: 23425d17667de32b0e300a8489293d67c9cfec7371782189652e8bf5d1a4c98c
  excluded_reason: adversarial_canonical_overlay_mislabel_expected_to_be_blocked
support_checks:
- claim_ref: outputs/review/project_overlays/_runtime_test_fixtures/2026-06-14-flexnote-canonical-overlay-runtime-fixture.md
  independent_anchor_ref: raw/articles/2026-06-13-flexnote-docs-source/inspected-pages.md#Extracted Source Facts
  result: not_ready
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
  reason: non_raw_source_item_cannot_be_final_support
human_confirmation_required: false
artifact_kind: live_readonly_test_artifact
retrieval_exclusion: true
default_retrieval: false
indexing_policy: exclude_from_default_retrieval_graph_pack_support
truth_mutation_allowed: false
action_basis_allowed: false
---

# Context Pack: V2-07-adversarial-canonical-overlay-mislabeled-support

## Boundary

This pack is a read-only attention surface. It is not action basis and does not write truth.

## Support Selection

- not_ready: `outputs/review/project_overlays/_runtime_test_fixtures/2026-06-14-flexnote-canonical-overlay-runtime-fixture.md` anchor=`raw/articles/2026-06-13-flexnote-docs-source/inspected-pages.md#Extracted Source Facts`