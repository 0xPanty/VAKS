---
record_kind: retrieval_receipt
expected_valid: false
expected_codes: [RV_URL_ONLY_DIRECT_SUPPORT]
receipt_id: rr-fail-url-only-supported-none-role
query_id: q-fail-url-only-supported-none-role
query_mode: review
requested_authority_bucket: raw_anchor
included_buckets: [raw_anchor]
rrf_scope: same_authority_bucket_only
selected_item_authority_buckets: [raw_anchor]
selected_item_pack_roles: [anchor]
selected_item_action_basis_allowed: false
support_result: supported
support_evidence_role: none
support_anchor_kind: url_only
independent_anchor_ref: https://example.invalid/source
---

# Failure: URL-Only Supported With None Role

Support is claimed through `support_result: supported` while the anchor remains
URL-only and the role tries to hide behind `none`.
