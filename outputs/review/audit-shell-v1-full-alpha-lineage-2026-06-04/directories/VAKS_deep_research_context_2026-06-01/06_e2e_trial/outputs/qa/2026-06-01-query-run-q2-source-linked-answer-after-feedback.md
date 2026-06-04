---
record_type: query-run
status: archived
created: 2026-06-01
updated: 2026-06-01
query_id: q2-source-linked-answer-after-feedback
session_id: vaks-e2e-trial-001
turn_id: step4
parent_query_id: q1-citation-action-basis
question_summary: "Can a source-linked LLM answer be treated as verified?"
verbatim_input: "If an LLM answer links sources, can VAKS treat it as verified?"
model_interpretation: "User asks whether source links are enough for reviewed / verified status."
query_intent: answer
query_scope:
  project: verified-action-knowledge-system
  domain: citation-backed answer review
  version: v0.3
  time_range: 2026-06-01
scope_key: v0.3-citation-support
inferred_keywords:
  - source links
  - verified support
  - citation
  - source span
seed_points:
  - fine_grained_citation_support_needed
  - citation_quality_is_separate_review_dimension
expansion_depth: small
activated_points:
  - wiki/claims/2026-06-01-fine-grained-citation-support-needed.md
  - wiki/claims/2026-06-01-citation-quality-needs-separate-review.md
activated_relations:
  - collision-citation-support-001
activated_routes:
  - evidence_support
  - source_span_boundary
  - verification_status_boundary
included_sources:
  - source-gophercite-2203-11147
  - source-front-2408-04568
  - source-alce-2305-14627
excluded_candidates:
  - "ALCE benchmark metric details not needed for this wording."
answer_path:
  - "Apply feedback: distinguish source-linked from source-supported."
  - "Use fine-grained support claim first."
  - "Answer verification question before action-readiness question."
warnings:
  - source_link_not_support
  - abstract_only_trial_evidence
gaps:
  - "No main-vault source-span rule copied into scratch as a local claim."
feedback_summary:
  positive_feedback:
  negative_feedback: "Q1 was too action-basis shaped."
  explicit_correction:
  review_pressure: "Future packs may need a local VAKS boundary claim."
  review_due_created: false
decision_outcome:
  decision_ref:
  recommendation: "Do not treat source-linked answer as verified without source-span support and review."
  confidence_at_decision: medium
  user_choice:
  outcome: unresolved
intent_confirmation:
  required: false
  user_confirmed:
tags:
  - query-run
  - feedback
  - e2e-trial
---

# Query Run Q2: After Feedback

## What Was Asked

If an LLM answer links sources, can VAKS treat it as verified?

## Activation Change

Compared with Q1, this run activated:

```text
source-linked vs source-supported vs verified
```

before:

```text
action-basis-ready
```

This is a scope-fit improvement caused by the feedback event.

## Answer

No. Source links are provenance. They become support only when the linked source span actually supports the target point. They become reviewed / verified only after review. They become action-basis-ready only after coverage and evidence sufficiency checks for that use.

## What Changed Because of Feedback

- The answer opened with the source-link boundary instead of action readiness.
- GopherCite and FRONT became the first activated sources because they speak more directly to specific evidence and fine-grained verification.
- ALCE remained support, but its benchmark-metric details were not pulled into the answer.

## Remaining Gap

The feedback improved activation shape, but it did not automatically create a local VAKS boundary claim. If this pattern matters, the vault may need a small reviewed local claim or concept note in a future mainline pass.

