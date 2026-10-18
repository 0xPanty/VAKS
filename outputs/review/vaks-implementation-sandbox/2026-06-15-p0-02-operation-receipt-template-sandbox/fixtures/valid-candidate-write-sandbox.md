---
record_kind: operation_receipt
fixture_kind: positive
fixture_id: valid-candidate-write-sandbox
operation_id: op-sandbox-p0-02-fixture-002
operation_time: 2026-06-15T00:05:00+08:00
actor: Builder Agent
actor_tier: candidate_write
operation_mode: write
actual_write_performed: true
intent_confirmation:
  required: true
  user_confirmed: true
  restated_intent: Create sandbox-only operation receipt fixtures inside the approved slice directory.
  success_criteria:
    - All writes stay inside the approved sandbox path.
    - No protected path is modified.
basis:
  context_pack_ref: outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md#p0-02-operation-receipt-template
  reviewed_support_refs: []
  candidate_refs:
    - outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md
  feedback_refs: []
  retrieval_receipt_refs: []
  basis_boundary:
    context_pack_is_not_action_basis: true
    candidate_refs_are_not_action_basis: true
    feedback_refs_are_not_truth_or_basis: true
    retrieval_receipts_are_not_support: true
target_paths:
  - outputs/review/vaks-implementation-sandbox/2026-06-15-p0-02-operation-receipt-template-sandbox/fixtures/valid-candidate-write-sandbox.md
proposed_changes:
  - mode: create_file
    summary: Add a positive operation receipt fixture for approved sandbox write.
approval:
  required: false
  approved_by:
  approval_source:
  approved_at:
  checked_body_hash:
  checked_body_hash_algorithm: sha256_body_canonical_v0
  approval_scope:
rollback:
  required: true
  possible: true
  rollback_plan: Delete this sandbox fixture file before product acceptance if it is found invalid.
result:
  status: performed
  performed_at: 2026-06-15T00:05:00+08:00
  output_refs:
    - outputs/review/vaks-implementation-sandbox/2026-06-15-p0-02-operation-receipt-template-sandbox/fixtures/valid-candidate-write-sandbox.md
warnings:
  - The upgrade plan is implementation context for this sandbox, not evidence support or action basis.
gaps: []
operation_boundary:
  receipt_not_truth: true
  receipt_not_review_approval: true
  receipt_not_reviewed_knowledge: true
  receipt_not_action_basis: true
  validator_pass_not_reviewer_approval: true
  sandbox_not_mainline: true
---

# Fixture: Valid Candidate Write In Sandbox

This is valid because the actor is `candidate_write`, the target path is inside
the approved sandbox directory, the user rule provides write authorization for
this bounded slice, and rollback is available by deleting the sandbox file.
