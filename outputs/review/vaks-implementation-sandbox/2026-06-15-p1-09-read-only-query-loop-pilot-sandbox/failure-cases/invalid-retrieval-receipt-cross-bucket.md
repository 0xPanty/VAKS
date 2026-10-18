---
record_kind: read_only_query_scenario
expected_valid: false
expected_outcome: blocked
expected_codes: [QL_RETRIEVAL_RECEIPT_INVALID, RV_CROSS_BUCKET_RRF]
scenario_id: ql-fail-invalid-retrieval-cross-bucket
story_kind: ordinary_orientation
query_mode: orientation
requested_authority_bucket: mixed_for_orientation
included_buckets: [reviewed, candidate]
selected_authority_buckets: [reviewed, candidate]
selected_pack_roles: [orientation, review_input]
rrf_scope: cross_authority_bucket
cross_bucket_rrf_used: true
---

# Failure: Invalid Retrieval Receipt Cross Bucket

The generated retrieval receipt violates P1-08 receipt validation.
