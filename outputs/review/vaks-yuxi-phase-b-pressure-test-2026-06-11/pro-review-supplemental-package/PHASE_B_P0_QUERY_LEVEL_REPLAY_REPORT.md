---
record_kind: sandbox_p0_query_level_replay_report
status: candidate
project_id: VAKS
created_at: 2026-06-11
truth_boundary: query_replay_not_mainline_decision
action_basis_allowed: false
---

# Phase B P0 Query-Level Replay Report

## What This Adds

```text
query-level top10 replay plus top20 paired query outcomes for existing 45 queries
metric dictionary with denominators
clean VAKS-only lexical + authority-bucket control
replay rows that can be independently recomputed
```

## Scope

```text
replay rows: 7200
query sets: main 30, holdout_used 15
corpora: primary, full
metric_result_limit: top20
replay_result_limit: top10
governance_window: top10
real original Yuxi runtime: not run
new blind adversarial set: not included in this P0 replay
```

## Clean Control Snapshot

| Test Set | Corpus | Mode | hit@5 | MRR | action leakage | forbidden top1 | cross-bucket |
|---|---|---|---:|---:|---:|---:|---:|
| main | primary | vaks_only_lexical_bucket | 26/30 | 0.8187 | 0.0000 | 0.0000 | 0.0000 |
| main | primary | vaks_b_bucket_local | 30/30 | 0.9233 | 0.0000 | 0.0000 | 0.0000 |
| main | primary | vaks_b_adapter_skeleton | 30/30 | 1.0000 | 0.0000 | 0.0000 | 0.0000 |
| main | primary | yuxi_native_profile | 30/30 | 0.9511 | 1.0000 | 0.5000 | 0.5000 |
| main | full | vaks_only_lexical_bucket | 25/30 | 0.7894 | 0.0000 | 0.0000 | 0.0000 |
| main | full | vaks_b_bucket_local | 30/30 | 0.8528 | 0.0000 | 0.0000 | 0.0000 |
| main | full | vaks_b_adapter_skeleton | 30/30 | 1.0000 | 0.0000 | 0.0000 | 0.0000 |
| main | full | yuxi_native_profile | 29/30 | 0.9041 | 1.0000 | 0.7500 | 0.7500 |
| holdout_used | primary | vaks_only_lexical_bucket | 10/15 | 0.5577 | 0.0000 | 0.0000 | 0.0000 |
| holdout_used | primary | vaks_b_bucket_local | 9/15 | 0.4724 | 0.0000 | 0.0000 | 0.0000 |
| holdout_used | primary | vaks_b_adapter_skeleton | 12/15 | 0.7811 | 0.0000 | 0.0000 | 0.0000 |
| holdout_used | primary | yuxi_native_profile | 10/15 | 0.5808 | 1.0000 | 0.6667 | 0.6667 |
| holdout_used | full | vaks_only_lexical_bucket | 11/15 | 0.5504 | 0.0000 | 0.0000 | 0.0000 |
| holdout_used | full | vaks_b_bucket_local | 10/15 | 0.4165 | 0.0000 | 0.0000 | 0.0000 |
| holdout_used | full | vaks_b_adapter_skeleton | 13/15 | 0.7591 | 0.0000 | 0.0000 | 0.0000 |
| holdout_used | full | yuxi_native_profile | 8/15 | 0.5137 | 1.0000 | 0.8333 | 0.8333 |

## Evidence Boundary

```text
This report fixes auditability gaps for existing local queries.
It does not answer whether original Yuxi runtime can reproduce the effect.
It does not create a fresh blind holdout.
It corrects the P0 stale_detection_rate denominator to include holdout_stale.
It does not approve C-lite, writeback, action basis, or runtime adoption.
```
