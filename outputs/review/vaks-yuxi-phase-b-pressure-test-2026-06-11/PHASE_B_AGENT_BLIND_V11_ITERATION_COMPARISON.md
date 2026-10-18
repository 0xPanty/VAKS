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
| primary | hit_at_5 | 30/30 | 30/30 | 0.0000 | same |
| primary | hit_at_10 | 30/30 | 30/30 | 0.0000 | same |
| primary | mrr | 0.9250 | 0.9250 | 0.0000 | same |
| primary | action_leakage_rate | 0.0000 | 0.0000 | 0.0000 | same |
| primary | forbidden_top1_rate | 0.0000 | 0.0000 | 0.0000 | same |
| primary | cross_bucket_violation_rate | 0.0000 | 0.0000 | 0.0000 | same |
| primary | warning_coverage_risk | 1.0000 | 1.0000 | 0.0000 | same |
| primary | clickback_coverage | 1.0000 | 1.0000 | 0.0000 | same |
| primary | hash_coverage | 1.0000 | 1.0000 | 0.0000 | same |
| primary | adapter_coverage | 1.0000 | 1.0000 | 0.0000 | same |
| primary | receipt_coverage | 1.0000 | 1.0000 | 0.0000 | same |
| primary | stale_detection_rate | 0.0000 | 0.0000 | 0.0000 | same |
| full | hit_at_5 | 30/30 | 30/30 | 0.0000 | same |
| full | hit_at_10 | 30/30 | 30/30 | 0.0000 | same |
| full | mrr | 0.9278 | 0.9278 | 0.0000 | same |
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

- improved: 0
- regressed: 0
- same: 30
- improved queries: none
- regressed queries: none

### full

- improved: 0
- regressed: 0
- same: 30
- improved queries: none
- regressed queries: none

## Iteration Verdict

- boundary pass: True
- primary MRR delta: 0.0000
- full noisy MRR delta: 0.0000
- query-level regressions: 0

Verdict: keep v1.1 as the next sandbox candidate.
