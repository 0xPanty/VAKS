---
record_kind: operation_receipt
expected_valid: false
expected_codes: [OV_CHECKED_BODY_HASH_MISMATCH]
operation_id: op-fail-hash-mismatch
actor_tier: reviewed_write
operation_mode: write
actual_write_performed: true
target_scope: reviewed
user_intent_confirmed: true
basis_materials: [reviewed_support]
approval_present: true
checked_body_hash: 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
checked_body_hash_match: false
rollback_required: true
rollback_plan_present: true
---

# Failure: Checked Body Hash Mismatch

Approval cannot apply to a changed body.
