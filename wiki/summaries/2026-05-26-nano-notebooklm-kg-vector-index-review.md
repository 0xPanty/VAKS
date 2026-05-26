---
type: summary
status: active
created: 2026-05-26
source:
  - raw/repos/2026-05-26-nano-notebooklm-source.md
source_repo: https://github.com/ArthurYangX/nano-NotebookLM
source_commit: 8458d9c2d3e958b1d5cf448fa4000448b28760b0
related_patterns:
  - wiki/patterns/hybrid-vector-bm25-rrf-with-graph-neighborhood.md
  - wiki/patterns/generated-graph-human-edit-overlay.md
  - wiki/patterns/embedding-preset-namespaced-index-cache.md
related_decisions:
  - wiki/decisions/2026-05-26-architecture-layering-v0-1.md
confidence: high
---

# nano-NotebookLM 知识图谱与向量索引架构分析

## 一句话判断

nano-NotebookLM 的强项不是 verified truth，而是把课程材料做成“可引用、可搜索、可编辑”的学习型 GraphRAG。

对本资料库最有价值的是三点：

```text
BM25 + FAISS + RRF 混合检索
concept embedding + BFS graph neighborhood
generated graph + human edit overlay
```

## 它的整体链路

```text
上传资料
  -> 文档抽取
  -> chunk_pages 保留 source_file / page / slide / location
  -> chunks.json
  -> FAISS vector index + BM25 index
  -> Stage A per-file macro topics
  -> Stage B per-chunk leaf concepts
  -> knowledge_graph.json
  -> GraphRAG / cited chat / editable mindmap
```

所有运行态数据基本放在 `artifacts/`，没有传统数据库。关键文件包括：

- `artifacts/courses/<course_id>/chunks.json`
- `artifacts/courses/<course_id>/knowledge_graph.json`
- `artifacts/courses/<course_id>/mindmap_edits.json`
- `artifacts/indices/faiss/<preset>/global/`
- `artifacts/indices/bm25/global.json`

## 向量索引设计

### VectorIndex

`VectorIndex` 用 FAISS `IndexFlatIP`，要求 embedding 归一化，所以 inner product 等价于 cosine。

它保存两类东西：

- `faiss.index`：向量索引。
- `chunks_meta.json`：chunk metadata，不把 embedding 混进 chunk 文本结构。

高信号点：

- `embed_fn` 注入，不硬绑某个 embedding 模型。
- `chunk_id -> vector` cache，可从旧 FAISS index reconstruct 出来，避免增量上传时全库重算。
- 检测 vector 维度不一致时丢弃 cache，重新 embedding，避免模型切换后的静默污染。

### BM25Index

BM25 用 JSON 保存 tokenized corpus 和 chunks，不用 pickle。

CJK 处理很朴素但实用：

```text
English words + Chinese single chars + Chinese bigrams
```

这对我们的中文资料库有参考价值：早期不用复杂分词，也可以先用 char/bigram 兜住中文关键词。

### HybridSearch

混合检索采用 RRF：

```text
vector_results = FAISS(query, top_k * 3)
bm25_results = BM25(query, top_k * 3)
score(chunk) = sum(weight / (rrf_k + rank))
```

价值：不会让纯向量或纯关键词单一路径垄断结果。对我们未来 raw/wiki 搜索层很适配。

## 知识图谱设计

### 两阶段抽取

Stage A：按 source file 抽 macro topics。

- 每个文件对应一个 chapter root。
- 每个文件抽 3-9 个 topic。
- topic 可以带 prerequisite_of，用于学习顺序。
- Stage A 并发有限制，避免多文件上传时打爆 LLM。

Stage B：按 chunk 抽 leaf concepts。

- prompt 里注入该文件的 topics。
- leaf concept 必须尽量挂到 parent_topic。
- 每个 concept 带 source_chunks，包含 chunk_id、source_file、location、page/slide。

最后合成：

```text
leaf concept -> topic -> chapter root
```

再加：

```text
depends-on / is-a / example-of / related
```

### Concept Embedding

GraphRAG 不是直接对 chunk 搜索，而是给 concept 做 embedding：

```text
concept name + definition + source chunk excerpt
```

这个设计很关键：concept embedding 不只看概念名，还加一小段原文上下文，避免跨语言或同名概念误配。

### Graph Search

GraphRAG 检索流程：

```text
query embedding
  -> cosine rank concept nodes
  -> top_k seed concepts
  -> BFS 2 hops along graph edges
  -> collect reachable nodes' source_chunks
  -> materialize chunks from chunks.json
  -> return cited SearchResult
```

它的图谱分数是 retrieval score，不是 truth confidence。

## 可编辑图谱 Overlay

系统抽取结果是 `knowledge_graph.json`。

用户编辑不直接改系统图，而是 append 到 `mindmap_edits.json`：

- add_node
- update_node
- delete_node
- add_edge
- delete_edge

每次读取图谱时：

```text
system KG + replay edit ops = rendered graph
```

高信号点：

- 重新抽取不会覆盖用户编辑。
- edit op 有校验，避免 dangling edge。
- root node 不能删除。
- node name/definition 被编辑后，会清空旧 concept_embedding，避免 GraphRAG 继续用旧向量排序。
- 写入 sidecar 使用临时文件 + replace + fsync，降低崩溃丢数据风险。

这个模式非常适合我们未来处理“AI 编译图谱 + 人类校正”。

## 对本资料库的借鉴

### 立即吸收为设计原则

- 任何搜索命中都必须回到 source chunk / source file。
- 图谱检索分数不能等同于可信度。
- AI 自动生成图谱和人类编辑应该分层保存。
- embedding 模型切换必须有命名空间或重建机制。
- 图谱节点修改后，相关 embedding/cache 必须失效。

### 中期可实现

- 本地混合检索：BM25 + vector + RRF。
- GraphRAG：先用 claim/pattern/concept 节点 embedding 找 seed，再扩展 supports/contradicts/refines/related 等关系。
- generated graph overlay：AI 生成结构 + 人类审定 sidecar。
- 检索 score gate：低分时不要硬答，回退到普通检索或要求更多来源。

### 不应直接照搬

- 它的 relation 类型太学习工具化：`is-a / part-of / depends-on / example-of / related`，不够表达 verified knowledge。
- 它的 graph extraction 允许基于 sample chunks 生成图谱；我们不能把 sample graph 当长期 truth。
- 它的知识图谱是为了学习可视化和问答，不是为了采纳决策。
- 它没有 claim-level 的 source_quality、negative_evidence、verification_status、confidence 治理。

## 和我们主线骨架的对应

| 主线骨架 | nano-NotebookLM 是否补充 | 判断 |
|---|---|---|
| SCHEMA.md | 部分补充 | 可参考 Chunk / Concept / Relation 模型，但需扩展 verified 字段 |
| 资料晋级流程 | 部分补充 | 两阶段抽取可参考，但我们还要 raw->summary->claim/pattern->decision |
| 验证门槛 | 弱补充 | score gate 可借鉴，但 retrieval gate 不是 truth gate |
| 关系模型 | 中等补充 | 给出基础教学关系，但我们需要 supports/contradicts/refines/replaces |
| 冲突裁决 | 不足 | 没有处理多来源 claim 冲突 |
| 健康检查 | 部分补充 | dangling edge、cache invalidation、score fallback 可借鉴 |
| 实现顺序 | 强补充 | 先 chunk/index，再 KG，再 GraphRAG，再 UI overlay，工程顺序清楚 |

## 当前采纳结论

采用为中期搜索扩展层和关系操作机制参考。

不进入第一阶段核心实现；第一阶段仍先完成：

```text
SCHEMA.md
晋级流程
验证门槛
关系模型
健康检查
```

