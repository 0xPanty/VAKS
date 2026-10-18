---
record_kind: operation_receipt
fixture_kind: failure_case
failure_id: receipt-claims-truth-or-approval
expected_result: blocked
expected_failure_reason: operation_receipt_claims_authority
operation_id: op-sandbox-p0-02-failure-009
actor: Builder Agent
actor_tier: candidate_write
operation_mode: write
actual_write_performed: true
approval:
  required: false
  checked_body_hash:
result:
  status: performed
operation_boundary:
  receipt_not_truth: false
  receipt_not_review_approval: false
  receipt_not_reviewed_knowledge: false
  receipt_not_action_basis: false
---

# Failure: Receipt Claims Truth Or Approval

Block because an operation receipt records process trace only. It cannot become
truth, review approval, reviewed knowledge, or action basis.

Oracle: fail only on `operation_receipt_claims_authority`.
