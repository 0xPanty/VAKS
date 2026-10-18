---
record_kind: sandbox_contract_notes
slice_id: 2026-06-15-p0-04-support-boundary-validator-sandbox
status: ready_for_recheck
truth_boundary: sandbox_notes_only
---

# Contract Notes

## Boundary

This validator is a negative gate. It can block invalid support claims. It
cannot certify a support claim as true, sufficient, reviewed, or action-ready.

## Why It Exists

P0-01 showed retrieval receipts can keep selected material from becoming
authority. P0-04 hardens the next boundary: a retrieved or selected item must
not become evidence support unless it has the right source-span-to-target shape.

## Not Enough For Support

These are useful for orientation or review pressure but not support by
themselves:

```text
candidate distillation
project overlay
source annotation
URL-only provenance
retrieval score
graph rank
feedback
source summary without inspected anchor
claim note repeating itself
legacy raw metadata
background context
```

## Product Reuse

Future slices can reuse this package as:

- a fixture corpus for P1 receipt validator pilot;
- input for the action-boundary failure matrix;
- a design reference for a future mainline support-boundary validator.

Future slices must not reuse it as:

- evidence support;
- reviewer approval;
- reviewed knowledge;
- action basis;
- mainline validator implementation without separate approval.
