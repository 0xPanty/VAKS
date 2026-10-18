---
type: source
status: source-captured
title: "RAG vs. GraphRAG: A Systematic Evaluation and Key Insights"
source_id: 2026-06-06-rag-vs-graphrag-systematic-evaluation-source
source_uri: https://arxiv.org/abs/2502.11371
source_url: https://arxiv.org/abs/2502.11371
source_type: paper
authors:
  - Haoyu Han
  - Li Ma
  - Yu Wang
  - Harry Shomer
  - Yongjia Lei
  - Zhisheng Qi
  - Kai Guo
  - Zhigang Hua
  - Bo Long
  - Hui Liu
  - Charu C. Aggarwal
  - Jiliang Tang
publisher: arXiv
venue: arXiv preprint
published_at: 2025-02-17
captured_at: 2026-06-06
captured_by: Codex
extracted_by: Codex
extracted_at: 2026-06-06
extraction_tool: web
extraction_model: Codex
version_or_commit: arXiv:2502.11371v3
source_status: active
raw_location: raw/papers/2026-06-06-rag-vs-graphrag-systematic-evaluation-source.md
processing_mode: arxiv-abstract-and-metadata-read
processing_level: light
review_priority: normal
review_owner: Codex
formalization_status: source-only
confidence_cap_reason: "Captured from arXiv abstract page and metadata; no full PDF deep read in this pass."
topics:
  - rag
  - graphrag
  - systematic-evaluation
  - structure-aware-retrieval
  - retrieval-tradeoffs
projects:
  - verified-action-knowledge-system
source_family: rag-vs-graphrag
upstream_sources: []
verification_status: primary-source-captured
candidate_relation_suggestions:
  - candidate:selective_graphrag_branch
  - candidate:retrieval_method_selection_by_task
  - candidate:graphrag_efficiency_tradeoff
---

# Source Record: RAG vs. GraphRAG

## Why Saved

This paper is relevant to VAKS because it compares RAG and GraphRAG under a
unified evaluation protocol and emphasizes trade-offs, failure modes, efficiency
concerns, and task-dependent strengths.

## Source Boundary

```text
arXiv abstract page = source provenance.
This card = raw/source record.
Batch extraction note = candidate comprehension.
Candidate points = review input only.
No reviewed VAKS knowledge is created by this record.
```

## Initial VAKS Signals

```text
GraphRAG should be treated as a selective branch, not default skeleton
retrieval method choice should depend on query/task type
efficiency and failure modes belong in retrieval receipt
graph-derived structures are context preparation aids, not truth
```

## Not Adopted Yet

```text
Do not make GraphRAG the primary VAKS store.
Do not treat graph rank or community summary as evidence support.
Do not assume GraphRAG is universally better than text RAG.
```

## Related Candidate Extraction

```text
outputs/review/2026-06-06-arxiv-retrieval-batch-candidate-distillation.md
outputs/review/2026-06-06-vaks-retrieval-external-source-extractions.md
outputs/review/2026-06-06-vaks-retrieval-candidate-knowledge-index.md
```
