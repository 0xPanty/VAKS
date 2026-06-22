---
record_kind: operation_receipt
expected_valid: false
expected_codes: [OV_UNKNOWN_ACTOR_TIER]
operation_id: op-fail-unknown-actor-tier
actor_tier: superuser
operation_mode: write
actual_write_performed: true
target_scope: sandbox
user_intent_confirmed: true
basis_materials: [reviewed_support]
rollback_required: true
rollback_plan_present: true
---

# Failure: Unknown Actor Tier Write

An unregistered actor tier attempts to bypass the operation permission matrix.
