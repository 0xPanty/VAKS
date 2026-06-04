---
record_type: feedback-event
status: accepted
created: 2026-06-01
updated: 2026-06-01
feedback_id: fb-q1-too-action-basis-shaped
created_by: Codex
feedback_source: conversation-derived
query_id: q1-citation-action-basis
session_id: vaks-e2e-trial-001
turn_id: step4
parent_query_id:
derived_from_turn_id: step3
question: "Can a citation-backed LLM answer be treated as action-basis-ready?"
query_intent: decision
query_scope:
  project: verified-action-knowledge-system
  domain: citation-backed answer review
  version: v0.3
  time_range: 2026-06-01
scope_key: v0.3-citation-support
target_type: answer
target_id: q1-citation-action-basis
feedback_type: too_broad
event_type: scope_mismatch
signal_type: narrower_followup
polarity: negative
signal_strength: -1
signal_confidence: 0.8
severity: medium
reason: "The answer correctly rejected citation-only action readiness, but it framed the question too much as action_basis and not enough as source-linked verification scope."
effect:
  activation_delta: 1
  usefulness_delta: 0
  scope_fit_delta: 1
  relation_activation_delta: 0
affects:
  usefulness: "No truth change; improve future answer framing."
  scope_fit: "For similar questions, activate source-span support and verification boundary before action readiness."
  activation_ranking: "Raise fine-grained support claim and ALCE citation-quality claim; lower benchmark-method detail."
  review_due: false
  future_recommendation: "Start with: source link != verified support."
  risk_calibration: "Warn when the user's wording asks about verified/action-ready status."
  option_framing: "Separate source-linked, supported, verified, and action-ready."
never_affects_directly:
  - truth_confidence
  - verification_status
  - source_reliability
decision_outcome:
  decision_ref:
  action_basis_ref:
  recommendation:
  confidence_at_decision:
  user_choice:
  outcome_precondition: []
  outcome: unresolved
  outcome_note:
requires_review: false
review_status: accepted
reviewed_by: Codex
reviewed_at: 2026-06-01
tags:
  - feedback-event
  - e2e-trial
---

# Feedback Event: Q1 Too Action-Basis Shaped

## What Happened

The answer was useful, but it over-activated the action-basis frame for a question that could also be about verified support.

## Why It Matters

Future similar questions should first separate these states:

```text
source-linked
source-supported
reviewed / verified
action-basis-ready
```

## Proposed Effect

For similar questions, activate the fine-grained support claim and source-span boundary first, then decide whether action readiness is even in scope.

## Safety Boundary

This feedback changes activation and scope-fit only. It does not change truth confidence or source reliability.

