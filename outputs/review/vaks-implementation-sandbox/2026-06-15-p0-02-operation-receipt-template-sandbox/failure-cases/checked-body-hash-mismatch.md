---
record_kind: operation_receipt
fixture_kind: failure_case
failure_id: checked-body-hash-mismatch
expected_result: blocked
expected_failure_reason: checked_body_hash_mismatch
operation_id: op-sandbox-p0-02-failure-004
actor: Reviewed Write Operator
actor_tier: reviewed_write
operation_mode: write
actual_write_performed: true
proposed_changes:
  - mode: reviewed_write
    body_hash: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
approval:
  required: true
  approved_by: owner-example
  checked_body_hash: bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
rollback:
  required: true
  possible: true
  rollback_plan: Restore previous body.
result:
  status: performed
operation_boundary:
  receipt_not_truth: true
  receipt_not_review_approval: true
  receipt_not_reviewed_knowledge: true
  receipt_not_action_basis: true
---

# Failure: Checked Body Hash Mismatch

Block because the approved body hash does not match the proposed body hash. P0-03
will own the validator, but this failure case keeps the boundary visible.

Oracle: fail only on `checked_body_hash_mismatch`.
