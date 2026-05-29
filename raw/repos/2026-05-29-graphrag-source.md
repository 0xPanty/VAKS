---
type: source
status: source-captured
title: "Microsoft GraphRAG"
source_id: 2026-05-29-graphrag-source
source_uri: https://microsoft.github.io/graphrag/index/default_dataflow/
source_url: https://microsoft.github.io/graphrag/index/default_dataflow/
source_type: repository-documentation
version_or_commit: GraphRAG docs and microsoft/graphrag repository checked 2026-05-29
captured_at: 2026-05-29
captured_by: Codex
processing_mode: immediate
processing_level: heavy
review_priority: normal
review_owner: Codex
formalization_status: candidate-generated
topics:
  - retrieval
  - graph-rag
  - text-units
  - community-reports
  - context-pack
projects:
  - verified-action-knowledge-system
verification_status: primary-source-captured
candidate_relation_suggestions: []
tags:
  - graphrag
  - retrieval-stratification
  - context-activation
---

# GraphRAG Source Record

## Why Captured

GraphRAG is a useful reference for graph-based retrieval and context preparation.
It is not a truth architecture for this vault.

## Source Identity

```text
Documentation: https://microsoft.github.io/graphrag/index/default_dataflow/
Repository: https://github.com/microsoft/graphrag
Method family: graph-based Retrieval-Augmented Generation
```

GraphRAG's default dataflow includes:

```text
Document
-> TextUnit
-> Entity / Relationship extraction
-> optional Claim extraction
-> Community Detection
-> Community Reports
-> embeddings for downstream search
```

GraphRAG query modes include:

```text
Global Search:
  community reports for whole-dataset themes and patterns

Local Search:
  entity-centered access to text units, relationships, covariates, and reports

DRIFT Search:
  combines community-level starting context with local follow-up exploration
```

## Extracted Architecture Point

For this vault, the useful lesson is graph retrieval stratification:

```text
low-level retrieval:
  source / text unit / claim / entity

high-level retrieval:
  theme / pattern / community / community report

relation neighborhood:
  reviewed relation neighborhood around the query seed
```

This strengthens context activation because a query can gather both concrete evidence anchors and broader thematic context.

## Adopt

```text
TextUnit-style source anchors for traceability
low-level vs high-level retrieval distinction
community / theme reports as context briefings
relation-neighborhood traversal for context activation
global/local style retrieval as context-pack preparation
```

## Do Not Adopt

```text
full GraphRAG runtime as core architecture
community summary as truth
graph rank as trust
auto-extracted entity / relationship as reviewed relation
LLM-derived claim status as vault verification_status
graph extraction bypassing review queue
```

## Fit To Current Architecture

Place in:

```text
Retrieval / cache
Activation / Context Activation
Association Neighborhood Activation
draft evidence / context envelope
Context Pack preparation
```

Do not place in:

```text
Truth Core
Review authority
Evidence Support Check
Evidence Sufficiency Gate
Reviewed Relations
Action readiness
```

## Review Notes

This source should be presented to Pro review as supplement 13.3 together with LightRAG.

The intended absorption is intentionally small:

```text
Graph retrieval can organize what gets recalled.
Review and evidence still decide what can be trusted or used for action.
```
