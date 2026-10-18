---
record_kind: source_capture_notes
status: captured
knowledge_status: raw
processing_tier: medium
source_id: 2026-06-12-yozm-obsidian-llm-wiki-second-brain
source_url: "https://yozm.wishket.com/magazine/detail/3792/"
captured_at: 2026-06-12
captured_by: Codex
source_hash: 7F6A46484184196EAD61A06FF64A1C56A77C86885F4B6D9BB6B79C71F18617A8
full_text_retained: false
copyright_boundary: "No full article text or HTML snapshot retained; notes below are paraphrase and routing anchors."
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
action_basis_allowed: false
truth_mutation_allowed: false
tags:
  - capture-notes
  - raw
  - copyright-limited
  - obsidian
  - llm-wiki
---

# Capture Notes: Yozm Obsidian LLM Wiki Second Brain

## Copyright Boundary

The public page includes an explicit copyright notice. This file does not retain
the full article text or HTML. It preserves source identity, capture metadata,
section-level paraphrase, and VAKS routing anchors only.

Use the original URL for drilldown:

```text
https://yozm.wishket.com/magazine/detail/3792/
```

## Capture Metadata

```yaml
title: "나만의 세컨 브레인: 옵시디언 기반 LLM 위키 구축기"
title_zh: "我的第二大脑：基于 Obsidian 的 LLM Wiki 构建记"
author: "곰씨네 IT 블로그"
publisher: "요즘IT / Wishket"
site_label_at_capture:
  category: "개발"
  reading_time: "10 분"
  published_relative: "1일 전"
  views: "8.9K"
captured_at: 2026-06-12
html_sha256: 7F6A46484184196EAD61A06FF64A1C56A77C86885F4B6D9BB6B79C71F18617A8
```

## Section Map

### Opening / summary

The article starts from the pain of using many AI tools while repeatedly
explaining personal situation and context. It frames LLM Wiki as a way to make
personal context durable and reusable for AI tools.

VAKS routing:

```text
context fatigue -> durable context surface -> authority-bucketed retrieval
```

### Why build a personal LLM Wiki

The author says work context was spread across lightweight notes, meeting notes,
office documents, code, project data, and multiple AI tools. The chosen direction
was to unify personal context in one system that AI agents can use.

VAKS routing:

```text
multi-source capture is useful
all-personal-data-in-one-vault is privacy-sensitive
```

### Obsidian setup and capture paths

The article describes using Obsidian as the vault, a theme and plugins, web
clipping from desktop, mobile sharing, and a temporary folder for unsupported
sources. Later cleanup is delegated to Claude Code workflows.

VAKS routing:

```text
capture surfaces are useful
temporary folder needs source hygiene and candidate boundaries
```

### GitHub private repo sync

The article uses a GitHub Private Repo for backup/sync and mentions mobile
access through Obsidian Sync or Working Copy, with token setup and account
security cautions.

VAKS routing:

```text
repo sync is a storage/sync option
private repo is not a complete security boundary
```

### Claude Code / CLI and root manual

The article uses Claude Code in a terminal context to ingest scattered material,
query the wiki, and periodically organize it. The root `CLAUDE.md` is treated as
the operating manual injected into new sessions, with SessionStart hooks as an
extra consistency mechanism.

VAKS routing:

```text
AGENTS / handoff / index entrypoints are valuable
hooked context injection can enforce stale or overbroad instructions
```

### Category design

The article asks Claude Code to design a personal wiki structure around identity,
thoughts, goals, history, people, assets, and work.

VAKS routing:

```text
category scaffolding should start light
do not copy personal categories into VAKS architecture by default
```

### Ingest

The article describes a custom `/ingest` workflow that reads newly collected
material and merges or links it into proper wiki pages. It also adds a sensitive
information masking step, while noting that regex detection is incomplete and
needs later checking.

VAKS routing:

```text
ingest should preserve raw source and candidate output
sensitive data requires quarantine, scan, and human review
regex masking is only a first-pass guard
```

### Lint

The article describes `/lint` as a recurring wiki health check for sensitive
data, contradictions, orphan pages, broken links, and related consistency
issues. It mentions scheduled automation.

VAKS routing:

```text
lint is maintenance input
lint output should not directly repair reviewed knowledge or mutate truth
```

### Query

The article describes `/query` as a workflow that gives AI access to the wiki so
answers become more personal and context-aware than generic AI answers.

VAKS routing:

```text
query can improve relevance
full-vault query must be filtered by raw / candidate / overlay / reviewed authority buckets
```

### Limitations

The article reports failures around image/OCR ingest accuracy, sensitive data
growth, GitHub account compromise risk, and the difficulty of sharing a personal
LLM Wiki with a team without duplicating context.

VAKS routing:

```text
image-derived ingest needs confidence and review
private data aggregation increases blast radius
personal/team wiki split needs explicit scope boundaries
```

## Key Entity Confidence

```yaml
title: high
source_url: high
publisher: high
author_label: medium
published_at: medium
tool_names:
  Obsidian: high
  GitHub Private Repo: high
  Claude Code: high
  Claude Code SessionStart Hook: medium
  Working Copy: medium
  obsidian-cli / obsidian-markdown / defuddle skill names: medium
implementation_details: low_until_official_docs_checked
```

## Local Routing

```yaml
candidate_distillation: outputs/review/2026-06-12-yozm-obsidian-llm-wiki-second-brain-candidate-distillation.md
project_overlay: outputs/review/project_lens_overlays/2026-06-12-yozm-obsidian-llm-wiki-second-brain-overlay.md
reviewed_knowledge_created: false
action_basis_allowed: false
truth_mutation_allowed: false
```
