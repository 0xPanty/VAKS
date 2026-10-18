---
record_kind: operation_receipt
fixture_kind: failure_case
failure_id: missing-intent-confirmation
expected_result: blocked
expected_failure_reason: required_intent_confirmation_missing
operation_id: op-sandbox-p0-02-failure-007
actor: Builder Agent
actor_tier: candidate_write
operation_mode: write
actual_write_performed: true
intent_confirmation:
  required: true
  user_confirmed: false
  restated_intent:
  success_criteria: []
target_paths:
  - outputs/review/vaks-implementation-sandbox/example/file.md
approval:
  required: false
  checked_body_hash:
rollback:
  required: true
  possible: true
  rollback_plan: Delete sandbox file.
result:
  status: performed
operation_boundary:
  receipt_not_truth: true
  receipt_not_review_approval: true
  receipt_not_reviewed_knowledge: true
  receipt_not_action_basis: true
---

# Failure: Missing Intent Confirmation

Block because a significant write says intent confirmation was required but was
not confirmed and has no restated intent or success criteria.

Oracle: fail only on `required_intent_confirmation_missing`.
