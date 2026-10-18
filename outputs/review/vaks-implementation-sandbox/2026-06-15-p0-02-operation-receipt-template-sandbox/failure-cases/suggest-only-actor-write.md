---
record_kind: operation_receipt
fixture_kind: failure_case
failure_id: suggest-only-actor-write
expected_result: blocked
expected_failure_reason: suggest_only_actor_cannot_perform_write
operation_id: op-sandbox-p0-02-failure-002
actor: Reviewer Agent
actor_tier: suggest_only
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

# Failure: Suggest-Only Actor Writes

Block because `suggest_only` may propose a write, but must keep
`actual_write_performed: false`.

Oracle: fail only on `suggest_only_actor_cannot_perform_write`.
