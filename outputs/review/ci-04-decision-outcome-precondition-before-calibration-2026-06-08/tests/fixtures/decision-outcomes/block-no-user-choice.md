---
fixture_id: ci04-block-no-user-choice
expected_result: BLOCK_EXPECTED
decision_outcome:
  decision_ref: wiki/decisions/example-decision.md
  action_basis_ref: outputs/context/example-action-basis.md
  recommendation: choose option A
  confidence_at_decision: medium
  user_choice:
  explicit_user_override:
  outcome: succeeded
  outcome_note: Something later succeeded.
expected_violation: missing user_choice_or_explicit_override
---

# BLOCK: No User Choice Or Override

The result may be useful as a note, but it cannot show whether the user followed
or rejected the recommendation.

