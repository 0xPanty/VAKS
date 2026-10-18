---
record_kind: read_only_query_scenario
expected_valid: true
expected_outcome: proposal_only_with_operation_receipt
expected_codes: []
scenario_id: ql-valid-agent-propose-write
story_kind: agent_propose_write
query_mode: orientation
requested_authority_bucket: reviewed
included_buckets: [reviewed]
selected_authority_buckets: [reviewed]
selected_pack_roles: [orientation]
selected_action_basis_allowed: false
operation_receipt_present: true
actor_tier: suggest_only
operation_mode: propose_write
operation_actual_write_performed: false
reviewed_write_performed: false
target_scope: sandbox
user_intent_confirmed: true
operation_basis_materials: [reviewed_support]
---

# Agent Propose Write Operation Receipt

The loop can propose a write only as proposal-only output with an operation
receipt; no reviewed write is performed.
