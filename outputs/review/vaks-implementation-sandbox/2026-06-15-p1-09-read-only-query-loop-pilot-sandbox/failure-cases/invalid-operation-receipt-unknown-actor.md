---
record_kind: read_only_query_scenario
expected_valid: false
expected_outcome: blocked
expected_codes: [QL_OPERATION_RECEIPT_INVALID, OV_UNKNOWN_ACTOR_TIER]
scenario_id: ql-fail-invalid-operation-unknown-actor
story_kind: agent_propose_write
query_mode: orientation
requested_authority_bucket: reviewed
included_buckets: [reviewed]
selected_authority_buckets: [reviewed]
selected_pack_roles: [orientation]
operation_receipt_present: true
actor_tier: superuser
operation_mode: propose_write
operation_actual_write_performed: false
target_scope: sandbox
user_intent_confirmed: true
operation_basis_materials: [reviewed_support]
---

# Failure: Invalid Operation Receipt Unknown Actor

The operation receipt uses an unregistered actor tier.
