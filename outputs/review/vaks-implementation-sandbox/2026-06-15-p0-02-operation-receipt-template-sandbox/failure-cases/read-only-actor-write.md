---
record_kind: operation_receipt
fixture_kind: failure_case
failure_id: read-only-actor-write
expected_result: blocked
expected_failure_reason: read_only_actor_cannot_write
operation_id: op-sandbox-p0-02-failure-001
actor: Explorer Agent
actor_tier: read_only
operation_mode: write
actual_write_performed: true
target_paths:
  - outputs/review/vaks-implementation-sandbox/example/file.md
approval:
  required: false
  checked_body_hash:
rollback:
  required: true
  possible: true
  rollback_plan: Delete the file.
result:
  status: performed
operation_boundary:
  receipt_not_truth: true
  receipt_not_review_approval: true
  receipt_not_reviewed_knowledge: true
  receipt_not_action_basis: true
---

# Failure: Read-Only Actor Writes

Block because `read_only` cannot perform `write`, even in sandbox.

Oracle: fail only on `read_only_actor_cannot_write`.
