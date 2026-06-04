---
record_type: feedback-event
status: pending
created:
updated:
feedback_id:
created_by:
feedback_source: explicit-user | conversation-derived | system-eval | action-result | decision-outcome
query_id:
session_id:
turn_id:
parent_query_id:
derived_from_turn_id:
question:
query_intent: answer | decision | implementation | research | content | memory
query_scope:
  project:
  domain:
  version:
  time_range:
scope_key:
target_type: point | relation | cluster | claim | pattern | decision | context-pack | answer | route | keyword | channel
target_id:
feedback_type: useful | irrelevant | misleading | wrong_scope | stale | missing | contradicted | incomplete | too_weak | too_broad
event_type: explicit_correction | missing_evidence | scope_mismatch | answer_helpful | contradiction_missed | action_outcome | decision_outcome
signal_type: explicit_positive | same_line_followup | narrower_followup | correction | wrong_scope | missing | topic_shift | none
polarity: positive | negative | neutral
signal_strength: -2 | -1 | 0 | 1 | 2
signal_confidence:
severity: low | medium | high
reason:
effect:
  activation_delta:
  usefulness_delta:
  scope_fit_delta:
  relation_activation_delta:
affects:
  usefulness:
  scope_fit:
  activation_ranking:
  review_due:
  future_recommendation:
  risk_calibration:
  option_framing:
never_affects_directly:
  truth_confidence
  verification_status
  source_reliability
decision_outcome:
  decision_ref:
  action_basis_ref:
  recommendation:
  confidence_at_decision:
  user_choice:
  outcome_precondition:
    - recommendation_recorded
    - user_choice_or_explicit_override_recorded
  outcome: succeeded | failed | mixed | unresolved
  outcome_note:
requires_review: true
review_status: pending
reviewed_by:
reviewed_at:
tags:
  - feedback-event
---

# Feedback Event

## What Happened


## Why It Matters


## Proposed Effect


## Relation Activation Boundary

```text
Feedback can change activation of a relation path.
It cannot directly change reviewed relation strength.
```

## Decision Outcome Calibration

- Decision / action basis:
- Recommendation:
- Confidence at decision:
- User choice:
- Outcome precondition:
- Outcome:
- Outcome note:
- Future recommendation / risk / scope-fit implication:

## Safety Boundary

```text
Positive feedback is weak.
Negative feedback creates review pressure.
Explicit correction creates review_due.
Decision outcome improves future recommendations, not truth.
```

This event must not directly change truth confidence, verification_status, or source reliability.

## Review Notes
