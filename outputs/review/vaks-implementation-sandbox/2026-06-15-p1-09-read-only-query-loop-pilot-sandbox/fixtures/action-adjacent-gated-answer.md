---
record_kind: read_only_query_scenario
expected_valid: true
expected_outcome: action_gated_answer
expected_codes: []
scenario_id: ql-valid-action-adjacent
story_kind: action_adjacent
query_mode: action
requested_authority_bucket: raw_anchor
included_buckets: [raw_anchor]
selected_authority_buckets: [raw_anchor]
selected_pack_roles: [support]
selected_action_basis_allowed: false
context_pack_present: true
support_check_present: true
action_readiness_check_present: true
support_result: supported
support_evidence_role: direct_support
support_anchor_kind: excerpt_or_passage
independent_anchor_ref: raw/articles/example-source.md#L20-L28
action_basis_ready_claimed: false
---

# Action-Adjacent Gated Answer

The loop may assemble context and support checks, but it does not claim ready
action basis.
