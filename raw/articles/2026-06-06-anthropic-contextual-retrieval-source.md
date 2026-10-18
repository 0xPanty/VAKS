---
type: source
status: source-captured
title: "Introducing Contextual Retrieval"
source_id: anthropic-contextual-retrieval-2024
source_uri: https://www.anthropic.com/engineering/contextual-retrieval
source_url: https://www.anthropic.com/engineering/contextual-retrieval
source_type: article
platform: web
author: "Daniel Ford / Anthropic"
publisher: Anthropic
published_at: 2024-09-19
updated_at:
captured_at: 2026-06-06
captured_by: Codex
raw_location: raw/articles/2026-06-06-anthropic-contextual-retrieval-source.md
processing_mode: public-web-read
processing_level: medium
review_priority: normal
review_owner: Codex
formalization_status: raw-only
source_status: active
confidence_cap_reason: "Public article summary/extraction only; no full local article copy preserved."
topics:
  - contextual-retrieval
  - rag
  - bm25
  - embeddings
  - reranking
  - context-pack
  - retrieval-evaluation
  - activation
projects:
  - verified-action-knowledge-system
candidate_relation_suggestions:
  - candidate:contextualized_retrieval_chunks
  - candidate:hybrid_recall_plus_rerank
  - candidate:context_pack_item_contextualized_snippet
  - candidate:retrieval_eval_failure_to_retrieve
tags:
  - raw-article
  - anthropic
  - retrieval
  - candidate-only
---

# Source Record: Anthropic Contextual Retrieval

## Why Saved

This public Anthropic article is relevant to the VAKS retrieval/query contract
because it provides a concrete retrieval design pattern:

```text
chunk-level document context
+ BM25 / lexical search
+ embedding search
+ rank fusion / deduplication
+ oversampled retrieval
+ reranking
```

It is especially relevant to VAKS because VAKS works with Markdown files,
headings, local paths, project names, version labels, and architecture terms.
Those often require both exact lexical matching and semantic matching.

## Source Boundary

```text
Article = external source provenance.
This card = raw/source record.
Extraction note = candidate comprehension.
Candidate points = review input only.
No reviewed VAKS knowledge is created by this record.
```

## What Was Observed

The article argues that ordinary chunking can remove important document-level
context. Anthropic's proposed method generates a short context string for each
chunk, prepends it to the chunk, and indexes that contextualized chunk for both
embeddings and BM25.

The article also reports retrieval-failure reductions for contextual embeddings,
contextual BM25, and reranking. These reported numbers are source claims, not
VAKS validation.

## VAKS Candidate Signals

Potential candidate knowledge points:

```text
contextualized_retrieval_chunks:
  chunk/index items should preserve document/path/heading context.

hybrid_recall_plus_rerank:
  BM25/lexical and embeddings cover different retrieval failure modes; rerank
  should follow oversampled first-stage retrieval.

context_pack_item_contextualized_snippet:
  pack item should distinguish raw snippet from contextualized snippet.

retrieval_eval_failure_to_retrieve:
  retrieval evaluation can first ask whether relevant anchors appear in the
  candidate pool before judging answer quality.
```

## Not Adopted Yet

Do not treat this article as:

```text
truth confidence for VAKS architecture
proof that a specific embedding provider should be used
permission to make contextualization mandatory for every light source
evidence support for action-facing claims without selector-grade anchor/warrant
```

## Related Candidate Extraction

```text
outputs/review/2026-06-06-vaks-retrieval-external-source-extractions.md
outputs/review/2026-06-06-anthropic-contextual-retrieval-candidate-distillation.md
```

