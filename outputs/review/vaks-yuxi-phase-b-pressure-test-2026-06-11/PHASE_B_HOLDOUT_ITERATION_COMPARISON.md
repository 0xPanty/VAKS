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
| primary | hit_at_5 | 9/15 | 10/15 | 1.0000 | improved |
| primary | hit_at_10 | 10/15 | 12/15 | 2.0000 | improved |
| primary | mrr | 0.4724 | 0.6088 | 0.1364 | improved |
| primary | action_leakage_rate | 0.0000 | 0.0000 | 0.0000 | same |
| primary | forbidden_top1_rate | 0.0000 | 0.0000 | 0.0000 | same |
| primary | cross_bucket_violation_rate | 0.0000 | 0.0000 | 0.0000 | same |
| primary | warning_coverage_risk | 1.0000 | 1.0000 | 0.0000 | same |
| primary | clickback_coverage | 1.0000 | 1.0000 | 0.0000 | same |
| primary | hash_coverage | 1.0000 | 1.0000 | 0.0000 | same |
| primary | adapter_coverage | 1.0000 | 1.0000 | 0.0000 | same |
| primary | receipt_coverage | 1.0000 | 1.0000 | 0.0000 | same |
| primary | stale_detection_rate | 0.0000 | 0.0000 | 0.0000 | same |
| full | hit_at_5 | 10/15 | 11/15 | 1.0000 | improved |
| full | hit_at_10 | 12/15 | 12/15 | 0.0000 | same |
| full | mrr | 0.4165 | 0.5924 | 0.1759 | improved |
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

- improved: 7
- regressed: 0
- same: 8
- improved queries: h01_similarity_is_not_proof (+0.5000), h02_positive_feedback_promotion (+0.5000), h05_stale_index_warning (+0.0139), h06_agent_memory_write_path (+0.5000), h07_yuxi_database_authority (+0.2500), h08_eval_score_greenlight (+0.1786), h10_old_sandbox_benchmark_truth (+0.1042)
- regressed queries: none

### full

- improved: 6
- regressed: 1
- same: 8
- improved queries: h01_similarity_is_not_proof (+0.7500), h02_positive_feedback_promotion (+0.5000), h05_stale_index_warning (+0.1389), h06_agent_memory_write_path (+0.7500), h09_raw_source_final_support (+0.5000), h14_activation_not_belief (+0.1667)
- regressed queries: h10_old_sandbox_benchmark_truth (-0.1667)

## Iteration Verdict

- boundary pass: True
- primary MRR delta: 0.1364
- full noisy MRR delta: 0.1759

Verdict: keep v1 as the next sandbox candidate.
