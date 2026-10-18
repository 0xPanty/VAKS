---
type: source
status: source-captured
title: "Elasticsearch Reciprocal Rank Fusion"
source_id: elastic-rrf-2026
source_uri: https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion
source_url: https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion
source_type: official_documentation
platform: web
author: "Elastic"
publisher: Elasticsearch Reference
published_at:
updated_at:
captured_at: 2026-06-06
captured_by: Codex
raw_location: raw/articles/2026-06-06-elastic-rrf-source.md
processing_mode: public-web-read
processing_level: medium
review_priority: normal
review_owner: Codex
formalization_status: raw-only
source_status: active
confidence_cap_reason: "Official Elasticsearch documentation; RRF is a retrieval-rank fusion method, not evidence support."
topics:
  - rrf
  - reciprocal-rank-fusion
  - hybrid-search
  - bm25
  - knn
  - sparse-vector
  - rank-window
  - activation
projects:
  - verified-action-knowledge-system
candidate_relation_suggestions:
  - candidate:rrf_as_rank_position_fusion
  - candidate:rank_window_as_oversampling_control
  - candidate:rrf_rank_not_evidence_support
tags:
  - raw-article
  - elasticsearch
  - rrf
  - hybrid-search
  - candidate-only
---

# Source Record: Elasticsearch Reciprocal Rank Fusion

## Why Saved

This Elastic documentation is relevant to VAKS because it gives a concrete,
production-facing definition of RRF as a way to combine results from multiple
retrievers.

For VAKS, RRF matters because lexical, semantic, sparse, metadata, and graph
branches produce scores that should not be naively mixed as one confidence
scale.

## Source Boundary

```text
Official docs = external source provenance.
This card = raw/source record.
Extraction note = candidate comprehension.
Candidate points = review input only.
No reviewed VAKS knowledge is created by this record.
```

## What Was Observed

Elastic describes RRF as combining and ranking documents from separate child
retrievers. It requires at least two child retrievers and uses rank positions
with parameters such as `rank_constant` and `rank_window_size`.

The docs show combinations such as kNN plus standard search, and standard BM25
plus sparse-vector retrieval. They also note that some search features are not
supported under RRF.

## VAKS Candidate Signals

Potential candidate knowledge points:

```text
rrf_as_rank_position_fusion:
  use rank positions to fuse heterogeneous retrieval channels.

rank_window_as_oversampling_control:
  first-stage retrievers should feed a sufficiently wide candidate window before
  pack selection or rerank.

rrf_rank_not_evidence_support:
  RRF output order is activation metadata, not support strength or truth.
```

## Not Adopted Yet

Do not treat this source as:

```text
Elasticsearch adoption decision
proof that RRF is best for every query
evidence support
truth confidence
replacement for rerank or claim/evidence binding
```

## Related Candidate Extraction

```text
outputs/review/2026-06-06-rag-eval-tracing-citation-rrf-batch-candidate-distillation.md
```
