---
record_kind: operation_receipt
fixture_kind: failure_case
failure_id: reviewed-write-missing-approval-hash
expected_result: blocked
expected_failure_reason: reviewed_write_missing_checked_body_hash
operation_id: op-sandbox-p0-02-failure-003
actor: Reviewed Write Operator
actor_tier: reviewed_write
operation_mode: write
actual_write_performed: true
intent_confirmation:
  required: true
  user_confirmed: true
basis:
  reviewed_support_refs:
    - wiki/claims/example-reviewed-support.md
target_paths:
  - wiki/claims/example-reviewed-note.md
approval:
  required: true
  approved_by: owner-example
  checked_body_hash:
rollback:
  required: true
  possible: true
  rollback_plan: Restore previous file body.
result:
  status: performed
operation_boundary:
  receipt_not_truth: true
  receipt_not_review_approval: true
  receipt_not_reviewed_knowledge: true
  receipt_not_action_basis: true
---

# Failure: Reviewed Write Missing Checked Body Hash

Block because reviewed write requires approval of the exact body. Approval
without `checked_body_hash` can drift.

Oracle: fail only on `reviewed_write_missing_checked_body_hash`.
