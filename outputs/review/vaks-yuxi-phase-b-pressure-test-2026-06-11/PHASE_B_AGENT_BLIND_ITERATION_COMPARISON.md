---
record_kind: sandbox_iteration_comparison
status: candidate
project_id: VAKS
created_at: 2026-06-11
truth_boundary: diagnostic_not_mainline_decision
action_basis_allowed: false
---

# Phase B Iteration Comparison

## Compared Versions

- `vaks_b_bucket_local`: v0 locked baseline from the previous passing sandbox version.
- `vaks_b_adapter_v1`: v1 adds anchor/path/exact-phrase aware ordering inside VAKS authority buckets.

## Summary Delta

| Corpus | Metric | v0 | v1 | Delta | Direction |
|---|---|---:|---:|---:|---|
| primary | hit_at_5 | 28/30 | 30/30 | 2.0000 | improved |
| primary | hit_at_10 | 30/30 | 30/30 | 0.0000 | same |
| primary | mrr | 0.8478 | 0.9250 | 0.0772 | improved |
| primary | action_leakage_rate | 0.0000 | 0.0000 | 0.0000 | same |
| primary | forbidden_top1_rate | 0.0000 | 0.0000 | 0.0000 | same |
| primary | cross_bucket_violation_rate | 0.0000 | 0.0000 | 0.0000 | same |
| primary | warning_coverage_risk | 1.0000 | 1.0000 | 0.0000 | same |
| primary | clickback_coverage | 1.0000 | 1.0000 | 0.0000 | same |
| primary | hash_coverage | 1.0000 | 1.0000 | 0.0000 | same |
| primary | adapter_coverage | 1.0000 | 1.0000 | 0.0000 | same |
| primary | receipt_coverage | 1.0000 | 1.0000 | 0.0000 | same |
| primary | stale_detection_rate | 0.0000 | 0.0000 | 0.0000 | same |
| full | hit_at_5 | 28/30 | 30/30 | 2.0000 | improved |
| full | hit_at_10 | 30/30 | 30/30 | 0.0000 | same |
| full | mrr | 0.7940 | 0.9278 | 0.1338 | improved |
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

- improved: 6
- regressed: 1
- same: 23
- improved queries: AQ-010 (+0.5000), AQ-016 (+0.1250), AQ-018 (+0.3571), AQ-020 (+0.6667), AQ-023 (+0.5000), AQ-024 (+0.6667)
- regressed queries: AQ-022 (-0.5000)

### full

- improved: 9
- regressed: 0
- same: 21
- improved queries: AQ-001 (+0.5000), AQ-008 (+0.5000), AQ-014 (+0.5000), AQ-016 (+0.1905), AQ-018 (+0.3571), AQ-020 (+0.5000), AQ-023 (+0.5000), AQ-024 (+0.1667), AQ-026 (+0.8000)
- regressed queries: none

## Iteration Verdict

- boundary pass: True
- primary MRR delta: 0.0772
- full noisy MRR delta: 0.1338

Verdict: keep v1 as the next sandbox candidate.
