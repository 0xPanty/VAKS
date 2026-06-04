---
type: source
status: source-captured
title: "Learning Fine-Grained Grounded Citations for Attributed Large Language Models"
source_id: source-front-2408-04568
source_uri: arXiv:2408.04568
source_url: https://arxiv.org/abs/2408.04568
source_type: paper
author: "Lei Huang et al."
publisher: arXiv / ACL Findings 2024
published_at: 2024-08-08
updated_at:
captured_at: 2026-06-01
captured_by: Codex
version_or_commit: v1
source_status: active
raw_location: raw/papers/2026-06-01-front-source.md
processing_mode: immediate
processing_level: medium
review_priority: normal
review_owner: Codex
formalization_status: raw-only
topics:
  - fine-grained-citations
  - evidence-support
  - attributed-llm
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

# Source Record: FRONT

## Why Captured

This source directly stresses that coarse document identifiers make fine-grained verification hard.

## Source Information

- URL: https://arxiv.org/abs/2408.04568
- DOI: https://doi.org/10.48550/arXiv.2408.04568
- arXiv metadata lines inspected: title/authors at lines 30-33; abstract at lines 38-40.
- Access level used in this trial: abstract source span.

## Source Anchor Matrix

| Anchor | Range | Short excerpt | Trial use |
|---|---|---|---|
| D1 | arXiv abstract line 39 | "coarse document identifiers" | Supports document-level citation insufficiency. |
| D2 | arXiv abstract line 39 | "fine-grained supporting quotes" | Supports source-span / quote-level evidence. |
| D3 | arXiv abstract line 40 | "highly supportive citations" | Supports citation quality as a separate quality target. |

## Extracted Candidate Points

1. Coarse document identifiers are not enough for fine-grained verification.
2. Fine-grained supporting quotes can improve verification of attributed answers.

## Not Adopted

- Do not adopt FRONT training.
- Do not treat citation quality improvement as VAKS action readiness.

