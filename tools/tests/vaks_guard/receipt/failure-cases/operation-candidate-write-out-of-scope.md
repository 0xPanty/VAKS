---
record_kind: operation_receipt
expected_valid: false
expected_codes: [OV_CANDIDATE_WRITE_OUT_OF_SCOPE]
operation_id: op-fail-candidate-out-of-scope
actor_tier: candidate_write
operation_mode: write
actual_write_performed: true
target_scope: reviewed
user_intent_confirmed: true
basis_materials: [reviewed_support]
approval_present: true
checked_body_hash: 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
checked_body_hash_match: true
rollback_required: true
rollback_plan_present: true
---

# Failure: Candidate Write Out Of Scope

A candidate-write actor attempts to write reviewed scope.
