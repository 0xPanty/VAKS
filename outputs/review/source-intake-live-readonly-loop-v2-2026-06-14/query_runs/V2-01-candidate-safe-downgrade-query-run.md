---
record_kind: query_run_trace
status: archived
query_id: V2-01-candidate-safe-downgrade
query_time: '2026-06-14T01:42:43+00:00'
question_summary: Live retrieved candidate is safely routed to review_input, not final support.
verbatim_input: mnemosyne vector memory candidate final support action basis
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
- ref: outputs/review/2026-06-11-AxDSan-mnemosyne-candidate-distillation.md
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
  retrieval_score: 85.0
  matched_terms:
  - action
  - basis
  - candidate
  - memory
  - mnemosyne
  - support
  - vector
  source_hash: 95939bb236c67d7dba28e880c3cc280d0bb79d01f47706f1914f3aef5183496e
  excluded_reason: live_candidate_hit_safely_routed_to_review_input
support_checks:
- claim_ref: no_final_support_selected
  independent_anchor_ref: ''
  result: not_ready
  resolution:
    status: not_checked
    reason: no support items
  reason: retrieved_items_remain_review_input_or_orientation_only
human_confirmation_required: false
artifact_kind: live_readonly_test_artifact
retrieval_exclusion: true
default_retrieval: false
indexing_policy: exclude_from_default_retrieval_graph_pack_support
truth_mutation_allowed: false
action_basis_allowed: false
---

# Query Run: V2-01-candidate-safe-downgrade

## Live Retrieval Boundary

This artifact was built from a local Markdown corpus scan. It is still read-only sandbox evidence, not Source Intake P0 approval.

## Top Retrieved Results

- rank 1: `outputs/review/2026-06-11-AxDSan-mnemosyne-candidate-distillation.md` score=85.00 kind=candidate_distillation status=candidate
- rank 2: `outputs/review/2026-06-14-kanna12580-kk-knowledge-agent-candidate-distillation.md` score=68.00 kind=candidate_distillation status=candidate
- rank 3: `outputs/review/2026-06-12-breferrari-obsidian-mind-candidate-distillation.md` score=56.50 kind=candidate_distillation status=candidate
- rank 4: `outputs/review/2026-06-14-agents365-ai-drawio-skill-candidate-distillation.md` score=54.00 kind=candidate_distillation status=candidate
- rank 5: `outputs/review/2026-06-11-RyanCodrai-turbovec-candidate-distillation.md` score=51.00 kind=candidate_distillation status=candidate
- rank 6: `outputs/review/2026-06-14-edochi-mdvs-candidate-distillation.md` score=48.50 kind=candidate_distillation status=candidate
- rank 7: `outputs/review/2026-06-14-google-open-knowledge-format-candidate-distillation.md` score=48.00 kind=candidate_distillation status=candidate
- rank 8: `outputs/review/2026-06-14-rohitg00-agentmemory-candidate-distillation.md` score=47.00 kind=candidate_distillation status=candidate
- rank 9: `outputs/review/2026-06-12-bilibili-apex-knowledge-schema-rag-candidate-distillation.md` score=46.50 kind=candidate_distillation status=candidate
- rank 10: `raw/repos/2026-06-11-AxDSan-mnemosyne-source.md` score=46.00 kind=source_card status=raw
- rank 11: `outputs/review/2026-06-11-zhizhuodemao-ai-reverse-toolkit-candidate-distillation.md` score=42.50 kind=candidate_distillation status=candidate
- rank 12: `outputs/review/2026-06-07-aal-ruller-pkm-second-brain-ai-companian-candidate-distillation.md` score=42.00 kind=candidate_distillation status=candidate

## Selected Pack Items

- `outputs/review/2026-06-11-AxDSan-mnemosyne-candidate-distillation.md` -> review_input / candidate_not_action_basis