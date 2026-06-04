# VAKS Audit Shell v1 Queue Cockpit Prototype

Date: 2026-06-04

This is a sandbox prototype. It does not change `SCHEMA.md`, the truth layer, or main-vault formal operation rules.

## Plain Purpose

This package turns audit shell v1 from card-first thinking into a queue-first backstage operator cockpit.

The goal is simple:

```text
show what needs attention now
keep ordinary material light
defer low-urgency review
open deep packets only when action/risk requires it
```

## Files

- `COCKPIT_QUEUE_ROWS.csv`: all 282 pressure-test rows remapped into cockpit lanes.
- `QUEUE_COCKPIT_SUMMARY.json`: lane and anchor-strength counts.
- `QUEUE_FIRST_COCKPIT_PROTOTYPE.md`: the cockpit design.
- `OPERATOR_TRIAGE_PILOT_SAMPLE_80.csv`: stratified sample for operator double-review.
- `OPERATOR_TRIAGE_PILOT_PROTOCOL.md`: how to run the 60-80 row operator pilot.
- `SEMANTIC_CLICKBACK_PILOT_SAMPLE_60.csv`: sample for click-back testing.
- `SEMANTIC_CLICKBACK_PROTOCOL.md`: click-back metrics and pass/fail rules.
- `SOURCE_FAMILY_INDEPENDENCE_TRAP_SAMPLE.csv`: source count / lineage trap sample.
- `SOURCE_FAMILY_INDEPENDENCE_TRAP_PROTOCOL.md`: independence-trap test protocol.
- `PRO_REVIEW_INTEGRATION.md`: how Pro's feedback changed the route.

## Current Prototype Counts

```text
total rows: 282
blocking_now: 11
regressed_reopen: 2
review_now: 30
deferred_review_unless_promoted: 109
ordinary_light: 113
folded_history: 17
```

Main unresolved queue now starts with:

```text
blocking_now + regressed_reopen + review_now = 43
```

That is the main design change: the shell keeps strict risk control without forcing all 152 thick-path items into the first screen.

