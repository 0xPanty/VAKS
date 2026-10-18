---
type: source
record_kind: source_card
status: source-captured
title: "LightRAG: Simple and Fast Retrieval-Augmented Generation"
source_id: 2026-05-29-lightrag-source
source_uri: https://arxiv.org/abs/2410.05779
source_url: https://arxiv.org/abs/2410.05779
source_type: paper
version_or_commit: arXiv:2410.05779v3 / HKUDS LightRAG repository checked 2026-05-29
captured_at: 2026-05-29
captured_by: Codex
review_priority: normal
review_owner: Codex
formalization_status: candidate-generated
topics:
  - retrieval
  - graph-rag
  - dual-level-retrieval
  - incremental-index
  - context-activation
projects:
  - verified-action-knowledge-system
verification_status: primary-source-captured
candidate_relation_suggestions: []
tags:
  - lightrag
  - graph-retrieval
  - retrieval-stratification
knowledge_status: raw
processing_tier: light
why_saved: see_body_or_legacy_record
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
---

# LightRAG Source Record

## Why Captured

LightRAG is a useful reference for lightweight graph-based retrieval.
It supports the idea that retrieval can combine graph structure with vector retrieval and separate low-level from high-level discovery.

## Source Identity

```text
Paper: LightRAG: Simple and Fast Retrieval-Augmented Generation
arXiv: https://arxiv.org/abs/2410.05779
Repository: https://github.com/HKUDS/LightRAG
```

## Extracted Architecture Point

LightRAG's useful lesson is not its runtime.
The useful point is the retrieval shape:

```text
graph structures help reveal cross-chunk dependencies
dual-level retrieval separates low-level detail from high-level knowledge discovery
incremental updates keep retrieval indexes current
```

## Adopt

```text
low-level / high-level retrieval distinction
graph structure as a recall aid for cross-chunk dependencies
incremental retrieval index updates as cache maintenance inspiration
combine graph and vector retrieval as candidate recall
```

## Do Not Adopt

```text
full LightRAG runtime as core architecture
graph extraction as reviewed knowledge
retrieval score as trust
high-level generated summary as truth
incremental index update as automatic truth update
```

## Fit To Current Architecture

Place in:

```text
Retrieval / cache
Activation / Context Activation
Association Neighborhood Activation
Context Pack preparation
future derived index maintenance
```

Do not place in:

```text
Truth Core
Review authority
Evidence Support Check
Evidence Sufficiency Gate
Reviewed Relations
Source reliability
```

## Review Notes

This source should be presented to Pro review as supplement 13.3 together with GraphRAG.

The intended absorption is intentionally small:

```text
Retrieval may be graph-aware and multi-level.
Truth remains source-backed, reviewed, and evidence-gated.
```
