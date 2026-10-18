---
fixture_id: ci04-block-truth-confidence-mutation
expected_result: BLOCK_EXPECTED
decision_outcome:
  decision_ref: wiki/decisions/example-decision.md
  recommendation: choose option A
  confidence_at_decision: medium
  user_choice: option A
  outcome: succeeded
  outcome_note: It worked.
proposed_mutation:
  truth_confidence: high
expected_violation: decision outcome cannot mutate truth_confidence
---

# BLOCK: Truth Confidence Mutation

Outcome success does not prove the underlying claim true.

