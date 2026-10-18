---
record_kind: sandbox_supplemental_completion_audit
status: complete_with_external_blockers
project_id: VAKS
created_at: 2026-06-11
truth_boundary: completion_audit_not_mainline_decision
action_basis_allowed: false
---

# Phase B Supplemental Completion Audit

## User Objective

```text
按照 Pro 要求把强压测试补全。
```

## Requirement Audit

| Requirement | Status | Evidence |
|---|---|---|
| P0 query-level replay, not summary-only | complete | `PHASE_B_P0_QUERY_LEVEL_REPLAY_CHECK.md`: pass / 0 errors, 7200 replay rows |
| Frozen corpus manifest / file-hash snapshot | complete | `PHASE_B_FROZEN_CORPUS_MANIFEST_CHECK.md`: pass / 0 errors, primary 409 files, full 4384 files |
| P0 top11-20 item-level receipts | complete | `PHASE_B_TOP11_20_ITEM_RECEIPTS_CHECK.md`: pass / 0 errors, 7200 receipt rows |
| Single-run Frozen Rerun v2 bundle | complete | `PHASE_B_FROZEN_RERUN_V2_CHECK.md`: pass / 0 errors, 14400 top20 rows, 720 query metrics, 32 summary rows |
| Blind relevance query set + judgment packet | complete_internal_only | `PHASE_B_BLIND_RELEVANCE_CHECK.md`: pass / 0 errors, 18 queries, 720 internal-only judgment rows |
| Internal relevance judgment | complete_internal_only | `PHASE_B_INTERNAL_RELEVANCE_JUDGMENT_REPORT.md`: 720 judgments, separate from expected_terms but not external human judgment |
| External/manual relevance double-judge kit | revised_template_ready_pending_external_judgment | `PHASE_B_EXTERNAL_RELEVANCE_JUDGMENT_KIT_CHECK.md`: pending_external_judgment / 0 errors, 720-row anonymous template + mapping |
| External blind query set kit | revised_template_ready_pending_external_queries | `PHASE_B_EXTERNAL_BLIND_QUERY_SET_KIT_CHECK.md`: pending_external_queries / 0 errors, 20-row query template + author manifest template |
| Metric dictionary and denominators | complete | `PHASE_B_METRIC_DICTIONARY.md`, `results/phase_b_metric_dictionary.json` |
| Clean VAKS-only lexical + authority-bucket control | complete | `results/phase_b_p0_clean_vaks_only_summary.csv`, P1/agent_blind clean summaries |
| Fresh adversarial set | complete | `queries_phase_b_adversarial.jsonl`, `PHASE_B_P1_ADVERSARIAL_AUDIT_CHECK.md`: pass / 0 errors |
| Promotion gate positive/negative calibration | complete | `PHASE_B_P1_PROMOTION_GATE_CALIBRATION_CHECK.md`: pass / 0 errors, 12 positive + 12 negative |
| Agent-blind adversarial set from no-context sub-agent | complete | `queries_phase_b_agent_blind.jsonl`, `PHASE_B_AGENT_BLIND_AUDIT_CHECK.md`: pass / 0 errors |
| External validation / C-lite前夜 specs | complete | `PHASE_B_NEXT_STEP_SPECS_CHECK.md`: pass / 0 errors |
| Pro supplemental review package | complete | `PHASE_B_SUPPLEMENTAL_PRO_PACKAGE_CHECK.md`: pass / 0 errors, 122 files |
| Pre-commit/evidence manifest | complete | `PHASE_B_PRE_COMMIT_MANIFEST_CHECK.md`: pass / 0 errors, 453 files |
| Original Yuxi runtime read-only rerun | externally blocked | `PHASE_B_ORIGINAL_YUXI_RUNTIME_FEASIBILITY.md`: Docker/Docker Compose unavailable |
| External human blind set | externally pending | agent_blind exists, but it is still an internal Codex sub-agent set |
| External blind query set | pending | external blind query template exists, but external filled queries have not been provided |
| Human/external relevance judgment | pending | internal heuristic judgments exist, but external human/Pro judgment has not replaced them |

## Current Evidence Summary

```text
P0 query replay: pass / 0 errors
P0 frozen corpus manifest: pass / 0 errors
P0 top11-20 item receipts: pass / 0 errors
P0 frozen rerun v2: pass / 0 errors
Blind relevance packet: pass / 0 errors
Internal relevance judgment: complete_internal_only
External/manual relevance judgment kit: revised_template_ready_pending_external_judgment
External blind query set kit: revised_template_ready_pending_external_queries
P1 fresh adversarial: pass / 0 errors
P1 promotion gate calibration: pass / 0 errors
Agent-blind adversarial: pass / 0 errors
Next-step specs: pass / 0 errors
Supplemental Pro package: pass / 0 errors
Pre-commit manifest: pass / 0 errors
```

## Boundary

```text
The local strong-pressure testing and P0 audit-hardening requested after Pro's critique have been completed.
The exact-run-alignment issue for P0 local proxy evidence is now addressed by Frozen Rerun v2.
The result supports keeping Phase B as a sandbox candidate.
The result does not validate original Yuxi runtime.
The result adds blind relevance judgments from an internal heuristic/model-assisted judge, but does not complete human/external relevance judgment yet.
The result now includes a revised anonymous external/manual double-judge + arbitration template, but that template still needs external filling before it can count as external relevance evidence.
The result now includes a revised external blind query authoring template plus author manifest template, but those files still need external filling before they can count as an external blind set.
The result does not approve C-lite, runtime adoption, writeback adoption, action basis, or mainline strong conclusions.
```

## Next External Step

```text
Send `vaks-yuxi-phase-b-p0-p1-supplemental-pro-review-package.zip` to Pro.
Ask Pro or external judges to fill `results/phase_b_blind_relevance_external_judgments.csv` from the included template.
Ask an external human or different model family to fill `queries_phase_b_external_blind.jsonl` from the included template.
If original Yuxi runtime must be tested, provide Docker/Docker Compose or a remote runner.
```
