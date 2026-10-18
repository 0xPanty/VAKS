---
type: sandbox_issue_recommendation_report
status: completed
created_at: 2026-06-05
truth_boundary: sandbox report only; not reviewed knowledge; not action basis
---

# Issues And Recommendations

## P1: Do Not Mainline The Object Model

Evidence:

```text
mainline copy insertion added 146 lines
average mainline readiness: 0.71 / 3
average leakage risk: 2.43 / 3
```

Recommendation:

```text
Keep only the already-landed generic sidecar boundary principle.
```

## P1: Keep Warrant Out Of The Overlay

Issue:

If the overlay stores warrant, residual risk, review verdict, or consequences,
it becomes a permanent mini-assurance-case layer.

Recommendation:

```text
Overlay routes.
v0.2.13 warrants.
```

## P2: Rename Retrieval Priority

Issue:

`retrieval priority` can read like importance, confidence, or authority.

Recommendation:

```text
Use default retrieval precedence / default search inclusion order / default read order.
```

## P2: Keep Candidate Snapshot Wording Weak

Issue:

`landed_snapshot` and `boundary_snapshot` are too easy to read as best practice
or universal ban.

Recommendation:

```text
candidate experience snapshot
candidate boundary snapshot
```

Require significance, validity, applicability, scope limits, and evidence refs.

## P2: Keep Lifecycle As Owner-Confirmed Operations

Issue:

Archive, delete+tombstone, carry-forward, and supersede are useful but become
heavy if modeled as formal status states.

Recommendation:

```text
Use them in closeout manifests.
Do not make them schema enums.
```

## P3: Reduce Minimal Fields

Recommended sandbox minimum:

```text
kp_ref
stance
borrow_scope
updated_at
```

Useful optional fields:

```text
non_borrow_scope
target_hint
outcome_ref
```

Drop or derive:

```text
review_origin
gate_hint as default field
anchor_health as manual field
```

## P3: More Non-Author Testing Needed

The simulated non-author check scored:

```text
19 / 24
```

That is usable, but not enough for mainline confidence.

Next test:

```text
Give 6-8 entries to another model/window without the design backstory.
Ask it to classify overlay vs decision vs action basis.
```
