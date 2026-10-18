---
type: candidate_pattern
status: active
pattern_id: retrieval-is-activation-not-truth
created_at: 2026-06-05
truth_boundary: candidate pattern only; not reviewed knowledge
source_family_ids:
  - sf-rag-engineering
  - sf-memory-retrieval
  - sf-graph-ontology
project_fit_refs:
  - outputs/review/project_borrowing_ledgers/VAKS.md
---

# Retrieval Is Activation, Not Truth

## One-Line Pattern

检索、向量相似度、rerank、GraphRAG、community summary、agentic retrieval 都只是把材料拿到面前；它们不是 truth confidence，不是 reviewed relation，也不是 action basis。

## Problem Addressed

很多 RAG / GraphRAG / memory 系统容易把“找到了”“相似”“排前面”“图上有关联”误写成“支持了”“更真”“可以行动”。

## Mechanism

- 检索结果只进入 activation / context preparation。
- evidence support 另行检查。
- relation 只有经过 review 才能成为 reviewed relation。
- dashboard / score / hit count / feedback heat 只做诊断或路由。

## Applicability

- RAG / GraphRAG / agentic retrieval。
- 记忆检索、上下文包、知识库问答。
- 需要严格区分候选和 review 的系统。

## Non-Goals and Trade-Offs

- 不否定检索价值。
- 不要求普通查询都做重 evidence review。
- 不把所有检索都变成审计流程。

## Derived From Sources

- `raw/videos/2026-06-04-bilibili-raglab-17-rag-visual-canvas-source.md`
- `raw/videos/2026-06-04-bilibili-disco-rag-search-to-analysis-source.md`
- `raw/videos/2026-06-04-bilibili-rf-mem-user-memory-retrieval-source.md`
- `raw/papers/2026-06-04-rf-mem-recollection-familiarity-source.md`
- `raw/repos/2026-06-04-come-context-memory-source.md`
- `raw/videos/2026-06-04-bilibili-ontology-methodology-knowledge-graph-source.md`

## Aliases or Near-Duplicates

- retrieval as context activation
- graph rank is not trust
- rerank is not support
- context pack preparation only

## Risk of Overreach

- 把这个模式误解成“不要 RAG”。
- 把 ordinary query 变得过重。
- 只写边界，不改善实际 retrieval quality。

## Project Fit Refs

- VAKS: `adapt`; it already matches the core boundary.

