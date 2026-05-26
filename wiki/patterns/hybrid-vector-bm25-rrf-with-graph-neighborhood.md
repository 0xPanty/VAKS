---
type: pattern
status: candidate
created: 2026-05-26
source_libraries:
  - ArthurYangX/nano-NotebookLM
related_concepts:
  - qmd-local-hybrid-search-layer
  - verified-vault-api-for-agent-brain
  - source-verification-and-trust-model
related_projects:
  - verified-vault
adoption_status: watch
tags:
  - search-layer
  - hybrid-retrieval
  - graph-rag
  - bm25
  - faiss
  - rrf
evidence_count: 1
confidence: high
negative_evidence:
  - algorithmic-graph-scoring-without-source-quality
---

# 设计模式：Hybrid Search + Graph Neighborhood

## 一句话定义

先用 BM25 + vector + RRF 找文本候选，再用 concept embedding 选图谱 seed 并沿关系边 BFS 扩展，最终返回带 source chunk 的引用结果。

## 解决的问题

- 纯关键词检索找不到语义相近内容。
- 纯向量检索容易错过术语、文件名、版本号、公式。
- 单 chunk 检索无法回答“两个概念怎么关联”。
- 图谱如果不回到 source chunk，会变成无证据的漂亮结构。

## 核心机制

```text
chunk layer:
  BM25(query)
  FAISS(query)
  RRF merge by chunk_id

graph layer:
  query_embedding
  cosine rank concept_embedding
  take top seed concepts
  BFS hop expansion over relation edges
  collect source_chunks
  materialize chunks from chunks.json
```

## 适用场景

- raw/wiki 规模变大，index/grep 不够时。
- 需要跨概念查找关系时。
- 需要从答案跳回原文证据时。
- agent 需要 context pack，但不能直接相信向量命中时。

## 不适用场景

- 当前资料库 schema 还没稳定。
- 资料数量还很少。
- 需要判断 claim 真假的场景。
- 图谱关系来源不清楚或未经验证。

## 来源证据

- `nano_notebooklm/kb/vector_index.py`：FAISS IndexFlatIP、chunk metadata、cached vector rebuild。
- `nano_notebooklm/kb/bm25_index.py`：英文 token + 中文 char/bigram，JSON 保存。
- `nano_notebooklm/kb/hybrid_search.py`：RRF 融合。
- `nano_notebooklm/kb/graph_search.py`：concept cosine seed + BFS hop expansion + source chunk materialization。
- `nano_notebooklm/skills/qa_skill.py`：GraphRAG 优先尝试，低分回退普通 RAG。

## 标签与量化

- domain: knowledge_retrieval
- problem: source_grounded_graph_search
- maturity: emerging
- complexity: medium
- problem_fit: 4
- reuse_value: 5
- implementation_cost: 4
- integration_fit: 4
- evidence_strength: 4
- reversibility: 5

## 交叉验证

- 相似来源：QMD 的 BM25 + vector + rerank；llm_wiki 的 graph relevance；用户旧 Zilliz 原文回溯方案。
- 支持证据：nano-NotebookLM 已有 GraphRAG 路由、score gate、fallback 测试。
- 反例：GraphRAG score 只是 retrieval confidence，不是 truth confidence。

## 项目融合建议

短期只记录，不实现。

中期接入时必须遵守：

1. 检索返回的是 candidate context，不是 verified conclusion。
2. context pack 必须带 source、chunk、relation path、retrieval_score。
3. claim/decision 仍以 evidence_level、confidence、negative_evidence 为准。
4. 低分或缺来源时不能硬答。

