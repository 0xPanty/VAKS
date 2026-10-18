---
record_kind: retrieval_receipt
expected_valid: false
expected_codes: [RV_UNKNOWN_AUTHORITY_BUCKET]
receipt_id: rr-fail-unknown-bucket
query_id: q-fail-unknown-bucket
query_mode: review
requested_authority_bucket: trusted_cache
included_buckets: [trusted_cache]
rrf_scope: same_authority_bucket_only
selected_item_authority_buckets: [trusted_cache]
selected_item_pack_roles: [support]
selected_item_action_basis_allowed: false
---

# Failure: Unknown Authority Bucket

An unregistered authority bucket attempts to bypass the retrieval boundary.
