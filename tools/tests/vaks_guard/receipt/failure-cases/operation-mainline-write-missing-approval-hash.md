---
record_kind: operation_receipt
expected_valid: false
expected_codes: [OV_REVIEWED_WRITE_MISSING_APPROVAL_OR_HASH]
operation_id: op-fail-mainline-write-missing-approval-hash
actor_tier: owner_final
operation_mode: write
actual_write_performed: true
target_scope: mainline
user_intent_confirmed: true
basis_materials: [reviewed_support]
approval_present: false
checked_body_hash:
checked_body_hash_match: true
owner_final_present: true
rollback_required: true
rollback_plan_present: true
---

# Failure: Mainline Write Missing Approval Hash

A mainline/formal write has intent and rollback, but lacks approval facts and
checked body hash.
