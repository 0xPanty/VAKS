---
record_kind: operation_receipt
expected_valid: false
expected_codes: [OV_SCHEMA_CHANGE_MISSING_OWNER_FINAL]
operation_id: op-fail-schema-no-owner
actor_tier: reviewed_write
operation_mode: schema_change
actual_write_performed: true
target_scope: mainline
user_intent_confirmed: true
basis_materials: [reviewed_support]
approval_present: true
checked_body_hash: 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
checked_body_hash_match: true
owner_final_present: false
rollback_required: true
rollback_plan_present: true
---

# Failure: Schema Change Without Owner Final

A schema change lacks owner-final authority.
