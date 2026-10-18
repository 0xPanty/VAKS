---
type: source
status: source-captured
title: "LlamaIndex: Build RAG with in-line citations"
source_id: llamaindex-citation-query-engine-2026
source_uri: https://developers.llamaindex.ai/python/examples/workflow/citation_query_engine/
source_url: https://developers.llamaindex.ai/python/examples/workflow/citation_query_engine/
source_type: official_documentation
platform: web
author: "LlamaIndex"
publisher: LlamaIndex Developer Documentation
published_at:
updated_at:
captured_at: 2026-06-06
captured_by: Codex
raw_location: raw/articles/2026-06-06-llamaindex-citation-query-engine-source.md
processing_mode: public-web-read
processing_level: medium
review_priority: normal
review_owner: Codex
formalization_status: raw-only
source_status: active
confidence_cap_reason: "Official example documentation; citation markers are workflow aids, not evidence support by themselves."
topics:
  - inline-citations
  - citation-query-engine
  - workflow-events
  - citation-chunks
  - claim-evidence-binding
  - context-pack
projects:
  - verified-action-knowledge-system
candidate_relation_suggestions:
  - candidate:citation_stage_as_explicit_workflow
  - candidate:numbered_source_nodes_for_pack_items
  - candidate:citation_marker_not_support
tags:
  - raw-article
  - llamaindex
  - citation
  - context-pack
  - candidate-only
---

# Source Record: LlamaIndex Citation Query Engine

## Why Saved

This LlamaIndex documentation is relevant because it demonstrates citation
generation as an explicit workflow, not a vague final-output decoration.

For VAKS, the useful part is:

```text
retrieved nodes
-> smaller citation nodes
-> numbered sources
-> answer synthesis constrained to cite numbered sources
```

This is close to VAKS's needed `pack item -> claim/evidence binding` pathway.

## Source Boundary

```text
Official docs = external source provenance.
This card = raw/source record.
Extraction note = candidate comprehension.
Candidate points = review input only.
No reviewed VAKS knowledge is created by this record.
```

## What Was Observed

The example defines workflow events for retrieved nodes and citation nodes. It
also defines prompts that ask the model to answer based on numbered sources,
cite appropriate sources, cite only when explicitly referencing a source, and
say when sources are not helpful.

The workflow then retrieves nodes, splits them into smaller citation chunks,
labels each as a numbered source, and synthesizes an answer from those nodes.

## VAKS Candidate Signals

Potential candidate knowledge points:

```text
citation_stage_as_explicit_workflow:
  citation creation should be a named post-retrieval stage.

numbered_source_nodes_for_pack_items:
  context pack items can expose stable numbered items for answer drafting, but
  must still keep path/selector refs behind the number.

citation_marker_not_support:
  a source number or citation marker is only a pointer until the claim-support
  relation is checked.
```

## Not Adopted Yet

Do not treat this source as:

```text
permission to accept citation markers as evidence
replacement for selector-grade anchors
replacement for warrant/gap/risk notes
mandatory LlamaIndex dependency
```

## Related Candidate Extraction

```text
outputs/review/2026-06-06-rag-eval-tracing-citation-rrf-batch-candidate-distillation.md
```
