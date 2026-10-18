---
record_kind: sandbox_top11_20_item_receipts_check
status: pass
project_id: VAKS
created_at: 2026-06-11
truth_boundary: receipt_check_not_runtime_validation
action_basis_allowed: false
---

# Phase B Top11-20 Item Receipts Check

## Result

```text
status: pass
error count: 0
receipt rows: 7200
query-mode-corpus groups: 720
missing first-hit receipts: 0
```

## Boundary

```text
This verifies rank 11-20 local replay receipts.
It keeps top10 governance metrics unchanged.
It does not validate original Yuxi runtime, answer-loop behavior, C-lite, or writeback.
```

## Errors

- none
