---
type: source
status: source-captured
title: "From Local to Global: A Graph RAG Approach to Query-Focused Summarization"
source_id: 2026-06-06-microsoft-graphrag-query-focused-summarization-source
source_uri: https://www.microsoft.com/en-us/research/publication/from-local-to-global-a-graph-rag-approach-to-query-focused-summarization/
source_url: https://www.microsoft.com/en-us/research/publication/from-local-to-global-a-graph-rag-approach-to-query-focused-summarization/
source_type: paper
authors:
  - Darren Edge
  - Ha Trinh
  - Newman Cheng
  - Joshua Bradley
  - Alex Chao
  - Apurva Mody
  - Steven Truitt
  - Dasha Metropolitansky
  - Robert Osazuwa Ness
  - Jonathan Larson
publisher: Microsoft Research
venue: Microsoft Research publication page
published_at: 2024-04
captured_at: 2026-06-06
captured_by: Codex
extracted_by: Codex
extracted_at: 2026-06-06
extraction_tool: web
extraction_model: Codex
version_or_commit: Microsoft Research page checked 2026-06-06; related preprint arXiv:2404.16130
source_status: active
raw_location: raw/papers/2026-06-06-microsoft-graphrag-query-focused-summarization-source.md
processing_mode: official-publication-page-read
processing_level: medium
review_priority: normal
review_owner: Codex
formalization_status: source-only
confidence_cap_reason: "Captured from official Microsoft Research publication page; no full PDF deep read in this pass."
topics:
  - graphrag
  - query-focused-summarization
  - global-questions
  - community-summaries
  - entity-graph
  - structure-aware-retrieval
  - context-pack
projects:
  - verified-action-knowledge-system
source_family: microsoft-graphrag-query-focused-summarization
upstream_sources:
  - raw/repos/2026-05-29-graphrag-source.md
verification_status: primary-source-captured
candidate_relation_suggestions:
  - candidate:global_question_as_qfs_mode
  - candidate:community_summary_as_global_briefing
  - candidate:local_to_global_graph_summarization_branch
tags:
  - raw-paper
  - microsoft-research
  - graphrag
  - query-focused-summarization
  - candidate-only
---

# Source Record: Microsoft GraphRAG Query-Focused Summarization

## Why Saved

This Microsoft Research publication page is relevant to the VAKS retrieval/query
contract because it explains the original GraphRAG motivation:

```text
ordinary RAG is good at retrieving explicit local information
global questions over an entire corpus are closer to query-focused summarization
query-focused summarization over large private corpora needs a scalable index
GraphRAG uses entity graphs and community summaries to support global sensemaking
```

For VAKS, this source strengthens the rule that graph/summary retrieval should
be a selective `corpus_global` or `relation_tracing` branch, not a default truth
layer.

## Source Boundary

```text
Official Microsoft Research publication page = external source provenance.
This card = raw/source record.
Extraction note = candidate comprehension.
Candidate points = review input only.
No reviewed VAKS knowledge is created by this record.
```

## Relation To Existing GraphRAG Source

Existing source card:

```text
raw/repos/2026-05-29-graphrag-source.md
```

That older card covers Microsoft GraphRAG repository/documentation behavior.
This card covers the Microsoft Research paper page and the design argument
behind local-to-global query-focused summarization.

## What Was Observed

The page frames a key mismatch:

```text
local retrieval:
  find specific information in source documents

global corpus question:
  summarize themes or patterns across the whole collection
```

The page describes GraphRAG's index shape:

```text
source documents
-> LLM-derived entity knowledge graph
-> community summaries for groups of related entities
```

It also describes the answer shape:

```text
use community summaries to create partial responses
-> summarize partial responses into a final global answer
```

The reported benefit is strongest for global sensemaking questions over large
text collections, particularly in comprehensiveness and diversity of answers.

## VAKS Candidate Signals

Potential candidate knowledge points:

```text
global_question_as_qfs_mode:
  "What are the main themes?" style queries are not ordinary top-k retrieval.

community_summary_as_global_briefing:
  community reports can brief a global question, but they remain derived context.

local_to_global_graph_summarization_branch:
  entity graph + community summaries + partial-response aggregation can be a
  selective retrieval branch for corpus_global questions.
```

## Not Adopted Yet

Do not treat this paper page as:

```text
permission to make GraphRAG the VAKS primary store
permission to treat community summaries as reviewed knowledge
permission to treat graph rank as trust
permission to bypass source selectors, evidence anchors, or v0.2.13 warrant gate
permission to build full Microsoft GraphRAG runtime now
```

## Related Candidate Extraction

```text
raw/repos/2026-05-29-graphrag-source.md
outputs/review/2026-06-06-microsoft-graphrag-query-focused-summarization-candidate-distillation.md
outputs/review/2026-06-06-vaks-retrieval-external-source-extractions.md
outputs/review/2026-06-06-vaks-retrieval-candidate-knowledge-index.md
```
