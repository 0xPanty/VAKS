---
type: sandbox_feedback_protocol
status: candidate_only
created_at: 2026-06-06
scope: feedback cache append-only protocol
truth_boundary: candidate feedback protocol only
---

# 04 Feedback Cache Protocol

## Core Rule

Feedback is an append-only event stream.

It can affect:

```text
activation
routing
scope hints
review_pressure
```

It cannot affect:

```text
truth confidence
reviewed note content
decision status
source reliability
```

## Event Kinds

| event_kind | Action | Truth effect |
|---|---|---|
| `useful_orientation` | locally promote activation / routing | none |
| `misleading_orientation` | locally downrank + maybe review_due | none |
| `scope_mismatch` | add scope/project reminder | none |
| `anchor_broken_or_source_changed` | set blocked or review_due | none |

## Required Scope

Every feedback event must include:

```yaml
project_ref:
observed_in_context:
target_ref:
event_time:
```

If project scope is unknown:

```text
do not globalize it
keep it as local review input
```

## Escalation

```text
single local feedback:
  activation/routing hint only

repeated negative feedback:
  review_due

action-facing misleading use:
  heavy_review_open

heavy review passed:
  possible reviewed boundary note / superseding decision / reviewed relation scope update
```

## Forbidden Effects

```text
truth_confidence_delta
auto_mutate_reviewed_note
universal ban from local feedback
automatic decision supersede
```
