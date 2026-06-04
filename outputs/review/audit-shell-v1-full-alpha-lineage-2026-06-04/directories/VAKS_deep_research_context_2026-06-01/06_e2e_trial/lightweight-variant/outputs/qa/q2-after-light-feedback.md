---
record_type: query-run-light
status: archived
created: 2026-06-01
variant: lightweight
query_id: q2-light-source-linked-answer
parent_query_id: q1-citation-action-basis
---

# Q2 After Lightweight Feedback

## Question

If an LLM answer links sources, can VAKS treat it as verified?

## Activated Because Of Feedback

```text
source-linked vs source-supported vs reviewed vs action-ready
```

Primary activated claims:

```text
mini-fine-grained-citation-support-needed
mini-citation-quality-needs-separate-review
```

## Answer

No. A source link is provenance. It becomes support only when a current source span supports the target point. It becomes reviewed / verified only after review. It becomes action-ready only after coverage and evidence sufficiency for that use.

## Scope-Fit Change From Q1

Q1 started from action readiness.

Q2 starts from source support and verification status, which better matches the wording.

## Remaining Gap

This is still manually recorded. No runtime proved activation changed.

