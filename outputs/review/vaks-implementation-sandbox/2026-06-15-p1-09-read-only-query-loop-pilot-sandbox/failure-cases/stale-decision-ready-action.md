---
record_kind: read_only_query_scenario
expected_valid: false
expected_outcome: blocked
expected_codes: [QL_STALE_DECISION_READY_ACTION]
scenario_id: ql-fail-stale-ready-action
story_kind: stale_decision
query_mode: action
requested_authority_bucket: reviewed
included_buckets: [reviewed]
selected_authority_buckets: [reviewed]
selected_pack_roles: [orientation]
stale_warning_present: true
stale_decision_used_for_ready_action: true
---

# Failure: Stale Decision Ready Action

A stale decision is allowed to produce ready action.
