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
| primary | hit_at_5 | 30/30 | 30/30 | 0.0000 | same |
| primary | hit_at_10 | 30/30 | 30/30 | 0.0000 | same |
| primary | mrr | 0.9233 | 1.0000 | 0.0767 | improved |
| primary | action_leakage_rate | 0.0000 | 0.0000 | 0.0000 | same |
| primary | forbidden_top1_rate | 0.0000 | 0.0000 | 0.0000 | same |
| primary | cross_bucket_violation_rate | 0.0000 | 0.0000 | 0.0000 | same |
| primary | warning_coverage_risk | 1.0000 | 1.0000 | 0.0000 | same |
| primary | clickback_coverage | 1.0000 | 1.0000 | 0.0000 | same |
| primary | hash_coverage | 1.0000 | 1.0000 | 0.0000 | same |
| primary | adapter_coverage | 1.0000 | 1.0000 | 0.0000 | same |
| primary | receipt_coverage | 1.0000 | 1.0000 | 0.0000 | same |
| primary | stale_detection_rate | 1.0000 | 1.0000 | 0.0000 | same |
| full | hit_at_5 | 30/30 | 30/30 | 0.0000 | same |
| full | hit_at_10 | 30/30 | 30/30 | 0.0000 | same |
| full | mrr | 0.8528 | 1.0000 | 0.1472 | improved |
| full | action_leakage_rate | 0.0000 | 0.0000 | 0.0000 | same |
| full | forbidden_top1_rate | 0.0000 | 0.0000 | 0.0000 | same |
| full | cross_bucket_violation_rate | 0.0000 | 0.0000 | 0.0000 | same |
| full | warning_coverage_risk | 1.0000 | 1.0000 | 0.0000 | same |
| full | clickback_coverage | 1.0000 | 1.0000 | 0.0000 | same |
| full | hash_coverage | 1.0000 | 1.0000 | 0.0000 | same |
| full | adapter_coverage | 1.0000 | 1.0000 | 0.0000 | same |
| full | receipt_coverage | 1.0000 | 1.0000 | 0.0000 | same |
| full | stale_detection_rate | 1.0000 | 1.0000 | 0.0000 | same |

## Query-Level MRR Movement

### primary

- improved: 4
- regressed: 0
- same: 26
- improved queries: q13_eval_not_readiness (+0.8000), q23_eval_greenlight (+0.5000), q26_source_changed (+0.5000), q29_noisy_old_sandbox (+0.5000)
- regressed queries: none

### full

- improved: 7
- regressed: 0
- same: 23
- improved queries: q01_core_score_boundary (+0.6667), q06_agent_memory (+0.6667), q07_source_hash (+0.6667), q12_yuxi_not_core (+0.7500), q23_eval_greenlight (+0.5000), q26_source_changed (+0.5000), q29_noisy_old_sandbox (+0.6667)
- regressed queries: none

## Iteration Verdict

- boundary pass: True
- primary MRR delta: 0.0767
- full noisy MRR delta: 0.1472

Verdict: keep v1 as the next sandbox candidate.
