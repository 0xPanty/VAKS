---
record_kind: retrieval_receipt
expected_valid: false
expected_codes: [RV_RECEIPT_CLAIMS_AUTHORITY]
receipt_id: rr-fail-claims-authority
query_id: q-fail-claims-authority
query_mode: review
requested_authority_bucket: reviewed
included_buckets: [reviewed]
rrf_scope: same_authority_bucket_only
selected_item_authority_buckets: [reviewed]
selected_item_pack_roles: [orientation]
selected_item_action_basis_allowed: false
receipt_claims: [reviewer_approval, action_basis]
---

# Failure: Retrieval Receipt Claims Authority

The receipt claims approval and action basis, which the receipt cannot create.
