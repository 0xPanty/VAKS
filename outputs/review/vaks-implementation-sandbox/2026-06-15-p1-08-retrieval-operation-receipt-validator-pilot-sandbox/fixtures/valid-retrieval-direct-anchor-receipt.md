---
record_kind: retrieval_receipt
expected_valid: true
expected_codes: []
receipt_id: rr-valid-direct-anchor
query_id: q-valid-direct-anchor
query_mode: review
requested_authority_bucket: raw_anchor
included_buckets: [raw_anchor]
rrf_scope: same_authority_bucket_only
cross_bucket_rrf_used: false
selected_item_authority_buckets: [raw_anchor]
selected_item_pack_roles: [support]
selected_item_action_basis_allowed: false
selected_by_claims_support: false
scores_are_support: false
graph_rank_claims_trust: false
legacy_raw_metadata_used: false
support_result: supported
support_evidence_role: direct_support
support_anchor_kind: excerpt_or_passage
independent_anchor_ref: raw/articles/example-source.md#L10-L18
receipt_claims: []
selected_by_is_not_support: true
same_bucket_rrf_only: true
cross_bucket_rank_not_authority: true
legacy_raw_metadata_excluded: true
candidate_overlay_feedback_not_support: true
url_only_not_direct_support: true
graph_rank_not_trust: true
receipt_not_review_approval: true
receipt_not_action_basis: true
receipt_not_reviewed_knowledge: true
---

# Valid Retrieval Direct Anchor Receipt

A raw source anchor can participate in a support check only because the target
has an independent stable anchor. The receipt still does not approve review or
action.
