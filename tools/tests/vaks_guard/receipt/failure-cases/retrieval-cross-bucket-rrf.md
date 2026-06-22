---
record_kind: retrieval_receipt
expected_valid: false
expected_codes: [RV_CROSS_BUCKET_RRF]
receipt_id: rr-fail-cross-bucket-rrf
query_id: q-fail-cross-bucket-rrf
query_mode: review
requested_authority_bucket: reviewed
included_buckets: [reviewed, candidate]
rrf_scope: cross_authority_bucket
cross_bucket_rrf_used: true
selected_item_authority_buckets: [reviewed, candidate]
selected_item_pack_roles: [orientation]
selected_item_action_basis_allowed: false
---

# Failure: Cross-Bucket RRF

Cross-bucket ranking is being treated as if it can preserve authority.
