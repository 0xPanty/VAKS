---
record_kind: read_only_query_scenario
expected_valid: false
expected_outcome: blocked
expected_codes: [QL_ORDINARY_QUERY_OVERSTRICT]
scenario_id: ql-fail-ordinary-overstrict
story_kind: ordinary_orientation
query_mode: orientation
requested_authority_bucket: mixed_for_orientation
included_buckets: [reviewed, candidate]
selected_authority_buckets: [reviewed, candidate]
selected_pack_roles: [orientation, review_input]
full_audit_required: true
---

# Failure: Ordinary Query Overstrict

The loop incorrectly requires a full audit for a plain orientation question.
