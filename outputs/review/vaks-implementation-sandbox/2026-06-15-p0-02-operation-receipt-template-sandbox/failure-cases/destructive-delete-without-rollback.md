---
record_kind: operation_receipt
fixture_kind: failure_case
failure_id: destructive-delete-without-rollback
expected_result: blocked
expected_failure_reason: destructive_operation_missing_rollback_plan
operation_id: op-sandbox-p0-02-failure-006
actor: Owner Final Operator
actor_tier: owner_final
operation_mode: delete
actual_write_performed: true
target_paths:
  - wiki/decisions/example-decision.md
approval:
  required: true
  approved_by: owner-example
  checked_body_hash:
rollback:
  required: true
  possible: false
  rollback_plan:
result:
  status: performed
operation_boundary:
  receipt_not_truth: true
  receipt_not_review_approval: true
  receipt_not_reviewed_knowledge: true
  receipt_not_action_basis: true
---

# Failure: Destructive Delete Without Rollback

Block because destructive operation needs an explicit rollback plan or explicit
owner-final acceptance that the action is non-reversible. This record has
neither.

Oracle: fail only on `destructive_operation_missing_rollback_plan`.
