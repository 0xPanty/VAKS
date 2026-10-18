---
record_kind: sandbox_report
slice_id: 2026-06-16-p2-51-user-decision-request-packet-sandbox
report: next-step
status: pass_product_grade_pending_user_question
---

# Next Step

This slice has `PASS_PRODUCT_GRADE`.

The packet may be shown to the user as a question:

```text
请选择 VAKS sandbox 下一步：

A. Keep sandbox as reference only.
B. Authorize a new read-only promotion review planning slice.
C. Authorize asking for a separately scoped mainline merge review.
D. Park or reject the sandbox chain.
```

Important: showing this question is not approval. If the user chooses B or C, start a new scoped turn/slice with a fresh开工卡. Do not execute any option from this slice.
