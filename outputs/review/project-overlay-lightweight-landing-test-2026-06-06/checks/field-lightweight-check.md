---
type: sandbox_check
status: completed
created_at: 2026-06-06
truth_boundary: check report only
---

# Field Lightweight Check

## Command

```powershell
python inline parser over project_overlays/*.md
```

## Results

```text
project_overlays/MISA.md: entries=8
  kp_ref=8
  stance=8
  borrow_scope=8
  updated_at=8

project_overlays/VAKS.md: entries=6
  kp_ref=6
  stance=6
  borrow_scope=6
  updated_at=6
```

## Interpretation

Every live overlay entry has the four required fields.

No live entry needs a YAML block, per-entry project field, `reason_1liner`,
manual target health field, review origin field, or gate field.

## Field Shape

Allowed live fields:

```text
kp_ref
stance
borrow_scope
updated_at
non_borrow_scope
target_hint
outcome_ref
```

Actual live fields used:

```text
kp_ref
stance
borrow_scope
updated_at
non_borrow_scope
target_hint
```

`outcome_ref` is not used in the active sample because outcomes are held in
closeout and candidate notes.

