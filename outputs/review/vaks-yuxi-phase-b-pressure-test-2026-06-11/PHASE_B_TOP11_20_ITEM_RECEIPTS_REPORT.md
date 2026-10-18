---
record_kind: sandbox_top11_20_item_receipts_report
status: candidate
project_id: VAKS
created_at: 2026-06-11
truth_boundary: item_receipts_are_replay_evidence_not_runtime_validation
action_basis_allowed: false
---

# Phase B Top11-20 Item Receipts Report

## What This Adds

```text
item-level receipts for ranks 11-20
covers the existing P0 main and holdout_used query sets
keeps top10 governance window unchanged
fills the visibility gap for ranks 11-20 in a later local rerun, but does not yet prove exact-run equivalence with the earlier P0 query metrics
```

## Counts

```text
receipt rows: 7200
query-mode-corpus rows summarized: 720
queries with first_hit_rank 11-20: 33
missing first-hit receipts: 0
```

## Boundary

```text
This is replay/audit evidence for local proxy runs.
It does not expand the governance window beyond top10.
It does not validate original Yuxi runtime, answer-loop behavior, C-lite, or writeback.
```

## Artifacts

```text
results/phase_b_top11_20_item_receipts.csv
results/phase_b_top11_20_item_receipts_summary.csv
results/phase_b_top11_20_item_receipts_summary.json
```
