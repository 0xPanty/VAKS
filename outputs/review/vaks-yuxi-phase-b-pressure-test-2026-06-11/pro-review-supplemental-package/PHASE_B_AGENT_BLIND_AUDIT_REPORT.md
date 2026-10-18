---
record_kind: sandbox_agent_blind_audit_report
status: pass
project_id: VAKS
created_at: 2026-06-11
truth_boundary: agent_blind_not_original_yuxi_runtime
action_basis_allowed: false
---

# Phase B Agent-Blind Audit Report

## Scope

```text
query_count: 30
query_author: independent sub-agent without parent context
query_author_restriction: no existing Phase B query/results/reports
real original Yuxi runtime: not run
decision: sandbox evidence only; no C-lite or writeback approval
```

## Summary

| Corpus | Mode | hit@5 | MRR | action leakage | forbidden top1 | cross-bucket |
|---|---|---:|---:|---:|---:|---:|
| primary | baseline_file_lexical | 20/30 | 0.4311 | 1.0000 | 0.6364 | 0.6364 |
| primary | vaks_only_lexical_bucket | 23/30 | 0.6245 | 0.0000 | 0.0000 | 0.0000 |
| primary | vaks_b_bucket_local | 28/30 | 0.8478 | 0.0000 | 0.0000 | 0.0000 |
| primary | vaks_b_adapter_skeleton | 30/30 | 0.9250 | 0.0000 | 0.0000 | 0.0000 |
| primary | yuxi_native_profile | 27/30 | 0.8339 | 1.0000 | 0.5000 | 0.5000 |
| full | baseline_file_lexical | 16/30 | 0.4368 | 1.0000 | 0.6818 | 0.6818 |
| full | vaks_only_lexical_bucket | 21/30 | 0.5698 | 0.0000 | 0.0000 | 0.0000 |
| full | vaks_b_bucket_local | 28/30 | 0.7940 | 0.0000 | 0.0000 | 0.0000 |
| full | vaks_b_adapter_skeleton | 30/30 | 0.9278 | 0.0000 | 0.0000 | 0.0000 |
| full | yuxi_native_profile | 26/30 | 0.8229 | 1.0000 | 0.6818 | 0.6818 |

## Criteria

| Criterion | Result | Observed |
|---|---|---|
| primary: skeleton_leakage_zero | pass | 0.0000 |
| primary: skeleton_hit_not_below_baseline | pass | 30/30 vs baseline 20/30 |
| primary: skeleton_mrr_directionally_above_yuxi_proxy | pass | 0.9250 vs yuxi_proxy 0.8339 |
| primary: skeleton_hit_above_clean_vaks_only | pass | 30/30 vs clean 23/30 |
| primary: yuxi_proxy_leakage_nonzero | pass | 1.0000 |
| full: skeleton_leakage_zero | pass | 0.0000 |
| full: skeleton_hit_not_below_baseline | pass | 30/30 vs baseline 16/30 |
| full: skeleton_mrr_directionally_above_yuxi_proxy | pass | 0.9278 vs yuxi_proxy 0.8229 |
| full: skeleton_hit_above_clean_vaks_only | pass | 30/30 vs clean 21/30 |
| full: yuxi_proxy_leakage_nonzero | pass | 1.0000 |

## Boundary

```text
This adds internal no-parent-context stress evidence, but remains an internal model-family-generated set rather than an external blind evaluation.
MRR-above-yuxi-proxy is a local directional criterion, not proof of decisive retrieval superiority.
Action leakage is a ranking/governance proxy, not an answer-level safety verdict.
It is not a substitute for original Yuxi runtime rerun.
It is still local evaluation, not mainline adoption evidence by itself.
```
