---
record_kind: operation_receipt
fixture_kind: positive_hypothetical
fixture_id: valid-reviewed-write-approved-example
operation_id: op-sandbox-p0-02-fixture-003
operation_time: 2026-06-15T00:10:00+08:00
actor: Reviewed Write Operator
actor_tier: reviewed_write
operation_mode: write
actual_write_performed: false
intent_confirmation:
  required: true
  user_confirmed: true
  restated_intent: Hypothetically record a reviewed write that has explicit approval and checked body hash.
  success_criteria:
    - Receipt shows approval and checked body hash.
    - This fixture performs no reviewed write.
basis:
  context_pack_ref: sandbox/context-packs/example-action-envelope.md
  reviewed_support_refs:
    - wiki/claims/example-reviewed-support.md#example
  candidate_refs: []
  feedback_refs: []
  retrieval_receipt_refs: []
  basis_boundary:
    context_pack_is_not_action_basis: true
    candidate_refs_are_not_action_basis: true
    feedback_refs_are_not_truth_or_basis: true
    retrieval_receipts_are_not_support: true
target_paths:
  - wiki/claims/example-reviewed-note.md
proposed_changes:
  - mode: hypothetical_reviewed_write
    body_hash: 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
    summary: Hypothetical reviewed write fixture; no real target write is performed.
approval:
  required: true
  approved_by: owner-final-example
  approval_source: sandbox-fixture-only
  approved_at: 2026-06-15T00:10:00+08:00
  checked_body_hash: 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
  checked_body_hash_algorithm: sha256_body_canonical_v0
  approval_scope: Hypothetical fixture body only.
rollback:
  required: true
  possible: true
  rollback_plan: Not applicable to real files; this fixture performs no reviewed write.
result:
  status: proposed_only
  performed_at:
  output_refs: []
warnings:
  - This is a sandbox fixture, not approval for the named target path.
gaps: []
operation_boundary:
  receipt_not_truth: true
  receipt_not_review_approval: true
  receipt_not_reviewed_knowledge: true
  receipt_not_action_basis: true
  validator_pass_not_reviewer_approval: true
  sandbox_not_mainline: true
---

# Fixture: Valid Reviewed Write Approval Shape

This fixture demonstrates the shape required for a reviewed write: explicit
approval plus a checked body hash. It does not perform or approve a real write.
