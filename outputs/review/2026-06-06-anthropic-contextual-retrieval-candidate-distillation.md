---
type: candidate_distillation
status: candidate_only
created_at: 2026-06-06
scope: Anthropic Contextual Retrieval -> VAKS retrieval/query contract
truth_boundary: candidate points only; not reviewed knowledge; not architecture decision; not action basis
source_ref: raw/articles/2026-06-06-anthropic-contextual-retrieval-source.md
extraction_ref: outputs/review/2026-06-06-vaks-retrieval-external-source-extractions.md
---

# Anthropic Contextual Retrieval Candidate Distillation

## Chain

This file tests the VAKS flow:

```text
external article
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
The extracted ideas are not VAKS-only. They are general retrieval design
patterns that can apply to many Markdown vaults, RAG systems, documentation
search systems, and agent context-pack pipelines.
```

But:

```text
They remain candidate points until reviewed against more sources and VAKS needs.
```

## Candidate Points

### CP-001: Contextualize Chunks Before Indexing

```yaml
candidate_id: cp-anthropic-contextualize-chunks-before-indexing
point_text: "Chunk/index items should carry short document-aware context before retrieval indexing."
candidate_general_knowledge: true
proposed_node_type: pattern
review_route: evidence_check
source_ref: raw/articles/2026-06-06-anthropic-contextual-retrieval-source.md
source_anchor:
  url: https://www.anthropic.com/engineering/contextual-retrieval
  section: "Introducing Contextual Retrieval / Implementing Contextual Retrieval"
evidence_granularity: article_section
promotion_readiness: not_ready
```

VAKS borrow scope:

```text
Use this to justify `contextualized_snippet` / local context fields in pack item
and index item candidates.
```

Non-borrow scope:

```text
Do not treat contextualized retrieval as evidence support or correctness.
```

Candidate tags:

```text
retrieval, contextual-retrieval, context-pack, activation
```

### CP-002: Hybrid Recall Should Be Default Baseline

```yaml
candidate_id: cp-anthropic-hybrid-recall-default
point_text: "BM25/lexical and dense semantic retrieval cover different failure modes and should be combined for robust recall."
candidate_general_knowledge: true
proposed_node_type: pattern
review_route: evidence_check
source_ref: raw/articles/2026-06-06-anthropic-contextual-retrieval-source.md
source_anchor:
  url: https://www.anthropic.com/engineering/contextual-retrieval
  section: "A primer on RAG / BM25 / combining embeddings and BM25"
evidence_granularity: article_section
promotion_readiness: not_ready
```

VAKS borrow scope:

```text
Use as support for a candidate hybrid recall baseline:
BM25/lexical + dense embeddings + rank fusion / deduplication.
```

Non-borrow scope:

```text
Do not turn fused rank or retrieval score into confidence.
```

Candidate tags:

```text
retrieval, hybrid-search, bm25, embeddings, activation
```

### CP-003: Oversample Before Reranking

```yaml
candidate_id: cp-anthropic-oversample-before-rerank
point_text: "High-quality reranking works best after a wider first-stage retrieval pool, not after an overly narrow top-k."
candidate_general_knowledge: true
proposed_node_type: pattern
review_route: evidence_check
source_ref: raw/articles/2026-06-06-anthropic-contextual-retrieval-source.md
source_anchor:
  url: https://www.anthropic.com/engineering/contextual-retrieval
  section: "Further boosting performance with Reranking"
evidence_granularity: article_section
promotion_readiness: not_ready
```

VAKS borrow scope:

```text
Use this to shape the retrieval pipeline:
first-stage candidate pool -> rerank window -> selected pack items.
```

Non-borrow scope:

```text
Do not make rerank score evidence support.
```

Candidate tags:

```text
retrieval, rerank, oversampling, pack-compiler
```

### CP-004: Pack Item Should Separate Raw Snippet And Contextualized Snippet

```yaml
candidate_id: cp-vaks-pack-item-contextualized-snippet
point_text: "Context-pack items should distinguish raw snippet from contextualized snippet and preserve source/path/heading context."
candidate_general_knowledge: true
proposed_node_type: concept
review_route: rationale_check
source_ref: raw/articles/2026-06-06-anthropic-contextual-retrieval-source.md
source_anchor:
  url: https://www.anthropic.com/engineering/contextual-retrieval
  section: "Contextual Retrieval"
evidence_granularity: article_section
promotion_readiness: not_ready
```

VAKS borrow scope:

```text
Add candidate fields:
snippet, contextualized_snippet, source_title_or_path,
heading_or_local_context, selector_or_offset.
```

Non-borrow scope:

```text
Do not let contextualized snippets replace selector-grade source anchors.
```

Candidate tags:

```text
context-pack, retrieval, citable-status, provenance
```

### CP-005: Retrieval Evaluation Should First Measure Failure To Retrieve

```yaml
candidate_id: cp-anthropic-failure-to-retrieve-eval
point_text: "Retrieval evaluation can start by checking whether relevant items appear in the candidate pool before judging answer quality."
candidate_general_knowledge: true
proposed_node_type: concept
review_route: evidence_check
source_ref: raw/articles/2026-06-06-anthropic-contextual-retrieval-source.md
source_anchor:
  url: https://www.anthropic.com/engineering/contextual-retrieval
  section: "Methodology / Performance improvements"
evidence_granularity: article_section
promotion_readiness: not_ready
```

VAKS borrow scope:

```text
Use as a future retrieval-eval idea: before evaluating final answer quality,
check whether expected source anchors were retrieved at all.
```

Non-borrow scope:

```text
Do not make retrieval recall metrics truth confidence or answer correctness.
```

Candidate tags:

```text
retrieval-eval, recall, query-run, diagnostics
```

## Proposed General Knowledge Point Candidates

These are possible future general knowledge points if later reviewed:

| Candidate slug | Proposed type | Why general |
|---|---|---|
| `contextualized-retrieval-chunks` | pattern | Applies to retrieval indexing beyond VAKS. |
| `hybrid-recall-plus-rerank` | pattern | Applies broadly to RAG/search systems. |
| `pack-item-contextualized-snippet` | concept | Applies to context-pack and citation-aware retrieval design. |
| `retrieval-eval-failure-to-retrieve` | concept | Applies to retrieval evaluation before answer evaluation. |

Current status:

```text
candidate_only
```

Do not create `wiki/patterns/` or `wiki/concepts/` entries until reviewed.

## Tags Are Navigation Only

Candidate tags:

```yaml
tags:
  - retrieval
  - contextual-retrieval
  - hybrid-search
  - bm25
  - embeddings
  - rerank
  - context-pack
  - activation
  - evidence-boundary
```

Rule:

```text
Tags help retrieval and dashboards.
Tags do not prove generality, adoption, truth, or action readiness.
```

## VAKS Project Borrowing View

This is a usage-layer borrowing view, not Project Overlay mainline.

```yaml
kp_candidate_ref: contextualized-retrieval-chunks
borrow_scope: "Use contextualized snippets for pack/index items so chunk retrieval preserves document/path/heading context."
non_borrow_scope: "Do not treat generated context as evidence support."
target_hint: "future retrieval/query contract; pack item fields"
stance: partial
```

```yaml
kp_candidate_ref: hybrid-recall-plus-rerank
borrow_scope: "Use BM25/lexical + dense retrieval + rank fusion + rerank as a candidate default recall baseline."
non_borrow_scope: "Do not treat fused rank, channel score, or rerank score as confidence."
target_hint: "future retrieval/query contract; recall funnel"
stance: watch
```

```yaml
kp_candidate_ref: pack-item-contextualized-snippet
borrow_scope: "Distinguish snippet and contextualized_snippet in pack item design."
non_borrow_scope: "Do not replace selector_or_offset or quote_window with summary text."
target_hint: "future context pack manifest / pack item contract"
stance: partial
```

```yaml
kp_candidate_ref: retrieval-eval-failure-to-retrieve
borrow_scope: "Use failure-to-retrieve as a future retrieval diagnostic."
non_borrow_scope: "Do not treat recall@k or retrieval failure rate as correctness/truth confidence."
target_hint: "future query-run trace / retrieval eval"
stance: watch
```

## Review / Promotion Requirements

Before any candidate becomes reviewed pattern/concept:

```text
1. Compare against at least one or two other sources:
   Elastic / Azure / Weaviate / LlamaIndex / RAG eval papers.

2. Check whether VAKS actually needs the concept now:
   retrieval/query contract yes; implementation not yet.

3. Preserve the boundary:
   retrieval improvement = activation quality improvement.
   evidence support still requires source anchor + quote window + warrant.

4. Decide node destination:
   pattern if it gives repeatable design behavior.
   concept if it names a field/boundary.
```

