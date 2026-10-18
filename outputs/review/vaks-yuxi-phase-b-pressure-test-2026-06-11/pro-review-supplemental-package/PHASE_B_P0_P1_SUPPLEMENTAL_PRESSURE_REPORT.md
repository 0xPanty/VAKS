---
record_kind: sandbox_p0_p1_supplemental_pressure_report
status: candidate
project_id: VAKS
created_at: 2026-06-11
truth_boundary: supplemental_pressure_not_mainline_decision
action_basis_allowed: false
---

# Phase B P0/P1 Supplemental Pressure Report

## Plain Conclusion

```text
Evidence is stronger than the Pro-reviewed package, but still bounded.

Stronger now:
- P0 query-level replay exists and validates with 0 errors.
- P0 frozen corpus manifest exists and validates with 0 errors.
- P0 top11-20 item-level receipts exist and validate with 0 errors.
- P0 Frozen Rerun v2 now provides one run_id with top20 item-level rows, query metrics, summary, and exact consistency validation.
- P1 fresh adversarial set passes local criteria.
- Agent-blind adversarial set from an independent sub-agent passes local criteria.
- Clean VAKS-only control is now separated.
- Promotion gate has positive/negative calibration, not only all-blocking behavior.

Still not proven:
- Original Yuxi runtime was not run.
- The P1 query set is fresh adversarial, not an external blind set.
- The agent-blind query set is independently generated inside Codex, not a real external human blind set.
- C-lite, runtime adoption, writeback, action basis, and original-Yuxi equivalence remain unapproved.
- Human relevance judgment is still not added.
```

## P0 Query-Level Replay

```text
artifact: PHASE_B_P0_QUERY_LEVEL_REPLAY_REPORT.md
check: PHASE_B_P0_QUERY_LEVEL_REPLAY_CHECK.md
status: pass
error_count: 0
replay_rows: 7200
query_metric_rows: 720
summary_rows: 32
```

P0 now supplies query-level paired outcomes, top10 replay, metric definitions, clean VAKS-only lexical control, and a validator that recomputes the P0 summary. It also fixes the stale denominator ambiguity by counting `holdout_stale` as stale-pressure evidence in the P0 summary.

## P0 Reproducibility Hardening

```text
frozen corpus manifest: pass / 0 errors
primary files: 409
full files: 4384
top11-20 item receipts: pass / 0 errors
top11-20 receipt rows: 7200
query sets covered by top11-20 receipts: main + holdout_used
```

This materially improves the remaining P0 audit gap: the previous package exposed top20 first-hit ranks at query level, but only top10 item-level replay. The new receipts expose ranks 11-20 for the existing 45 P0 queries in a later local rerun, while keeping the governance window at top10.

Boundary:

```text
The corpus manifest makes the local corpus reproducible.
The top11-20 receipts make rank 11-20 candidates visible in the later local rerun.
They do not yet prove exact-run equivalence with the earlier P0 query metrics.
Neither artifact validates original Yuxi runtime, answer-loop behavior, C-lite, or writeback.
```

## P0 Frozen Rerun V2

```text
artifact: PHASE_B_FROZEN_RERUN_V2_REPORT.md
check: PHASE_B_FROZEN_RERUN_V2_CHECK.md
status: pass
error_count: 0
run_id: phase_b_frozen_rerun_v2_20260611T142435Z
top20 item rows: 14400
query metric rows: 720
summary rows: 32
```

Frozen Rerun v2 is the stricter P0 evidence bundle requested after Pro's critique. It pins corpus manifest, query manifest, script hashes, top20 item-level export, top1-10 replay, top11-20 receipts, query metrics, and summary under one `run_id`.

The validator checks exact cross-artifact consistency inside the bundle: query metrics and summary must be recoverable from the top20 item-level rows.

Boundary:

```text
This resolves the exact-run-alignment problem for local P0 proxy evidence.
It does not add human relevance judgment.
It does not run original Yuxi runtime.
It does not approve C-lite, writeback, action basis, or core-doc strong conclusions.
```

## P1 Fresh Adversarial Retrieval/Governance

```text
artifact: PHASE_B_P1_ADVERSARIAL_AUDIT_REPORT.md
check: PHASE_B_P1_ADVERSARIAL_AUDIT_CHECK.md
status: pass
query_count: 30
failed_criteria: 0
```

Key rows:

| Corpus | Mode | hit@5 | MRR | action leakage |
|---|---|---:|---:|---:|
| primary | baseline_file_lexical | 15/30 | 0.3861 | 1.0000 |
| primary | vaks_only_lexical_bucket | 26/30 | 0.7537 | 0.0000 |
| primary | vaks_b_bucket_local | 27/30 | 0.7174 | 0.0000 |
| primary | vaks_b_adapter_skeleton | 28/30 | 0.8556 | 0.0000 |
| primary | yuxi_native_profile | 28/30 | 0.8167 | 1.0000 |
| full | baseline_file_lexical | 17/30 | 0.4933 | 1.0000 |
| full | vaks_only_lexical_bucket | 26/30 | 0.7211 | 0.0000 |
| full | vaks_b_bucket_local | 27/30 | 0.7778 | 0.0000 |
| full | vaks_b_adapter_skeleton | 28/30 | 0.8611 | 0.0000 |
| full | yuxi_native_profile | 27/30 | 0.8028 | 1.0000 |

Interpretation:

```text
VAKS-only lexical shows in current local tests that the boundary layer can keep measured leakage at 0, but retrieval is weaker than skeleton.
Yuxi-like proxy suggests stronger retrieval signals under the current proxy harness, but leaks action/evidence authority under the current leakage proxy.
Skeleton combines both in this sandbox: better retrieval than clean VAKS-only and zero measured leakage.
```

## Agent-Blind Adversarial Retrieval/Governance

```text
artifact: PHASE_B_AGENT_BLIND_AUDIT_REPORT.md
check: PHASE_B_AGENT_BLIND_AUDIT_CHECK.md
status: pass
query_count: 30
query_author: independent sub-agent without parent context
failed_criteria: 0
```

Key rows:

| Corpus | Mode | hit@5 | MRR | action leakage |
|---|---|---:|---:|---:|
| primary | baseline_file_lexical | 20/30 | 0.4311 | 1.0000 |
| primary | vaks_only_lexical_bucket | 23/30 | 0.6245 | 0.0000 |
| primary | vaks_b_bucket_local | 28/30 | 0.8478 | 0.0000 |
| primary | vaks_b_adapter_skeleton | 30/30 | 0.9250 | 0.0000 |
| primary | yuxi_native_profile | 27/30 | 0.8339 | 1.0000 |
| full | baseline_file_lexical | 16/30 | 0.4368 | 1.0000 |
| full | vaks_only_lexical_bucket | 21/30 | 0.5698 | 0.0000 |
| full | vaks_b_bucket_local | 28/30 | 0.7940 | 0.0000 |
| full | vaks_b_adapter_skeleton | 30/30 | 0.9278 | 0.0000 |
| full | yuxi_native_profile | 26/30 | 0.8229 | 1.0000 |

Interpretation:

```text
The internal no-parent-context stress set strengthens the same direction as the fresh local set.
It remains an internal model-family-generated set rather than an external blind evaluation.
It shows stronger separation between clean VAKS-only and skeleton retrieval.
Skeleton-vs-Yuxi-proxy MRR is directional local evidence, not decisive retrieval-superiority proof.
Action leakage is a ranking/governance proxy, not an answer-level safety verdict.
It still does not validate original Yuxi runtime or C-lite.
```

## P1 Promotion Gate Calibration

```text
artifact: PHASE_B_P1_PROMOTION_GATE_CALIBRATION_REPORT.md
check: PHASE_B_P1_PROMOTION_GATE_CALIBRATION_CHECK.md
status: pass
positive_cases: 12
negative_cases: 12
TPR: 1.0000
FPR: 0.0000
automatic_promotion_allowed: 0
formal_writeback_allowed: 0
reviewed_relation_creation_allowed: 0
```

This addresses the earlier critique that the gate only proved negative blocking. The positive cases mean eligible for manual promotion-candidate handling, not automatic writeback. This is a rule-logic rebuttal, not proof of operational calibration on real mixed evidence packets. The TPR/FPR figures are synthetic-case diagnostics and must not be treated as real operational calibration.

## Original Yuxi Runtime

```text
artifact: PHASE_B_ORIGINAL_YUXI_RUNTIME_FEASIBILITY.md
status: blocked_by_environment
docker: unavailable
docker compose: unavailable
original Yuxi runtime result: unknown
```

This remains a hard boundary. The current tests support VAKS-wrapped Yuxi-like retrieval as a sandbox candidate. They do not prove original Yuxi runtime behavior.

## Updated Decision

```text
keep_phase_b_as_sandbox_candidate: yes
enter_c_lite: no
runtime_adoption: no
writeback_adoption: no
mainline_strong_conclusion: no
P0 frozen rerun v2: complete with exact bundle consistency check
human relevance judgment: still missing
next required external check: original Yuxi read-only rerun, external blind set, or Pro review of this supplemental package
```
