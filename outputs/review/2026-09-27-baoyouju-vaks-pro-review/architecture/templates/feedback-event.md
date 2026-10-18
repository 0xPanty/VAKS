---
record_kind: feedback_event
status: logged
knowledge_status: candidate
processing_tier: light
lifecycle_state: feedback_cached
retrieval_policy:
  policy_kind: project_context_only
  pack_allowed: review_input_only
  action_basis_allowed: false
  warning_code: feedback_not_truth
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
forbidden_truth_mutation_fields_absent: true
reviewed_note_mutation_allowed: false
source_reliability_mutation_allowed: false
event_kind:
target_ref:
project_ref:
observed_in_context:
event_time:
review_pressure_effect: none
query_run_ref:
note:
---

# Feedback Event

## Boundary

This event is append-only.

It can affect activation, routing, scope hints, and review pressure in the
recorded context. It cannot directly change truth confidence, reviewed notes,
decisions, source cards, or candidate notes.

## Allowed Event Kinds

```text
useful_orientation
misleading_orientation
scope_mismatch
anchor_broken_or_source_changed
```

## Scope

```text
project_ref:
observed_in_context:
target_ref:
```

Do not generalize this event outside its recorded project/context without later
review.

## Immediate Effect

```text
retrieval_heuristic_change:
review_pressure_effect:
temporary_project_warning:
```

## Review Escalation

Escalate only if repeated scoped negative feedback appears, action-facing use
was misled, an anchor/source needed for action is broken, or a project boundary /
decision / reviewed relation may need to change.
