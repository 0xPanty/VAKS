# VAKS Queue-First Operator Cockpit Pro Review Package

Date: 2026-06-04

## What This Package Is

This package asks Pro to review the latest VAKS audit shell v1 direction after the shift from card-first to queue-first.

The current candidate is:

```text
operator-only sandbox candidate convention
queue-first risk-tiered review cockpit
not formal adoption
not schema change
not truth-layer change
not user-facing card UI
```

## Read Order

1. `00_READ_FIRST/PRO_OPEN_REVIEW_PROMPT.md`
2. `01_CANDIDATE/2026-06-04-audit-shell-v1-pro-review-integration-queue-cockpit.md`
3. `02_PROTOTYPE/QUEUE_FIRST_COCKPIT_PROTOTYPE.md`
4. `02_PROTOTYPE/QUEUE_COCKPIT_SUMMARY.json`
5. `02_PROTOTYPE/COCKPIT_QUEUE_ROWS.csv`
6. `04_PILOTS/OPERATOR_TRIAGE_PILOT_PROTOCOL.md`
7. `04_PILOTS/SEMANTIC_CLICKBACK_PROTOCOL.md`
8. `04_PILOTS/SOURCE_FAMILY_INDEPENDENCE_TRAP_PROTOCOL.md`
9. `03_PRESSURE_TEST/PRESSURE_TEST_REPORT.md`
10. `01_CANDIDATE/2026-06-04-audit-shell-v1-candidate-operation-convention.md`

## Key Numbers

Pressure test:

```text
282 real vault files
ordinary: 113
for_review: 139
blocking: 11
regressed: 2
resolved_folded: 17
false-lite: 0
over-heavy: 0
direct full audit: 152
```

Queue-first prototype:

```text
blocking_now: 11
regressed_reopen: 2
review_now: 30
deferred_review_unless_promoted: 109
ordinary_light: 113
folded_history: 17
```

Main first-screen unresolved queue:

```text
11 + 2 + 30 = 43 rows
```

## Review Posture

Do not merely check whether the current wording is acceptable.

Please openly review, research, compare to mature systems, challenge the abstraction, and suggest better designs.

The important question is:

```text
Should VAKS continue from audit shell v1 toward a queue-first operator cockpit, and what must change before it can move beyond sandbox candidate?
```

