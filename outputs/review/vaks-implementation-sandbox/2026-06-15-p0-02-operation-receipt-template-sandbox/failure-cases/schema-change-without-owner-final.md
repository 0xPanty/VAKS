---
record_kind: operation_receipt
fixture_kind: failure_case
failure_id: schema-change-without-owner-final
expected_result: blocked
expected_failure_reason: schema_change_requires_owner_final
operation_id: op-sandbox-p0-02-failure-005
actor: Builder Agent
actor_tier: candidate_write
operation_mode: schema_change
actual_write_performed: true
target_paths:
  - SCHEMA.md
approval:
  required: true
  approved_by:
  checked_body_hash:
rollback:
  required: true
  possible: true
  rollback_plan: Revert schema section.
result:
  status: performed
operation_boundary:
  receipt_not_truth: true
  receipt_not_review_approval: true
  receipt_not_reviewed_knowledge: true
  receipt_not_action_basis: true
---

# Failure: Schema Change Without Owner Final

Block because `schema_change` requires `owner_final`. In this active sandbox
program, protected architecture files also remain out of write scope.

Oracle: fail only on `schema_change_requires_owner_final`.
