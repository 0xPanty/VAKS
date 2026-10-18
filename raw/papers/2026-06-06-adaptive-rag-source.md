---
type: source
status: source-captured
title: "Adaptive-RAG: Learning to Adapt Retrieval-Augmented Large Language Models through Question Complexity"
source_id: 2026-06-06-adaptive-rag-source
source_uri: https://arxiv.org/abs/2403.14403
source_url: https://arxiv.org/abs/2403.14403
source_type: paper
authors:
  - Soyeong Jeong
  - Jinheon Baek
  - Sukmin Cho
  - Sung Ju Hwang
  - Jong C. Park
publisher: arXiv
venue: NAACL 2024
published_at: 2024-03-21
captured_at: 2026-06-06
captured_by: Codex
extracted_by: Codex
extracted_at: 2026-06-06
extraction_tool: web
extraction_model: Codex
version_or_commit: arXiv:2403.14403v2
source_status: active
raw_location: raw/papers/2026-06-06-adaptive-rag-source.md
processing_mode: arxiv-abstract-and-metadata-read
processing_level: light
review_priority: normal
review_owner: Codex
formalization_status: source-only
confidence_cap_reason: "Captured from arXiv abstract page and metadata; no full PDF deep read in this pass."
topics:
  - adaptive-rag
  - query-complexity
  - retrieval-router
  - query-planning
  - cost-governance
projects:
  - verified-action-knowledge-system
source_family: adaptive-rag
upstream_sources: []
verification_status: primary-source-captured
candidate_relation_suggestions:
  - candidate:query_complexity_router
  - candidate:retrieval_strategy_as_costed_choice
---

# Source Record: Adaptive-RAG

## Why Saved

This paper is relevant to VAKS because it frames retrieval strategy as an
adaptive choice based on question complexity. The arXiv abstract says simple
queries can suffer unnecessary computational overhead, while complex multi-step
queries can be under-served by simple methods.

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
query complexity should influence retrieval depth
no-retrieval, single-step retrieval, and iterative retrieval are distinct modes
planner output should record why a strategy was chosen
retrieval cost and latency are part of the design contract
```

## Not Adopted Yet

```text
Do not implement Adaptive-RAG's classifier as a VAKS requirement.
Do not make every query agentic or multi-hop.
Do not let planner confidence become truth confidence.
```

## Related Candidate Extraction

```text
outputs/review/2026-06-06-arxiv-retrieval-batch-candidate-distillation.md
outputs/review/2026-06-06-vaks-retrieval-external-source-extractions.md
outputs/review/2026-06-06-vaks-retrieval-candidate-knowledge-index.md
```
