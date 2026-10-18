---
record_kind: retrieval_receipt_failure_case
case_id: legacy-metadata-support
expected_future_validator_result: fail
reason: legacy_raw_metadata_used_as_support_signal
---

# Legacy Metadata As Support

Invalid pattern:

```yaml
selected_items:
  - ref: raw/articles/example-source.md
    authority_bucket: raw_anchor
    pack_role: support
    selected_by:
      metadata: "legacy freshness/source_quality field"
      legacy_raw_metadata: true
support_boundary:
  legacy_raw_metadata_excluded: false
```

Why this fails:

```text
Legacy raw metadata is retained for audit only. It must not become retrieval,
graph, pack, support, trust, or action signal.
```
