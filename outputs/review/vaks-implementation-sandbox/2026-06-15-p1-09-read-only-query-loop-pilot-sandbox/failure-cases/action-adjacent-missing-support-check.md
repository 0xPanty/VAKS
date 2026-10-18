---
record_kind: read_only_query_scenario
expected_valid: false
expected_outcome: blocked
expected_codes: [QL_ACTION_ADJACENT_MISSING_GATE]
scenario_id: ql-fail-action-missing-support
story_kind: action_adjacent
query_mode: action
requested_authority_bucket: raw_anchor
included_buckets: [raw_anchor]
selected_authority_buckets: [raw_anchor]
selected_pack_roles: [support]
context_pack_present: true
support_check_present: false
action_readiness_check_present: true
support_result: not_ready
---

# Failure: Action-Adjacent Missing Support Check

The action-adjacent flow skips a required support check.
