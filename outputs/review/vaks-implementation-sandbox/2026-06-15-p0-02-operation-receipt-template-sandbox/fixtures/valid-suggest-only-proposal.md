---
record_kind: operation_receipt
fixture_kind: positive
fixture_id: valid-suggest-only-proposal
operation_id: op-sandbox-p0-02-fixture-001
operation_time: 2026-06-15T00:00:00+08:00
actor: Reviewer Agent
actor_tier: suggest_only
operation_mode: propose_write
actual_write_performed: false
intent_confirmation:
  required: false
  user_confirmed: false
  restated_intent: Suggest a future operation receipt shape without modifying target files.
  success_criteria:
    - Proposal remains advisory.
    - No target write is performed.
basis:
  context_pack_ref: sandbox/context-packs/example-operation-contract.md
  reviewed_support_refs: []
  candidate_refs:
    - outputs/review/example-candidate.md
  feedback_refs: []
  retrieval_receipt_refs:
    - outputs/review/vaks-implementation-sandbox/2026-06-15-p0-01-retrieval-receipt-template-sandbox/fixtures/valid-orientation-receipt.md
  basis_boundary:
    context_pack_is_not_action_basis: true
    candidate_refs_are_not_action_basis: true
    feedback_refs_are_not_truth_or_basis: true
    retrieval_receipts_are_not_support: true
target_paths:
  - outputs/review/vaks-implementation-sandbox/example-next-slice/artifact/example.md
proposed_changes:
  - mode: proposed_only
    summary: Draft a sandbox-only operation receipt example.
approval:
  required: false
  approved_by:
  approval_source:
  approved_at:
  checked_body_hash:
  checked_body_hash_algorithm: sha256_body_canonical_v0
  approval_scope:
rollback:
  required: false
  possible: true
  rollback_plan: No target write was performed; discard proposal text if not useful.
result:
  status: proposed_only
  performed_at:
  output_refs: []
warnings:
  - Candidate and retrieval refs are orientation only.
gaps: []
operation_boundary:
  receipt_not_truth: true
  receipt_not_review_approval: true
  receipt_not_reviewed_knowledge: true
  receipt_not_action_basis: true
  validator_pass_not_reviewer_approval: true
  sandbox_not_mainline: true
---

# Fixture: Valid Suggest-Only Proposal

This is valid because `suggest_only` proposes a write but does not perform one.
The candidate and retrieval references are labeled as non-basis orientation.
