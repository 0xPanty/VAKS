---
record_kind: sandbox_v11_iteration_comparison
status: candidate
project_id: VAKS
created_at: 2026-06-11
truth_boundary: diagnostic_not_mainline_decision
action_basis_allowed: false
---

# Phase B v1.1 Iteration Comparison

## Compared Versions

- `vaks_b_adapter_v1`: previous sandbox candidate.
- `vaks_b_adapter_v1_1`: v1.1 adds topic-anchor routing for resource-filter and benchmark/lint/diagnostic boundary queries.

## Summary Delta

| Corpus | Metric | v1 | v1.1 | Delta | Direction |
|---|---|---:|---:|---:|---|
| primary | hit_at_5 | 10/15 | 12/15 | 2.0000 | improved |
| primary | hit_at_10 | 12/15 | 13/15 | 1.0000 | improved |
| primary | mrr | 0.6088 | 0.7811 | 0.1723 | improved |
| primary | action_leakage_rate | 0.0000 | 0.0000 | 0.0000 | same |
| primary | forbidden_top1_rate | 0.0000 | 0.0000 | 0.0000 | same |
| primary | cross_bucket_violation_rate | 0.0000 | 0.0000 | 0.0000 | same |
| primary | warning_coverage_risk | 1.0000 | 1.0000 | 0.0000 | same |
| primary | clickback_coverage | 1.0000 | 1.0000 | 0.0000 | same |
| primary | hash_coverage | 1.0000 | 1.0000 | 0.0000 | same |
| primary | adapter_coverage | 1.0000 | 1.0000 | 0.0000 | same |
| primary | receipt_coverage | 1.0000 | 1.0000 | 0.0000 | same |
| primary | stale_detection_rate | 0.0000 | 0.0000 | 0.0000 | same |
| full | hit_at_5 | 11/15 | 13/15 | 2.0000 | improved |
| full | hit_at_10 | 12/15 | 13/15 | 1.0000 | improved |
| full | mrr | 0.5924 | 0.7591 | 0.1667 | improved |
| full | action_leakage_rate | 0.0000 | 0.0000 | 0.0000 | same |
| full | forbidden_top1_rate | 0.0000 | 0.0000 | 0.0000 | same |
| full | cross_bucket_violation_rate | 0.0000 | 0.0000 | 0.0000 | same |
| full | warning_coverage_risk | 1.0000 | 1.0000 | 0.0000 | same |
| full | clickback_coverage | 1.0000 | 1.0000 | 0.0000 | same |
| full | hash_coverage | 1.0000 | 1.0000 | 0.0000 | same |
| full | adapter_coverage | 1.0000 | 1.0000 | 0.0000 | same |
| full | receipt_coverage | 1.0000 | 1.0000 | 0.0000 | same |
| full | stale_detection_rate | 0.0000 | 0.0000 | 0.0000 | same |

## Query-Level MRR Movement

### primary

- improved: 3
- regressed: 0
- same: 12
- improved queries: h08_eval_score_greenlight (+0.7500), h10_old_sandbox_benchmark_truth (+0.8333), h13_resource_filter_before_search (+1.0000)
- regressed queries: none

### full

- improved: 3
- regressed: 0
- same: 12
- improved queries: h08_eval_score_greenlight (+0.8333), h10_old_sandbox_benchmark_truth (+0.6667), h13_resource_filter_before_search (+1.0000)
- regressed queries: none

## Iteration Verdict

- boundary pass: True
- primary MRR delta: 0.1723
- full noisy MRR delta: 0.1667
- query-level regressions: 0

Verdict: keep v1.1 as the next sandbox candidate.
