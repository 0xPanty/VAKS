---
record_kind: read_only_query_scenario
expected_valid: true
expected_outcome: candidate_blocked_as_support
expected_codes: []
scenario_id: ql-valid-candidate-temptation
story_kind: candidate_temptation
query_mode: orientation
requested_authority_bucket: candidate
included_buckets: [candidate]
selected_authority_buckets: [candidate]
selected_pack_roles: [review_input]
selected_action_basis_allowed: false
candidate_used_as_support: false
candidate_used_as_action_basis: false
candidate_boundary_warning_present: true
---

# Candidate Temptation Blocked

The candidate looks useful but remains review input, not evidence support or
action basis.
