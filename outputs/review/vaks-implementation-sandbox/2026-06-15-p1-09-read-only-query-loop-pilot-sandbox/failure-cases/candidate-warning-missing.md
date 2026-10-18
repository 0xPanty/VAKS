---
record_kind: read_only_query_scenario
expected_valid: false
expected_outcome: blocked
expected_codes: [QL_CANDIDATE_WARNING_MISSING]
scenario_id: ql-fail-candidate-warning-missing
story_kind: candidate_temptation
query_mode: orientation
requested_authority_bucket: candidate
included_buckets: [candidate]
selected_authority_buckets: [candidate]
selected_pack_roles: [review_input]
selected_action_basis_allowed: false
candidate_used_as_support: false
candidate_boundary_warning_present: false
---

# Failure: Candidate Warning Missing

The loop shows candidate material without exposing the boundary warning.
