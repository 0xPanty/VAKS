---
record_kind: retrieval_receipt
expected_valid: false
expected_codes: [RV_URL_ONLY_DIRECT_SUPPORT]
receipt_id: rr-fail-url-only
query_id: q-fail-url-only
query_mode: review
requested_authority_bucket: raw_anchor
included_buckets: [raw_anchor]
rrf_scope: same_authority_bucket_only
selected_item_authority_buckets: [raw_anchor]
selected_item_pack_roles: [support]
selected_item_action_basis_allowed: false
support_result: supported
support_evidence_role: direct_support
support_anchor_kind: url_only
independent_anchor_ref: https://example.invalid/source
---

# Failure: URL-Only Direct Support

A bare URL is provenance, not a sufficient direct support anchor.
