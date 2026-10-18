---
record_kind: read_only_query_scenario
expected_valid: false
expected_outcome: blocked
expected_codes: [QL_READ_ONLY_ACTION_BASIS_CLAIM]
scenario_id: ql-fail-action-basis-claim
story_kind: action_adjacent
query_mode: action
requested_authority_bucket: raw_anchor
included_buckets: [raw_anchor]
selected_authority_buckets: [raw_anchor]
selected_pack_roles: [support]
context_pack_present: true
support_check_present: true
action_readiness_check_present: true
support_result: supported
support_evidence_role: direct_support
support_anchor_kind: excerpt_or_passage
independent_anchor_ref: raw/articles/example-source.md#L30-L34
action_basis_ready_claimed: true
---

# Failure: Read-Only Loop Claims Action Basis

The loop claims ready action basis even though P1-09 is read-only.
