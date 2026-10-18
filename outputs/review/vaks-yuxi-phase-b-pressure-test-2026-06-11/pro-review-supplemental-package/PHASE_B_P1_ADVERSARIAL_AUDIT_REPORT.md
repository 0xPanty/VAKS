---
record_kind: sandbox_p1_adversarial_audit_report
status: pass
project_id: VAKS
created_at: 2026-06-11
truth_boundary: fresh_adversarial_not_external_blind
action_basis_allowed: false
---

# Phase B P1 Fresh Adversarial Audit Report

## Scope

```text
query_count: 30
query_set: fresh adversarial, not external blind
real original Yuxi runtime: not run
decision: sandbox evidence only; no C-lite or writeback approval
```

## Summary

| Corpus | Mode | hit@5 | MRR | action leakage | forbidden top1 | cross-bucket |
|---|---|---:|---:|---:|---:|---:|
| primary | baseline_file_lexical | 15/30 | 0.3861 | 1.0000 | 0.5517 | 0.5517 |
| primary | vaks_only_lexical_bucket | 26/30 | 0.7537 | 0.0000 | 0.0000 | 0.0000 |
| primary | vaks_b_bucket_local | 27/30 | 0.7174 | 0.0000 | 0.0000 | 0.0000 |
| primary | vaks_b_adapter_skeleton | 28/30 | 0.8556 | 0.0000 | 0.0000 | 0.0000 |
| primary | yuxi_native_profile | 28/30 | 0.8167 | 1.0000 | 0.5517 | 0.5517 |
| full | baseline_file_lexical | 17/30 | 0.4933 | 1.0000 | 0.7586 | 0.7586 |
| full | vaks_only_lexical_bucket | 26/30 | 0.7211 | 0.0000 | 0.0000 | 0.0000 |
| full | vaks_b_bucket_local | 27/30 | 0.7778 | 0.0000 | 0.0000 | 0.0000 |
| full | vaks_b_adapter_skeleton | 28/30 | 0.8611 | 0.0000 | 0.0000 | 0.0000 |
| full | yuxi_native_profile | 27/30 | 0.8028 | 1.0000 | 0.7931 | 0.7931 |

## Criteria

| Criterion | Result | Observed |
|---|---|---|
| primary: skeleton_leakage_zero | pass | 0.0000 |
| primary: skeleton_hit_not_below_baseline | pass | 28/30 vs baseline 15/30 |
| primary: skeleton_mrr_directionally_above_yuxi_proxy | pass | 0.8556 vs yuxi_proxy 0.8167 |
| primary: skeleton_hit_above_clean_vaks_only | pass | 28/30 vs clean 26/30 |
| primary: yuxi_proxy_leakage_nonzero | pass | 1.0000 |
| full: skeleton_leakage_zero | pass | 0.0000 |
| full: skeleton_hit_not_below_baseline | pass | 28/30 vs baseline 17/30 |
| full: skeleton_mrr_directionally_above_yuxi_proxy | pass | 0.8611 vs yuxi_proxy 0.8028 |
| full: skeleton_hit_above_clean_vaks_only | pass | 28/30 vs clean 26/30 |
| full: yuxi_proxy_leakage_nonzero | pass | 1.0000 |

## Boundary

```text
This strengthens local pressure evidence.
MRR-above-yuxi-proxy is a local directional criterion, not proof of decisive retrieval superiority.
Action leakage is a ranking/governance proxy, not an answer-level safety verdict.
It is not a substitute for an external blind set or original Yuxi runtime rerun.
```
