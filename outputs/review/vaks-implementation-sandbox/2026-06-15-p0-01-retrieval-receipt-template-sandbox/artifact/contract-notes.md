---
record_kind: retrieval_receipt_contract_notes
slice_id: 2026-06-15-p0-01-retrieval-receipt-template-sandbox
status: draft_for_review
truth_boundary: sandbox_contract_notes_only
---

# Contract Notes

## Minimal Required Fields

The template must keep these fields visible:

- `record_kind: retrieval_receipt`
- `query_id`
- `query_time`
- `query_mode`
- `requested_authority_bucket`
- `included_buckets`
- `excluded_buckets`
- `rrf_scope: same_authority_bucket_only`
- `retrieval_engines`
- `retrieval_filters`
- `selected_items`
- `excluded_items`
- `support_checks`
- `warnings`
- `gaps`
- `support_boundary`

## Future Validator Hints

These hints are for later slices only. They are not implemented here.

Future validator should fail when:

- `rrf_scope` is not `same_authority_bucket_only`.
- a candidate, overlay, feedback event, or source annotation has
  `pack_role: support`.
- `legacy_raw_metadata` is true.
- `scores_are_support` is true.
- `url_only_not_direct_support` is false.
- support result is `supported` but `independent_anchor_ref` is missing.
- a feedback item changes truth confidence, verification status, source
  reliability, reviewed note, or reviewed relation.

## Boundary Wording To Preserve

Use this wording in later slices:

```text
Retrieval can decide what to inspect next.
Retrieval cannot decide what to believe or act on.
```

## Why This Is Not Overbuilt

The artifact is a static Markdown/YAML contract with fixtures. It avoids:

- parser implementation;
- schema migration;
- vector or graph runtime;
- MCP writes;
- Obsidian integration;
- long-running services;
- automatic promotion.

That keeps it small enough for P0-01 while still reusable by the next validator
and read-only query-loop slices.
