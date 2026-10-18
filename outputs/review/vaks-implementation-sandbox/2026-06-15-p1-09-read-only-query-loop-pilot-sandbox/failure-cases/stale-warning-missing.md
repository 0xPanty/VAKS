---
record_kind: read_only_query_scenario
expected_valid: false
expected_outcome: blocked
expected_codes: [QL_STALE_WARNING_MISSING]
scenario_id: ql-fail-stale-warning-missing
story_kind: stale_decision
query_mode: orientation
requested_authority_bucket: reviewed
included_buckets: [reviewed]
selected_authority_buckets: [reviewed]
selected_pack_roles: [orientation]
stale_warning_present: false
stale_decision_used_for_ready_action: false
---

# Failure: Stale Warning Missing

A stale decision appears without a stale/superseded warning.
