---
type: candidate_distillation
status: candidate_only
created_at: 2026-06-06
scope: Google Cloud Gemini Enterprise Hybrid Search -> VAKS retrieval/query contract
truth_boundary: candidate points only; not reviewed knowledge; not architecture decision; not action basis
source_ref: raw/articles/2026-06-06-google-cloud-gemini-enterprise-hybrid-search-source.md
---

# Google Cloud Gemini Enterprise Hybrid Search Candidate Distillation

## Chain

This file tests the VAKS flow:

```text
external official documentation
-> source record
-> source extraction
-> candidate points
-> possible general knowledge point candidates
-> tags / indexes / project borrowing view
```

Boundary:

```text
This is candidate distillation.
It does not create reviewed claims, reviewed patterns, or action basis.
```

## General Knowledge Candidate Judgment

Overall judgment:

```text
yes, this source contains reusable general knowledge point candidates.
```

Reason:

```text
The product-specific implementation is Google Cloud Vector Search / Gemini
Enterprise, but the retrieval architecture ideas are broader: semantic search
and token/keyword search cover different failure modes, RRF is useful when raw
scores are not comparable, alpha-style balancing belongs in retrieval
configuration, and reranking is a later-stage activation refinement.
```

## Candidate Points

### CP-001: Hybrid Search As Default Recall Baseline

```yaml
candidate_id: cp-google-hybrid-search-as-default-recall-baseline
point_text: "Default recall should include lexical/token and semantic/vector channels because they cover different retrieval failure modes."
candidate_general_knowledge: true
proposed_node_type: pattern
review_route: rationale_check
source_ref: raw/articles/2026-06-06-google-cloud-gemini-enterprise-hybrid-search-source.md
source_anchor:
  url: https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/vector-search/about-hybrid-search?hl=zh-cn
  section: "Why hybrid search matters"
evidence_granularity: official_doc_section
promotion_readiness: not_ready
```

VAKS borrow scope:

```text
Make hybrid recall the likely default candidate baseline for the retrieval
contract: lexical/token + semantic/vector + metadata filters, fused before
pack compilation.
```

Non-borrow scope:

```text
Do not treat hybrid recall as evidence support or as an adopted infrastructure
decision.
```

Candidate tags:

```text
hybrid-search, lexical-retrieval, semantic-retrieval, retrieval-baseline
```

### CP-002: Exact Match Branch For Codenames And Identifiers

```yaml
candidate_id: cp-google-exact-match-branch-for-codenames-and-identifiers
point_text: "Exact identifiers, codenames, SKUs, file paths, headings, and version strings need lexical/token retrieval rather than dense-only retrieval."
candidate_general_knowledge: true
proposed_node_type: pattern
review_route: rationale_check
source_ref: raw/articles/2026-06-06-google-cloud-gemini-enterprise-hybrid-search-source.md
source_anchor:
  url: https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/vector-search/about-hybrid-search?hl=zh-cn
  section: "Why combine semantic search with keyword search"
evidence_granularity: official_doc_section
promotion_readiness: not_ready
```

VAKS borrow scope:

```text
Use lexical/token branches for VAKS-specific identifiers such as SCHEMA.md,
v0.2.13, source IDs, script names, heading names, project terms, and exact
file paths.
```

Non-borrow scope:

```text
Do not assume semantic/vector search can recover all internal vocabulary.
Do not let exact-match hits become evidence support without selector anchors.
```

Candidate tags:

```text
exact-match, identifiers, codenames, file-paths, lexical-retrieval
```

### CP-003: RRF Fuses Incomparable Retrieval Ranks

```yaml
candidate_id: cp-google-rrf-fuses-incomparable-retrieval-ranks
point_text: "RRF is useful for hybrid retrieval because it fuses rank positions from methods whose raw scores are not directly comparable."
candidate_general_knowledge: true
proposed_node_type: concept
review_route: rationale_check
source_ref: raw/articles/2026-06-06-google-cloud-gemini-enterprise-hybrid-search-source.md
source_anchor:
  url: https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/vector-search/about-hybrid-search?hl=zh-cn
  section: "Reciprocal Rank Fusion"
evidence_granularity: official_doc_section
promotion_readiness: not_ready
```

VAKS borrow scope:

```text
Use rank-position fusion in the retrieval layer when combining lexical,
semantic, sparse, metadata, or other channels. Record fused rank as activation
metadata.
```

Non-borrow scope:

```text
Do not compare raw channel scores as if they shared one confidence scale.
Do not treat fused rank as truth confidence.
```

Candidate tags:

```text
rrf, rank-fusion, hybrid-search, activation-boundary
```

### CP-004: Alpha As Retrieval Profile Knob

```yaml
candidate_id: cp-google-alpha-as-retrieval-profile-knob
point_text: "Keyword/vector balance should be an explicit retrieval-profile knob rather than an implicit truth or confidence signal."
candidate_general_knowledge: true
proposed_node_type: concept
review_route: rationale_check
source_ref: raw/articles/2026-06-06-google-cloud-gemini-enterprise-hybrid-search-source.md
source_anchor:
  url: https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/vector-search/about-hybrid-search?hl=zh-cn
  section: "Hybrid search alpha"
evidence_granularity: official_doc_section
promotion_readiness: not_ready
```

VAKS borrow scope:

```text
Represent keyword/vector balance as `retrieval_profile`, for example:
identifier-heavy, balanced, semantic-heavy, or exploratory.
```

Non-borrow scope:

```text
Do not copy Google alpha values as universal defaults before VAKS has its own
fixtures and query-run feedback.
```

Candidate tags:

```text
retrieval-profile, alpha, hybrid-search, query-config
```

### CP-005: Hybrid Rerank As Two-Stage Retrieval

```yaml
candidate_id: cp-google-hybrid-rerank-as-two-stage-retrieval
point_text: "Hybrid recall can feed a later reranking stage, but rerank output remains activation or diagnostic metadata."
candidate_general_knowledge: true
proposed_node_type: pattern
review_route: rationale_check
source_ref: raw/articles/2026-06-06-google-cloud-gemini-enterprise-hybrid-search-source.md
source_anchor:
  url: https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/vector-search/about-hybrid-search?hl=zh-cn
  section: "Reranking after hybrid search"
evidence_granularity: official_doc_section
promotion_readiness: not_ready
```

VAKS borrow scope:

```text
Keep the retrieval funnel as recall first, then rerank, then pack compile.
Use oversampling so reranker can see enough candidates.
```

Non-borrow scope:

```text
Do not let rerank score replace source selector, quote window, warrant, or
claim-level evidence binding.
```

Candidate tags:

```text
rerank, two-stage-retrieval, retrieval-funnel, evidence-boundary
```

## Minimal VAKS Design Implications

If promoted later, this source would strengthen the retrieval contract in these
places:

```text
planner_output:
  retrieval_profile: identifier-heavy | balanced | semantic-heavy | exploratory

retrievers_called:
  lexical_or_token:
  semantic_or_vector:
  metadata_filter:

fusion_method:
  rrf or equivalent rank-position fusion

pack_item:
  matched_channels:
  channel_ranks:
  fused_rank:
  rerank_score:
  citable_status:
```

Boundary sentence to preserve:

```text
Hybrid rank, alpha, RRF position, and rerank score are activation or diagnostic
signals only unless linked to explicit source anchors and a claim-level warrant.
```

## What VAKS Should Not Borrow Yet

Do not turn this into:

```text
Google Cloud dependency
one universal alpha setting
RRF rank as confidence
semantic-only retrieval
rerank score as evidence
product-specific limitation as VAKS architecture rule
```

## Adoption Judgment

```text
adopt:
  hybrid retrieval as a strong candidate baseline for recall

adapt:
  alpha-style balance into VAKS retrieval profiles
  RRF into an activation-only fusion receipt

watch:
  exact values and product implementation details until VAKS has real query-run data

reject for core:
  treating fused rank, alpha, or rerank score as truth confidence
```
