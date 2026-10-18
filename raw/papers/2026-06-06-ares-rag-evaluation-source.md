---
type: source
status: source-captured
title: "ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems"
source_id: 2026-06-06-ares-rag-evaluation-source
source_uri: https://arxiv.org/abs/2311.09476
source_url: https://arxiv.org/abs/2311.09476
source_type: paper
authors:
  - Jon Saad-Falcon
  - Omar Khattab
  - Christopher Potts
  - Matei Zaharia
publisher: arXiv
venue: NAACL 2024
published_at: 2023-11-16
captured_at: 2026-06-06
captured_by: Codex
extracted_by: Codex
extracted_at: 2026-06-06
extraction_tool: web
extraction_model: Codex
version_or_commit: arXiv:2311.09476v2
source_status: active
raw_location: raw/papers/2026-06-06-ares-rag-evaluation-source.md
processing_mode: arxiv-abstract-and-metadata-read
processing_level: light
review_priority: normal
review_owner: Codex
formalization_status: source-only
confidence_cap_reason: "Captured from arXiv abstract page and metadata; no full PDF deep read in this pass."
topics:
  - rag-evaluation
  - context-relevance
  - answer-faithfulness
  - answer-relevance
  - evaluator-boundary
projects:
  - verified-action-knowledge-system
source_family: ares
upstream_sources: []
verification_status: primary-source-captured
candidate_relation_suggestions:
  - candidate:rag_eval_dimensions_are_separate
  - candidate:evaluator_scores_are_diagnostics
---

# Source Record: ARES

## Why Saved

This paper is relevant to VAKS because it separates RAG evaluation into
component-level dimensions, including context relevance, answer faithfulness,
and answer relevance. That supports the VAKS boundary that retrieval success,
groundedness/faithfulness, and answer usefulness are not the same thing.

The user-provided list included ARES twice. This source card intentionally
deduplicates it into one provenance record.

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
evaluation dimensions should stay separated
context relevance is not answer faithfulness
answer faithfulness is not answer relevance
automated evaluation remains diagnostic unless reviewed
small human-annotated checks can calibrate evaluators
```

## Not Adopted Yet

```text
Do not implement ARES as a required VAKS evaluator.
Do not treat evaluator scores as truth confidence.
Do not let an automated judge promote reviewed knowledge.
```

## Related Candidate Extraction

```text
outputs/review/2026-06-06-arxiv-retrieval-batch-candidate-distillation.md
outputs/review/2026-06-06-vaks-retrieval-external-source-extractions.md
outputs/review/2026-06-06-vaks-retrieval-candidate-knowledge-index.md
```
