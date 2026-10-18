---
record_kind: read_only_query_scenario
expected_valid: false
expected_outcome: blocked
expected_codes: [QL_AGENT_PROPOSE_WRITE_PERFORMED_WRITE]
scenario_id: ql-fail-propose-performs-write
story_kind: agent_propose_write
query_mode: orientation
requested_authority_bucket: reviewed
included_buckets: [reviewed]
selected_authority_buckets: [reviewed]
selected_pack_roles: [orientation]
operation_receipt_present: true
actor_tier: suggest_only
operation_mode: propose_write
operation_actual_write_performed: true
reviewed_write_performed: true
target_scope: reviewed
user_intent_confirmed: true
operation_basis_materials: [reviewed_support]
---

# Failure: Proposal Performs Reviewed Write

The propose-write story performs a reviewed write.
