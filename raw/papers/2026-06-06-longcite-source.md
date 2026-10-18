---
type: source
status: source-captured
title: "LongCite: Enabling LLMs to Generate Fine-grained Citations in Long-context QA"
source_id: 2026-06-06-longcite-source
source_uri: https://arxiv.org/abs/2409.02897
source_url: https://arxiv.org/abs/2409.02897
source_type: paper
authors:
  - Jiajie Zhang
  - Yushi Bai
  - Xin Lv
  - Wanjun Gu
  - Danqing Liu
  - Minhao Zou
  - Shulin Cao
  - Lei Hou
  - Yuxiao Dong
  - Ling Feng
  - Juanzi Li
publisher: arXiv
venue: arXiv preprint
published_at: 2024-09-04
captured_at: 2026-06-06
captured_by: Codex
extracted_by: Codex
extracted_at: 2026-06-06
extraction_tool: web
extraction_model: Codex
version_or_commit: arXiv:2409.02897v3
source_status: active
raw_location: raw/papers/2026-06-06-longcite-source.md
processing_mode: arxiv-abstract-and-metadata-read
processing_level: light
review_priority: normal
review_owner: Codex
formalization_status: source-only
confidence_cap_reason: "Captured from arXiv abstract page and metadata; no full PDF deep read in this pass."
topics:
  - longcite
  - citations
  - fine-grained-citation
  - claim-evidence-binding
  - long-context-qa
projects:
  - verified-action-knowledge-system
source_family: longcite
upstream_sources: []
verification_status: primary-source-captured
candidate_relation_suggestions:
  - candidate:sentence_level_citation_binding
  - candidate:citation_quality_is_separate_from_answer_quality
---

# Source Record: LongCite

## Why Saved

This paper is relevant to VAKS because it targets fine-grained sentence-level
citations in long-context QA. That maps directly to VAKS's desired
claim-to-evidence binding layer for action-facing answers.

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
long answers need fine-grained citation mapping
sentence-level citation is closer to VAKS claim-level anchors than document-level links
citation generation still needs verification
benchmarks and trained models are not required for VAKS's minimal design
```

## Not Adopted Yet

```text
Do not implement LongCite training or LongCite-45k as VAKS infrastructure.
Do not treat citation presence as evidence sufficiency.
Do not allow citation text to replace source selectors and warrant.
```

## Related Candidate Extraction

```text
outputs/review/2026-06-06-arxiv-retrieval-batch-candidate-distillation.md
outputs/review/2026-06-06-vaks-retrieval-external-source-extractions.md
outputs/review/2026-06-06-vaks-retrieval-candidate-knowledge-index.md
```
