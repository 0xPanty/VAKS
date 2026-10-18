---
record_kind: operation_receipt
expected_valid: false
expected_codes: [OV_REVIEWED_WRITE_MISSING_APPROVAL_OR_HASH]
operation_id: op-fail-reviewed-write-missing-approval-hash
actor_tier: reviewed_write
operation_mode: write
actual_write_performed: true
target_scope: reviewed
user_intent_confirmed: true
basis_materials: [reviewed_support]
approval_present: false
checked_body_hash:
rollback_required: true
rollback_plan_present: true
---

# Failure: Reviewed Write Missing Approval Hash

A reviewed write lacks approval facts and checked body hash.
