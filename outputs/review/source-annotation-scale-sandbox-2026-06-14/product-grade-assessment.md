---
record_kind: sandbox_product_grade_assessment
status: complete
created_at: 2026-06-14
scope: source-annotation-product-grade-verdict
truth_boundary: sandbox_recommendation_not_main_architecture
---

# Product-Grade Assessment

## Direct Verdict

This is now a product-grade pilot design.

It is not yet a production-operated product.

Plainly:

```text
safe to pilot: yes
safe to use for a long time with gates: yes
safe to call proven production: not yet
```

## Why It Will Not Rot Like Old Tags

The old risk was:

```text
every useful thing becomes another loose sticky/tag
```

The new design avoids that by splitting the system into operational lanes:

```text
working inbox = what a human handles now
locator pool = stable annotation memory
repair queue = broken or ambiguous anchors
stale queue = old anchors that need refresh
source health = source-level load and digest status
AI review-input pack = bounded context, not proof
```

So growth does not mainly create a larger human inbox. Growth mostly enters the
locator pool and source-health dashboard.

## Long-Run Safety Mechanisms

The design has tested controls for:

```text
bad anchors
stale anchors
duplicate ids
malformed selectors
annotation-as-support misuse
annotation-as-action-basis misuse
project borrow verdict pollution
oversized AI context packs
single-source context dominance
dense source scale debt
missing next actions
missing blocked reasons
```

## Latest Quantitative Evidence

Updated enterprise gate:

```text
5,000 annotations: passed in 3.848s
10,000 annotations: passed in 8.364s
mutations caught: 29 / 29
bad context packs caught: 5 / 5
AI contamination: 0
10k working inbox: 303
10k locator pool: 9,088
10k context pack: 60 items, 24 sources, max 5 per source
source digest backlog: 9
digest backlog p95 age: 14 days
```

Long-run workflow simulation:

```text
180 simulated days
16,820 final annotations
working inbox stayed bounded
flat inbox baseline became unusable
```

## What Still Needs Real Use

Synthetic tests cannot prove:

```text
real Obsidian Bases comfort
real PDF / OCR / ASR / video anchor drift
human repair habits
backup and sync behavior with thousands of files
whether source digests are actually maintained
```

Those are pilot questions, not architecture blockers.

## Final Level

Use this label:

```text
L4 product-grade pilot design
```

Do not use this label yet:

```text
L5 production-operated product
```

