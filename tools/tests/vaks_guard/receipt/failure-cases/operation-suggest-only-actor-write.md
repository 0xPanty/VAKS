---
record_kind: operation_receipt
expected_valid: false
expected_codes: [OV_ACTOR_TIER_CANNOT_WRITE]
operation_id: op-fail-suggest-only-write
actor_tier: suggest_only
operation_mode: write
actual_write_performed: true
target_scope: sandbox
user_intent_confirmed: true
basis_materials: [reviewed_support]
---

# Failure: Suggest-Only Actor Write

A suggest-only actor may propose but must not perform a write.
