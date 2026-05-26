---
type: qa
question: "ArthurYangX/nano-NotebookLM 的知识图谱和向量索引设计有什么可借鉴？"
asked_at: 2026-05-26
sources:
  - raw/repos/2026-05-26-nano-notebooklm-source.md
  - wiki/summaries/2026-05-26-nano-notebooklm-kg-vector-index-review.md
related_patterns:
  - wiki/patterns/hybrid-vector-bm25-rrf-with-graph-neighborhood.md
  - wiki/patterns/generated-graph-human-edit-overlay.md
  - wiki/patterns/embedding-preset-namespaced-index-cache.md
confidence: high
---

# Q&A：nano-NotebookLM 知识图谱和向量索引分析

## 结论

这个库值得看，而且比普通 NotebookLM clone 更有工程含量。

它最值得我们借鉴的是：

1. 混合检索：BM25 + FAISS + RRF。
2. GraphRAG：concept embedding seed + BFS graph neighborhood。
3. 可编辑生成图谱：AI 生成图谱和人类编辑 overlay 分离。
4. Embedding preset 命名空间：模型切换不污染旧索引。
5. 检索回退：GraphRAG 低分时回退普通 RAG，而不是硬答。

## 大白话理解

它不是把资料丢进向量库然后问答。

它是两套召回一起跑：

```text
普通文本召回：
  关键词 BM25 + 语义 FAISS -> RRF 合并

图谱召回：
  问题 embedding -> 找最像的概念节点 -> 沿图谱边扩散 -> 回到原文 chunk
```

这样问“某个概念是什么”时可以用普通 RAG；问“两个概念有什么关系”时，图谱邻域更有优势。

## 对我们的价值

它能补我们的中后期实现，不是补第一阶段。

对应到主线骨架：

- 补 relation model：给了基础图谱节点/边/邻域检索实现，但关系类型要扩展。
- 补 health check：提醒我们必须处理 dangling edge、stale embedding、低分回退。
- 补 search layer：给了可落地的 BM25 + vector + graph retrieval 组合。
- 补 human review 边界：overlay 思想非常适合 AI 生成知识和人类审定分离。

## 不能照搬的地方

它的图谱服务学习工具，不服务 verified decision。

所以：

- 它的 relation score 不能当 truth score。
- 它的 concept graph 不能替代 claim graph。
- 它的 `related` 边太宽泛，不能直接进入我们的高置信关系。
- 它没有 negative evidence / conflicting sources / source_quality / adoption decision。

## 当前采纳建议

短期：

- 记录模式，不实现。
- 用它帮助我们设计 `SCHEMA.md` 里的 relation 类型和 retrieval metadata。

中期：

- 资料规模上来后，可实现一个轻量版：

```text
local BM25
  + optional vector index
  + relation-neighborhood expansion
  + source-grounded context pack
```

长期：

- 如果做本地 API/context pack，GraphRAG 可以成为 resolver 的一个分支，但必须输出：

```text
source
chunk/location
relation_path
retrieval_score
verification_status
confidence
negative_evidence
```

## 最关键的边界

GraphRAG 只能回答“可能相关的上下文在哪里”。

我们的 verified knowledge system 要回答的是：

```text
这个结论可不可信？
有哪些证据？
有哪些反例？
能不能采纳？
采纳后怎么验证和回退？
```

这两层不能混。

