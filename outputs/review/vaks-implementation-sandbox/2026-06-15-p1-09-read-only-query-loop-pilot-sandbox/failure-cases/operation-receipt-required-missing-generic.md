---
record_kind: read_only_query_scenario
expected_valid: false
expected_outcome: blocked
expected_codes: [QL_OPERATION_RECEIPT_REQUIRED]
scenario_id: ql-fail-operation-receipt-required-generic
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
independent_anchor_ref: raw/articles/example-source.md#L40-L44
operation_receipt_required: true
operation_receipt_present: false
---

# Failure: Generic Operation Receipt Required Missing

A non-agent-propose-write scenario explicitly requires an operation receipt but
does not emit one.
