---
record_kind: retrieval_receipt
expected_valid: false
expected_codes: [RV_LEGACY_RAW_METADATA_USED]
receipt_id: rr-fail-legacy-metadata
query_id: q-fail-legacy-metadata
query_mode: review
requested_authority_bucket: raw_anchor
included_buckets: [raw_anchor]
rrf_scope: same_authority_bucket_only
selected_item_authority_buckets: [raw_anchor]
selected_item_pack_roles: [anchor]
selected_item_action_basis_allowed: false
legacy_raw_metadata_used: true
---

# Failure: Legacy Raw Metadata Used

Legacy raw metadata is being included where support-grade anchors are required.
