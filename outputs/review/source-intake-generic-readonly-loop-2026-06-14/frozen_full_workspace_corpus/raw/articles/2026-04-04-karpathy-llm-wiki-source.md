---
type: source
record_kind: source_card
status: source-captured
title: "LLM Wiki"
source_url: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
source_type: gist
author: Andrej Karpathy
publisher: GitHub Gist
published_at: 2026-04-04
captured_at: 2026-05-26
captured_by: Codex
topics:
  - llm-wiki
  - compiled-knowledge
  - obsidian
  - agentic-knowledge-base
projects:
  - verified-knowledge-system
sources:
  - https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
verification_status: primary-source
evidence_level: primary
source_integrity:
  capture_confidence: high
verified_by: Codex
last_verified: 2026-05-26
next_review: 2026-06-26
candidate_relation_suggestions:
  - target: "[[2026-04-04-karpathy-llm-wiki-pattern]]"
    type: derived_from
    strength: 5
    confidence: high
    evidence:
      - "[[2026-04-04-karpathy-llm-wiki-source]]"
    rationale: "This summary is directly derived from Karpathy's original LLM Wiki gist."
    created: 2026-05-26
    last_verified: 2026-05-26
  - target: "[[markdown-system-of-record-derived-indexes]]"
    type: supports
    strength: 4
    confidence: high
    evidence:
      - "[[2026-04-04-karpathy-llm-wiki-source]]"
    rationale: "The gist frames the wiki as markdown files plus index/log and Git history."
    created: 2026-05-26
    last_verified: 2026-05-26
  - target: "[[verified-vault-api-for-agent-brain]]"
    type: refines
    strength: 3
    confidence: medium
    evidence:
      - "[[2026-04-04-karpathy-llm-wiki-source]]"
    rationale: "The gist supports index-first agent querying but does not itself define a verified API."
    created: 2026-05-26
    last_verified: 2026-05-26
tags:
  - source/primary
  - llm-wiki
  - karpathy
  - obsidian
knowledge_status: raw
processing_tier: light
source_id: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
why_saved: see_body_or_legacy_record
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
legacy_raw_metadata:
  source_quality: 5
  freshness: 5
  relevance: 5
  cross_source_count: 1
---
# 来源记录：Karpathy LLM Wiki

## 为什么收录

这是 Karpathy 对 LLM Wiki 模式的原始 idea file，后续 Hermes `llm-wiki` skill、多个 Obsidian/agent wiki 项目都以它为上游模式。对本资料库来说，它是 `raw source -> wiki -> query/lint` 思路的高质量源头材料。

## 核心内容

原文主张：普通 RAG 每次查询都重新从 raw documents 检索和拼答案，知识没有复利；LLM Wiki 则让 LLM 持续维护一个结构化、互链的 Markdown wiki，把知识先编译、再持续更新。

核心比喻：

```text
Obsidian = IDE
LLM = programmer / maintainer
Wiki = codebase
```

三层架构：

- `raw sources`：用户筛选的原始资料，不被 LLM 修改。
- `wiki`：LLM 生成和维护的 Markdown 页面，包括 summary、entity、concept、comparison、synthesis。
- `schema`：约束 LLM 如何 ingest、query、lint 和维护 wiki 的操作契约。

三类操作：

- `ingest`：加入新来源，生成 summary，更新 index、entity/concept pages、log。
- `query`：先读 wiki/index，再读相关页面，综合回答，重要回答回写 wiki。
- `lint`：查冲突、过期主张、孤立页面、缺失链接、缺口和新问题。

## 来源信息

- 作者：Andrej Karpathy
- 发布方：GitHub Gist
- 发布时间：2026-04-04
- 原始链接：https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- 采集方式：直接读取 gist 页面。

## 标签与量化

- source_type: gist / idea-file
- evidence_level: primary
- verification_status: primary-source
- source_quality: 5
- freshness: 5
- relevance: 5
- confidence: high
- cross_source_count: 1

## 已验证内容

- 原文明确提出 `raw sources / wiki / schema` 三层。
- 原文明确提出 ingest / query / lint 三类操作。
- 原文明确认为 index/log 是 LLM 和人导航 wiki 的关键文件。
- 原文明确说小中规模下 index 文件可以避免过早引入 embedding RAG。
- 原文明确把 qmd、Obsidian Web Clipper、Graph View、Dataview、Git 作为可选工具。

## 未验证内容

- 作者没有给出固定实现，也没有给出可运行代码。
- “维护成本接近零”是模式判断，不是已经量化验证的工程事实。
- 该模式默认 LLM 拥有 wiki 写权；对我们的 verified vault，需要改成权限分层和 review 队列。

## 冲突或疑点

- 原文说 raw sources 是 source of truth，但我们当前进一步区分：raw 是来源真相，正式结论必须进入 verified claim/pattern/decision 后才是知识层真相。
- 原文默认 wiki 是 LLM-owned layer；我们当前改为 Codex/user-reviewed write，Misa/gbrain read-only 或 suggest-only。
- 原文的 entity/concept/comparison 页面类型偏通用 wiki；我们采用 source/summary/claim/pattern/anti-pattern/decision 的 verified knowledge schema。

## 可复用点

- 保留 `raw` 不可变原则。
- 保留 `SCHEMA.md` 作为 Agent 操作契约。
- 保留 index-first 查询。
- 保留 log/health/lint 思路。
- 保留 valuable answer file-back，即重要问答沉淀为 `outputs/qa` 或正式节点。
- 保留 Git 作为版本审计层。

## 下一步

- 用本文校准 `SCHEMA.md`：我们已经吸收三层架构、ingest/query/lint、index/log、搜索边界和 AI 写入边界。
- 不直接采用“LLM 完全 owns wiki”；维持 Misa/gbrain read-only、candidate review、Codex reviewed write。
