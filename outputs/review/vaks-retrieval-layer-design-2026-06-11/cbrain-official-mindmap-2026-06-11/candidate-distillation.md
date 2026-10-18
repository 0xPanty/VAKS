---
type: candidate_distillation
status: draft
title: "cBrain 官网脑图：树形导航、分层搜索与知识工作台"
created_at: "2026-06-11"
created_by: Codex
processing_level: heavy
processing_tier: heavy
knowledge_status: candidate
overlay_state: retrieval_layer_workspace
review_pressure: none
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: retrieval_layer_design_review_required
action_basis_allowed: false
truth_mutation_allowed: false
derived_from:
  - outputs/review/vaks-retrieval-layer-design-2026-06-11/cbrain-official-mindmap-2026-06-11/source-card.md
  - outputs/review/vaks-retrieval-layer-design-2026-06-11/cbrain-official-mindmap-2026-06-11/cbrain-official-mindmap-type4.json
  - outputs/review/vaks-retrieval-layer-design-2026-06-11/cbrain-official-mindmap-2026-06-11/node-details/
projects:
  - verified-action-knowledge-system
topics:
  - retrieval-workbench
  - activation-surface
  - layered-search
  - tree-navigation
  - node-note-model
  - query-intent-router
  - knowledge-quantity-signal
borrow_value: strong
borrow_order: P1_for_workbench_navigation_P2_for_retrieval_engine
evidence_strength: medium_for_design_low_for_runtime
tags:
  - candidate-only
  - source-distillation
  - retrieval-layer-design
  - cbrain
  - design-only
---

# 候选蒸馏：cBrain 官网脑图

## 一句话

这条 cBrain 官网脑图对 VAKS 检索层开发区是 **P1 工作台参考**，不是检索算法参考。

说人话：它厉害的地方不是“向量检索多强”，而是把一个知识系统做成了能看、能点、能钻、能搜索、能学习的入口。对 VAKS 来说，它最有价值的是 **检索前的导航层、检索中的分层搜索、检索后的节点工作台**。

## 它的主要逻辑

从公开脑图和节点详情看，它的系统逻辑是：

```text
知识体系入口
-> 树形脑图导航
-> 节点详情/笔记承载内容
-> 标题/别名搜索
-> 笔记全文搜索
-> 资料/图书全文搜索
-> 知识量化/连接度辅助观察
-> 学习方法指导用户怎么拆、怎么连、怎么复用
```

这不是一个纯检索引擎，而是一个 **知识工作台**。

## 对 VAKS 检索层最有价值的点

### 1. 检索入口不应该只有一个搜索框

cBrain 的脑图提醒我们：用户找知识时，很多时候不是直接知道关键词，而是先需要一个结构入口。

VAKS 可以借：

```text
retrieval home
  -> source intake
  -> candidate distillation
  -> reviewed knowledge
  -> decisions
  -> risk / stale / conflict
  -> retrieval-layer experiments
```

也就是先让用户知道“有哪些抽屉”，再搜索。

### 2. 分层搜索比全库搜索更适合知识系统

cBrain 的搜索体系大意是：

```text
先搜节点标题/别名
再搜笔记内容
再搜资料库/图书全文
```

VAKS 可以改造成：

```text
1. structure search:
   path / heading / topic / alias / source_id

2. note search:
   source card / candidate distillation / summary / decision

3. evidence/source search:
   raw source / retained text / snapshot / citation span

4. semantic rerank:
   only inside allowed authority buckets
```

这个很适合我们现在的 bucket-first 检索层。

### 3. 树形导航适合做 query intent router 的可视化

cBrain 把“关于 / 教程 / 更多 / 价格”等做成树。VAKS 可以把任务意图做成树：

```text
我要恢复上下文
我要找某个来源
我要判断一个候选点
我要找反例/风险
我要组 context pack
我要准备 action basis
```

这比让用户从空白搜索框开始更稳。

### 4. 节点详情层适合承载 anchor queue

cBrain 的节点不是只有标题，关键节点还有 note。VAKS 的检索结果也不应该只返回文件名，而应该返回：

```text
anchor title
layer/status
source path
heading/span
why retrieved
allowed use
risk / challenge / missing context
next action
```

这就是 VAKS 的 anchor queue 工作台化。

### 5. 知识量化只能借作 activation signal

cBrain 的 `kq` / 知识量机制很有启发：节点连接、子节点、内容积累可以帮助用户观察某块知识是否“厚”。

VAKS 可以借成：

```text
coverage_hint
activation_weight
retrieval_priority_hint
review_pressure_hint
```

但不能借成：

```text
truth confidence
evidence support
reviewed relation strength
action readiness
```

## 跟 VAKS 的核心区别

| 维度 | cBrain | VAKS |
|---|---|---|
| 核心目标 | 建个人知识体系和学习工作台 | 支撑可验证行动 |
| 主要结构 | 树形脑图 + 节点笔记 | source / candidate / reviewed / action 分层 |
| 检索逻辑 | 节点标题 -> 笔记 -> 资料 | query intent -> authority bucket -> hybrid recall -> anchor queue |
| 量化逻辑 | kq / 连接度 / 子节点 | activation / coverage / review pressure，不能当 truth |
| 风险 | 结构清楚会被误读为可靠 | 边界太强可能牺牲检索体验 |
| 最适合借用位置 | workbench / activation surface | core truth/review 之外 |

## 对 VAKS 检索层的具体借鉴

### Borrow 1: Structure-first Retrieval Entry

先给结构，再给搜索。

```text
用户先选择任务/区域
-> 系统确定允许桶
-> 再做关键词/语义检索
```

这会减少“全库乱搜”的风险。

### Borrow 2: Layered Search Mode

VAKS 可以设计四段检索：

```text
title/alias/path search
metadata/status/topic search
full-text/BM25 search
vector rerank inside allowlist
```

每一段都必须保留 `knowledge_status` 和 `retrieval_policy`。

### Borrow 3: Node Workbench

把检索结果从“列表”升级成“节点卡片”：

```text
node identity
source anchor
status badge
allowed use
support/challenge/risk/missing
open source / open distillation / build context pack
```

### Borrow 4: Up/Down/Left/Center Retrieval Moves

cBrain 的“上下左中”可以转译为 VAKS 检索操作：

```text
下:
  split source into candidate points / chunks

上:
  synthesize candidates into pattern / decision pressure

左:
  retrieve siblings, related sources, counterexamples, stale decisions

中:
  focus current task and build context pack
```

这比“搜索一下”更像一个可操作的检索工作台。

### Borrow 5: KQ As Non-Authority Signal

借它的量化直觉，但换成 VAKS 安全字段：

```text
coverage_count
anchor_count
review_queue_count
conflict_count
last_used_at
last_reviewed_at
source_span_count
```

这些只帮助激活和排序，不证明真伪。

## 不要借鉴

```text
不要把树形目录当 VAKS schema。
不要把节点连接数/kq 当可信度。
不要把图谱边当 reviewed relation。
不要让公开分享页默认暴露 raw/candidate。
不要用产品导航替代 evidence/review/action gate。
不要让“看起来结构完整”替代 source support。
```

## 融合判断

```yaml
fusion_decision: adapt-for-workbench
borrow_value: strong
borrow_order: P1_for_workbench_navigation_P2_for_retrieval_engine
core_schema_change_now: no
mainline_change_now: no
best_layer:
  - retrieval workbench
  - activation surface
  - query intent router UI
  - anchor queue UI
  - context-pack preparation
avoid_layer:
  - truth core
  - reviewed relation
  - action basis
  - evidence support
```

## 对检索层开发区的落点

这条应该放在 `frontier-source-ledger` 里，但分类不是 vector/search algorithm，而是：

```text
retrieval workbench / navigation source
```

它回答的问题是：

```text
VAKS 检索层怎样让用户先看到结构、再选择范围、再搜索、再钻取证据？
```

不是：

```text
用什么 ANN 算法最快？
```

