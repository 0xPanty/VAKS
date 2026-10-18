---
fixture_id: ci04-block-casual-approval
expected_result: BLOCK_EXPECTED
decision_outcome:
  decision_ref: wiki/decisions/example-decision.md
  action_basis_ref: outputs/context/example-action-basis.md
  recommendation: choose option A
  confidence_at_decision: medium
  user_choice: looks good
  explicit_user_override:
  outcome: succeeded
  outcome_note: Later looked fine.
expected_violation: casual approval is not a recorded choice or explicit override
---

# BLOCK: Casual Approval

"Looks good" is review pressure or conversational agreement. It is not a
recorded decision choice for outcome calibration.

