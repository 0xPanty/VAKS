---
type: pattern
status: draft
created: 2026-05-26
source_libraries:
  - garrytan/gbrain
related_concepts:
  - verified-knowledge-system
  - source-verification-and-trust-model
related_projects:
  - verified-knowledge-system
adoption_status: adapt
tags:
  - system-of-record
  - markdown
  - derived-index
evidence_count: 1
confidence: high
negative_evidence:
  - copying-full-second-brain-runtime-before-schema-stabilizes
replaces:
superseded_by:
extension_points:
  - SCHEMA.md
  - health-check
  - local-api
---

# 设计模式：Markdown system of record + derived indexes

## 一句话定义

Markdown/YAML 是可信主记录，DB、向量索引、搜索缓存、图谱边都是可重建的派生层。

## 解决的问题

避免系统被数据库、向量库或 UI 锁死；也避免 AI 写入多个位置后出现“到底谁是准的”。

## 适用场景

- 资料库需要长期可读、可 Git 审计。
- 未来可能接入 Obsidian、脚本、API、RAG、MCP 多种工具。
- 需要 AI 写入，但要可回滚、可 diff、可人工审查。

## 不适用场景

- 强事务、高并发、实时协同编辑为主的系统。
- 数据完全结构化且不需要 Markdown 人类阅读的业务表。

## 反例与避坑

- 失败条件：Markdown 格式没有 schema，导致 parser/writer 不可逆。
- 相似反模式：DB 和 Markdown 双写但没有 canonical owner。
- 复杂度风险：为了派生索引过早引入完整数据库服务。
- 替代方案：早期只用 Markdown + index 文件；规模上来再派生 DB/index。

## 来源证据

- gbrain `docs/architecture/system-of-record.md` 强调新用户知识表必须先定义 Markdown shape、parser、writer、reconciler、round-trip test。
- gbrain `docs/guides/compiled-truth.md` / `docs/guides/brain-vs-memory.md` 强调 brain repo/markdown 才是系统记录，DB/index/cache 可重建。

## 标签与量化

- domain: knowledge-system
- problem: source-of-truth
- maturity: emerging
- complexity: medium
- problem_fit: 5
- reuse_value: 5
- implementation_cost: 3
- integration_fit: 5
- evidence_strength: 4
- reversibility: 5

## 交叉验证

- 相似来源：Karpathy LLM Wiki、llm_wiki、Obsidian Markdown vault。
- 历史项目影子：用户强调“文件为准，对话为辅”，需要 durable writeback。
- 支持证据：Markdown 可 Git diff，可被 Obsidian 和 agent 同时读写。
- 反例：只做 DB/RAG 会让证据链和人工审查变弱。

## 最小实现方式

1. 先写 `SCHEMA.md` 定义每类文件字段。
2. 只允许 AI 修改 Markdown canonical 文件。
3. 所有索引、Bases、搜索、context pack 都从 Markdown 派生。
4. 健康检查验证 frontmatter、链接、来源、状态是否可解析。

## 项目融合建议

立即采用为底层原则。不要把未来 vector DB / local API 当主记录。

## 验证指标

- 任一 derived index 删除后可从 Markdown 重建。
- 任一重要 claim / decision 都能回到 Markdown source。
- AI 写入能通过 git diff 人工审查。

