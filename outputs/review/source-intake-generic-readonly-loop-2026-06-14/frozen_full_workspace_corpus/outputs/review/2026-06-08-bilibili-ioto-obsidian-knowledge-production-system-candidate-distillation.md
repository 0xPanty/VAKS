---
type: candidate_distillation
record_kind: candidate_distillation
status: draft
title: "IOTO 的价值在项目推进台和输入/输出/成果边界，不在 VAKS truth/review 核心"
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
  - raw/videos/2026-06-08-bilibili-ioto-obsidian-knowledge-production-system-source.md
projects:
  - verified-action-knowledge-system
topics:
  - ioto
  - obsidian
  - project-workbench
  - daily-task-list
  - input-output-result-boundary
  - context-pack-execution
  - workflow-carry-forward
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

# 候选蒸馏：IOTO 的价值在项目推进台和输入/输出/成果边界，不在 VAKS truth/review 核心

## 一句话

这条视频对 VAKS 是 P2 借鉴。

它不是在讲证据审查，也不是在讲怎样判断知识真假。它有价值的地方是：作者把 Obsidian 里的知识工作拆成了一个可每天执行的项目流程。

说人话：

```text
输入 = 别人给我的资料
输出 = 我写给自己看的思考
任务 = 今天这个项目要推进什么
成果 = 我要交付给别人看的东西
```

VAKS 可以借这个“推进逻辑”，不能借它当“审查逻辑”。

## Borrow Tag

```yaml
borrow_value: medium
borrow_order: P2
borrow_scope:
  - project-workbench
  - daily-task-list
  - input-output-result-boundary
  - context-pack-execution-surface
  - artifact-creation-shortcuts
  - lightweight-review-of-carry-forward
not_borrow_scope:
  - reviewed truth
  - evidence support
  - truth confidence
  - reviewed relation
  - action basis without gate
  - folder-structure-as-schema
  - paid-product-implementation-details
```

为什么不是 P1：

```text
VAKS 已经有 raw / candidate / reviewed / action basis 的硬边界；
这条视频没有补证据审查、冲突处理、source support 或 action basis。

但它很好地补了一个使用层问题：
用户每天怎么围绕一个项目推进 source、thinking、review 和 deliverable。
```

## 他的逻辑链条

作者的逻辑不是“先建一堆文件夹”，而是：

```text
1. 先承认知识生产有不同对象
   输入、内部思考、任务、对外成果不是一回事。

2. 再给每个对象不同标准
   输入要能回到来源；
   输出只要未来自己能看懂；
   成果必须符合别人能接收的标准；
   任务负责把项目往前推。

3. 然后用项目把它们绑在一起
   任务和成果按项目对应；
   从项目任务列表里创建输入、输出和成果；
   新建文件自动带项目属性。

4. 最后用日期任务列表形成日常中枢
   今天看今天的项目任务；
   昨天没完成的滚到今天；
   相邻日期可以回顾推进轨迹。

5. UI 只负责降低摩擦
   快捷面板让创建更快；
   但作者反复强调不要复杂控制面板，越简单越好。
```

## 对 VAKS 的直接启发

VAKS 现在强在“边界”和“审查”，但未来真实使用时也需要一个薄的项目推进面：

```text
当前项目:
  待处理 source
  待蒸馏 candidate
  待 review point
  待补证据 item
  待输出 decision / article / product note
  上次未完成的 carry-forward
```

这个面不需要变成大而全 dashboard。它应该更像 IOTO 的日期任务列表：

```text
今天我要推进什么？
这些东西属于哪个项目？
每个东西现在卡在 raw / candidate / review / action 的哪一层？
哪些没完成，需要带到下一次工作？
```

## Candidate Point

VAKS 可以把“知识系统”和“项目推进”分开设计：

```text
knowledge spine:
  source -> candidate -> review -> reviewed -> relation -> context pack -> action

execution spine:
  project -> today workbench -> create artifact -> carry forward -> use ledger
```

两条线要连接，但不能互相污染。

```text
任务推进可以改变工作状态；
不能改变 truth confidence。

未完成项可以滚动；
不能自动说明内容已经变得更可信。

成果可以发布；
但进入行动或对外主张前要过 action_basis gate。
```

## 可以借

- “输出给自己，成果给别人”的边界解释。
- 项目级日期任务列表作为每天工作的中枢。
- 从任务列表直接创建相关 artifact，并自动带项目 / 状态 / 类型元数据。
- 未完成项滚动到下一天，但要记录为 workflow carry-forward。
- 用相邻日期回顾项目推进。
- 快捷面板要薄，只降低摩擦，不抢走注意力。

## 不能借

- 不把 IOTO 的一级文件夹直接搬成 VAKS schema。
- 不把“输出”当 reviewed knowledge；在 VAKS 里它更接近 candidate comprehension。
- 不把“成果”当 action basis；成果要对外可用仍需证据范围检查。
- 不把文件创建、链接插入、属性附加当作 review。
- 不把未完成任务迁移当进展证明。
- 不借复杂控制面板；VAKS 应避免为了看起来完整而加重日常使用负担。

## 与 VAKS 现有设计的关系

VAKS 内核仍然是：

```text
Capture -> Understand -> Review -> Connect -> Act and Learn
```

IOTO 对应的是外层执行体验：

```text
Capture:
  输入资料。

Understand:
  写给自己看的输出 / 思考。

Review:
  IOTO 视频没有解决；VAKS 继续用 evidence-aware review。

Connect:
  项目属性把相关材料聚合起来。

Act and Learn:
  成果、carry-forward、每日回顾和 use feedback。
```

最自然的融合位置：

```text
Activation / Context Pack / Project Workbench
```

不自然的位置：

```text
Truth Confidence / Reviewed Relation / Evidence Support
```

## 对 VAKS 的最小落地建议

现在不改核心 schema。

可以先记一个未来设计方向：

```text
VAKS project workbench:
  - 按项目聚合 source / candidate / review / decision / output。
  - 每个 item 明确显示 layer 和 action_basis_allowed。
  - 提供 create source card / create candidate / create review packet 的快捷入口。
  - 未完成项可 carry forward，但写入 workflow/use ledger，不写入 truth 层。
  - 默认轻界面，不做重 dashboard。
```

如果后面真的做，可以把它做成只读/半自动面板：

```text
read:
  raw/videos, raw/articles, raw/repos, outputs/review, REVIEW_QUEUE

write:
  只写 candidate/task/use-ledger/workbench state

never write:
  reviewed claims, reviewed relations, truth confidence, action basis
```

## Risk / Inhibition

```text
risk:
  项目工作台容易滑成任务管理软件，反而分散知识审查注意力。
  用户可能把“有项目属性”和“已经理解/审查过”混为一谈。
  未完成项滚动多了，会变成永久待办噪声。
  成果导向容易让系统为了产出而跳过证据检查。

inhibition:
  工作台 item 必须显示 layer/status。
  carry-forward 必须记录原因或至少记录次数。
  publishable output 必须区分 draft / reviewed / action_basis_ready。
  快捷创建只补元数据，不自动提升 knowledge_status。
```

## 融合判断

```text
fusion_decision: adapt-lightly / keep-as-P2-reference
borrow_value: medium
borrow_order: P2
evidence_strength: medium
implementation_cost: medium
integration_fit: medium-high
reversibility: high
```

## 为什么是 P2

这条比普通 Obsidian 操作教程更有价值，因为它有一条清楚的生产链：

```text
资料 -> 思考 -> 项目推进 -> 对外成果
```

这正好能补 VAKS 未来“怎么每天用起来”的部分。

但它不是 P1，因为它没有补 VAKS 最硬的东西：

```text
source support
evidence packet
point collision
reviewed relation
truth/action basis
```

所以当前结论：

```text
可以作为 VAKS 项目工作台 / context-pack execution surface 的 P2 参考。
不进入 reviewed pattern，不改 core schema。
```
