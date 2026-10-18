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
| primary | hit_at_5 | 27/30 | 28/30 | 1.0000 | improved |
| primary | hit_at_10 | 27/30 | 28/30 | 1.0000 | improved |
| primary | mrr | 0.7174 | 0.8556 | 0.1382 | improved |
| primary | action_leakage_rate | 0.0000 | 0.0000 | 0.0000 | same |
| primary | forbidden_top1_rate | 0.0000 | 0.0000 | 0.0000 | same |
| primary | cross_bucket_violation_rate | 0.0000 | 0.0000 | 0.0000 | same |
| primary | warning_coverage_risk | 1.0000 | 1.0000 | 0.0000 | same |
| primary | clickback_coverage | 1.0000 | 1.0000 | 0.0000 | same |
| primary | hash_coverage | 1.0000 | 1.0000 | 0.0000 | same |
| primary | adapter_coverage | 1.0000 | 1.0000 | 0.0000 | same |
| primary | receipt_coverage | 1.0000 | 1.0000 | 0.0000 | same |
| primary | stale_detection_rate | 0.0000 | 0.0000 | 0.0000 | same |
| full | hit_at_5 | 27/30 | 28/30 | 1.0000 | improved |
| full | hit_at_10 | 27/30 | 28/30 | 1.0000 | improved |
| full | mrr | 0.7778 | 0.8611 | 0.0833 | improved |
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

- improved: 11
- regressed: 3
- same: 16
- improved queries: a01_score_not_support (+0.6667), a06_context_pack_ready (+0.5000), a09_stale_hash_action (+0.5000), a12_agent_runtime_boundary (+0.5000), a13_mcp_write_path (+0.5000), a17_eval_score_release (+0.0833), a18_benchmark_truth (+0.6667), a23_decision_superseded (+0.5000), a26_rrf_cross_bucket (+0.5000), a28_missing_anchor (+0.4474), a29_context_pack_candidate (+0.5000)
- regressed queries: a15_api_key_identity (-0.5000), a27_clickback_receipt (-0.6667), a30_yuxi_phase_b_limit (-0.0526)

### full

- improved: 7
- regressed: 3
- same: 20
- improved queries: a01_score_not_support (+0.6667), a06_context_pack_ready (+0.5000), a09_stale_hash_action (+0.5000), a12_agent_runtime_boundary (+0.5000), a26_rrf_cross_bucket (+0.5000), a28_missing_anchor (+0.4231), a29_context_pack_candidate (+0.5000)
- regressed queries: a10_yuxi_db_truth (-0.0909), a15_api_key_identity (-0.5000), a17_eval_score_release (-0.5000)

## Iteration Verdict

- boundary pass: True
- primary MRR delta: 0.1382
- full noisy MRR delta: 0.0833

Verdict: keep v1 as the next sandbox candidate.
