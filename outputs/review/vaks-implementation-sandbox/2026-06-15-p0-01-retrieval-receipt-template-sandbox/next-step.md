---
record_kind: sandbox_next_step
slice_id: 2026-06-15-p0-01-retrieval-receipt-template-sandbox
status: pass_product_grade_pending_next_slice
truth_boundary: next_step_recommendation_only
---

# Next Step

## If Product Acceptance Passes

The next slice may be:

```text
P0-02 operation receipt template sandbox
```

But do not start it automatically. The next round must first output its own
slice id, rationale, write scope, non-write scope, acceptance standard, and stop
conditions, then wait for user confirmation.

## If Revision Is Required

Stay in this slice. Builder fixes only files under:

```text
outputs/review/vaks-implementation-sandbox/2026-06-15-p0-01-retrieval-receipt-template-sandbox/
```

Then Reviewer, Boundary Auditor, and Product Acceptance must run again.

## If Blocked

Stop and ask the user. Do not route around the block.

## Still Not Mainline

Even with `PASS_PRODUCT_GRADE`, this remains sandbox output. It cannot be merged
into `templates/`, `tools/`, schema, wiki, or Obsidian without separate user
approval.
