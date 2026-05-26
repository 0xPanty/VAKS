---
type: claim
status: cross-checked
claim: "Vault index should guide AI context loading before reading detailed notes."
created: 2026-05-26
topics:
  - context-routing
  - obsidian
  - agentic-vault
related_projects:
  - 资料库
sources:
  - "[[2026-01-thinking-os-with-ai-vault-source]]"
  - "[[2026-05-26-obsidian-ai-series-integration]]"
supporting_sources:
  - "Karpathy LLM Knowledge Bases workflow"
  - "Claude Code memory documentation"
conflicting_sources:
evidence_level: secondary
verification_status: cross-checked
confidence: 4
impact: 5
last_verified: 2026-05-26
next_review:
tags:
  - claim/high-signal
  - context/index-first
---

# 主张：Vault index should guide AI context loading

## 主张

AI 操作资料库时，应该先读取轻量索引和主题页，再按需打开相关笔记，而不是直接全量读取 vault。

## 为什么重要

这能降低上下文污染，提升资料定位速度，也符合我们“不急着上 RAG，先用索引和 Markdown 跑通”的阶段判断。

## 支持证据

- 用户提供的一月文章明确描述 vault index 帮 agent 决定拉取哪些 notes。
- Karpathy 工作流强调小规模阶段维护索引文件，让 LLM 先读索引定位。
- Claude Code 官方 memory 文档也体现了“入口文件启动加载，详细 topic 按需读取”的设计倾向。

## 反例 / 冲突证据

- index 过期会误导 AI。
- 对大规模 vault，纯索引可能不够，需要全文搜索或 RAG。

## 标签与量化

- evidence_level: secondary
- verification_status: cross-checked
- confidence: 4
- impact: 5
- relevance: 5

## 验证方式

建立 `vault-index.md` 后，用新窗口测试能否快速定位资料，并记录 AI 误读/漏读情况。

## 当前结论

高信号，可作为当前资料库的一条核心设计候选。

## 复查计划

当资料超过 200 条后，复查是否需要增加全文搜索或 RAG。

