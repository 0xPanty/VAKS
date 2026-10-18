---
type: source
status: source-captured
title: "Lost in the Middle: How Language Models Use Long Contexts"
source_id: 2026-06-06-lost-in-the-middle-source
source_uri: https://arxiv.org/abs/2307.03172
source_url: https://arxiv.org/abs/2307.03172
source_type: paper
authors:
  - Nelson F. Liu
  - Kevin Lin
  - John Hewitt
  - Ashwin Paranjape
  - Michele Bevilacqua
  - Fabio Petroni
  - Percy Liang
publisher: arXiv
venue: TACL 2023
published_at: 2023-07-06
captured_at: 2026-06-06
captured_by: Codex
extracted_by: Codex
extracted_at: 2026-06-06
extraction_tool: web
extraction_model: Codex
version_or_commit: arXiv:2307.03172v3
source_status: active
raw_location: raw/papers/2026-06-06-lost-in-the-middle-source.md
processing_mode: arxiv-abstract-and-metadata-read
processing_level: light
review_priority: normal
review_owner: Codex
formalization_status: source-only
confidence_cap_reason: "Captured from arXiv abstract page and metadata; no full PDF deep read in this pass."
topics:
  - long-context
  - context-pack
  - lost-in-the-middle
  - retrieval
  - context-ordering
projects:
  - verified-action-knowledge-system
source_family: lost-in-the-middle
upstream_sources: []
verification_status: primary-source-captured
candidate_relation_suggestions:
  - candidate:position_aware_context_pack_ordering
  - candidate:context_pack_is_not_context_dump
---

# Source Record: Lost in the Middle

## Why Saved

This paper is relevant to the VAKS retrieval/query contract because it shows
that long context is not automatically usable context. The arXiv abstract says
models can perform best when relevant information appears near the beginning or
end of the input, and degrade when relevant information is in the middle.

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
context pack order matters
long context should not become raw dumping
critical anchors should be easy to find, not buried
pack compiler should preserve drilldown and selector-grade evidence
```

## Not Adopted Yet

```text
Do not turn this into a universal prompt-order law.
Do not use position heuristics as evidence support.
Do not assume long context removes retrieval or selector needs.
```

## Related Candidate Extraction

```text
outputs/review/2026-06-06-arxiv-retrieval-batch-candidate-distillation.md
outputs/review/2026-06-06-vaks-retrieval-external-source-extractions.md
outputs/review/2026-06-06-vaks-retrieval-candidate-knowledge-index.md
```
