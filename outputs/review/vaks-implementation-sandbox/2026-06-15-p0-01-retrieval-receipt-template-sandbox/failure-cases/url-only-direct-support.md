---
record_kind: retrieval_receipt_failure_case
case_id: url-only-direct-support
expected_future_validator_result: fail
reason: url_only_citation_marked_direct_support
---

# URL-Only Direct Support

Invalid pattern:

```yaml
selected_items:
  - ref: https://example.com/source
    authority_bucket: raw_anchor
    pack_role: support
    source_anchor:
      source_ref: https://example.com/source
      selector:
      source_hash:
      chunk_hash:
      evidence_granularity: metadata_only
support_checks:
  - target_ref: review-candidate:target
    proposed_support_item_ref: https://example.com/source
    independent_anchor_ref: https://example.com/source
    evidence_role: direct_support
    result: supported
```

Why this fails:

```text
A URL is provenance, not direct support. The receipt needs a source span,
snapshot, code anchor, transcript segment, quote selector, or equivalent
inspected anchor for support checking.
```
