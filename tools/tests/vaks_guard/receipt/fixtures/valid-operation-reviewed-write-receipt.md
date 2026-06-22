---
record_kind: operation_receipt
expected_valid: true
expected_codes: []
operation_id: op-valid-reviewed-write
actor_tier: reviewed_write
operation_mode: write
actual_write_performed: true
target_scope: reviewed
user_intent_confirmed: true
basis_materials: [reviewed_support]
approval_present: true
checked_body_hash: 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
checked_body_hash_match: true
owner_final_present: false
rollback_required: true
rollback_plan_present: true
operation_claims: []
receipt_not_truth: true
receipt_not_review_approval: true
receipt_not_reviewed_knowledge: true
receipt_not_action_basis: true
validator_pass_not_reviewer_approval: true
sandbox_not_mainline: true
---

# Valid Reviewed Write Operation Receipt

This is a normalized positive example for a reviewed write with explicit
approval facts, checked body hash, intent confirmation, and rollback plan.
