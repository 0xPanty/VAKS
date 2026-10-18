---
record_kind: query_run_trace
status: archived
query_id: V2-07-adversarial-canonical-overlay-mislabeled-support
query_time: '2026-06-14T01:42:43+00:00'
question_summary: Errant assembler marks a canonical project_overlays hit as support; gate must block.
verbatim_input: canonical overlay runtime fixture FlexNote visual workbench project overlay support
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
retrieval_filters:
  include_candidates: true
  include_overlays: active_project_only
  include_runtime_test_artifacts: false
  writeback_allowed: false
  promotion_allowed: false
  truth_mutation_allowed: false
selected_items:
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

# Query Run: V2-07-adversarial-canonical-overlay-mislabeled-support

## Live Retrieval Boundary

This artifact was built from a local Markdown corpus scan. It is still read-only sandbox evidence, not Source Intake P0 approval.

## Top Retrieved Results

- rank 1: `outputs/review/project_overlays/_runtime_test_fixtures/2026-06-14-flexnote-canonical-overlay-runtime-fixture.md` score=90.50 kind=project_overlay status=candidate
- rank 2: `outputs/review/project_lens_overlays/2026-06-13-flexnote-vaks-visual-knowledge-workbench-overlay.md` score=88.50 kind=project_overlay status=candidate
- rank 3: `outputs/review/project_lens_overlays/2026-06-14-rohitg00-agentmemory-misa-vaks-bridge-overlay.md` score=46.00 kind=project_overlay status=candidate
- rank 4: `outputs/review/project_lens_overlays/2026-06-14-agents365-ai-drawio-skill-vaks-visualization-overlay.md` score=41.00 kind=project_overlay status=candidate
- rank 5: `outputs/review/2026-06-13-flexnote-docs-candidate-distillation.md` score=40.50 kind=candidate_distillation status=candidate
- rank 6: `outputs/review/project_lens_overlays/2026-06-14-kanna12580-kk-knowledge-agent-misa-kb-memory-overlay.md` score=40.00 kind=project_overlay status=candidate
- rank 7: `outputs/review/project_lens_overlays/2026-06-14-benmaster82-Kwipu-vaks-local-graph-rag-overlay.md` score=39.50 kind=project_overlay status=candidate
- rank 8: `outputs/review/project_lens_overlays/2026-06-14-adithya-s-k-omniparse-vaks-raw-intake-overlay.md` score=36.50 kind=project_overlay status=candidate
- rank 9: `outputs/review/project_lens_overlays/2026-06-14-edochi-mdvs-vaks-validation-search-overlay.md` score=33.50 kind=project_overlay status=candidate
- rank 10: `outputs/review/2026-06-12-breferrari-obsidian-mind-candidate-distillation.md` score=29.50 kind=candidate_distillation status=candidate
- rank 11: `raw/articles/2026-06-13-flexnote-docs-source.md` score=29.50 kind=source_card status=raw
- rank 12: `outputs/review/2026-06-13-bilibili-obsidian-homepage-plugin-workbench-candidate-distillation.md` score=28.00 kind=candidate_distillation status=candidate

## Selected Pack Items

- `outputs/review/project_overlays/_runtime_test_fixtures/2026-06-14-flexnote-canonical-overlay-runtime-fixture.md` -> support / overlay_not_authority