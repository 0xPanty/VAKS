---
record_type: lightweight-path-trial-rules
status: draft
created: 2026-06-01
scope: sandbox-only
schema_change: false
main_vault_write: false
---

# Lightweight Path Variant Rules

## Purpose

Test Opus's suggestion:

```text
Keep the main architecture. Do not change SCHEMA.
For small claim / support-refine collision / scope-fit feedback, use a lighter path.
Big decisions still use the full gate.
```

## Rule 1: Small Claim Mini Review

Use when:

```text
one narrow point
one or a few source spans
not action-ready
not decision basis
not contested
not high-risk
```

Minimum fields:

```yaml
point:
source_anchor:
support_check:
scope_limit:
risk_note:
promotion_result:
```

Do not require:

```text
full Evidence Packet
full omission_check
strongest_rebuttal
numeric confidence beyond low/medium/high wording
```

Escalate to full gate if:

```text
used for action basis
strong reviewed relation
high-impact claim
explicit contradiction
```

## Rule 2: Support / Refine Collision Summary

Use when multiple sources converge or refine the same point but do not contradict each other.

Minimum fields:

```yaml
cluster_point:
sources:
  - source_id
    contribution: supports | refines | cautions
    anchor:
shared_scope:
remaining_gap:
resolution:
```

Do not force one `item_type` if the issue is both synthesis and missing evidence.

Escalate to full Point Collision / Evidence Packet if:

```text
sources conflict
independence is needed for confidence
claim becomes action basis
reviewer explicitly challenges it
```

## Rule 3: Scope-Fit Feedback Stub

Use for small feedback that changes activation / framing only.

Minimum fields:

```yaml
feedback:
target:
problem:
next_time_activate:
next_time_avoid:
truth_boundary:
```

Do not require:

```text
signal_strength
signal_confidence
numeric activation_delta
full decision_outcome
```

Escalate to full feedback-event if:

```text
explicit correction
action outcome
decision outcome
contradiction missed
high-severity wrong answer
```

## Trial Boundary

These are scratch rules only. They do not change main-vault templates or schema.

