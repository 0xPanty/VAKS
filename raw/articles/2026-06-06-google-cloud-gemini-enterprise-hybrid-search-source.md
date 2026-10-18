---
type: source
status: source-captured
title: "混合搜索简介"
source_id: google-cloud-gemini-enterprise-hybrid-search-2026
source_uri: https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/vector-search/about-hybrid-search
source_url: https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/vector-search/about-hybrid-search?hl=zh-cn
source_type: official_documentation
platform: web
author: "Google Cloud Documentation"
publisher: Google Cloud
published_at:
updated_at: 2026-06-05
captured_at: 2026-06-06
captured_by: Codex
raw_location: raw/articles/2026-06-06-google-cloud-gemini-enterprise-hybrid-search-source.md
processing_mode: public-web-read
processing_level: medium
review_priority: normal
review_owner: Codex
formalization_status: raw-only
source_status: active
confidence_cap_reason: "Official documentation read from public web; Chinese page notes AI translation may contain errors; product details are Google-specific."
topics:
  - hybrid-search
  - vector-search
  - semantic-search
  - token-search
  - sparse-retrieval
  - bm25
  - splade
  - rrf
  - rerank
  - retrieval-profile
projects:
  - verified-action-knowledge-system
candidate_relation_suggestions:
  - candidate:hybrid_search_as_default_recall_baseline
  - candidate:exact_match_branch_for_codenames_and_identifiers
  - candidate:rrf_fuses_incomparable_retrieval_ranks
  - candidate:alpha_as_retrieval_profile_knob
  - candidate:hybrid_rerank_as_two_stage_retrieval
tags:
  - raw-article
  - google-cloud
  - gemini-enterprise
  - hybrid-search
  - retrieval
  - candidate-only
---

# Source Record: Google Cloud Gemini Enterprise Hybrid Search

## Why Saved

This Google Cloud documentation is relevant to the VAKS retrieval/query contract
because it states a production-search reason for hybrid retrieval:

```text
semantic/vector search is strong for meaning
keyword/token search is strong for exact identifiers
hybrid search combines both
RRF can merge ranks from retrieval methods with different score scales
an alpha-style retrieval profile can tune keyword/vector balance
reranking can be applied after the initial hybrid result set
```

For VAKS, this especially matters because the vault contains many exact or
near-exact identifiers:

```text
file paths
headings
source IDs
version strings
schema names
architecture terms
project code names
tool/script names
```

These are often poor semantic-only targets but excellent lexical/token targets.

## Source Boundary

```text
Official Google Cloud documentation = external source provenance.
This card = raw/source record.
Extraction note = candidate comprehension.
Candidate points = review input only.
No reviewed VAKS knowledge is created by this record.
```

## Translation / Product Caveat

The Chinese documentation page notes that Google uses AI translation and that
translations can contain errors. Treat exact wording as translation-sensitive.

Also, the page describes Google Cloud / Gemini Enterprise product behavior. VAKS
should borrow the retrieval design idea, not the product dependency.

## What Was Observed

The page defines hybrid search as a common IR pattern that combines:

```text
semantic search / vector search
keyword search / token-based search
```

It explains that semantic search does not cover all retrieval requirements.
Examples where semantic search can be weak include:

```text
arbitrary product numbers or SKU
new product names
company-proprietary code names
out-of-domain data
```

The page also describes token-based search through sparse methods such as:

```text
TF-IDF
BM25
SPLADE
```

For result fusion, the page describes Reciprocal Rank Fusion:

```text
RRF combines rankings from vector search and keyword search.
RRF relies on rank positions rather than raw score comparison.
This is useful because different search methods produce scores on different scales.
```

The page also describes a balance knob:

```text
alpha = 0 means keyword-only
alpha = 1 means vector-only
default alpha is 0.5
```

And it points to reranking after hybrid search as a later-stage quality step.

## VAKS Candidate Signals

Potential candidate knowledge points:

```text
hybrid_search_as_default_recall_baseline:
  default recall should include lexical/token and semantic/vector channels.

exact_match_branch_for_codenames_and_identifiers:
  exact identifiers need lexical/token retrieval rather than dense-only search.

rrf_fuses_incomparable_retrieval_ranks:
  fusion should avoid pretending raw BM25, vector, sparse, and reranker scores
  share one truth scale.

alpha_as_retrieval_profile_knob:
  keyword/vector balance belongs in retrieval profile configuration, not in
  truth confidence.

hybrid_rerank_as_two_stage_retrieval:
  initial hybrid recall can be followed by reranking, provided rerank signals
  remain activation/diagnostic signals.
```

## Not Adopted Yet

Do not treat this article as:

```text
permission to use Google Cloud as VAKS infrastructure
evidence that one alpha value is universally correct
evidence that RRF rank or rerank score is truth confidence
permission to collapse activation score into evidence support
permission to remove claim-level anchors or warrant checks
```

## Related Candidate Extraction

```text
outputs/review/2026-06-06-vaks-retrieval-external-source-extractions.md
outputs/review/2026-06-06-google-cloud-gemini-enterprise-hybrid-search-candidate-distillation.md
outputs/review/2026-06-06-vaks-retrieval-candidate-knowledge-index.md
```
