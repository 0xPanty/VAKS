---
record_kind: sandbox_p0_query_level_replay_check
status: pass
project_id: VAKS
created_at: 2026-06-11
truth_boundary: query_replay_not_mainline_decision
action_basis_allowed: false
---

# Phase B P0 Query-Level Replay Check

## Result

```text
p0 query replay check status: pass
error count: 0
replay rows: 7200
query metric rows: 720
summary rows: 32
```

## Boundary

```text
Adds query-level replay and metric definitions.
Does not run original Yuxi runtime.
Does not create a fresh blind holdout.
Does not approve C-lite, writeback, action basis, or runtime adoption.
```

## Errors

- none
