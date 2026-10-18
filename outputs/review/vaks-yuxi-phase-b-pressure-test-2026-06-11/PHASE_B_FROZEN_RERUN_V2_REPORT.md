---
record_kind: sandbox_frozen_rerun_v2_report
status: candidate
project_id: VAKS
created_at: 2026-06-11
truth_boundary: single_run_replay_bundle_not_runtime_validation
action_basis_allowed: false
---

# Phase B Frozen Rerun V2 Report

## What This Adds

```text
run_id: phase_b_frozen_rerun_v2_20260611T142435Z
single invocation over frozen corpus/query/script hashes
top20 item-level export
top1-10 replay split
top11-20 receipt split
query-level metrics
summary
corpus and query manifests
```

## Counts

```text
corpus file records: 4793
query records: 45
top20 item rows: 14400
query metric rows: 720
summary rows: 32
```

## Boundary

```text
Frozen Rerun v2 should be treated as the authoritative exact-run local P0 bundle going forward.
Older P0 summaries remain historical artifacts and should not be mixed with v2 as headline evidence.
It is still expected_terms-based proxy retrieval evidence, not human relevance judgment.
It does not validate original Yuxi runtime.
It does not approve C-lite, writeback, action basis, or core-doc strong conclusions.
```
