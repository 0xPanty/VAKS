---
record_kind: operation_receipt
expected_valid: false
expected_codes: [OV_ROLLBACK_REQUIRED]
operation_id: op-fail-delete-no-rollback
actor_tier: owner_final
operation_mode: delete
actual_write_performed: true
target_scope: reviewed
user_intent_confirmed: true
basis_materials: [reviewed_support]
owner_final_present: true
approval_present: true
checked_body_hash: 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
checked_body_hash_match: true
rollback_required: true
rollback_plan_present: false
---

# Failure: Delete Without Rollback

A destructive operation lacks a rollback plan.
