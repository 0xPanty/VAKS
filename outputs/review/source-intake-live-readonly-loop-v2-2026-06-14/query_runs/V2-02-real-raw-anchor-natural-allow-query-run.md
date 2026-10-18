---
record_kind: query_run_trace
status: archived
query_id: V2-02-real-raw-anchor-natural-allow
query_time: '2026-06-14T01:42:43+00:00'
question_summary: Real raw anchor must be naturally retrieved and allowed read-only.
verbatim_input: FlexNote Extracted Source Facts local-first card tag database inspected pages
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
retrieval_filters:
  include_candidates: true
  include_overlays: active_project_only
  include_runtime_test_artifacts: false
  writeback_allowed: false
  promotion_allowed: false
  truth_mutation_allowed: false
selected_items:
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

# Query Run: V2-02-real-raw-anchor-natural-allow

## Live Retrieval Boundary

This artifact was built from a local Markdown corpus scan. It is still read-only sandbox evidence, not Source Intake P0 approval.

## Top Retrieved Results

- rank 1: `raw/articles/2026-06-13-flexnote-docs-source/inspected-pages.md` score=104.00 kind=source_card status=raw
- rank 2: `outputs/review/2026-06-13-flexnote-docs-candidate-distillation.md` score=56.00 kind=candidate_distillation status=candidate
- rank 3: `raw/repos/2026-05-27-knowledge-base-server-source.md` score=41.50 kind=source_card status=raw
- rank 4: `raw/articles/2026-06-13-flexnote-docs-source.md` score=39.00 kind=source_card status=raw
- rank 5: `raw/repos/2026-05-27-kagantic-vault-structure-source.md` score=37.50 kind=source_card status=raw
- rank 6: `raw/repos/2026-05-27-dusk-obsidian-vault-source.md` score=35.50 kind=source_card status=raw
- rank 7: `outputs/review/2026-06-11-AxDSan-mnemosyne-candidate-distillation.md` score=34.50 kind=candidate_distillation status=candidate
- rank 8: `outputs/review/project_lens_overlays/2026-06-13-flexnote-vaks-visual-knowledge-workbench-overlay.md` score=32.50 kind=project_overlay status=candidate
- rank 9: `raw/repos/2026-06-11-awesome-obsidian-vault/alexiachen-my-notes-source.md` score=31.50 kind=source_card status=raw
- rank 10: `raw/repos/2026-06-11-safishamsi-graphify-source.md` score=31.50 kind=source_card status=raw
- rank 11: `raw/repos/2026-05-26-llm-wiki-source.md` score=31.00 kind=source_card status=raw
- rank 12: `raw/repos/2026-05-27-kepano-obsidian-source.md` score=31.00 kind=source_card status=raw

## Selected Pack Items

- `raw/articles/2026-06-13-flexnote-docs-source/inspected-pages.md` -> support / raw_is_provenance_only