---
fixture_id: ci04-block-reviewed-relation-creation
expected_result: BLOCK_EXPECTED
decision_outcome:
  decision_ref: wiki/decisions/example-decision.md
  recommendation: choose option A
  confidence_at_decision: medium
  user_choice: option A
  outcome: succeeded
  outcome_note: It worked.
proposed_mutation:
  reviewed_relation: creates_supports_relation
expected_violation: decision outcome cannot create reviewed_relation
---

# BLOCK: Reviewed Relation Creation

Outcome calibration can create review pressure, not reviewed relations.

