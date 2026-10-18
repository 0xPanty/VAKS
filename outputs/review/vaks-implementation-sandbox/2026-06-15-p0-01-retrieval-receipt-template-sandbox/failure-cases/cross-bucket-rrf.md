---
record_kind: retrieval_receipt_failure_case
case_id: cross-bucket-rrf
expected_future_validator_result: fail
reason: cross_bucket_ranking_presented_as_authority
---

# Cross-Bucket RRF

Invalid pattern:

```yaml
requested_authority_bucket: mixed_for_orientation
included_buckets:
  - reviewed
  - candidate
  - feedback
rrf_scope: cross_authority_bucket
selected_items:
  - ref: wiki/claims/example.md
    authority_bucket: reviewed
    diagnostic_scores:
      rrf_rank: 2
  - ref: outputs/review/example-candidate.md
    authority_bucket: candidate
    diagnostic_scores:
      rrf_rank: 1
```

Why this fails:

```text
RRF can merge signals inside one authority bucket. It must not merge reviewed,
candidate, raw, overlay, or feedback items into one authority-looking list.
```
