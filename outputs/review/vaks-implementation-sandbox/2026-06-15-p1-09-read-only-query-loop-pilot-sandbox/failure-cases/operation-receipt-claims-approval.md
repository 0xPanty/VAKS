---
record_kind: read_only_query_scenario
expected_valid: false
expected_outcome: blocked
expected_codes: [QL_OPERATION_RECEIPT_INVALID, OV_RECEIPT_CLAIMS_AUTHORITY]
scenario_id: ql-fail-operation-claims-approval
story_kind: agent_propose_write
query_mode: orientation
requested_authority_bucket: reviewed
included_buckets: [reviewed]
selected_authority_buckets: [reviewed]
selected_pack_roles: [orientation]
operation_receipt_present: true
actor_tier: suggest_only
operation_mode: propose_write
operation_actual_write_performed: false
target_scope: sandbox
user_intent_confirmed: true
operation_basis_materials: [reviewed_support]
operation_claims: [reviewer_approval, action_basis]
---

# Failure: Operation Receipt Claims Approval

The operation receipt claims approval and action basis.
