---
type: source
status: source-captured
title: "Attributed Question Answering: Evaluation and Modeling for Attributed Large Language Models"
source_id: source-attributed-qa-2212-08037
source_uri: arXiv:2212.08037
source_url: https://arxiv.org/abs/2212.08037
source_type: paper
author: "Bernd Bohnet et al."
publisher: arXiv
published_at: 2022-12-15
updated_at: 2023-02-10
captured_at: 2026-06-01
captured_by: Codex
version_or_commit: v2
source_status: active
raw_location: raw/papers/2026-06-01-attributed-qa-source.md
processing_mode: immediate
processing_level: medium
review_priority: normal
review_owner: Codex
formalization_status: raw-only
topics:
  - attributed-qa
  - citation-evaluation
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

# Source Record: Attributed QA

## Why Captured

This source gives a second, independent paper on attribution as a measurable capability for information-seeking LLMs.

## Source Information

- URL: https://arxiv.org/abs/2212.08037
- DOI: https://doi.org/10.48550/arXiv.2212.08037
- arXiv metadata lines inspected: title/authors at lines 34-36; abstract at lines 40-41.
- Access level used in this trial: abstract source span.

## Source Anchor Matrix

| Anchor | Range | Short excerpt | Trial use |
|---|---|---|---|
| B1 | arXiv abstract line 40 | "attribute the text" | Supports attribution as a key capability. |
| B2 | arXiv abstract line 41 | "How to measure attribution?" | Supports review/evaluation framing. |

## Extracted Candidate Points

1. Attribution is a key capability for information-seeking LLMs.
2. Attribution needs measurement, not just display.

## Not Adopted

- Do not adopt the paper's evaluation framework wholesale.
- Do not treat human annotations in the paper as VAKS reviewer status.

