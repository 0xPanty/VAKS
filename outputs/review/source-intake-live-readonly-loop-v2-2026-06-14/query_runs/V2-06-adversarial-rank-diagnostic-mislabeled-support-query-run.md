---
record_kind: query_run_trace
status: archived
query_id: V2-06-adversarial-rank-diagnostic-mislabeled-support
query_time: '2026-06-14T01:42:43+00:00'
question_summary: Errant assembler uses retrieval rank as support anchor; gate must block.
verbatim_input: FlexNote visual workbench source anchor candidate overlay tag database context pack
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
- ref: outputs/review/2026-06-13-flexnote-docs-candidate-distillation.md
  record_kind: candidate_distillation
  knowledge_status: candidate
  pack_role: support
  warning_code: candidate_not_action_basis
  action_basis_allowed: false
  truth_mutation_allowed: false
  independent_anchor_ref: retrieval_rank:1:score:89.5000
  selected_by:
    lexical: true
    semantic: false
    graph: false
    metadata: true
    rank: true
    dashboard: false
    legacy_raw_metadata: false
  retrieval_rank: 1
  retrieval_score: 89.5
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
  source_hash: 875108c0ae9d3a00c2e666d3cd4f04eb9475e1a6143fc19c3ec27c3d37928aaf
  excluded_reason: adversarial_rank_anchor_expected_to_be_blocked
support_checks:
- claim_ref: outputs/review/2026-06-13-flexnote-docs-candidate-distillation.md
  independent_anchor_ref: retrieval_rank:1:score:89.5000
  result: not_ready
  resolution:
    status: not_checked
    reason: anchor ref has no selector
    method: path_selector_heading_or_string_resolution
  reason: non_raw_source_item_cannot_be_final_support
human_confirmation_required: false
artifact_kind: live_readonly_test_artifact
retrieval_exclusion: true
default_retrieval: false
indexing_policy: exclude_from_default_retrieval_graph_pack_support
truth_mutation_allowed: false
action_basis_allowed: false
---

# Query Run: V2-06-adversarial-rank-diagnostic-mislabeled-support

## Live Retrieval Boundary

This artifact was built from a local Markdown corpus scan. It is still read-only sandbox evidence, not Source Intake P0 approval.

## Top Retrieved Results

- rank 1: `outputs/review/2026-06-13-flexnote-docs-candidate-distillation.md` score=89.50 kind=candidate_distillation status=candidate
- rank 2: `outputs/review/project_lens_overlays/2026-06-13-flexnote-vaks-visual-knowledge-workbench-overlay.md` score=87.00 kind=project_overlay status=candidate
- rank 3: `outputs/review/2026-06-13-bilibili-book-note-workflow-candidate-distillation.md` score=74.00 kind=candidate_distillation status=candidate
- rank 4: `outputs/review/2026-06-13-bilibili-edge-recall-contextual-active-recall-candidate-distillation.md` score=65.50 kind=candidate_distillation status=candidate
- rank 5: `outputs/review/2026-06-11-AxDSan-mnemosyne-candidate-distillation.md` score=64.50 kind=candidate_distillation status=candidate
- rank 6: `outputs/review/2026-06-11-zhizhuodemao-ai-reverse-toolkit-candidate-distillation.md` score=64.00 kind=candidate_distillation status=candidate
- rank 7: `outputs/review/2026-06-13-bilibili-obsidian-homepage-plugin-workbench-candidate-distillation.md` score=61.00 kind=candidate_distillation status=candidate
- rank 8: `outputs/review/2026-06-14-agents365-ai-drawio-skill-candidate-distillation.md` score=58.00 kind=candidate_distillation status=candidate
- rank 9: `outputs/review/2026-06-14-kanna12580-kk-knowledge-agent-candidate-distillation.md` score=57.00 kind=candidate_distillation status=candidate
- rank 10: `outputs/review/2026-06-11-cyrilxbt-n8n-obsidian-business-brain-candidate-distillation.md` score=54.50 kind=candidate_distillation status=candidate
- rank 11: `outputs/review/2026-06-12-breferrari-obsidian-mind-candidate-distillation.md` score=54.50 kind=candidate_distillation status=candidate
- rank 12: `outputs/review/2026-06-14-google-open-knowledge-format-candidate-distillation.md` score=54.50 kind=candidate_distillation status=candidate

## Selected Pack Items

- `outputs/review/2026-06-13-flexnote-docs-candidate-distillation.md` -> support / candidate_not_action_basis