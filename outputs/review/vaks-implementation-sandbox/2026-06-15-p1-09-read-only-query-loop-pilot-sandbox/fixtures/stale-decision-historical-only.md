---
record_kind: read_only_query_scenario
expected_valid: true
expected_outcome: historical_only_ready_action_blocked
expected_codes: []
scenario_id: ql-valid-stale-decision
story_kind: stale_decision
query_mode: orientation
requested_authority_bucket: reviewed
included_buckets: [reviewed]
selected_authority_buckets: [reviewed]
selected_pack_roles: [orientation]
selected_action_basis_allowed: false
stale_warning_present: true
stale_decision_used_for_ready_action: false
action_basis_ready_claimed: false
---

# Stale Decision Historical Only

A stale decision may explain history while ready action remains blocked.
