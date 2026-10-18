---
record_kind: source_card
type: source
status: source-captured
title: "Obsidian MCP + Hybrid Retrieval: 2026 Reference"
source_id: web-blakecrosley-obsidian-mcp-hybrid-retrieval-2026-06-07
source_uri: blakecrosley:guides/obsidian
source_url: https://blakecrosley.com/guides/obsidian
source_type: article
author: Blake Crosley
publisher: blakecrosley.com
published_at: unknown
captured_at: 2026-06-07
captured_by: Codex
extracted_at: 2026-06-07
extracted_by: Codex
extraction_tool: web + Invoke-WebRequest metadata check
version_or_commit: "HTML SHA256 8642D5FFC45D28368F4EE0A158AE2459AD64C201A8ACE83121E08BE5D4E1977B"
source_status: active
http_status_observed: 200
html_content_length_observed: 329022
raw_location: raw/articles/2026-06-07-blakecrosley-obsidian-mcp-hybrid-retrieval-source.md
raw_text_status: not_retained_full_web_article
processing_mode: article-review
processing_level: medium
processing_tier: medium
knowledge_status: raw
overlay_state: none
review_pressure: none
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
review_priority: normal
review_owner: Codex
formalization_status: raw-only
access_boundary: public_web_no_cookies
verification_status: source_page_observed_not_independently_verified
topics:
  - obsidian
  - mcp
  - hybrid-retrieval
  - bm25
  - vector-search
  - credential-filtering
  - index-hygiene
projects:
  - verified-action-knowledge-system
source_family: ai-obsidian-retrieval-runtime-guide
related_outputs:
  - outputs/review/2026-06-07-blakecrosley-obsidian-mcp-hybrid-retrieval-candidate-distillation.md
  - outputs/review/project_overlays/VAKS/VAKS-blakecrosley-obsidian-mcp-hybrid-retrieval-2026-06-07.md
tags:
  - raw-article
  - blakecrosley
  - obsidian
  - retrieval-runtime
  - candidate-only
---

# Source: Blake Crosley Obsidian MCP Hybrid Retrieval

## 为什么收录

这篇文章把 AI + Obsidian 的问题从“文件夹怎么摆”推进到“AI 怎么可靠检索 vault”。它对 VAKS 的价值在 retrieval runtime、MCP 边界、索引卫生、credential filtering 和 token budget，而不是 Obsidian 个人工作法。

## 来源信息

- 作者：Blake Crosley
- 发布方：blakecrosley.com
- 原始链接：https://blakecrosley.com/guides/obsidian
- 采集时间：2026-06-07
- HTTP 状态：200
- HTML SHA256：`8642D5FFC45D28368F4EE0A158AE2459AD64C201A8ACE83121E08BE5D4E1977B`
- 原文全文：未复制保留；本卡只保留 provenance、主题锚点和候选抽取。

## Intake Boundary

```yaml
processing_tier: medium
knowledge_status: raw
retrieval_policy:
  policy_kind: source_identity_only
  action_basis_allowed: false
promotion_gate: none
truth_mutation_allowed: false
```

Source card 只提供来源身份和回查路径，不提供 reviewed relation、truth confidence 或 action basis。

## Source Anchors

| Anchor | Observed topic | Candidate extraction | Boundary |
|---|---|---|---|
| page title / metadata | Obsidian MCP + Hybrid Retrieval reference | Treat as retrieval/runtime guide | Page claims need implementation check before adoption |
| retrieval sections | BM25, vector retrieval, fusion/ranking | Hybrid retrieval can support context pack preparation | Retrieval rank is not trust |
| index hygiene sections | index ignore, filtering, chunking | Vault indexing needs exclusion and hygiene rules | Index is derived cache |
| credential/safety sections | credential filtering before embedding/search | Sensitive data must be filtered before tool/index exposure | Filtering is safety control, not review |
| MCP sections | local tool access to vault/search | MCP should be read-first and path-scoped | No write access by default |

## 初步看点

Strong for VAKS runtime design:

- retrieval should combine lexical and semantic signals;
- index inputs need explicit exclusion and credential filtering;
- MCP should expose narrow read tools with token limits and source paths;
- chunking and frontmatter shape affect retrieval quality.

## 明显疑点

- Implementation details, version claims, and performance claims need separate source/code verification.
- A retrieval/MCP guide cannot justify enabling write tools.
- It does not replace VAKS source/review/action-basis boundaries.
