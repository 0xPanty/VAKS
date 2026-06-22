---
type: candidate_distillation
record_kind: candidate_distillation
status: draft
title: "cBrain 脑图对 VAKS 的价值在外层工作台，不在 truth/review 核心"
created_at: "2026-06-08"
created_by: Codex
processing_tier: medium
knowledge_status: candidate
overlay_state: none
review_pressure: none
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
derived_from:
  - raw/articles/2026-06-08-cbrain-knowledge-system-mindmap-source.md
projects:
  - verified-action-knowledge-system
topics:
  - knowledge-graph-ui
  - activation-surface
  - node-note-model
  - public-share-page
  - productized-knowledge-system
  - context-workbench
borrow_value: medium
borrow_order: P2
evidence_strength: medium
tags:
  - candidate-only
  - source-distillation
  - design-only
  - vaks-borrow-P2
provisional: true
---

# 候选蒸馏：cBrain 脑图对 VAKS 的价值在外层工作台，不在 truth/review 核心

## 一句话

这个 cBrain 分享页值得蒸馏，借鉴等级是 P2。

它对 VAKS 的价值不是“怎么验证知识真伪”，而是“一个个人知识体系如何被做成可浏览、可钻取、可分享、可多视图展示的产品界面”。

说人话：

```text
VAKS 管的是：资料进来后，怎么不乱、怎么审、怎么别把 AI 总结当真。
cBrain 这个页面展示的是：知识体系长出来后，怎么让人看、找、钻、分享。
```

所以它能借外壳，不能借内核。

## Borrow Tag

```yaml
borrow_value: medium
borrow_order: P2
borrow_scope:
  - activation-surface
  - knowledge-map-ui
  - node-drilldown
  - node-note-split
  - public-share-page
  - multi-view-graph-workbench
  - onboarding-demo
not_borrow_scope:
  - reviewed truth
  - evidence support
  - truth confidence
  - reviewed relation
  - core schema
  - action basis
  - kq-as-quality-score
```

为什么不是 P1：

```text
它没有解决 VAKS 最核心的问题：
source provenance、candidate/reviewed 边界、evidence support、point collision、action basis。

但它很好地展示了：
知识体系如果只存在 Markdown 文件里，用户未必能感受到全局结构；
一个外层工作台可以把结构、节点、笔记和探索路径亮出来。
```

## 来源支撑

本次公开快照显示：

- 根节点是 `c知识体系`。
- `mapInfo` 有 243 条脑图节点。
- `nodeInfo` 有 274 条节点详情。
- 273 个节点带有笔记内容。
- 节点笔记总字符数约 320701。
- 顶层分支包括底层智慧、人文艺术、科学知识、信息技术、实践体系、资源管理。
- 页面前端提供脑图、旭日图、树状图、矩阵树图、关系图等视图。

这些信息只说明这个公开页面有足够内容和结构，值得作为设计参考；不说明其中任何知识判断已经被验证。

## Candidate Point

VAKS 未来可以把 reviewed / candidate / source / context pack 的 Markdown 底座，投射成一个外层“知识工作台”：

```text
左边或主区:
  结构图 / 节点树 / 关系图 / review queue map

节点详情:
  source links
  candidate summary
  reviewed claims
  support / challenge / scope notes
  review status
  activation tier
  use feedback

操作:
  drill down
  search
  open source card
  open review packet
  show related decisions
  export/share context pack
```

这里的重点不是“图谱更炫”，而是把 VAKS 的边界看得见：

```text
raw 是 raw
candidate 是 candidate
reviewed 是 reviewed
action basis 是 action basis
```

## 应该吸收

- 同一套节点数据可以有多种视图：脑图、树、关系图、统计面板。
- 节点导航和节点详情分离：结构负责找路，详情负责上下文。
- 公开分享页可以作为 onboarding/demo，让别人快速理解一个系统。
- 节点钻取比一次性展开全库更适合大型知识体系。
- 颜色、计数、标签可以作为 UI 状态，但必须解释清楚含义。

## 不应该吸收

- 不要把 cBrain 的个人分类树搬成 VAKS schema。
- 不要把 `kq`、访问量、节点数、颜色当成知识质量或 truth confidence。
- 不要把图谱连线当 reviewed relation。
- 不要让可视化界面替代 Evidence Packet / Evidence Support Check。
- 不要把公开展示层 API 当作 VAKS 后端架构参考。
- 不要把个人知识节点内容直接变成 VAKS reviewed knowledge。

## 与 VAKS 现有设计的关系

VAKS 已经有这些内核：

```text
Capture -> Understand -> Review -> Connect -> Act and Learn

raw/source card
candidate distillation
review queue
reviewed claim / pattern / decision
memory tier / activation
context pack
feedback ledger
```

cBrain 对应的不是这些内核，而是这些内核之上的可视化和使用表面：

```text
VAKS core:
  严格边界、证据、审查、行动依据。

cBrain-like surface:
  浏览、钻取、搜索、展示、分享、多视图。
```

最自然的融合位置：

```text
Activation / Context Pack / Workbench
```

不自然的位置：

```text
Source Intake / Evidence Review / Truth Confidence
```

## 对 VAKS 的最小落地建议

现在不建议改核心 schema。

最小吸收方式：

```text
先做一个只读 VAKS cockpit 原型：
  读取 wiki/indexes、raw/source cards、outputs/review。
  展示 source -> candidate -> reviewed -> decision 的状态。
  每个节点明确显示 layer 和 action_basis_allowed。
  不允许 UI 直接改变 truth。
```

如果更轻：

```text
先在未来 docs / product sketch 里记录：
  VAKS 需要一个 cBrain-like activation surface。
```

## Risk / Inhibition

```text
risk:
  图谱 UI 很容易制造“看起来都连上了，所以都可信”的错觉。
  大型个人分类树容易诱导 VAKS 过度分类。
  计数和颜色容易被误读成质量分。
  公开分享页容易暴露不该公开的 raw/candidate 信息。

inhibition:
  每个 UI 节点必须显示 layer/status。
  confidence 只能来自 review，不来自图谱位置或颜色。
  public share 默认只分享 safe context pack，不分享原始敏感资料。
  graph edge 默认是 candidate/activation relation，除非已 reviewed。
```

## 融合判断

```text
fusion_decision: adapt / watch
borrow_value: medium
borrow_order: P2
evidence_strength: medium
implementation_cost: medium-high
integration_fit: medium
reversibility: high
```

## 后续行动

- 若未来做 VAKS viewer / cockpit / context-pack UI，这条进入 P2 参考。
- 当前不改 `SCHEMA.md`，不新增 reviewed pattern。
- 需要实现前，应再补一轮 UI/UX 横向比较：cBrain、Obsidian Graph/Base、NotebookLM-style source map、GraphRAG viewers。
