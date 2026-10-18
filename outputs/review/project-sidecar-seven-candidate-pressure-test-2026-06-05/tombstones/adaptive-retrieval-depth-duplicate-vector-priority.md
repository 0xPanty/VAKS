---
type: tombstone
status: sandbox_trial
created_at: 2026-06-05
project: MISA
kp_ref: outputs/review/candidate_pattern_bank/adaptive-retrieval-depth.md
deleted_lens_ref: outputs/review/project-sidecar-seven-candidate-pressure-test-2026-06-05/misa_overlay/MISA.md#entry-adaptive-retrieval-depth-duplicate-vector-priority
truth_boundary: tombstone audit only; never semantic retrieval; not reviewed knowledge; not action basis
---

# Tombstone: adaptive-retrieval-depth duplicate vector priority

## Delete Reason

The entry is duplicate, unanchored, and misleading:

```text
borrow_scope: Tune vector priority in Misa based on attention queue scores.
target_hint: vector priority everywhere
```

It collapses adaptive retrieval into priority tuning and risks treating
attention scores as authority/confidence.

## Downstream Refs

```text
none_confirmed
```

## Audit Rule

This tombstone is for de-dup and audit only. It must never enter semantic
retrieval and must not be used as evidence that adaptive retrieval is rejected.
