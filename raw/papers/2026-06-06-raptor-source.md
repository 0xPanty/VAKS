---
type: source
status: source-captured
title: "RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval"
source_id: 2026-06-06-raptor-source
source_uri: https://arxiv.org/abs/2401.18059
source_url: https://arxiv.org/abs/2401.18059
source_type: paper
authors:
  - Parth Sarthi
  - Salman Abdullah
  - Aditi Tuli
  - Shubh Khanna
  - Anna Goldie
  - Christopher D. Manning
publisher: arXiv
venue: arXiv preprint
published_at: 2024-01-31
captured_at: 2026-06-06
captured_by: Codex
extracted_by: Codex
extracted_at: 2026-06-06
extraction_tool: web
extraction_model: Codex
version_or_commit: arXiv:2401.18059v1
source_status: active
raw_location: raw/papers/2026-06-06-raptor-source.md
processing_mode: arxiv-abstract-and-metadata-read
processing_level: light
review_priority: normal
review_owner: Codex
formalization_status: source-only
confidence_cap_reason: "Captured from arXiv abstract page and metadata; no full PDF deep read in this pass."
topics:
  - raptor
  - hierarchical-retrieval
  - summary-tree
  - structure-aware-retrieval
  - context-pack
projects:
  - verified-action-knowledge-system
source_family: raptor
upstream_sources: []
verification_status: primary-source-captured
candidate_relation_suggestions:
  - candidate:summary_tree_as_selective_structure_branch
  - candidate:multi_level_abstraction_retrieval
---

# Source Record: RAPTOR

## Why Saved

This paper is relevant to the VAKS retrieval/query contract because it treats
retrieval over long documents as a multi-level abstraction problem rather than
only short contiguous chunk lookup. The arXiv abstract describes recursively
embedding, clustering, and summarizing chunks into a tree, then retrieving from
that tree at inference time.

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
summary trees can support corpus/global or long-document synthesis
multi-level summaries are context-preparation aids
summary nodes must remain derived navigation, not truth
drilldown to source selector remains required for evidence use
```

## Not Adopted Yet

```text
Do not make RAPTOR the default retrieval architecture.
Do not treat generated summaries as reviewed knowledge.
Do not use summary tree hits as evidence support without source anchors.
```

## Related Candidate Extraction

```text
outputs/review/2026-06-06-arxiv-retrieval-batch-candidate-distillation.md
outputs/review/2026-06-06-vaks-retrieval-external-source-extractions.md
outputs/review/2026-06-06-vaks-retrieval-candidate-knowledge-index.md
```
