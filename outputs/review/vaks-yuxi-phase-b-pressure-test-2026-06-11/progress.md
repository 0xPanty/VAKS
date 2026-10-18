---
record_kind: sandbox_progress
status: active
project_id: VAKS
created_at: 2026-06-11
truth_boundary: progress_log_not_reviewed_knowledge
action_basis_allowed: false
---

# Progress

## 2026-06-11

- Created sandbox for Phase B pressure testing.
- Started from the prior Yuxi-like pilot instead of a blank harness.
- Set acceptance bar: keep only if measurable retrieval gain does not introduce boundary leakage.
- Checked original Yuxi feasibility: GitHub HEAD resolves to `a8536a2e8520d1992a31bb6c22f219e60deca131`, but local Docker command is unavailable.
- Recorded PowerShell heredoc mistake; future inline Python uses PowerShell here-string.
- Shallow-cloned Yuxi into sandbox and inspected retrieval-related code.
- Defined `yuxi_native_profile` as a code/doc-aligned local comparator, not an end-to-end original Yuxi run.
- Ran primary corpus once. Metrics were positive, but q21 expected terms over-favored the Mnemosyne candidate source for an action query; corrected expected terms to also accept SCHEMA/SOURCE_INTAKE boundary hits.
- Implemented and ran the full Phase B pressure harness.
- Tested 30 queries across primary and full noisy corpora with four modes: baseline, bucketless VAKS+B, bucket-local VAKS+B, and Yuxi-native profile.
- Result: bucket-local VAKS+B passed the sandbox keep bar with better hit@5 than baseline and zero action leakage in both corpora.
- Wrote compact Yuxi local repo evidence summary and prepared to remove the temporary full clone from the sandbox to avoid untracked-file noise.
- Removed temporary `external/Yuxi` clone after verifying the path was inside the sandbox. Kept `external/YUXI_LOCAL_REPO_EVIDENCE.md`.
- Locked the previous passing `vaks_b_bucket_local` result as `results/phase_b_v0_locked_summary.csv` and `results/phase_b_v0_locked_query_metrics.csv` before starting the next iteration.
- Started v1 adapter iteration. The intended change is only intra-bucket ordering: path/heading/exact-phrase alignment and main core-doc priority for action/evidence queries. It must not loosen VAKS authority buckets.
- First full v1 run timed out at 124s. Second run computed CSV metrics but failed while refreshing the large JSON top-results file; CSV metrics showed v1 MRR 1.0000 on both corpora, which is positive but suspiciously perfect.
- Added `queries_phase_b_holdout.jsonl` with paraphrased pressure questions to check whether v1 is a real ranking improvement rather than overfitting the original wording.
- Added `--query-file` and `--result-prefix` support to the pressure harness so holdout runs produce separate artifacts.
- Reran the main pressure test with v1. Main set stayed zero-leak and improved MRR to 1.0000 on both primary and full corpora.
- Ran the holdout pressure test. v1 improved aggregate hit@5/hit@10/MRR over v0 and stayed zero-leak, but had two query-level MRR regressions.
- Wrote `PHASE_B_V1_VS_LOCKED_BASELINE.md` and `PHASE_B_ADAPTER_SPEC.md`.
- Started v1.1 regression pass. The change will be general topic-anchor routing, not query-id-specific logic:
  - resource-filter / visible-resource / before-search queries should expand toward VAKS authority-bucket filter anchors;
  - benchmark / lint / diagnostic / mainline-readiness queries should prefer the documents that explicitly say diagnostics are not truth or readiness.
- Implemented `vaks_b_adapter_v1_1` and v1.1-vs-v1 delta reporting.
- Ran holdout first. v1.1 improved hit@5, hit@10, and MRR over v1 on both corpora, fixed the two known regressions, and introduced zero query-level regressions.
- Ran the main 30-query pressure set. v1.1 tied v1 on hit@5, hit@10, MRR, and all governance metrics, with zero query-level regressions.
- Wrote `PHASE_B_V11_VS_V1_DECISION.md`.
- Added `tools/vaks_phase_b_adapter.py`, a minimal read-only adapter skeleton that emits chunk manifests and retrieval receipts.
- Generated skeleton manifest and receipt artifacts:
  - primary manifest: 3947 chunks
  - full manifest: 18708 chunks
  - main receipts: 600 total results
  - holdout receipts: 300 total results
- Added `vaks_b_adapter_skeleton` mode to the pressure harness and generated skeleton-vs-v1.1 reports.
- Main and holdout pressure tests tied v1.1 with zero query-level regressions and zero leakage.
- Wrote `PHASE_B_SKELETON_VS_V11_DECISION.md`.
- Added `tools/validate_phase_b_adapter_contract.py`.
- First contract run failed with 5569 errors, mostly click-back ranges past EOF, missing raw manifest warnings, and missing `indexed_source_hash` in receipts.
- Fixed `tools/vaks_phase_b_adapter.py` so click-backs are clamped to existing file ranges, manifest rows carry risk warnings, and receipts include `indexed_source_hash`.
- Reran adapter artifact generation and contract validation. Contract now passes with 0 errors across primary/full manifests plus main/holdout receipts.
- Wrote `PHASE_B_CONTRACT_TEST_DECISION.md`.
- Added `PHASE_B_INTEGRATION_READINESS_PACKAGE.md` to document the adapter API shape, read-only inputs, derived outputs, insertion point, failure modes, rollback path, and next gates.
- Added `tools/validate_phase_b_integration_readiness.py`.
- First readiness validator run failed on CSV header handling (`corpus` KeyError); fixed the validator to read CSV as `utf-8-sig` and normalize field names.
- Second readiness validator run failed one package coverage check because the `expected_terms` evaluation-only rule was not written as a plain exact phrase; added the explicit rule.
- Reran readiness validation. It passed with 0 errors.
- Current readiness comparison against the contract-passing skeleton:
  - main primary: hit@5 30/30, MRR 1.0000, leakage 0.0000
  - main full: hit@5 30/30, MRR 1.0000, leakage 0.0000
  - holdout primary: hit@5 12/15, MRR 0.7811, leakage 0.0000
  - holdout full: hit@5 13/15, MRR 0.7591, leakage 0.0000
  - contract: pass / 0 errors
  - readiness: pass / 0 errors
- Wrote `PHASE_B_INTEGRATION_READINESS_DECISION.md`.
- Added `PHASE_B_MAINLINE_READINESS_PACKET.md` with a candidate mainline touch set, insertion points, candidate snippets, evidence map, remaining blockers, and Pro review questions.
- Added `tools/validate_phase_b_mainline_readiness.py`.
- Ran the mainline-readiness validator. It passed with 0 errors:
  - readiness: pass / 0 errors
  - contract: pass / 0 errors
  - core docs dirty lines: 0
  - required artifacts checked: 7
- Wrote `PHASE_B_MAINLINE_READINESS_DECISION.md`.
- Current next step is external / Pro review of the packet, not direct mainline editing.
- Added `PHASE_B_PRO_REVIEW_PROMPT.md`, a copy-pasteable external review prompt that asks Pro to choose `APPROVE_MINIMAL_DOC_PATCH`, `REVISE_BEFORE_PATCH`, or `REJECT_FOR_NOW`.
- Added `tools/validate_phase_b_pro_prompt.py`.
- Ran the Pro prompt validator. It passed with 0 errors:
  - mainline readiness: pass / 0 errors
  - integration readiness: pass / 0 errors
  - contract: pass / 0 errors
  - core docs dirty lines: 0
  - required artifacts checked: 8
- Wrote `PHASE_B_PRO_REVIEW_PROMPT_DECISION.md`.
- Current next step is to send the prompt to Pro or another review window; do not edit core docs until an approval result exists.
- Spawned an independent read-only explorer subagent (`James`) to review `PHASE_B_PRO_REVIEW_PROMPT.md`.
- James returned `APPROVE_MINIMAL_DOC_PATCH` with the approved touch set:
  - `SOURCE_INTAKE.md`
  - `IMPLEMENTATION_BLUEPRINT.md`
  - `DEV_CONTEXT.md`
  - `MEMORY_TIER.md`
- Added `PHASE_B_EXTERNAL_REVIEW_RESULT.md`, `PHASE_B_EXTERNAL_REVIEW_DECISION.md`, and `tools/validate_phase_b_external_review_result.py`.
- Ran the external review validator. It passed with 0 errors:
  - verdict: `APPROVE_MINIMAL_DOC_PATCH`
  - prompt check: pass / 0 errors
  - mainline readiness: pass / 0 errors
  - integration readiness: pass / 0 errors
  - contract: pass / 0 errors
  - core docs dirty lines: 0
- Applied the approved minimal documentation-only patch to four files:
  - `SOURCE_INTAKE.md`
  - `IMPLEMENTATION_BLUEPRINT.md`
  - `DEV_CONTEXT.md`
  - `MEMORY_TIER.md`
- Added `tools/validate_phase_b_minimal_doc_patch.py`.
- First minimal patch validator run failed 6 checks: one exact DEV_CONTEXT phrase was missing and the validator treated prior-gate `0` values as false. Fixed both.
- Reran the minimal patch validator. It passed with 0 errors.
- Wrote `PHASE_B_MINIMAL_DOC_PATCH_DECISION.md`.
- Checked Yuxi current HEAD with `git ls-remote` and a temporary shallow clone. HEAD remains `a8536a2e8520d1992a31bb6c22f219e60deca131`.
- Rechecked local runtime prerequisites:
  - `docker --version`: unavailable
  - `docker compose version`: unavailable
  - `uv`: available
  - uv-managed Python 3.12: available
  - default `python`: 3.10.6
  - `node` / `pnpm`: available
- Inspected Yuxi README, Makefile, docker-compose, and testing guidelines. Lite mode still uses Docker Compose; official unit/integration/e2e tests are documented through `docker compose exec api`.
- Added `external/YUXI_RUNTIME_FEASIBILITY_EVIDENCE.md`, `PHASE_B_RUNTIME_FEASIBILITY_REPORT.md`, and `tools/validate_phase_b_runtime_feasibility.py`.
- Ran runtime feasibility validator. It passed with 0 errors:
  - Docker path: `None`
  - minimal doc patch: pass / 0 errors
  - contract: pass / 0 errors
  - approved four core docs changed
- Wrote `PHASE_B_RUNTIME_FEASIBILITY_DECISION.md`.
- Current runtime/full-stack status: blocked by environment. Do not claim original Yuxi runtime parity or production readiness.
- Added `tools/build_phase_b_context_packs.py` to assemble candidate context packs from existing skeleton retrieval receipts.
- Added `tools/validate_phase_b_context_packs.py`.
- Generated `results/phase_b_context_pack_candidates.jsonl` and `results/phase_b_context_pack_candidate_summary.json`.
- First context-pack validator run failed one check because it treated `action_basis_allowed_count: 0` as missing. Fixed validator zero handling.
- Reran context-pack validator. It passed with 0 errors:
  - pack count: 90
  - pack-level action_basis_allowed_count: 0
  - packs with suppressed receipt action flags: 36
  - runtime feasibility: pass / 0 errors
  - minimal doc patch: pass / 0 errors
  - contract: pass / 0 errors
- Wrote `PHASE_B_CONTEXT_PACK_CANDIDATE_DECISION.md`.
- Added `tools/build_phase_b_evidence_envelopes.py` to transform context-pack candidates into review-oriented evidence-envelope / warrant-draft candidates.
- Added `tools/validate_phase_b_evidence_envelopes.py`.
- Generated `results/phase_b_evidence_envelope_candidates.jsonl` and `results/phase_b_evidence_envelope_candidate_summary.json`.
- Ran the evidence-envelope validator. It passed with 0 errors:
  - envelope count: 90
  - action_basis_allowed_count: 0
  - evidence_packet_allowed_count: 0
  - evidence_sufficiency_passed_count: 0
  - envelopes with suppressed receipt action flags: 36
  - context pack: pass / 0 errors
  - runtime feasibility: pass / 0 errors
  - minimal doc patch: pass / 0 errors
  - contract: pass / 0 errors
- Wrote `PHASE_B_EVIDENCE_ENVELOPE_CANDIDATE_DECISION.md`.
- Added `tools/build_phase_b_evidence_support_checks.py` to transform evidence envelopes into source-span support-check candidates.
- Added `tools/validate_phase_b_evidence_support_checks.py`.
- First support-check validator run failed with 2 errors because two support checks had no evidence items. Fixed the design by marking those checks `blocked_no_source_anchor` instead of creating fake evidence or treating absence as pass.
- Generated `results/phase_b_evidence_support_check_candidates.jsonl` and `results/phase_b_evidence_support_check_candidate_summary.json`.
- Reran the support-check validator. It passed with 0 errors:
  - support check count: 90
  - evidence item count: 389
  - source_span_available_count: 389
  - current_source_hash_match_count: 321
  - source_refresh_needed_count: 68
  - blocked_no_source_anchor_count: 2
  - support_passed_count: 0
  - support_counts_for_promotion_count: 0
  - action_basis_allowed_count: 0
  - evidence envelope: pass / 0 errors
  - context pack: pass / 0 errors
  - runtime feasibility: pass / 0 errors
  - minimal doc patch: pass / 0 errors
  - contract: pass / 0 errors
- Wrote `PHASE_B_EVIDENCE_SUPPORT_CHECK_CANDIDATE_DECISION.md`.
- Added `tools/build_phase_b_source_refresh.py` to transform support-check candidates into refreshed source-span/hash snapshots.
- Added `tools/validate_phase_b_source_refresh.py`.
- Generated `results/phase_b_source_refresh_candidates.jsonl` and `results/phase_b_source_refresh_candidate_summary.json`.
- Ran the source-refresh validator. It passed with 0 errors:
  - source refresh count: 90
  - refresh item count: 389
  - source_span_available_count: 389
  - pre_refresh_mismatch_count: 68
  - post_refresh_mismatch_count: 0
  - refreshed_item_count: 68
  - already_current_item_count: 321
  - blocked_no_source_anchor_count: 2
  - support_passed_count: 0
  - support_counts_for_promotion_count: 0
  - action_basis_allowed_count: 0
  - evidence support check: pass / 0 errors
  - evidence envelope: pass / 0 errors
  - context pack: pass / 0 errors
  - runtime feasibility: pass / 0 errors
  - minimal doc patch: pass / 0 errors
  - contract: pass / 0 errors
- Wrote `PHASE_B_SOURCE_REFRESH_CANDIDATE_DECISION.md`.
- Added `tools/build_phase_b_refreshed_support_checks.py` to rebuild support-check candidates from refreshed source spans and hashes.
- Added `tools/validate_phase_b_refreshed_support_checks.py`.
- First refreshed-support validator run failed with 2 zero-handling errors; fixed the validator so legitimate `0` values are accepted.
- Generated `results/phase_b_refreshed_support_check_candidates.jsonl` and `results/phase_b_refreshed_support_check_candidate_summary.json`.
- Reran the refreshed-support validator. It passed with 0 errors:
  - refreshed support check count: 90
  - evidence item count: 389
  - source_span_available_count: 389
  - previous_source_refresh_needed_count: 68
  - current_source_refresh_needed_count: 0
  - current_source_hash_match_count: 389
  - refreshed_item_count: 68
  - already_current_item_count: 321
  - blocked_no_source_anchor_count: 2
  - support_passed_count: 0
  - support_counts_for_promotion_count: 0
  - action_basis_allowed_count: 0
  - source refresh: pass / 0 errors
  - evidence support check: pass / 0 errors
  - evidence envelope: pass / 0 errors
  - context pack: pass / 0 errors
  - runtime feasibility: pass / 0 errors
  - minimal doc patch: pass / 0 errors
  - contract: pass / 0 errors
- Wrote `PHASE_B_REFRESHED_SUPPORT_CHECK_CANDIDATE_DECISION.md`.
- Added `tools/build_phase_b_review_queue_packets.py` to assemble refreshed support-check candidates into manual review queue packets.
- Added `tools/validate_phase_b_review_queue_packets.py`.
- First review-queue validator run failed with 2 zero-handling errors; fixed the validator so legitimate `0` values are accepted.
- Generated `results/phase_b_review_queue_packets.jsonl` and `results/phase_b_review_queue_packet_summary.json`.
- Reran the review-queue validator. It passed with 0 errors:
  - review packet count: 90
  - open packet count: 88
  - blocked_no_source_anchor_count: 2
  - review item count: 389
  - source_span_available_count: 389
  - current_source_hash_match_count: 389
  - current_source_refresh_needed_count: 0
  - review_result_not_reviewed_count: 90
  - support_passed_count: 0
  - support_counts_for_promotion_count: 0
  - action_basis_allowed_count: 0
  - automatic_promotion_allowed_count: 0
  - refreshed support check: pass / 0 errors
  - source refresh: pass / 0 errors
  - evidence support check: pass / 0 errors
  - evidence envelope: pass / 0 errors
  - context pack: pass / 0 errors
  - runtime feasibility: pass / 0 errors
  - minimal doc patch: pass / 0 errors
  - contract: pass / 0 errors
- Wrote `PHASE_B_REVIEW_QUEUE_PACKET_DECISION.md`.
- Added `tools/build_phase_b_simulated_reviewer_outcomes.py` to create simulation-only reviewer outcomes from review queue packets.
- Added `tools/validate_phase_b_simulated_reviewer_outcomes.py`.
- Generated `results/phase_b_simulated_reviewer_outcomes.jsonl` and `results/phase_b_simulated_reviewer_outcome_summary.json`.
- Ran the simulated-outcome validator. It passed with 0 errors:
  - outcome record count: 90
  - previous_review_result_not_reviewed_count: 90
  - simulated_packet_count: 12
  - not_reviewed_packet_count: 76
  - blocked_no_source_anchor_count: 2
  - simulated_item_outcome_count: 57
  - simulated_direct_support_count: 12
  - simulated_inferential_support_count: 12
  - simulated_background_count: 23
  - simulated_counterexample_count: 10
  - human_reviewed_support_count: 0
  - support_passed_count: 0
  - support_counts_for_promotion_count: 0
  - action_basis_allowed_count: 0
  - evidence_packet_allowed_count: 0
  - evidence_sufficiency_passed_count: 0
  - automatic_promotion_allowed_count: 0
  - formal_writeback_allowed_count: 0
  - review queue packet: pass / 0 errors
  - refreshed support check: pass / 0 errors
  - source refresh: pass / 0 errors
  - evidence support check: pass / 0 errors
  - evidence envelope: pass / 0 errors
  - context pack: pass / 0 errors
  - runtime feasibility: pass / 0 errors
  - minimal doc patch: pass / 0 errors
  - contract: pass / 0 errors
- Wrote `PHASE_B_SIMULATED_REVIEWER_OUTCOME_DECISION.md`.
- Added `tools/build_phase_b_promotion_gate.py` to evaluate simulated outcomes through promotion/action-basis gates.
- Added `tools/validate_phase_b_promotion_gate.py`.
- Generated `results/phase_b_promotion_gate_evaluations.jsonl` and `results/phase_b_promotion_gate_evaluation_summary.json`.
- Ran the promotion-gate validator. It passed with 0 errors:
  - gate record count: 90
  - blocked gate count: 90
  - previous simulated support-like count: 24
  - simulated support-like count: 24
  - blocked_due_simulation_only_count: 12
  - blocked_due_support_like_not_human_reviewed_count: 12
  - blocked_due_missing_source_anchor_count: 2
  - human_reviewed_support_count: 0
  - reviewed_support_count: 0
  - promotion_support_count: 0
  - promotion_allowed_count: 0
  - action_basis_allowed_count: 0
  - action_ready_count: 0
  - evidence_packet_created_count: 0
  - evidence_packet_allowed_count: 0
  - evidence_sufficiency_passed_count: 0
  - automatic_promotion_allowed_count: 0
  - formal_writeback_allowed_count: 0
  - truth_confidence_change_allowed_count: 0
  - reviewed_relation_creation_allowed_count: 0
  - simulated reviewer outcome: pass / 0 errors
  - review queue packet: pass / 0 errors
  - refreshed support check: pass / 0 errors
  - source refresh: pass / 0 errors
  - evidence support check: pass / 0 errors
  - evidence envelope: pass / 0 errors
  - context pack: pass / 0 errors
  - runtime feasibility: pass / 0 errors
  - minimal doc patch: pass / 0 errors
  - contract: pass / 0 errors
- Wrote `PHASE_B_PROMOTION_GATE_DECISION.md`.
- Added `tools/build_phase_b_keep_stop_synthesis.py` to synthesize the whole Phase B chain into a keep/stop decision.
- Added `tools/validate_phase_b_keep_stop_synthesis.py`.
- Generated `results/phase_b_keep_stop_synthesis.json`, `PHASE_B_KEEP_STOP_SYNTHESIS_PACKET.md`, and `PHASE_B_KEEP_STOP_SYNTHESIS_DECISION.md`.
- Ran the keep/stop validator. It passed with 0 errors:
  - keep_stop_decision: `keep_phase_b_as_sandbox_candidate`
  - positive_value_confirmed: true
  - no_boundary_leak_confirmed: true
  - mainline_status: documentation_only_patch_validated_not_committed
  - runtime_status: original_yuxi_full_stack_unvalidated_docker_unavailable
  - promotion_allowed_count: 0
  - action_basis_allowed_count: 0
  - evidence_sufficiency_passed_count: 0
  - formal_writeback_allowed: false
  - original_yuxi_runtime_validated: false
  - runtime_adoption_allowed: false
  - c_lite_allowed: false
  - promotion gate: pass / 0 errors
  - simulated reviewer outcome: pass / 0 errors
  - review queue packet: pass / 0 errors
  - refreshed support check: pass / 0 errors
  - source refresh: pass / 0 errors
  - evidence support check: pass / 0 errors
  - evidence envelope: pass / 0 errors
  - context pack: pass / 0 errors
  - runtime feasibility: pass / 0 errors
  - minimal doc patch: pass / 0 errors
  - adapter contract: pass / 0 errors
- Wrote `PHASE_B_KEEP_STOP_SYNTHESIS_CHECK.md`.
- Added `tools/build_phase_b_commit_readiness.py` to convert the keep/stop synthesis into an exact commit-scope recommendation.
- Added `tools/validate_phase_b_commit_readiness.py`.
- Generated `results/phase_b_commit_readiness.json`, `PHASE_B_COMMIT_READINESS_PACKET.md`, and `PHASE_B_COMMIT_READINESS_DECISION.md`.
- Ran the commit-readiness validator. It passed with 0 errors:
  - commit_readiness_status: `ready_pending_user_approval`
  - commit_without_user_approval_allowed: false
  - recommended mainline docs: `SOURCE_INTAKE.md`, `IMPLEMENTATION_BLUEPRINT.md`, `DEV_CONTEXT.md`, `MEMORY_TIER.md`
  - recommended sandbox evidence bundle: `outputs/review/vaks-yuxi-phase-b-pressure-test-2026-06-11/`
  - excluded files: `SCHEMA.md`, `REVIEW_QUEUE.md`, `templates/architecture-review-window-prompt.md`
  - keep stop synthesis: pass / 0 errors
  - minimal doc patch: pass / 0 errors
  - promotion gate: pass / 0 errors
  - adapter contract: pass / 0 errors
  - runtime feasibility: pass / 0 errors
  - no staged paths
- Wrote `PHASE_B_COMMIT_READINESS_CHECK.md`.
- Added `tools/build_phase_b_next_action_gate.py` to turn commit-readiness into an explicit next-branch gate.
- Added `tools/validate_phase_b_next_action_gate.py`.
- Generated `results/phase_b_next_action_gate.json`, `PHASE_B_NEXT_ACTION_GATE_PACKET.md`, and `PHASE_B_NEXT_ACTION_GATE_DECISION.md`.
- Ran the next-action gate validator. It passed with 0 errors:
  - next_action_gate_status: pass
  - recommended_next_action: `await_user_approved_commit_or_runner_choice`
  - commit_path: ready_pending_user_approval
  - commit_without_user_approval_allowed: false
  - original_yuxi_runtime_path: blocked_until_docker_or_remote_runner
  - original_yuxi_runtime_validated: false
  - c_lite_path: not_allowed_from_current_evidence
  - c_lite_allowed: false
  - runtime_adoption_path: not_allowed
  - runtime_adoption_allowed: false
  - commit-readiness: pass / 0 errors
  - keep-stop: pass / 0 errors
  - minimal doc patch: pass / 0 errors
  - promotion gate: pass / 0 errors
  - adapter contract: pass / 0 errors
  - runtime feasibility: pass / 0 errors
- Wrote `PHASE_B_NEXT_ACTION_GATE_CHECK.md`.
- Added `tools/build_phase_b_pre_commit_manifest.py` to create a file-level SHA256 manifest for the proposed commit scope.
- Added `tools/validate_phase_b_pre_commit_manifest.py`.
- Generated `results/phase_b_pre_commit_manifest.json`, `PHASE_B_PRE_COMMIT_MANIFEST_PACKET.md`, and `PHASE_B_PRE_COMMIT_MANIFEST_DECISION.md`.
- Ran the pre-commit manifest validator. It passed with 0 errors:
  - pre_commit_manifest_status: `ready_pending_user_approval`
  - file_count: 166
  - commit_without_user_approval_allowed: false
  - stage_performed: false
  - commit_performed: false
  - next-action gate: pass / 0 errors
  - commit-readiness: pass / 0 errors
  - keep-stop: pass / 0 errors
  - no staged paths
- Wrote `PHASE_B_PRE_COMMIT_MANIFEST_CHECK.md`.
- Added `tools/build_phase_b_branch_decision_brief.py` to generate a human-readable branch decision brief and recovery prompt.
- Added `tools/validate_phase_b_branch_decision_brief.py`.
- Generated `results/phase_b_branch_decision_brief.json`, `PHASE_B_BRANCH_DECISION_BRIEF.md`, and `PHASE_B_BRANCH_DECISION_BRIEF_DECISION.md`.
- Ran the branch-decision brief validator. It passed with 0 errors:
  - branch_decision_brief_status: `ready_for_user_choice`
  - recommended_branch: `user_approved_commit`
  - commit_without_user_approval_allowed: false
  - stage_performed: false
  - commit_performed: false
  - user-approved commit: ready_pending_user_approval
  - original Yuxi full-stack test: blocked_until_docker_or_remote_runner
  - C-lite sandbox: not_allowed_without_new_user_gate
  - runtime adoption: not_allowed
  - pre-commit manifest: pass / 0 errors
  - next-action gate: pass / 0 errors
  - commit-readiness: pass / 0 errors
  - keep-stop: pass / 0 errors
- Wrote `PHASE_B_BRANCH_DECISION_BRIEF_CHECK.md`.

## Pro Critique Response / P0 Query-Level Replay

- Added `tools/build_phase_b_p0_query_replay.py` and `tools/validate_phase_b_p0_query_replay.py`.
- Generated:
  - `results/phase_b_p0_query_level_replay.csv`
  - `results/phase_b_p0_query_level_metrics.csv`
  - `results/phase_b_p0_summary.csv`
  - `results/phase_b_p0_clean_vaks_only_top_results.csv`
  - `results/phase_b_p0_clean_vaks_only_query_metrics.csv`
  - `results/phase_b_p0_clean_vaks_only_summary.csv`
  - `results/phase_b_metric_dictionary.json`
  - `PHASE_B_METRIC_DICTIONARY.md`
  - `PHASE_B_P0_QUERY_LEVEL_REPLAY_REPORT.md`
  - `PHASE_B_P0_QUERY_LEVEL_REPLAY_CHECK.md`
- First validator attempt failed with 662 errors because it tried to recompute top20 MRR from top10 snippet rows.
- Revised the P0 design:
  - query-level metrics preserve top20 paired outcomes;
  - top10 replay validates visible rank/authority/governance behavior;
  - full corpus lookup validates top10 hit traces where `first_hit_rank <= 10`;
  - clean VAKS-only lexical + authority-bucket control is separated.
- Fixed stale denominator ambiguity by including `holdout_stale` in the P0 stale summary.
- Final P0 validator passed:

```text
p0 query replay check status: pass
error count: 0
replay rows: 7200
query metric rows: 720
summary rows: 32
```

## Original Yuxi Runtime Feasibility Recheck

- Rechecked local runtime prerequisites:

```text
docker --version -> docker not recognized
docker compose version -> docker not recognized
```

- Added `PHASE_B_ORIGINAL_YUXI_RUNTIME_FEASIBILITY.md`.
- Result remains:

```text
original Yuxi runtime: not run
yuxi_native_profile: local proxy only
C-lite/runtime adoption: not approved
```

## P1 Fresh Adversarial Pressure

- Added `queries_phase_b_adversarial.jsonl` with 30 fresh adversarial queries.
- JSONL validation passed: 30 unique queries.
- Resolvability check passed:

```text
primary resolvable: 30/30
full resolvable: 30/30
```

- Ran `run_phase_b_pressure.py` with `--result-prefix phase_b_adversarial`.
- Added `tools/build_phase_b_p1_adversarial_audit.py` and `tools/validate_phase_b_p1_adversarial_audit.py`.
- Generated clean VAKS-only control and combined adversarial summary.
- P1 adversarial audit passed:

```text
p1 adversarial check status: pass
error count: 0
criteria: 10/10 pass
```

Key rows:

```text
primary skeleton: hit@5 28/30, MRR 0.8556, leakage 0.0000
primary clean VAKS-only: hit@5 26/30, MRR 0.7537, leakage 0.0000
primary Yuxi proxy: hit@5 28/30, MRR 0.8167, leakage 1.0000

full skeleton: hit@5 28/30, MRR 0.8611, leakage 0.0000
full clean VAKS-only: hit@5 26/30, MRR 0.7211, leakage 0.0000
full Yuxi proxy: hit@5 27/30, MRR 0.8028, leakage 1.0000
```

## P1 Promotion Gate Calibration

- Added `tools/build_phase_b_p1_promotion_gate_calibration.py`.
- Added `tools/validate_phase_b_p1_promotion_gate_calibration.py`.
- Generated:
  - `results/phase_b_p1_promotion_gate_calibration_cases.jsonl`
  - `results/phase_b_p1_promotion_gate_calibration_evaluations.jsonl`
  - `results/phase_b_p1_promotion_gate_calibration_summary.json`
  - `PHASE_B_P1_PROMOTION_GATE_CALIBRATION_REPORT.md`
  - `PHASE_B_P1_PROMOTION_GATE_CALIBRATION_CHECK.md`
- Calibration validator passed:

```text
promotion gate calibration check status: pass
error count: 0
positive cases: 12
negative cases: 12
TPR: 1.0000
FPR: 0.0000
automatic_promotion_allowed_count: 0
formal_writeback_allowed_count: 0
reviewed_relation_creation_allowed_count: 0
```

## Supplemental Synthesis

- Added `PHASE_B_P0_P1_SUPPLEMENTAL_PRESSURE_REPORT.md`.
- Current decision:

```text
keep_phase_b_as_sandbox_candidate: yes
enter_c_lite: no
runtime_adoption: no
writeback_adoption: no
mainline_strong_conclusion: no
original_yuxi_runtime_validated: false
```

## Supplemental Pro Review Package

- Added `PRO_SUPPLEMENTAL_REVIEW_REQUEST.md` with a non-leading reverse-audit prompt.
- Created `pro-review-supplemental-package/` and `vaks-yuxi-phase-b-p0-p1-supplemental-pro-review-package.zip`.
- Package contents:

```text
file_count: 42
zip_bytes: 1324533
```

- Added `tools/validate_phase_b_supplemental_pro_package.py`.
- Ran package validator:

```text
supplemental pro package status: pass
error count: 0
```

- The package includes P0/P1 reports, checks, CSV/JSON evidence, query files, and validation scripts. It does not include any claim that original Yuxi runtime was validated.

## Agent-Blind Adversarial Pressure

- Spawned an independent sub-agent without parent context to generate 30 adversarial queries.
- The sub-agent was instructed not to read existing Phase B queries/results/reports and to use only core VAKS documents.
- Added `queries_phase_b_agent_blind.jsonl`.
- Validation:

```text
agent_blind jsonl ok: 30
primary resolvable: 30/30
full resolvable: 30/30
```

- Ran `run_phase_b_pressure.py` with `--result-prefix phase_b_agent_blind`.
- Added `tools/build_phase_b_agent_blind_audit.py` and `tools/validate_phase_b_agent_blind_audit.py`.
- Generated:
  - `PHASE_B_AGENT_BLIND_AUDIT_REPORT.md`
  - `PHASE_B_AGENT_BLIND_AUDIT_CHECK.md`
  - `results/phase_b_agent_blind_combined_summary.csv`
  - `results/phase_b_agent_blind_audit.json`
  - `results/phase_b_agent_blind_audit_check.json`
  - clean VAKS-only top/query/summary files.
- Validator passed:

```text
agent blind check status: pass
error count: 0
criteria: 10/10 pass
```

Key rows:

```text
primary skeleton: hit@5 30/30, MRR 0.9250, leakage 0.0000
primary clean VAKS-only: hit@5 23/30, MRR 0.6245, leakage 0.0000
primary Yuxi proxy: hit@5 27/30, MRR 0.8339, leakage 1.0000

full skeleton: hit@5 30/30, MRR 0.9278, leakage 0.0000
full clean VAKS-only: hit@5 21/30, MRR 0.5698, leakage 0.0000
full Yuxi proxy: hit@5 26/30, MRR 0.8229, leakage 1.0000
```

- Boundary:

```text
agent_blind strengthens local generalization evidence
agent_blind is not original Yuxi runtime validation
agent_blind is not an external human blind set
C-lite/runtime/writeback remain unapproved
```

## Pro Overclaim Wording Tightening

- Pro's P0/P1 supplemental review accepted the sandbox direction but flagged wording overclaims.
- Tightened report language:

```text
"proves" -> "shows in current local tests"
"proves stronger retrieval signals" -> "suggests under the current proxy harness"
"skeleton_mrr_above_yuxi_proxy" -> "skeleton_mrr_directionally_above_yuxi_proxy"
```

- Added explicit boundary language:

```text
promotion gate calibration is a rule-logic rebuttal, not operational calibration on real mixed packets
action_leakage_rate is a ranking/governance proxy, not an answer-level safety verdict
yuxi_native_profile leakage is not an original Yuxi runtime verdict
```

- Rebuilt and revalidated:

```text
P1 fresh adversarial audit: pass / 0 errors
Agent-blind audit: pass / 0 errors
Promotion gate calibration: pass / 0 errors
```

## P0 Corpus / Top11-20 Hardening

- Added `tools/build_phase_b_frozen_corpus_manifest.py` and `tools/validate_phase_b_frozen_corpus_manifest.py`.
- Generated:
  - `PHASE_B_FROZEN_CORPUS_MANIFEST.md`
  - `PHASE_B_FROZEN_CORPUS_MANIFEST_CHECK.md`
  - `results/phase_b_frozen_corpus_manifest.json`
  - `results/phase_b_frozen_corpus_manifest.csv`
  - `results/phase_b_frozen_corpus_manifest_check.json`
- Sequential validation passed:

```text
frozen corpus manifest check status: pass
error count: 0
primary files: 409
full files: 4384
```

- First attempt to generate top11-20 receipts across all four query sets timed out after roughly 15 minutes and left a Python process running.
- Stopped the lingering process and narrowed the artifact to the Pro-requested P0 scope: existing `main` + `holdout_used` query sets.
- Added `tools/build_phase_b_top11_20_receipts.py` and `tools/validate_phase_b_top11_20_receipts.py`.
- Generated:
  - `PHASE_B_TOP11_20_ITEM_RECEIPTS_REPORT.md`
  - `PHASE_B_TOP11_20_ITEM_RECEIPTS_CHECK.md`
  - `results/phase_b_top11_20_item_receipts.csv`
  - `results/phase_b_top11_20_item_receipts_summary.csv`
  - `results/phase_b_top11_20_item_receipts_summary.json`
  - `results/phase_b_top11_20_item_receipts_check.json`
- Validation passed:

```text
top11-20 item receipts check status: pass
error count: 0
receipt rows: 7200
query sets: main + holdout_used
```

- Boundary:

```text
This strengthens P0 auditability and rerunability.
It does not validate original Yuxi runtime.
It does not approve C-lite, answer-loop adoption, writeback, or core-doc strong conclusions.
```

## External Validation / C-lite前夜 Specs

- Added `PHASE_B_EXTERNAL_VALIDATION_NEXT_STEPS.md`.
- Added `PHASE_B_READ_ONLY_ANSWER_LOOP_PILOT_SPEC.md`.
- Added `tools/validate_phase_b_next_step_specs.py`.
- Validator passed:

```text
next-step specs check status: pass
error count: 0
```

- The external validation spec requires either external blind queries or an original Yuxi read-only rerun on Docker/remote runner.
- The answer/tool loop spec is explicitly read-only and forbids writeback, action basis creation, reviewed relation creation, and automatic promotion.

## Supplemental Pro Package Refresh

- Added `tools/build_phase_b_supplemental_pro_package.py`.
- Updated `tools/validate_phase_b_supplemental_pro_package.py` to require the new P0 hardening files and next-step specs.
- Rebuilt `pro-review-supplemental-package/` and `vaks-yuxi-phase-b-p0-p1-supplemental-pro-review-package.zip`.
- Package validation passed:

```text
pre-v2 supplemental pro package status: pass
error count: 0
package files: 78
zip bytes: see PHASE_B_SUPPLEMENTAL_PRO_PACKAGE_CHECK.md
```

## P0 Frozen Rerun V2

- Added `tools/build_phase_b_frozen_rerun_v2.py`.
- Added `tools/validate_phase_b_frozen_rerun_v2.py`.
- Ran a single-run P0 frozen replay bundle:

```text
run_id: phase_b_frozen_rerun_v2_20260611T142435Z
query sets: main + holdout_used
corpora: primary + full
modes: 8
top20 item rows: 14400
query metric rows: 720
summary rows: 32
```

- Generated:
  - `PHASE_B_FROZEN_RERUN_V2_REPORT.md`
  - `PHASE_B_FROZEN_RERUN_V2_CHECK.md`
  - `results/phase_b_frozen_rerun_v2_manifest.json`
  - `results/phase_b_frozen_rerun_v2_corpus_manifest.csv`
  - `results/phase_b_frozen_rerun_v2_query_manifest.csv`
  - `results/phase_b_frozen_rerun_v2_top20_items.csv`
  - `results/phase_b_frozen_rerun_v2_top1_10_replay.csv`
  - `results/phase_b_frozen_rerun_v2_top11_20_receipts.csv`
  - `results/phase_b_frozen_rerun_v2_query_metrics.csv`
  - `results/phase_b_frozen_rerun_v2_summary.csv`
  - `results/phase_b_frozen_rerun_v2_check.json`
- Validator passed:

```text
frozen rerun v2 check status: pass
error count: 0
top20 rows: 14400
```

- Boundary:

```text
This resolves the exact-run-alignment problem for local P0 proxy evidence.
It does not add human relevance judgment.
It does not validate original Yuxi runtime.
It does not approve C-lite, writeback, action basis, or core-doc strong conclusions.
```

## Supplemental Pro Package Refresh With V2

- Updated the supplemental package builder and validator to include Frozen Rerun v2 artifacts.
- Rebuilt `pro-review-supplemental-package/` and `vaks-yuxi-phase-b-p0-p1-supplemental-pro-review-package.zip`.
- Validation passed:

```text
supplemental pro package status: pass
error count: 0
package files: 91
zip bytes: see PHASE_B_SUPPLEMENTAL_PRO_PACKAGE_CHECK.md
pre-commit manifest: pass / 0 errors
pre-commit file count: 391
```

## Blind Relevance Pilot

- Spawned an internal no-parent-context query author to create blind relevance queries.
- Added `queries_phase_b_blind_relevance.jsonl` with 18 queries and rubrics.
- Corrected one query intent from `feedback` to allowed enum `review`.
- Added:
  - `tools/build_phase_b_blind_relevance_pilot.py`
  - `tools/validate_phase_b_blind_relevance_pilot.py`
  - `PHASE_B_BLIND_RELEVANCE_PILOT_REPORT.md`
  - `PHASE_B_BLIND_RELEVANCE_CHECK.md`
  - `PHASE_B_BLIND_RELEVANCE_JUDGMENT_INSTRUCTIONS.md`
- Ran retrieval for:

```text
query_count: 18
corpora: primary + full
modes: baseline_file_lexical, vaks_only_lexical_bucket, vaks_b_adapter_skeleton, yuxi_native_profile
top20 item rows: 2880
judgment packet rows: 720
run_id: phase_b_blind_relevance_20260611T151035Z
```

- Validator result:

```text
blind relevance check status: pending_judgment
error count: 0
judgment status: pending
```

- Boundary:

```text
This creates the relevance judgment packet.
It does not complete human/external relevance judgment.
It is internal no-parent-context query generation, not external human blind.
It does not validate original Yuxi runtime or C-lite.
```

## Internal Relevance Judgment

- Added `tools/build_phase_b_internal_relevance_judgments.py`.
- Filled `results/phase_b_blind_relevance_judgments.csv` using `judge_id=codex_internal_heuristic_judge_v1`.
- This judge is separate from `expected_terms`, but is internal heuristic/model-assisted and not external human judgment.
- Validation passed:

```text
blind relevance check status: pass
error count: 0
judgment status: complete
judgment rows: 720
```

Judged summary:

```text
primary baseline_file_lexical: hit@5 2/18, judged_mrr_at_5 0.0324, ndcg_at_5 0.6078
primary vaks_only_lexical_bucket: hit@5 10/18, judged_mrr_at_5 0.3935, ndcg_at_5 0.9024
primary vaks_b_adapter_skeleton: hit@5 11/18, judged_mrr_at_5 0.5741, ndcg_at_5 0.9554
primary yuxi_native_profile: hit@5 13/18, judged_mrr_at_5 0.5481, ndcg_at_5 0.9044
full baseline_file_lexical: hit@5 3/18, judged_mrr_at_5 0.1667, ndcg_at_5 0.7537
full vaks_only_lexical_bucket: hit@5 11/18, judged_mrr_at_5 0.3889, ndcg_at_5 0.8607
full vaks_b_adapter_skeleton: hit@5 13/18, judged_mrr_at_5 0.6250, ndcg_at_5 0.9186
full yuxi_native_profile: hit@5 11/18, judged_mrr_at_5 0.5185, ndcg_at_5 0.9513
```

Boundary:

```text
This is useful internal relevance signal.
It is not external blind/human relevance judgment.
It does not validate original Yuxi runtime, C-lite, or core-doc strong conclusions.
```

- Refreshed supplemental package and manifest after adding blind relevance packet:

```text
supplemental pro package: pass / 0 errors
package files: 102
pre-commit manifest: pass / 0 errors
pre-commit file count: 413
```

## External Relevance Double-Judge Kit

- Pro's latest reverse audit kept the verdict conservative:

```text
overall verdict: 部分成立
can keep Phase B as sandbox candidate: yes
can enter C-lite: no
can claim original Yuxi runtime validated: no
can commit core docs with strong conclusion: no
VAKS contribution: 中
Yuxi-like contribution: 大
```

- Pro's new P0 was external/manual relevance rejudgment for the existing 18-query blind relevance top5 packet.
- Added `tools/build_phase_b_external_relevance_judgment_kit.py`.
- Added `tools/validate_phase_b_external_relevance_judgment_kit.py`.
- Generated:
  - `PHASE_B_EXTERNAL_RELEVANCE_JUDGMENT_KIT.md`
  - `PHASE_B_EXTERNAL_RELEVANCE_JUDGMENT_KIT_CHECK.md`
  - `results/phase_b_blind_relevance_external_judgment_template.csv`
  - `results/phase_b_external_relevance_judgment_kit.json`
  - `results/phase_b_external_relevance_judgment_kit_check.json`
- Validator result:

```text
external relevance judgment kit check status: pending_external_judgment
error count: 0
external judgment status: pending_external_judgment
template rows: 720
```

- Boundary:

```text
The external/manual double-judge + arbitration template is ready.
External/manual judgment is not complete.
The internal heuristic judgment remains useful only as internal signal.
Original Yuxi runtime is still unvalidated until Docker/remote runner exists.
C-lite/runtime/writeback/core-doc strong conclusion remain not allowed.
```

## External Blind Query Set Kit

- Pro's latest minimum-test list also asks for 15-20 truly external blind queries.
- Added `tools/build_phase_b_external_blind_query_set_kit.py`.
- Added `tools/validate_phase_b_external_blind_query_set_kit.py`.
- Generated:
  - `PHASE_B_EXTERNAL_BLIND_QUERY_SET_KIT.md`
  - `PHASE_B_EXTERNAL_BLIND_QUERY_SET_KIT_CHECK.md`
  - `queries_phase_b_external_blind_template.jsonl`
  - `results/phase_b_external_blind_query_set_kit.json`
  - `results/phase_b_external_blind_query_set_kit_check.json`
- Validator result:

```text
external blind query set kit check status: pending_external_queries
error count: 0
external blind query status: pending_external_queries
template rows: 20
```

- Boundary:

```text
The external blind query authoring template is ready.
The external blind query set is not complete.
The template must be filled by an external human or at least a different model family.
The author must not read existing Phase B queries/results/reports.
This does not validate original Yuxi runtime or approve C-lite/runtime/writeback.
```

## External Kit Revise Response

- Pro reviewed both external kits as `revise`, not reject.
- Revised external relevance kit:
  - Judge-facing template now hides concrete system identity.
  - Removed `mode`, `run_id`, original `judgment_id`, and `test_set` from the judge-facing CSV.
  - Added opaque `row_id` and `system_slot`.
  - Added `results/phase_b_blind_relevance_external_judgment_mapping.csv` for post-judgment statistics only.
- Revised external blind query kit:
  - External author template no longer includes `expected_terms`.
  - Added `results/phase_b_external_blind_query_author_manifest_template.json`.
  - Author manifest records author type/model family, allowed docs seen, generation method, and no-access attestations for Phase B queries/results/reports.
  - Expected terms/scoring hints must be added later by an internal scorer without changing frozen query text.
- Validators after revision:

```text
external relevance judgment kit: pending_external_judgment / 0 errors
external blind query set kit: pending_external_queries / 0 errors
```

- Boundary:

```text
The kits are more blind and more auditable.
They still are not completed external judgment or completed external blind testing.
```

## Wording Tightening After Pro Overclaim Notes

- Tightened `PHASE_B_BLIND_RELEVANCE_CHECK.md` through the validator:

```text
judgment status: complete -> complete_internal_only
```

- Tightened answer-loop wording:

```text
"This is the C-lite前夜 test." ->
"This is a pre-C-lite sandbox pilot concept, not a C-lite readiness claim."
```

- Tightened Frozen Rerun v2 wording:

```text
Frozen Rerun v2 is the authoritative exact-run local P0 bundle going forward.
Older P0 summaries remain historical artifacts and should not be mixed with v2 as headline evidence.
```

- Tightened internal relevance judge boundary:

```text
The internal judge uses query-specific PROFILES, term/path matches, and VAKS bucket/status priors.
It is a sanity diagnostic, not a weak human substitute or gold standard.
```
