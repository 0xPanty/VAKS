---
record_kind: operation_receipt
expected_valid: false
expected_codes: [OV_ACTOR_TIER_CANNOT_WRITE]
operation_id: op-fail-read-only-write
actor_tier: read_only
operation_mode: write
actual_write_performed: true
target_scope: sandbox
user_intent_confirmed: true
basis_materials: [reviewed_support]
---

# Failure: Read-Only Actor Write

A read-only actor performed a write.
