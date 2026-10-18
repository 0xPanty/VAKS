---
fixture_id: ci04-pass-user-choice
expected_result: PASS
decision_outcome:
  decision_ref: wiki/decisions/example-decision.md
  action_basis_ref: outputs/context/example-action-basis.md
  recommendation: choose option A because it matched the stated constraints
  confidence_at_decision: medium
  user_choice: option A
  explicit_user_override:
  override_rationale:
  outcome_precondition:
    - recommendation_recorded
    - confidence_at_decision_recorded
    - user_choice_or_explicit_override_recorded
    - outcome_note_recorded
  outcome: succeeded
  outcome_note: The chosen option worked for the stated scope.
  calibration_allowed: true
  calibration_targets:
    - future_recommendation
    - risk_calibration
    - scope_fit
    - option_framing
  calibration_forbidden_targets:
    - truth_confidence
    - verification_status
    - source_reliability
    - review_verdict
    - reviewed_relation
    - action_basis_readiness
---

# PASS: Recommendation And User Choice

The recommendation chain is complete enough to calibrate future recommendations.

