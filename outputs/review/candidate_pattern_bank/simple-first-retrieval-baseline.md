---
type: candidate_pattern
status: draft
pattern_id: simple-first-retrieval-baseline
created_at: 2026-06-05
truth_boundary: candidate pattern only; not reviewed knowledge
source_family_ids:
  - sf-rag-engineering
project_fit_refs:
  - outputs/review/project_borrowing_ledgers/VAKS.md
---

# Simple-First Retrieval Baseline

## One-Line Pattern

在引入复杂向量、GraphRAG、agentic retrieval 前，先测试 BM25、SQLite/FTS、关键词、结构化过滤等简单 baseline。

## Problem Addressed

很多项目一上来就做向量库和复杂 agent loop，反而忽略了文档结构、关键词、过滤器、BM25 等便宜稳定的 baseline。

## Mechanism

- 对普通资料先做关键词/FTS/BM25 baseline。
- 向量检索作为补充，而不是默认唯一入口。
- 复杂 retrieval 只在简单 baseline 不够时增加。
- 对每种 retrieval 保留失败案例。

## Applicability

- 小型/中型本地知识库。
- 资料结构清楚、关键词强的领域。
- VAKS ordinary query / light capture。

## Non-Goals and Trade-Offs

- 不等于向量检索没用。
- 不等于复杂 RAG 都应该拒绝。
- 简单检索也会漏语义变体。

## Derived From Sources

- `raw/videos/2026-06-04-bilibili-rag-back-to-bm25-sqlite-source.md`
- `raw/videos/2026-06-04-bilibili-rag-failure-chunking-rerank-prompt-source.md`
- `raw/videos/2026-06-04-bilibili-raglab-17-rag-visual-canvas-source.md`

## Aliases or Near-Duplicates

- BM25 before vector
- local FTS baseline
- simple retrieval first
- retrieval minimalism

## Risk of Overreach

- 被误读成“反向量”。
- 简单 baseline 缺少语义扩展。
- 对复杂多跳问题不足。

## Project Fit Refs

- VAKS: `watch`; candidate for lightweight ordinary query.
