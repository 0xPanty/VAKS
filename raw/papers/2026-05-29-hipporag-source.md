---
type: source
record_kind: source_card
status: source-captured
title: "HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models"
source_id: 2026-05-29-hipporag-source
source_uri: https://arxiv.org/abs/2405.14831
source_url: https://arxiv.org/abs/2405.14831
source_type: paper
version_or_commit: arXiv:2405.14831 / NeurIPS 2024
captured_at: 2026-05-29
captured_by: Codex
review_priority: normal
review_owner: Codex
formalization_status: candidate-generated
topics:
  - retrieval
  - association
  - context-activation
  - graph-rag
projects:
  - verified-action-knowledge-system
verification_status: unverified
candidate_relation_suggestions: []
tags:
  - hipporag
  - association-retrieval
  - context-activation
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

# HippoRAG Source Record

## Why Captured

HippoRAG is a conceptual reference for the vault's Association / Context Activation layer.
It supports the wording:

```text
The vault does not retrieve isolated chunks.
It activates an evidence-aware association neighborhood.
```

## Source Identity

- Paper: `HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models`
- arXiv: https://arxiv.org/abs/2405.14831
- NeurIPS page: https://papers.nips.cc/paper_files/paper/2024/hash/6ddc001d07ca4f319af96a3024f6dbd1-Abstract-Conference.html
- Code reference: https://github.com/OSU-NLP-Group/HippoRAG

## Extracted Architecture Point

HippoRAG combines LLM-based extraction, a knowledge graph, and Personalized PageRank-style graph retrieval to support associative retrieval over external knowledge.

For this vault, the useful point is not the full system.
The useful point is the retrieval framing:

```text
query -> activate an association neighborhood
```

## Adopt

```text
association retrieval as context activation
query-triggered neighborhood expansion
support / challenge / risk / decision / scope appearing together
association path as recall explanation
```

## Do Not Adopt

```text
full HippoRAG stack as a core module
LLM-generated graph as the formal reviewed knowledge graph
Personalized PageRank as evidence, support, confidence, or truth
graph traversal as reviewed relation creation
association score as action readiness
```

## Fit To Current Architecture

Place in:

```text
Runtime / Workbench
-> Retrieval / cache
-> Activation / Context Activation
-> draft evidence / context envelope
-> Context Pack
```

Do not place in:

```text
Truth Core
Review authority
Evidence Support Check
Evidence Sufficiency Gate
Reviewed Relations
```

## Review Notes

This source should be presented to Pro review as supplement 9.

The intended absorption is intentionally small:

```text
Association Neighborhood Activation:
  retrieval lights up a reviewed neighborhood;
  review and evidence still decide what can support action.
```
