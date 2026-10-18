---
type: candidate_distillation
record_kind: candidate_distillation
status: draft
title: "出链和反链适合做 VAKS 激活导航，不适合做 reviewed relation"
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
  - raw/videos/2026-06-08-bilibili-obsidian-outlinks-graph-source.md
projects:
  - verified-action-knowledge-system
topics:
  - outlinks
  - backlinks
  - graph-view
  - association-activation
  - context-pack-viewer
  - reviewed-relation-boundary
borrow_value: low
borrow_order: P3
evidence_strength: medium
tags:
  - candidate-only
  - source-distillation
  - design-only
  - vaks-borrow-P3
provisional: true
---

# 候选蒸馏：出链和反链适合做 VAKS 激活导航，不适合做 reviewed relation

## 一句话

这条视频对 VAKS 是 P3 借鉴：有用，但偏基础。它提醒我们，VAKS 未来的图谱 / context-pack viewer 可以借鉴 Obsidian 的出链、反链、局部图和全局图，让用户更容易看见上下文关系。

但它不能进入核心审查逻辑。普通链接只是“可能有关”，不是“已经支持”。

## Borrow Tag

```yaml
borrow_value: low
borrow_order: P3
borrow_scope:
  - onboarding
  - activation-surface
  - candidate-association
  - local-context-graph
  - outlink-backlink-ui
not_borrow_scope:
  - reviewed relation
  - evidence support
  - truth confidence
  - decision support
  - action basis
  - graph-density-as-quality
```

## Candidate Point

VAKS 可以把连接分成两种：

```text
ordinary link:
  raw / candidate 层里的普通导航关系。
  作用是发现上下文、回到来源、激活相关材料。

reviewed relation:
  经过 evidence-aware review 的关系。
  需要明确 support / challenge / scope / risk。
```

Obsidian 的出链和反链属于第一种。它们非常适合帮助用户找路，但不能替代第二种。

## 可以借

- Outlinks：当前节点主动指向哪些资料、候选点、相关笔记。
- Backlinks：哪些资料、候选点、项目上下文引用了当前节点。
- Local graph：围绕当前问题生成一跳或两跳 context neighborhood。
- Global graph：用于 onboarding、健康检查和整体结构感，不用于判断真假。

## 不能借

- 不借“连线 = 支持”。
- 不借“图谱越密 = 知识越好”。
- 不借“反链多 = 更可信”。
- 不借“全局图越大 = 系统越成熟”。

## 对 VAKS 的最小吸收

暂时不改 schema。

如果未来做 viewer，可以这样落：

```text
每条边必须有 relation_state:
  ordinary_link
  candidate_relation
  reviewed_relation
  action_basis_relation

默认显示:
  ordinary/candidate 边是浅色
  reviewed 边需要明确标识
  action-basis 边必须有来源和审查记录
```

这能保留 Obsidian 图谱的易用性，同时不污染 VAKS 的 truth core。

## VAKS 层级归位

```text
Capture:
  允许普通链接快速记录关联。

Understand:
  出链/反链帮助理解当前节点上下文。

Review:
  普通链接不能自动升级为 reviewed relation。

Connect:
  candidate association discovery。

Activation / Context Pack:
  local graph 很适合做 context pack 的可视化入口。

Decision / Action:
  不可作为行动依据。

Use Ledger / Feedback:
  用户反馈可以影响链接的 usefulness / activation 权重，不改变 truth。
```

## 融合判断

```text
fusion_decision: watch / adapt-lightly
borrow_value: low
borrow_order: P3
evidence_strength: medium
implementation_cost: medium
integration_fit: medium
reversibility: high
```

## 为什么是 P3

这条讲的是 Obsidian 很基础的使用方式。我们已经知道 VAKS 需要 Connect / Activation / Context Pack，也已经区分普通关系和 reviewed relation。所以它不是 P1/P2。

它仍然值得留，因为它可以当作新手解释材料和 viewer 设计提醒：

```text
图谱负责帮人找路；
审查负责判断能不能信。
```
