---
record_kind: read_only_query_scenario
expected_valid: false
expected_outcome: blocked
expected_codes: [QL_OPERATION_RECEIPT_REQUIRED]
scenario_id: ql-fail-propose-missing-operation-receipt
story_kind: agent_propose_write
query_mode: orientation
requested_authority_bucket: reviewed
included_buckets: [reviewed]
selected_authority_buckets: [reviewed]
selected_pack_roles: [orientation]
operation_receipt_present: false
reviewed_write_performed: false
operation_actual_write_performed: false
---

# Failure: Missing Operation Receipt

An agent propose-write flow has no operation receipt.
