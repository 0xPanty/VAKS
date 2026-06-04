---
type: source
status: source-captured
title: "Teaching language models to support answers with verified quotes"
source_id: source-gophercite-2203-11147
source_uri: arXiv:2203.11147
source_url: https://arxiv.org/abs/2203.11147
source_type: paper
author: "Jacob Menick et al."
publisher: arXiv
published_at: 2022-03-21
updated_at:
captured_at: 2026-06-01
captured_by: Codex
version_or_commit: v1
source_status: active
raw_location: raw/papers/2026-06-01-gophercite-source.md
processing_mode: immediate
processing_level: medium
review_priority: normal
review_owner: Codex
formalization_status: raw-only
topics:
  - verified-quotes
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

# Source Record: GopherCite

## Why Captured

This paper is useful because it frames citation / quote support as aid for appraisal, while still starting from the trust problem.

## Source Information

- URL: https://arxiv.org/abs/2203.11147
- arXiv metadata lines inspected: title/authors at lines 34-37; abstract at lines 42-43.
- Access level used in this trial: abstract source span.

## Source Anchor Matrix

| Anchor | Range | Short excerpt | Trial use |
|---|---|---|---|
| C1 | arXiv abstract line 42 | "without fact-checking" | Supports the boundary that citation is not enough by itself. |
| C2 | arXiv abstract line 42 | "specific evidence for their claims" | Supports source-span evidence as useful. |
| C3 | arXiv abstract line 43 | "abstain from answering when unsure" | Supports gap exposure / not-ready behavior. |

## Extracted Candidate Points

1. Users cannot trust individual model claims without fact-checking.
2. Citing specific evidence aids correctness appraisal.
3. Abstention is part of responsible evidence-backed QA when unsure.

## Not Adopted

- Do not adopt RLHP or GopherCite runtime.
- Do not treat quote support as final truth.

