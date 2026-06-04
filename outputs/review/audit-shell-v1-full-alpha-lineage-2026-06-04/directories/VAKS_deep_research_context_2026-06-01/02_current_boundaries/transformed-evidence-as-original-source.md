---
type: anti-pattern
status: active
created: 2026-06-01
updated: 2026-06-01
domain: evidence-review
failure_mode: "Treating OCR, translation, bbox, layout, or table-derived text as original source support without a recoverable original anchor."
severity: 4
likelihood: 3
complexity_cost: 2
related_projects:
  - verified-action-knowledge-system
replacement:
  - evidence item with original source anchor
  - transformed evidence marked as review input
  - original page / table cell / image region / passage anchor before promotion or action basis
verification_status: reviewed
evidence_level: synthetic
confidence: medium
last_verified: 2026-06-01
next_review: 2026-06-15
epistemic_type: take
relations:
  - target: "[[REVIEW_QUEUE]]"
    type: risk_of
    strength: 4
    confidence: medium
    evidence:
      - "[[transformed-evidence-as-original-source]]"
    rationale: "Transformed evidence can look source-backed while hiding OCR, translation, layout, or extraction errors."
    created: 2026-06-01
    last_verified: 2026-06-01
decision: avoid
tags:
  - anti-pattern
  - evidence-support
  - source-anchor
  - transformed-evidence
---

# Anti-pattern: Transformed Evidence As Original Source

## AI-readable preamble

OCR text, translated text, bbox snippets, layout-derived text, and table summaries are transformed evidence.

They can help review, but they should not be treated as original source support unless the reviewer can recover the original page, passage, image region, table cell, or equivalent anchor.

This anti-pattern is a narrow evidence-support guardrail. It does not make ordinary capture heavier.

## Problem

Transformed evidence can silently introduce errors:

```text
OCR swaps columns or digits
translation drops a condition
bbox cropping omits a qualifier
layout extraction joins unrelated paragraphs
table summaries hide row / column context
```

If the transformed text is then cited as direct support, the review may appear source-backed while the original evidence no longer supports the point.

## Failure conditions

- OCR output is used as promotion support without the original page / cell / image anchor.
- A translation is used as the only quote for a risk-sensitive answer, but the original passage is not preserved.
- A bbox or layout crop is treated as the whole relevant source context.
- A table summary is cited without row / column / cell identity or the original table anchor.
- A transformed excerpt becomes action-basis evidence even though the transformation process is not reviewable.

## Boundary

This check applies when transformed evidence is used for:

```text
promotion
strong reviewed relation
decision
context pack / action basis
risk-sensitive answer
explicit evidence challenge
```

It should not run for ordinary source capture, ordinary summaries, or low-risk browsing notes.

## Replacement

Keep the transformed artifact as review input, then anchor it back to the original:

```text
transformed text
-> original source / page / passage / table cell / image bbox
-> evidence_support check
-> promotion or action use only if the original anchor supports the point
```

If the original anchor cannot be recovered, keep the point as candidate material, weak support, or a review question.

## Non-goals

- Do not add OCR / translation / bbox fields to `SCHEMA.md` yet.
- Do not require bbox or OCR metadata for ordinary capture.
- Do not treat transformation error as automatic falsification.
- Do not create a new evidence-processing lane.
