---
record_kind: p1_candidate_point
status: candidate
knowledge_status: candidate
project_id: VAKS
created_at: 2026-06-11
created_by: Codex
source:
  - raw/repos/2026-06-11-safishamsi-graphify-source.md
  - outputs/review/2026-06-11-safishamsi-graphify-candidate-distillation.md
  - wiki/summaries/2026-06-11-safishamsi-graphify-architecture-review.md
processing_tier: heavy
retrieval_policy:
  policy_kind: project_context_only
  default_scope: project_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: p1_candidate_not_authority
promotion_gate: retrieval_layer_comparison_and_sandbox_required
action_basis_allowed: false
truth_mutation_allowed: false
borrow_value: strong
borrow_order: P1
target_layer:
  - retrieval-layer
  - derived-graph-cache
  - agent-gateway
  - context-pack-preparation
tags:
  - p1
  - candidate-only
  - graph-retrieval
  - code-graph
  - retrieval-layer-design
---

# P1 Candidate: Graphify Code/Document Graph Retrieval Layer

## 说人话

Graphify 给 VAKS 的最大启发是：

```text
别只做“搜文字/搜向量”。
先把资料库的结构关系抽出来，让 AI 能沿着结构找上下文。
```

它像一张项目地图。搜索不是直接问“哪段文本最像”，而是先找到相关节点，再看它周围的函数、文件、概念、社区、调用、导入、文档关系。

## 放在 VAKS 检索层的位置

```text
Query Intent Router
-> Authority / Scope Bucket Filter
-> Graph Retrieval Inside Allowed Bucket
-> Lexical / Vector / Graph Hybrid Recall
-> Bucket-Local Rerank
-> Anchor Queue
-> Context Pack
-> Evidence / Action Gate
```

Graphify 对应的是第三步：`Graph Retrieval Inside Allowed Bucket`。

注意：必须先过滤 bucket，再跑图。

## 能借鉴的最小设计

### 输入

```yaml
query:
  text:
  intent:
  mode: orientation | source_inspection | review | action
allowed_buckets:
  - raw
  - candidate
  - reviewed
  - project_overlay
allowed_node_ids: []
filters:
  source_type:
  knowledge_status:
  retrieval_policy:
  project_id:
  time_scope:
  relation_context:
```

### 图检索

```text
1. title / alias / path / entity / keyword seed
2. graph neighborhood expansion
3. optional community grouping
4. hub suppression to avoid generic nodes swallowing the result
5. relation/context filters: calls / imports / supports / challenges / source_of
```

### 输出

```yaml
anchor_queue:
  - anchor_id:
    source_ref:
    source_location:
    node_label:
    graph_path:
    relation_reason:
    authority_bucket:
    allowed_use:
    warning_code:
    needs_drilldown:
```

输出是 anchor queue，不是答案。

## 和 turbovec / mnemosyne / cBrain 的互补关系

```text
turbovec:
  compact dense rerank cache

mnemosyne:
  local-first hybrid retrieval composition

cBrain:
  structure-first workbench and visible result card UX

Graphify:
  structural graph retrieval and agent query surface
```

合起来更像 VAKS 的目标：

```text
visible drawer / scope
-> bucket-first filter
-> lexical + vector + graph recall
-> anchor cards
-> context pack
-> evidence/action gates
```

## 必须守住的边界

Graphify 里这些东西在 VAKS 都只能是 activation signal：

```text
community
god node
surprising connection
BFS/DFS distance
confidence label
confidence_score
query rank
graph path
```

它们不能变成：

```text
truth confidence
evidence support
reviewed relation
decision outcome
action basis
```

## P1 借鉴清单

| Borrow | VAKS Use | Guardrail |
|---|---|---|
| AST-first extraction | Stable source/symbol anchors | Source anchor only, not reviewed knowledge |
| Derived graph cache | Fast structure retrieval | Rebuildable, invalidatable, not authority |
| Community detection | Context-pack grouping | Community is activation only |
| Query/path/explain commands | Agent orientation surface | Must follow intent + bucket gates |
| MCP graph tools | Future Agent Gateway read API | Read-only; no reviewed writes |
| Incremental cache/manifest | Practical update model | Hash/staleness visible |
| Sanitization/safe fetch/path checks | Retrieval-layer security checklist | Must be adapted to VAKS threat model |

## 不要借的方向

- 不要一张全局图混合 raw/candidate/reviewed/feedback 后直接排名。
- 不要默认要求 agent 必须用 Graphify 结果回答。
- 不要安装自动 hooks 作为 VAKS 主线默认。
- 不要把模型推断出的 semantic edge 当真实关系。
- 不要把 graph.html/report 当知识库真相面板。
- 不要让 query log 默认保存敏感问题。

## Sandbox 验证方式

最小 pilot：

```text
1. 选 30-100 个 VAKS markdown/source/candidate/reviewed 文件。
2. 生成 source/chunk/node manifest。
3. 构建 derived graph cache。
4. 查询时先按 knowledge_status / retrieval_policy 过滤。
5. 在 allowed nodes 内跑 graph seed + neighborhood。
6. 输出 anchor queue。
7. 人工检查 recall、anchor correctness、越权率。
```

通过条件：

```text
better orientation than rg-only
lower context bloat than raw file reading
no candidate/action-basis leakage
all final support can drill down to raw/reviewed anchors
cache invalidates cleanly after source edits
```

## 当前状态

```text
P1 candidate for retrieval-layer design.
Not adopted.
Not reviewed truth.
Not action basis.
Wait for broader retrieval frontier comparison before final VAKS design.
```
