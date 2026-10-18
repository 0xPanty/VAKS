---
type: source
status: source-captured
title: "TruLens Feedback API and RAG Triad"
source_id: trulens-feedback-rag-triad-2026
source_uri: https://www.trulens.org/reference/trulens/feedback/
source_url: https://www.trulens.org/reference/trulens/feedback/
source_type: official_documentation
platform: web
author: "TruLens / TruEra"
publisher: TruLens
published_at:
updated_at:
captured_at: 2026-06-06
captured_by: Codex
raw_location: raw/articles/2026-06-06-trulens-feedback-rag-triad-source.md
processing_mode: public-web-read
processing_level: medium
review_priority: normal
review_owner: Codex
formalization_status: raw-only
source_status: active
confidence_cap_reason: "Official docs/API reference read from public web; evaluator metrics are diagnostics, not VAKS truth support."
related_urls:
  - https://www.trulens.org/getting_started/core_concepts/rag_triad/
topics:
  - rag-evaluation
  - feedback-functions
  - context-relevance
  - groundedness
  - answer-relevance
  - evaluator-boundary
  - claim-level-support
projects:
  - verified-action-knowledge-system
candidate_relation_suggestions:
  - candidate:rag_triad_as_diagnostic_separation
  - candidate:groundedness_as_claim_level_context_support_check
  - candidate:evaluator_score_not_truth_confidence
tags:
  - raw-article
  - trulens
  - rag-evaluation
  - groundedness
  - candidate-only
---

# Source Record: TruLens Feedback API and RAG Triad

## Why Saved

The user provided the TruLens feedback API reference as part of a retrieval-layer
source batch. The API reference exposes evaluator functions, and the related
TruLens RAG Triad page gives the conceptual split that matters for VAKS:

```text
context relevance
groundedness
answer relevance
```

This source is relevant because VAKS is currently separating:

```text
retrieval activation
-> context pack construction
-> answer/use draft
-> claim/evidence support and warrant gate
```

TruLens supports the same high-level separation, but VAKS must keep evaluator
scores diagnostic-only.

## Source Boundary

```text
Official docs = external source provenance.
This card = raw/source record.
Extraction note = candidate comprehension.
Candidate points = review input only.
No reviewed VAKS knowledge is created by this record.
```

## What Was Observed

The RAG Triad page says RAG can still hallucinate when retrieval fails or
irrelevant context is used in the response. It defines three evaluations:

```text
context relevance:
  whether retrieved chunks are relevant to the input query

groundedness:
  whether response claims are supported by retrieved context

answer relevance:
  whether the final response helps answer the user input
```

The feedback API reference includes `groundedness_measure_with_cot_reasons`,
which takes `source` and `statement`, splits statements into component
sentences, and uses an LLM provider to check support with reasons.

## VAKS Candidate Signals

Potential candidate knowledge points:

```text
rag_triad_as_diagnostic_separation:
  query-run receipts should separate context relevance, groundedness, and answer
  relevance diagnostics.

groundedness_as_claim_level_context_support_check:
  groundedness should operate closer to sentence/claim level than whole-answer
  vibes.

evaluator_score_not_truth_confidence:
  an evaluator score can guide review or debugging, but cannot create reviewed
  truth, reviewed relation, action readiness, or evidence support by itself.
```

## Not Adopted Yet

Do not treat this source as:

```text
permission to add universal truth confidence scores
permission to let LLM judges approve action basis
proof that retrieved context is complete
proof that groundedness equals correctness outside the context
replacement for v0.2.13 warrant gate
```

## Related Candidate Extraction

```text
outputs/review/2026-06-06-rag-eval-tracing-citation-rrf-batch-candidate-distillation.md
```
