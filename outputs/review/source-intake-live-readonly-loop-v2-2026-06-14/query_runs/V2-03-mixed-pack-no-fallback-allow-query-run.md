---
record_kind: query_run_trace
status: archived
query_id: V2-03-mixed-pack-no-fallback-allow
query_time: '2026-06-14T01:42:43+00:00'
question_summary: Mixed pack must include naturally retrieved raw anchor; no force_anchor_hit fallback allowed.
verbatim_input: FlexNote Extracted Source Facts visual workbench candidate overlay source anchor tag database context pack
  inspected pages
active_project: VAKS
query_mode: review
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
  excluded_reason: ''
- ref: outputs/review/2026-06-13-flexnote-docs-candidate-distillation.md
  record_kind: candidate_distillation
  knowledge_status: candidate
  pack_role: review_input
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
  excluded_reason: candidate_not_final_support
- ref: outputs/review/project_lens_overlays/2026-06-13-flexnote-vaks-visual-knowledge-workbench-overlay.md
  record_kind: project_overlay
  knowledge_status: candidate
  pack_role: review_input
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
  excluded_reason: overlay_not_final_support
- ref: outputs/review/2026-06-13-bilibili-book-note-workflow-candidate-distillation.md
  record_kind: candidate_distillation
  knowledge_status: candidate
  pack_role: orientation
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
  excluded_reason: rank_signal_is_diagnostic_not_support
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

# Query Run: V2-03-mixed-pack-no-fallback-allow

## Live Retrieval Boundary

This artifact was built from a local Markdown corpus scan. It is still read-only sandbox evidence, not Source Intake P0 approval.

## Top Retrieved Results

- rank 1: `outputs/review/2026-06-13-flexnote-docs-candidate-distillation.md` score=92.50 kind=candidate_distillation status=candidate
- rank 2: `raw/articles/2026-06-13-flexnote-docs-source/inspected-pages.md` score=91.00 kind=source_card status=raw
- rank 3: `outputs/review/project_lens_overlays/2026-06-13-flexnote-vaks-visual-knowledge-workbench-overlay.md` score=87.00 kind=project_overlay status=candidate
- rank 4: `outputs/review/2026-06-13-bilibili-book-note-workflow-candidate-distillation.md` score=74.00 kind=candidate_distillation status=candidate
- rank 5: `outputs/review/2026-06-11-AxDSan-mnemosyne-candidate-distillation.md` score=66.50 kind=candidate_distillation status=candidate
- rank 6: `outputs/review/2026-06-13-bilibili-edge-recall-contextual-active-recall-candidate-distillation.md` score=65.50 kind=candidate_distillation status=candidate
- rank 7: `outputs/review/2026-06-11-zhizhuodemao-ai-reverse-toolkit-candidate-distillation.md` score=64.00 kind=candidate_distillation status=candidate
- rank 8: `outputs/review/2026-06-13-bilibili-obsidian-homepage-plugin-workbench-candidate-distillation.md` score=61.00 kind=candidate_distillation status=candidate
- rank 9: `outputs/review/2026-06-14-agents365-ai-drawio-skill-candidate-distillation.md` score=58.00 kind=candidate_distillation status=candidate
- rank 10: `outputs/review/2026-06-14-kanna12580-kk-knowledge-agent-candidate-distillation.md` score=57.00 kind=candidate_distillation status=candidate
- rank 11: `raw/repos/2026-05-27-dusk-obsidian-vault-source.md` score=56.00 kind=source_card status=raw
- rank 12: `outputs/review/2026-06-11-cyrilxbt-n8n-obsidian-business-brain-candidate-distillation.md` score=54.50 kind=candidate_distillation status=candidate

## Selected Pack Items

- `raw/articles/2026-06-13-flexnote-docs-source/inspected-pages.md` -> support / raw_is_provenance_only
- `outputs/review/2026-06-13-flexnote-docs-candidate-distillation.md` -> review_input / candidate_not_action_basis
- `outputs/review/project_lens_overlays/2026-06-13-flexnote-vaks-visual-knowledge-workbench-overlay.md` -> review_input / overlay_not_authority
- `outputs/review/2026-06-13-bilibili-book-note-workflow-candidate-distillation.md` -> orientation / candidate_not_action_basis