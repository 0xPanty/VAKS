---
type: candidate_distillation
record_kind: candidate_distillation
status: draft
title: "OneFeed：把推荐流和搜索查询统一成一个生成式检索框架"
created_at: 2026-06-11
created_by: Codex
processing_tier: heavy
knowledge_status: candidate
provisional: true
overlay_state: none
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
  - raw/papers/2026-06-11-guoxun-onefeed-source.md
  - raw/papers/2026-06-11-onefeed-unified-feed-query-generation-source/eprint/main.tex
  - wiki/summaries/2026-06-11-guoxun-onefeed-architecture-review.md
  - outputs/review/project_lens_overlays/2026-06-11-onefeed-search-recommendation-fusion.md
  - outputs/review/vaks-retrieval-layer-design-2026-06-11/p2-onefeed-feed-search-query-generation.md
projects:
  - verified-action-knowledge-system
topics:
  - search-recommendation-fusion
  - query-generation
  - feed-recommendation
  - semantic-id
  - feedback-loop
  - retrieval-layer
borrow_value: medium
borrow_order: P2_for_retrieval_layer_design
evidence_strength: medium_for_method_low_for_empirical_claims
dev_context_hint:
  core: retrieval-layer-design
  support: query-expansion-and-feedback-routing
  risk: expected-results-and-closed-loop-truth-mutation
  cold_references: recommendation-system-specific-modeling
tags:
  - candidate-only
  - source-distillation
  - arxiv
  - retrieval-layer
  - search-recommendation-fusion
  - design-only
---

# 候选蒸馏：OneFeed

## 一句话

OneFeed 想解决的是：推荐流只看隐式行为，搜索只看显式 query，这两套系统割裂了。

它提出一个统一生成式框架：同一个用户行为编码器，一头生成内容语义 ID 用于推荐候选，一头生成自然语言 query 用于搜索候选，再把两边候选融合。

## 先说最重要的降级

这篇不是完整实证论文。

它自己写得很清楚：

```text
当前版本是 methodological contribution
实验表格是 expected performance estimates
完整 public-dataset training 会在后续版本补
```

附录还有 checklist：数据预处理、弱 query 构造、leakage check、full model、baselines、ablation、case studies 等都还在待完成列表里。

所以 VAKS 可以借它的架构想法，不能借它的性能表当证据。

## 它的核心设计

```text
heterogeneous user behavior sequence
-> shared behavior encoder
-> Feed Semantic ID Generator
-> Intent Query Generator
-> SID-Query alignment objective
-> semantic-ID candidates + query-retrieved candidates
-> fused feed ranking
-> implicit feedback loop
```

更白话一点：

```text
你平时点了什么、看了多久、喜欢/跳过什么
-> 系统学一个共同的用户意图表示
-> 一边猜你接下来可能要看的内容编号
-> 一边猜你可能会搜什么词
-> 用内容编号和搜索词各自召回候选
-> 合并候选
-> 再用你的反馈继续改进
```

## 对 VAKS 有用的点

### 1. 隐式激活和显式查询可以互相补

VAKS 当前也有类似问题：

```text
用户显式问的问题
历史项目、近期材料、使用反馈形成的隐式上下文
```

OneFeed 的启发是：不要把它们做成两条互不相干的检索路。

VAKS 可借成：

```text
explicit query
  -> user intent

recent work / project overlay / feedback ledger
  -> activation hints

both
  -> allowed bucket and anchor queue
```

### 2. 生成 query 可以做候选扩展

OneFeed 的 Intent Query Generator 不是为了回答用户，而是为了扩展候选池。

VAKS 可以借：

```text
用户问法太窄
-> 生成 2-5 个受控检索改写 / 相关 query
-> 只在允许 bucket 里搜索
-> 输出 anchor queue
```

这和普通“让 LLM 多写几个搜索词”不同，VAKS 必须加：

```text
authority bucket
scope
project id
time/version
source type
action_basis_allowed
```

### 3. Semantic ID 可以理解成结构化锚点

OneFeed 用内容 semantic ID 做生成式推荐检索。

VAKS 不一定要照搬推荐系统里的 SID，但可以吸收一个思想：

```text
把内容映射成稳定、可组合、可召回的结构化锚点
```

在 VAKS 里更像：

```text
source_id
chunk_id
claim_id
project_overlay_id
review_queue_id
anchor_path
```

### 4. SID-Query Alignment 对 VAKS 是“意图-锚点对齐”

OneFeed 用对比学习让内容 semantic ID 和 query 表示靠近。

VAKS 的低风险翻译不是马上训练模型，而是做：

```text
query intent
<-> anchor type
<-> retrieval bucket
<-> context-pack role
```

也就是把“用户想干什么”对齐到“该找哪类锚点”。

### 5. 反馈闭环只能改 activation，不能改 truth

OneFeed 的闭环反馈用于继续提升两个生成头。

VAKS 可以借反馈闭环，但必须改边界：

```text
positive feedback:
  improve activation / routing / query rewrite candidates

negative feedback:
  create review_pressure / scope warning

explicit correction:
  create review_due

forbidden:
  feedback directly changes truth confidence
  feedback directly promotes reviewed relation
  feedback directly changes action basis
```

## 值得放进检索层开发区的 P2 点

```text
P2: Query-generation-assisted retrieval expansion

query + active project context
-> generate controlled query variants
-> bucket-first retrieval
-> merge lexical/vector/graph candidates
-> anchor queue
-> feedback adjusts future activation, not truth
```

## 不要借的方向

- 不要把“预期性能表”当 benchmark evidence。
- 不要用弱伪 query 构造出的结果支撑真实检索质量。
- 不要把用户点击/停留/正反馈当作知识更真。
- 不要做无边界的自增强闭环，否则会放大偏见和历史路径依赖。
- 不要让生成 query 越过 source scope、authority bucket、action basis gate。
- 不要把推荐系统里的商业指标直接搬进 VAKS 的知识治理。

## Candidate Points

| Candidate Point | VAKS Fit | Boundary |
|---|---|---|
| Explicit query and implicit activation should be jointly considered. | Strong | Activation is not truth. |
| Generated query variants can expand recall. | Medium/Strong | Must be bucket-filtered and source-anchored. |
| Semantic IDs suggest stable retrieval anchors. | Medium | VAKS anchors stay source/review/schema based. |
| Alignment between query intent and content anchors is valuable. | Medium | Avoid unreviewed learned relevance as authority. |
| Feedback loop can improve retrieval routing. | Strong | Feedback cannot mutate truth confidence. |
| Expected-performance tables are not evidence. | Strong as caution | Require measured results or sandbox pilot. |

## 和 VAKS 检索层的关系

OneFeed 对 VAKS 不是核心检索引擎，而是一个辅助思路：

```text
when user query is underspecified
or active project context is strong
or recall is too narrow
then generate controlled query variants
and retrieve inside allowed buckets
```

它和 Graphify / turbovec / mnemosyne 的位置不同：

```text
turbovec:
  vector rerank primitive

mnemosyne:
  local hybrid retrieval composition

Graphify:
  structural graph retrieval and agent orientation

OneFeed:
  query-generation-assisted candidate expansion and feedback routing
```

## 当前判断

```text
borrow_value: medium
borrow_order: P2
empirical_evidence: low
method_design_value: medium
action_readiness: not_ready
```

后续只有在 VAKS retrieval pilot 里证明 query variants 提升 recall 且不越权，才值得升级。
