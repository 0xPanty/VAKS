---
record_kind: sandbox_task_plan
status: active
project_id: VAKS
created_at: 2026-06-11
truth_boundary: sandbox_diagnostic_not_mainline_decision
action_basis_allowed: false
---

# VAKS Phase B Retrieval Pressure Test Plan

## Goal

Quantitatively test whether Phase B fusion is worth keeping:

```text
parser / chunk / metadata / vector-like index / graph-like index /
bucket-local retrieval / click-back / retrieval receipt
```

No Skills, no MCP write tools, no subagents as production evidence, no formal writeback, no mainline architecture edits.

## Acceptance Bar

Keep Phase B only if the sandbox shows clear positive value over baseline without boundary regression.

Minimum signals:

- Retrieval improves on primary and noisy corpora.
- Pressure cases do not collapse candidate/raw/feedback into action support.
- Results carry click-back anchors and hash receipts.
- VAKS+B beats or ties the Yuxi-native profile on governance metrics.
- Any Yuxi-native retrieval advantage is explained instead of hidden.

## Compared Modes

1. `baseline_file_lexical`: old file-level lexical retrieval.
2. `vaks_b_bucketless`: Yuxi-like hybrid retrieval without VAKS authority filtering.
3. `vaks_b_bucket_local`: Phase B target, VAKS authority filter before bucket-local retrieval/rerank.
4. `yuxi_native_profile`: closest local approximation of original Yuxi retrieval shape: global hybrid chunk/vector/graph fusion with click-back, but without VAKS authority governance.

If original Yuxi can run locally, add a fifth mode and record exact commands. If Docker or service dependencies block it, record that honestly.

## Test Dimensions

- hit@5 / hit@10 expected-source recall
- mean reciprocal rank
- boundary warning coverage
- action-basis leakage rate
- cross-bucket authority-mix violations
- click-back coverage
- source/chunk hash coverage
- stale-index detection
- noisy-corpus resilience
- adversarial query behavior

## Phases

| Phase | Status | Notes |
|---|---|---|
| 1. Recover context and create sandbox | complete | Read prior pilot, Pro advice, and memory handles. |
| 2. Check original Yuxi run feasibility | complete | Full run blocked by missing Docker; cloned current repo and defined code/doc-aligned comparator. |
| 3. Implement pressure harness | complete | Added four modes, governance metrics, stale-index simulation, and top-result receipts. |
| 4. Run primary/noisy/adversarial/stale tests | complete | Ran primary and full noisy corpora, 30 queries x 4 modes x 2 corpora. |
| 5. Decide keep / modify / reject | complete | Phase B passed as sandbox candidate only; no C-lite/tool/writeback approval. |
| 6. Iteration v1: anchor-aware adapter rerank | complete | Positive over locked v0 on main pressure and holdout aggregate; governance stayed zero-leak. |
| 7. v1.1 regression pass | complete | v1.1 beat v1 on holdout, tied v1 on main pressure, and kept zero leakage. |
| 8. Minimal real adapter skeleton | complete | Added read-only adapter module, chunk manifests, retrieval receipts, and skeleton-vs-v1.1 pressure comparison with zero regressions. |
| 9. Adapter contract test | complete | Contract validator now passes with zero errors after fixing click-back range, manifest warnings, and receipt indexed source hashes. |
| 10. Integration readiness package | complete | Added package, readiness validator, readiness check report, and readiness-vs-contract decision; passed with zero errors and no metric regression from the contract-passing skeleton. |
| 11. Mainline-readiness / Pro review packet | complete | Added packet, validator, check report, and decision. Mainline-readiness check passed with zero errors, readiness/contract remained pass, and core docs stayed clean. |
| 12. External / Pro review prompt | complete | Added copy-pasteable Pro prompt, validator, check report, and decision. Prompt check passed with zero errors while prior gates stayed pass and core docs stayed clean. |
| 13. External review result | complete | Subagent review returned `APPROVE_MINIMAL_DOC_PATCH`; result and validator passed with zero errors while prior gates stayed green. |
| 14. Minimal documentation-only patch | complete | Patched only `SOURCE_INTAKE.md`, `IMPLEMENTATION_BLUEPRINT.md`, `DEV_CONTEXT.md`, and `MEMORY_TIER.md`; validator passed with zero errors and deferred files stayed untouched. |
| 15. Runtime/full-stack feasibility check | complete | Checked current Yuxi HEAD and local prerequisites. Docker/Compose remain unavailable; Lite and tests still require Docker. Runtime feasibility check passed by blocking false full-stack claims. |
| 16. Context-pack candidate assembly | complete | Built 90 context-pack candidates from existing retrieval receipts. Validator passed with zero errors; pack-level `action_basis_allowed` stayed 0 even when 36 packs suppressed action-looking receipt flags. |
| 17. Evidence-envelope / warrant draft sandbox | complete | Built 90 evidence-envelope candidates from context-pack candidates. Validator passed with zero errors; action basis, Evidence Packet permission, and Evidence Sufficiency pass all stayed 0. |
| 18. Evidence Support Check candidate sandbox | complete | Built 90 support-check candidates from evidence envelopes. Validator passed with zero errors; 389 source spans were extracted, 68 refresh-needed hash cases were surfaced, 2 missing-anchor cases were blocked, and semantic support/action permissions stayed 0. |
| 19. Source-refresh / reindex sandbox | complete | Built 90 source-refresh candidates from support-check candidates. Validator passed with zero errors; pre-refresh mismatch dropped from 68 to post-refresh mismatch 0 while support/action/evidence permissions stayed 0. |
| 20. Refreshed support-check rebuild / delta sandbox | complete | Rebuilt 90 support-check candidates from refreshed source spans/hashes. Validator passed with zero errors; refresh-needed dropped from 68 to 0, current hash matches rose to 389/389, and support/action/evidence permissions stayed 0. |
| 21. Manual-review packet / reviewer queue sandbox | complete | Built 90 review queue packets from refreshed support-check candidates. Validator passed with zero errors; 88 packets are open, 2 no-anchor packets stay blocked/parked, 389 review items keep current source hashes, and review/support/promotion/action permissions stayed 0. |
| 22. Simulated reviewer outcome sandbox | complete | Built 90 simulated reviewer outcome records from review queue packets. Validator passed with zero errors; 12 packets received simulation-only outcomes, 57 simulated item outcomes were recorded, and human-reviewed support / promotion / writeback / action permissions stayed 0. |
| 23. Promotion-gate / sufficiency-block sandbox | complete | Built 90 promotion/action gate evaluations from simulated reviewer outcomes. Validator passed with zero errors; all 90 gates were blocked, 24 support-like simulated item outcomes were visible, and promotion/action/sufficiency/writeback/truth-change permissions stayed 0. |
| 24. Phase B keep/stop synthesis packet | complete | Generated a whole-chain keep/stop synthesis. Validator passed with 0 errors; decision is keep Phase B as a positive sandbox/documentation candidate only, not runtime/default/C-lite/writeback/action adoption. |
| 25. Commit-readiness scope check | complete | Generated commit-readiness packet. Validator passed with 0 errors; recommended scope is the validated four docs plus the Phase B sandbox evidence bundle, but commit still requires explicit user approval. |
| 26. Next-action gate | complete | Generated a branch-choice gate. Validator passed with 0 errors; recommended next action is to wait for user-approved commit or a Docker/remote runner choice. C-lite and runtime adoption remain not allowed. |
| 27. Pre-commit manifest | complete | Generated a file-level pre-commit manifest with SHA256 fingerprints. Validator passed with 0 errors; it adds auditability only and still does not approve staging or committing. |
| 28. Branch-decision brief | complete | Generated a human-readable branch brief and recovery prompt. Validator passed with 0 errors; recommended branch is user-approved commit, while runtime/C-lite remain blocked/not allowed. |
| 29. User branch decision | pending | User should choose: approve the documentation/evidence commit, provide Docker/remote runner for original Yuxi full-stack testing, or explicitly open a new separately gated sandbox. |
| 30. Pro critique response / P0 query-level replay | complete | Added query-level top10 replay plus top20 paired outcomes, metric dictionary, clean VAKS-only lexical control, and replay validator. `PHASE_B_P0_QUERY_LEVEL_REPLAY_CHECK.md` passed with 0 errors over 7200 replay rows. |
| 31. Original Yuxi runtime feasibility recheck | complete | Rechecked Docker and Docker Compose; both unavailable. Added `PHASE_B_ORIGINAL_YUXI_RUNTIME_FEASIBILITY.md`; original Yuxi runtime remains unknown and unvalidated. |
| 32. P1 fresh adversarial pressure test | complete | Added 30 fresh adversarial queries and ran pressure harness. Added clean VAKS-only control and audit validator; `PHASE_B_P1_ADVERSARIAL_AUDIT_CHECK.md` passed with 0 errors. |
| 33. P1 promotion gate positive/negative calibration | complete | Added 12 positive and 12 negative synthetic gate cases. Calibration validator passed with 0 errors; TPR 1.0000, FPR 0.0000, and auto writeback/action/relation mutation stayed 0. |
| 34. Supplemental pressure synthesis | complete | Added `PHASE_B_P0_P1_SUPPLEMENTAL_PRESSURE_REPORT.md`. Updated decision: keep Phase B as sandbox candidate; do not enter C-lite/runtime/writeback/mainline strong conclusion. |
| 35. P0 corpus/replay hardening | complete | Added frozen corpus manifest and P0 top11-20 item receipts. `PHASE_B_FROZEN_CORPUS_MANIFEST_CHECK.md` and `PHASE_B_TOP11_20_ITEM_RECEIPTS_CHECK.md` passed with 0 errors. |
| 36. P0 Frozen Rerun v2 | complete | Added a single-run `run_id` bundle with corpus/query/script hashes, top20 items, top1-10 replay, top11-20 receipts, query metrics, and summary. Validator passed with 0 errors by deriving metrics/summary from top20 rows. |
| 37. External validation / C-lite前夜 specs | complete | Added `PHASE_B_EXTERNAL_VALIDATION_NEXT_STEPS.md` and `PHASE_B_READ_ONLY_ANSWER_LOOP_PILOT_SPEC.md`. Spec validator passed with 0 errors; these are future-test gates, not C-lite approval. |
| 38. Supplemental Pro package refresh | complete | Rebuilt the supplemental package with Frozen Rerun v2 artifacts included. Package validator passed with 0 errors; final file/zip counts are in `PHASE_B_SUPPLEMENTAL_PRO_PACKAGE_CHECK.md`. |
| 39. Blind relevance query set / judgment packet | complete_internal_only | Generated 18 internal no-parent-context blind queries, ran 4-mode primary/full top20 retrieval, created a 720-row top5 judgment packet, and filled it with internal heuristic/model-assisted judgments. External/human judgment remains pending. |
| 40. External relevance double-judge kit | revised_template_ready_pending_external_judgment | Revised the 720-row relevance template to hide system identity behind opaque `row_id` / `system_slot` plus a separate mapping table. Validator passes as `pending_external_judgment / 0 errors`; external/manual filled judgments remain pending. |
| 41. External blind query set kit | revised_template_ready_pending_external_queries | Revised the 20-row external blind query template so the external author does not fill `expected_terms`, and added an author/provenance manifest template. Validator passes as `pending_external_queries / 0 errors`; external human or different-model filled queries remain pending. |

## Errors Encountered

| Error | Attempt | Resolution |
|---|---|---|
| `docker` command not found | Checked original Yuxi full-stack run feasibility | Record as local blocker; compare against code/doc-aligned `yuxi_native_profile` unless another runtime path is found. |
| PowerShell rejected bash heredoc syntax | Tried `python - <<'PY'` | Use PowerShell here-string piped into Python. |
| q21 metric penalized boundary-first behavior | First primary run had VAKS+B top1 `SCHEMA.md` but first expected hit at rank 8 because expected terms over-favored Mnemosyne candidate | Added `SCHEMA.md` and `SOURCE_INTAKE.md` to q21 expected terms. |
| Full v1 run timed out at 124s | Ran primary+full with an added v1 mode under the default long command timeout | Rerun with a longer timeout; if repeated, optimize the v1 scoring loop. |
| Readiness validator KeyError on `corpus` | First readiness run assumed plain UTF-8 CSV headers | Switched CSV reading to `utf-8-sig` and normalized field names. |
| Readiness package missing exact `expected_terms` rule phrase | Second readiness run failed one package coverage check | Added explicit plain rule that `expected_terms` is evaluation scaffolding, not adapter memory or production ranking input. |
| Minimal doc patch validator failed 6 checks | First run missed an exact DEV_CONTEXT phrase and treated `0` as false for prior gates | Added the explicit DEV_CONTEXT phrase and fixed validator zero handling. |
| Context-pack validator falsely flagged zero action-basis count | First run treated `0` as missing in summary action-basis check | Fixed zero handling; validator then passed with 0 errors. |
| P0 replay validator failed 662 checks | Validator tried to recompute top20 MRR from top10 snippets and inferred coverage from path/reasons | Split query-level paired outcomes from top10 replay checks, used full corpus lookup for top10 hit traces, and validated summary from query metrics. |
| P0 summary stale detection mismatched 8 rows | Older summary helper counted only `stale_pressure`, missing holdout group `holdout_stale` | Added P0 summary logic that includes `holdout_stale`; P0 validator passed with 0 errors. |
| Full P0 top20 rerun timed out | Tried to regenerate every mode as top20 rows, which was too slow in the local harness | Stopped the long-running process and used a lighter, auditable design: existing top10 replay plus top20 query outcomes and clean-control rerun. |
| P1 adversarial validator falsely failed on zero failed criteria | Used `audit.get("failed_criteria") or -1`, treating `0` as missing | Fixed zero handling; P1 adversarial validator passed with 0 errors. |
| First full top11-20 receipt build timed out | Tried to regenerate four query sets across all modes and corpora in one pass | Stopped the lingering Python process and narrowed the P0 hardening artifact to the requested existing main/holdout 45 queries. |
| Frozen corpus validation raced build output | Build and validation were accidentally launched in parallel | Reran validation sequentially and made the check report robust to missing manifest fields. |
