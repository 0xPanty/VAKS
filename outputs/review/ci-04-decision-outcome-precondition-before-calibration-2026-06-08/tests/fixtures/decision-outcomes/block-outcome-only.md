---
fixture_id: ci04-block-outcome-only
expected_result: BLOCK_EXPECTED
decision_outcome:
  decision_ref: wiki/decisions/example-decision.md
  action_basis_ref:
  recommendation:
  confidence_at_decision:
  user_choice:
  explicit_user_override:
  outcome: failed
  outcome_note: It did not work.
expected_violation: missing recommendation and missing user_choice_or_explicit_override
---

# BLOCK: Outcome Only

An outcome without the recommendation chain cannot calibrate future recommendations.

