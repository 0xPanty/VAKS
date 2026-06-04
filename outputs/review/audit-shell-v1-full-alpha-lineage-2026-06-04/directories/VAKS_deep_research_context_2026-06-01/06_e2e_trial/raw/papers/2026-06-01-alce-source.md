---
type: source
status: source-captured
title: "Enabling Large Language Models to Generate Text with Citations"
source_id: source-alce-2305-14627
source_uri: arXiv:2305.14627
source_url: https://arxiv.org/abs/2305.14627
source_type: paper
author: "Tianyu Gao; Howard Yen; Jiatong Yu; Danqi Chen"
publisher: arXiv / EMNLP 2023
published_at: 2023-05-24
updated_at: 2023-10-31
captured_at: 2026-06-01
captured_by: Codex
version_or_commit: v2
source_status: active
raw_location: raw/papers/2026-06-01-alce-source.md
processing_mode: immediate
processing_level: heavy
review_priority: high
review_owner: Codex
formalization_status: raw-only
topics:
  - citation-evaluation
  - attributed-llm
  - evidence-support
projects:
  - verified-action-knowledge-system
source_family: arxiv-attributed-llm-citation
upstream_sources: []
verification_status: source-captured
candidate_relation_suggestions: []
tags:
  - source-record
  - e2e-trial
---

# Source Record: ALCE

## Why Captured

This is the first source for the E2E trial because it directly describes LLM citation evaluation and separates answer correctness from citation quality.

## Source Information

- URL: https://arxiv.org/abs/2305.14627
- DOI: https://doi.org/10.48550/arXiv.2305.14627
- arXiv metadata lines inspected: title/authors at lines 34-37; abstract at lines 42-44.
- Access level used in this trial: abstract source span, not full paper review.

## Source Anchor Matrix

| Anchor | Range | Short excerpt | Trial use |
|---|---|---|---|
| A1 | arXiv abstract lines 42-43 | "retrieve supporting evidence" | Candidate point about citation-backed generation requiring evidence retrieval. |
| A2 | arXiv abstract line 43 | "fluency, correctness, and citation quality" | Candidate point about citation quality as separate review dimension. |
| A3 | arXiv abstract line 44 | "lack complete citation support" | Candidate point about incomplete citation support in current systems. |

## Extracted Candidate Points

1. Citation-backed LLM systems need to retrieve supporting evidence, not only emit source labels.
2. Citation quality should be evaluated separately from fluency and correctness.
3. Current citation-backed systems can still lack complete citation support.

## Not Adopted

- Do not adopt ALCE metrics as a VAKS benchmark.
- Do not treat benchmark correlation with human judgments as VAKS truth confidence.
- Do not infer action readiness from ALCE alone.

## Friction Notes

- `processing_level: heavy` felt inflated because only the abstract was inspected.
- The source template wants author / publisher / updated_at cleanly, but arXiv metadata is easy while many articles will not be.
- The source record has no obvious place for "abstract-only source span used intentionally".

