---
type: source
record_kind: source_card
status: source-captured
title: "How to Build a JARVIS Inside Obsidian With Claude Code"
source_url:
source_type: article
author: cyrilXBT
publisher:
published_at:
captured_at: 2026-05-27
captured_by: Codex
review_priority: normal
review_owner: Codex
formalization_status: reviewed
topics:
  - obsidian
  - claude-code
  - content-workflow
  - agent-skills
  - feedback-loop
projects:
  - verified-action-knowledge-system
sources: []
verification_status: single-source
evidence_level: anecdotal
source_integrity:
  capture_confidence: medium
verified_by: Codex review of user-pasted text
last_verified: 2026-05-27
next_review: 2026-06-03
candidate_relation_suggestions:
  - target: "[[2026-05-27-jarvis-content-vault-review]]"
    type: derived_from
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-27-jarvis-obsidian-claude-code-source]]"
    rationale: "The review summarizes this article as a content-production workflow rather than a verified truth architecture."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[published-performance-feedback-loop]]"
    type: supports
    strength: 4
    confidence: medium
    evidence:
      - "[[2026-05-27-jarvis-obsidian-claude-code-source]]"
    rationale: "The article's strongest new point is closing the loop by attaching performance data to published outputs."
    created: 2026-05-27
    last_verified: 2026-05-27
tags:
  - source/article
  - content-workflow
  - obsidian
  - claude-code
knowledge_status: raw
processing_tier: light
source_id: legacy:2026-05-27-jarvis-obsidian-claude-code-source
why_saved: see_body_or_legacy_record
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
raw_location: C:/Users/Administrator/Documents/资料库/raw/articles/2026-05-27-jarvis-obsidian-claude-code-source.md
legacy_raw_metadata:
  source_quality: 3
  freshness: 4
  relevance: 3
  cross_source_count: 1
---
# 来源记录：JARVIS inside Obsidian with Claude Code

## 为什么收录

用户提供全文并询问“好像是比较基础的？”。这篇文章是前一篇 automated vault / daily brief 思路的内容创作者版本，适合作为外围操作层参考，不适合作为本资料库核心 truth schema。

## 核心内容

文章提出一个 Obsidian + Claude Code 的“JARVIS”内容系统：

```text
raw capture
-> typed captures
-> connections
-> content briefs
-> written drafts
-> published archive with performance data
-> monthly performance review
```

它把 vault 明确设计成内容生产系统，而不是 verified knowledge system。

## 来源信息

- 作者：署名/账号为 cyrilXBT。
- 发布方：未提供原始 URL。
- 发布时间：未提供。
- 原始链接：未提供。
- 采集方式：用户在对话中粘贴全文，Codex 摘要入库。

## 已验证内容

- 文章结构完整，包含 vault folder layout、CLAUDE.md、四个 Claude Code skills、daily ritual、weekly connection session、published performance data loop。
- 文章目标是内容创作：captures、connections、briefs、writing、published metrics。
- 文章没有提供 verified truth layer、evidence schema、claim review、decision/action risk model。

## 未验证内容

- 未验证作者实际系统效果。
- 未验证 Claude Code skills 在真实 Obsidian vault 中的稳定性。
- 未验证 performance data review 是否能长期提升内容质量。

## 冲突或疑点

- “JARVIS”表述偏营销，容易让人误以为是通用智能体系统。
- 文章允许 Claude Code process inbox、move notes、generate briefs、write content；这对内容系统可接受，但不能套到本资料库 formal truth layer。
- 按 note type 分文件夹对内容创作有用，但不适合作为 verified knowledge node schema。

## 可复用点

- `01-CAPTURES` 按 observations / reactions / patterns / questions / numbers 分型，能增强跨主题连接。
- `skills/` 作为可复用工作流集合，呼应我们已有 Skills as Action Modules。
- `04-PUBLISHED` 保存输出和 performance data，能迁移为本系统的 feedback timeline / action result records。
- daily ritual 和 weekly connection session 可以作为 review workflow 的轻量参考。

## 下一步

- 作为内容生产/反馈层参考保留。
- 不作为核心架构采用。
- 若未来实现 `IMPLEMENTATION_BLUEPRINT.md`，可把 published performance loop 放入 feedback adapter 章节。
