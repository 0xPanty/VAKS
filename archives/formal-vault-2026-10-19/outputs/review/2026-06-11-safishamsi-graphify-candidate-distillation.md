---
type: candidate_distillation
status: draft
title: "Graphify：代码/文档图谱化的 agent 检索层"
created_at: 2026-06-11
created_by: Codex
processing_level: heavy
processing_tier: heavy
knowledge_status: candidate
provisional: true
overlay_state: project_sidecar_created
review_pressure: review_due
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
derived_from:
  - raw/repos/2026-06-11-safishamsi-graphify-source.md
  - raw/repos/_snapshots/2026-06-11-safishamsi-graphify-565026d3d10f.zip
  - wiki/summaries/2026-06-11-safishamsi-graphify-architecture-review.md
  - outputs/review/project_lens_overlays/2026-06-11-graphify-graph-retrieval-layer.md
  - outputs/review/vaks-retrieval-layer-design-2026-06-11/p1-graphify-code-graph-retrieval-layer.md
projects:
  - verified-action-knowledge-system
topics:
  - graph-retrieval
  - code-graph
  - agent-context
  - tree-sitter
  - community-detection
  - retrieval-layer
  - boundary-governance
borrow_value: strong
borrow_order: P1_for_retrieval_layer_design
evidence_strength: medium_for_design_low_for_vaks_runtime
dev_context_hint:
  core: retrieval-layer-design
  support: agent-context-and-derived-graph-cache
  risk: graph-rank-confidence-and-hooks-must-not-be-authority
  cold_references: implementation-package-until-sandboxed
tags:
  - candidate-only
  - source-distillation
  - github
  - graph-retrieval
  - retrieval-layer
  - design-only
---

# 候选蒸馏：Graphify

## 一句话

Graphify 是一个“把项目文件抽成知识图谱，再让 AI 先查图、再读源码”的检索层。

说人话：它不是 SQL，也不是传统 RAG，也不是单纯向量库。它像给一个代码库/资料夹做一张结构地图：文件、函数、类、导入、调用、文档概念、图片/论文/视频转出来的概念，都变成节点和边。AI 问问题时先从这张图里找相关区域，再决定要不要打开原文件。

## 它的主要逻辑

```text
detect files
-> local code extraction by tree-sitter / deterministic parsers
-> optional video/audio transcription
-> docs/papers/images semantic extraction
-> merge nodes/edges into NetworkX graph
-> Leiden/Louvain community detection
-> report + graph.json + graph.html
-> CLI/MCP/assistant skill queries
```

核心不是“召回一段最像的 chunk”，而是：

```text
先把系统结构显出来
再围绕结构做 scoped traversal
最后给 agent 一小包可读上下文
```

## 对 VAKS 最有借鉴的点

### 1. 图检索可以做“结构导航”，不是证据支持

Graphify 的图边很适合做：

```text
source / file / symbol / concept orientation
neighbor activation
community briefing
impact surface
```

但对 VAKS 来说，它不能做：

```text
truth confidence
evidence support
reviewed relation
action basis
```

这个区别非常关键。Graphify 能帮我们“先看到该看哪里”，不能替我们判断“这个说法是否成立”。

### 2. 本地 AST 抽取比全靠模型稳

它对代码结构尽量用 tree-sitter 本地抽取：

```text
classes
functions
imports
calls
source_file
source_location
```

这个思路适合 VAKS 的检索层：能确定的结构就不要靠模型猜。未来 VAKS 如果做 repo/source adapter，应该优先抽稳定锚点，再让模型做候选理解。

### 3. 社区分群适合 context pack 预组织

Graphify 用 Leiden/Louvain 把图分成 communities，又找 god nodes、surprising connections、suggested questions。

这可以借鉴成 VAKS 的：

```text
activation neighborhood
context-pack sectioning
risk/challenge candidate discovery
review queue hints
```

边界是：community 只是分组和导航，不是“同一社区就互相支持”。

### 4. Query-first agent habit 值得借鉴，但不能强制越界

Graphify 很强调：有 `graphify-out/graph.json` 时，AI 先跑 `graphify query`，再 grep/read raw files。

VAKS 可借鉴的是“先走 retrieval adapter，拿到锚点清单和边界标签”。不能照搬的是强制 hook：

```text
bad for VAKS:
  any query -> automatically use graph result as preferred answer context

better for VAKS:
  query intent -> authority bucket -> allowed retrieval adapter -> anchor queue
```

### 5. 增量 cache 和 manifest 是工程上很实用的

Graphify 的 hash/cache/manifest 思路适合 VAKS 派生检索层：

```text
Markdown/YAML/source snapshot = authority
graph/vector/BM25/cache = rebuildable derived layer
source/chunk hash = stale detection and invalidation
```

VAKS 最需要的不是“永远最新的自动总结”，而是“能重建、能失效、能追溯”的索引。

### 6. 安全边界有可借鉴清单

Graphify 明确处理了几个检索层常见风险：

```text
skip likely secret files
safe URL fetch and SSRF checks
graph file size cap
graph path must stay inside graphify-out
sanitize labels and metadata
prompt-injection wrappers / neutralization
hook install/uninstall boundaries
```

VAKS 未来做 agent gateway 或 derived graph cache 时，这些应该进入风险清单。

## 和我们当前检索思路的差别

| 维度 | Graphify | VAKS 应该怎么吸收 |
|---|---|---|
| 核心目标 | 让 AI 快速理解代码/资料夹结构 | 让检索高效，同时守住 raw/candidate/reviewed/action 边界 |
| 数据形态 | graph.json / report / HTML / MCP tools | Markdown/YAML authority + rebuildable graph/cache/index |
| 召回逻辑 | 词匹配 seed + BFS/DFS + context filter | authority bucket first + lexical/vector/graph recall inside bucket |
| 置信标签 | EXTRACTED / INFERRED / AMBIGUOUS | 可做 review hints，但不能等于 truth confidence |
| 自动化 | hooks、assistant rules、MCP | 只能作为显式 adapter/sandbox，不能默认越权 |
| 输出 | scoped graph context | anchor queue + allowed-use label + context pack |

## Candidate Points

| Candidate Point | VAKS Fit | Boundary |
|---|---|---|
| Deterministic structure extraction should precede semantic interpretation where possible. | Strong | Extraction is provenance/anchor aid, not truth. |
| Graph communities can organize retrieval context. | Strong | Community membership is activation only. |
| Query-first assistant workflows reduce blind grep and context bloat. | Medium/Strong | Must respect user intent and authority buckets. |
| Confidence tags on extracted/inferred/ambiguous graph edges are useful review routing. | Medium | They cannot become VAKS truth confidence. |
| Incremental graph/cache rebuild is necessary for practical retrieval. | Strong | Cache is derived and rebuildable. |
| MCP graph tools can expose retrieval to agents. | Medium | Future Agent Gateway must quarantine writes and support claims. |

## 值得进入检索层开发区的 P1 设计点

```text
P1: Authority-bucketed graph retrieval adapter

Input:
  query intent
  allowed buckets
  source/chunk IDs
  relation/context filters

Recall:
  title/path/entity/keyword seed
  graph neighborhood expansion
  community summary / god-node hints

Output:
  anchor queue
  relation path as explanation
  warning_code and allowed_use
  drilldown links to raw source / reviewed note

Forbidden:
  graph rank as trust
  inferred edge as reviewed relation
  community as support
  hook as default authority
```

## 不该直接借的部分

- 不要把 `graph.json` 当 VAKS source of truth。
- 不要让 `INFERRED` edge 自动变成 reviewed relation。
- 不要让 community/god node 变成“更可信”。
- 不要默认安装 hooks 或 assistant 强制规则。
- 不要在没有 source/chunk authority labels 的情况下混检 raw、candidate、reviewed。
- 不要让 query log 泄露用户敏感查询。
- 不要把 README benchmark 当作 VAKS 性能证据，必须本地 pilot。

## 下一步

把 Graphify 放入 VAKS 检索层开发区，作为“结构图检索 / agent orientation / derived graph cache”的 P1 候选输入。后续等向量库、BM25/稀疏检索、hybrid/RRF、reranker、chunking/eval 都吸收完，再做 VAKS 定制检索层设计。
