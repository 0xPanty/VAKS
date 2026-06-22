---
record_kind: retrieval_receipt
expected_valid: false
expected_codes: [RV_SELECTED_BY_AS_SUPPORT]
receipt_id: rr-fail-selected-by
query_id: q-fail-selected-by
query_mode: review
requested_authority_bucket: reviewed
included_buckets: [reviewed]
rrf_scope: same_authority_bucket_only
selected_item_authority_buckets: [reviewed]
selected_item_pack_roles: [support]
selected_item_action_basis_allowed: false
selected_by_claims_support: true
scores_are_support: true
---

# Failure: Selected-By As Support

The receipt confuses retrieval selection or score with evidence support.
