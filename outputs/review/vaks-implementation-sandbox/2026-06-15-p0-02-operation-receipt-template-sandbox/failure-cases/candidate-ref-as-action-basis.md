---
record_kind: operation_receipt
fixture_kind: failure_case
failure_id: candidate-ref-as-action-basis
expected_result: blocked
expected_failure_reason: candidate_ref_used_as_action_basis
operation_id: op-sandbox-p0-02-failure-008
actor: Builder Agent
actor_tier: candidate_write
operation_mode: write
actual_write_performed: true
basis:
  context_pack_ref:
  reviewed_support_refs: []
  candidate_refs:
    - outputs/review/example-candidate-distillation.md
  basis_boundary:
    context_pack_is_not_action_basis: true
    candidate_refs_are_not_action_basis: false
target_paths:
  - outputs/review/vaks-implementation-sandbox/example/file.md
warnings:
  - Candidate selected as sufficient action basis.
result:
  status: performed
operation_boundary:
  receipt_not_truth: true
  receipt_not_review_approval: true
  receipt_not_reviewed_knowledge: true
  receipt_not_action_basis: false
---

# Failure: Candidate Ref Used As Action Basis

Block because candidate refs can orient review but cannot create ready action
basis.

Oracle: fail only on `candidate_ref_used_as_action_basis`.
