---
fixture_id: ci04-pass-explicit-override
expected_result: PASS
decision_outcome:
  decision_ref: wiki/decisions/example-decision.md
  action_basis_ref: outputs/context/example-action-basis.md
  recommendation: choose option A because it matched the stated constraints
  confidence_at_decision: low
  user_choice:
  explicit_user_override: chose option B despite recommendation
  override_rationale: user prioritized speed over the earlier quality constraint
  outcome_precondition:
    - recommendation_recorded
    - confidence_at_decision_recorded
    - user_choice_or_explicit_override_recorded
    - outcome_note_recorded
  outcome: mixed
  outcome_note: Faster delivery worked, but quality degraded.
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

# PASS: Explicit User Override

The user did not follow the recommendation, but the override was explicit and
auditable, so the outcome can calibrate future option framing.

