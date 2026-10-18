---
record_kind: read_only_query_scenario
expected_valid: false
expected_outcome: blocked
expected_codes: [QL_CANDIDATE_USED_AS_SUPPORT]
scenario_id: ql-fail-candidate-support
story_kind: candidate_temptation
query_mode: action
requested_authority_bucket: candidate
included_buckets: [candidate]
selected_authority_buckets: [candidate]
selected_pack_roles: [support]
selected_action_basis_allowed: true
candidate_used_as_support: true
candidate_boundary_warning_present: true
---

# Failure: Candidate Used As Support

A candidate source is treated as support/action basis.
