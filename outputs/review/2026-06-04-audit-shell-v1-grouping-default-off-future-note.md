---
type: future-note
status: parked
created: 2026-06-04
project: verified-action-knowledge-system
subject: audit-shell-v1-grouping-default-off
scope: future-operator-cockpit-enhancement
---

# Audit Shell v1 Grouping Future Note

## Plain Note

Grouping / merging can be useful later, but it is not needed for the current Audit Shell v1 formal operator-only graduation.

Current status:

```text
grouping default-off
not a blocker
not part of current formal graduation
future enhancement only
```

## Why It May Help

Grouping can reduce operator load when many rows share the same low-risk handling pattern, such as:

```text
old handoff history
source record only
summary / QA not truth
transcript needs key-entity check
diagnostic output not authority
```

It can shorten the first screen and make repeated issues easier to scan.

## Why It Stays Off For Now

Grouping can hide a dangerous row inside a harmless-looking group.

Breakout must happen before grouping whenever a row has:

```text
blocking
regressed
action-basis use
rule / convention basis use
explicit challenge
conflict
missing anchor
weak evidence anchor
source-family independence risk
different landing strength
different risk reason
```

## Future Pilot Needed

Before grouping can be enabled by default, run a separate `grouping default-off pilot`.

Minimum tests:

1. Mixed-group trap: a high-risk row inside many low-risk rows must be split out.
2. Breakout trigger test: every trigger above must force per-row handling.
3. Same-class batch test: truly identical low-risk rows can be grouped without changing their state.
4. Click-back test: group view must still jump back to every original row.
5. Count-bait test: group size must not become support strength, truth confidence, or action readiness.

## Boundary

Grouping is only a queue compressor.

It cannot change:

```text
state
lane
truth confidence
evidence support
action readiness
promotion receipt requirement
```

