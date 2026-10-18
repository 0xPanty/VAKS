---
type: source
status: source-captured
title: "Agentic retrieval in Azure AI Search"
source_id: microsoft-azure-ai-search-agentic-retrieval-2026
source_uri: https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview
source_url: https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview?tabs=quickstarts
source_type: official_documentation
platform: web
author: "Microsoft Learn"
publisher: Microsoft
published_at:
updated_at: 2026-06-02
captured_at: 2026-06-06
captured_by: Codex
raw_location: raw/articles/2026-06-06-microsoft-azure-ai-search-agentic-retrieval-source.md
processing_mode: public-web-read
processing_level: medium
review_priority: normal
review_owner: Codex
formalization_status: raw-only
source_status: active-with-preview-caveats
confidence_cap_reason: "Official documentation read via web extraction; product features include GA and preview boundaries."
topics:
  - agentic-retrieval
  - azure-ai-search
  - query-planning
  - subquery-decomposition
  - parallel-retrieval
  - semantic-reranking
  - retrieval-receipt
  - activity-plan
  - grounding-data
  - context-pack
projects:
  - verified-action-knowledge-system
candidate_relation_suggestions:
  - candidate:query_plan_as_retrieval_output
  - candidate:parallel_subquery_retrieval
  - candidate:modular_retrieval_response
  - candidate:activity_plan_as_retrieval_receipt
  - candidate:agentic_retrieval_cost_governance
tags:
  - raw-article
  - microsoft
  - azure-ai-search
  - agentic-retrieval
  - retrieval
  - candidate-only
---

# Source Record: Azure AI Search Agentic Retrieval

## Why Saved

This Microsoft Learn article is relevant to the VAKS retrieval/query contract
because it describes agentic retrieval as a multi-query pipeline for complex
questions. It includes several design ideas directly useful to VAKS:

```text
LLM-based query planning
subquery decomposition
parallel subquery execution
hybrid retrieval over text/vector fields
semantic reranking
modular response with query plan, source documents, and activity plan
cost / latency awareness
```

## Source Boundary

```text
Official Microsoft documentation = external source provenance.
This card = raw/source record.
Extraction note = candidate comprehension.
Candidate points = review input only.
No reviewed VAKS knowledge is created by this record.
```

## Product / Version Caveat

The page states that some features are generally available through the
`2026-04-01` REST API, while other capabilities remain in preview through
`2026-05-01-preview`.

VAKS should treat product availability and API details as time-sensitive.

## What Was Observed

The article describes agentic retrieval as:

```text
complex user/agent query
-> LLM query planning
-> focused subqueries
-> parallel query execution
-> keyword/vector/hybrid search
-> semantic reranking per subquery
-> unified retrieval response
```

The response includes:

```text
grounding data for the next conversation turn
reference data / source documents for inspection
activity plan showing query execution steps
```

The page also emphasizes cost/latency tradeoffs:

```text
agentic retrieval adds latency
query planning and reranking consume tokens
activity logs help inspect issued queries and parameters
reasoning effort / fan-out / number of sources affect cost
```

## VAKS Candidate Signals

Potential candidate knowledge points:

```text
query_plan_as_retrieval_output:
  query planning should be a visible retrieval artifact, not hidden prompt logic.

parallel_subquery_retrieval:
  complex questions can be decomposed into focused subqueries that run in
  parallel.

modular_retrieval_response:
  retrieval output should separate grounding data, source/reference data, and
  execution details.

activity_plan_as_retrieval_receipt:
  query execution steps should be inspectable as a receipt/trace.

agentic_retrieval_cost_governance:
  planner complexity, fan-out, reasoning effort, rerank window, and source
  count should be visible cost/latency controls.
```

## Not Adopted Yet

Do not treat this article as:

```text
permission to make agentic retrieval always-on
proof that Azure's knowledge base object should be copied into VAKS
evidence that preview APIs are stable architecture dependencies
permission to treat retrieval response as reviewed truth
action basis for implementing Azure AI Search
```

## Related Candidate Extraction

```text
outputs/review/2026-06-06-vaks-retrieval-external-source-extractions.md
outputs/review/2026-06-06-microsoft-azure-ai-search-agentic-retrieval-candidate-distillation.md
outputs/review/2026-06-06-vaks-retrieval-candidate-knowledge-index.md
```

