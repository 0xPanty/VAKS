---
record_kind: read_only_query_scenario
expected_valid: true
expected_outcome: orientation_answer
expected_codes: []
scenario_id: ql-valid-ordinary-orientation
story_kind: ordinary_orientation
query_mode: orientation
requested_authority_bucket: mixed_for_orientation
included_buckets: [reviewed, candidate]
selected_authority_buckets: [reviewed, candidate]
selected_pack_roles: [orientation, review_input]
full_audit_required: false
selected_action_basis_allowed: false
---

# Ordinary Orientation Answer

An ordinary question can receive orientation context without a full audit or
action-basis gate.
