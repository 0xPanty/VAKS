# Operator Triage Pilot Protocol

## Purpose

Test whether the queue-first cockpit helps an operator make the correct first action faster and more reliably.

This is not a preference test and not a visual UI test.

## Sample

Use:

```text
OPERATOR_TRIAGE_PILOT_SAMPLE_80.csv
```

Current sample size:

```text
80 rows
```

It is stratified across:

- ordinary light,
- review now,
- deferred review,
- blocking,
- resolved/folded,
- regressed,
- authority-bait adversarial rows.

## Reviewers

Run with two operators if possible:

```text
Codex operator
Pro/reviewer operator
```

Each reviewer should only see the cockpit row first, not the full source file.

## What To Record

For each row:

```text
time_to_first_action_seconds
chosen_action
should_open_deep_packet
actionability_judgment
anchor_strength_understood
authority_boundary_understood
wrong_actionability
serious_miss
authority_misunderstanding
notes
```

## Correct First Actions

Allowed action labels:

```text
light_save
defer_review
review_now
block_and_fix_anchor
fold_history
reopen_regressed
open_deep_packet
```

## Proposed Gates

Hard gates:

```text
serious_false_lite = 0
wrong_actionability_on_high_risk = 0
serious_miss = 0
severe_authority_misunderstanding = 0
```

Product gates:

```text
median_time_to_first_correct_triage improves 25-30% vs direct full audit
ordinary rows stay light
deferred rows do not flood main unresolved queue
```

Soft gate:

```text
minor authority misunderstanding <= 5%
```

## Interpretation

Passing this pilot means:

```text
the operator cockpit is usable enough for the next sandbox step
```

It does not mean:

```text
formal adoption
truth-layer change
schema change
```

