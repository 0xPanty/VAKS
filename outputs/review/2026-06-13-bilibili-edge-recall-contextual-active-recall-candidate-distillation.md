---
type: review_output
record_kind: candidate_distillation
status: candidate_only
provisional: true
created_at: 2026-06-13
created_by: Codex
source_title: 收藏≠学会｜把“看过”变成“记住”
source_ref: raw/videos/2026-06-13-bilibili-bv1rlvg6oeut-edge-recall-source.md
source_record: raw/videos/2026-06-13-bilibili-bv1rlvg6oeut-edge-recall-source.md
source_url: https://www.bilibili.com/video/BV1RLVG6oEut/
author: 鱼先生的模块化Obsidian
platform: bilibili
transcript_method: local_asr
asr_engine: openai-whisper
asr_model: small
processing_tier: heavy
knowledge_status: candidate
overlay_state: none
review_pressure: review_due
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: review_input_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
review_priority: high
borrow_value: strong
borrow_order: P2_candidate_for_human_memory_workbench
fit_layers:
  - Activation
  - Context Pack
  - Use Ledger / Feedback
  - Cooling / Reactivation
  - UI / Workbench
blocked_layers:
  - Reviewed Knowledge
  - Truth Confidence
  - Action Basis
tags:
  - vaks-distill-candidate
  - edge-recall
  - contextual-active-recall
  - source-anchored-recall-card
  - spaced-repetition
  - no-source-pollution
  - activation-workbench
  - use-ledger-feedback
  - cooling-reactivation
  - dashboard-not-truth
---

# Edge Recall - Contextual Active Recall 强蒸馏

## 说人话结论

这条视频解决的不是“资料怎么入库”，而是“资料进库以后，人到底有没有记住”。它的核心判断很朴素：收藏不等于学会，看过不等于记住，AI 能回答也不等于你会用。

Edge Recall 的产品思路是：复习卡不脱离原笔记，不用特殊符号污染原文；在原文位置显示/隐藏答案；用状态栏、侧栏、卡组和移动端把复习变成随手动作；用间隔重复和难度反馈安排下一次复习；用图表给用户复习反馈。

VAKS 有类似思路，但层级不同：我们已经有 `Activation Tier`、`Cooling / Reactivation`、`Use Ledger / Feedback`，这些是系统怎么激活资料、复查资料、记录使用反馈。Edge Recall 是人侧记忆工作台：用户怎么把关键知识真的记住。它可以补 VAKS 的使用体验层，但不能改 truth core。

## VAKS 有没有类似思路？

有，像，但不完全一样。

VAKS 现在类似的部分：

- `Activation Tier`：hot/warm/cold 决定什么资料应该被更早激活。
- `Cooling / Reactivation`：旧资料默认冷却，用到时再被唤醒。
- `Use Ledger / Feedback`：记录知识被怎么用、哪里失败、哪里需要复查。
- `review_due`：明确纠错、失败、遗漏会触发复查压力。
- `Context Pack`：回答或行动前，把相关上下文聚合出来。

Edge Recall 补的部分：

- 人要不要主动回忆。
- 复习卡怎么不污染原文。
- 复习时怎么保持原文上下文。
- 记忆难度和复习结果怎么驱动下次再激活。
- 移动端怎么做微复习。
- 图表怎么让用户坚持复习。

所以它不是 VAKS 的 truth/review 模块，而是可以作为 `Human Memory / Recall Workbench` 的候选参考。

## Source Anchors

- `raw/videos/2026-06-13-bilibili-bv1rlvg6oeut-edge-recall-source/segments.md` 00:00-00:32：AI 时代更要把知识记在脑子里，反对什么都问 AI 却不思考不记忆。
- `raw/videos/2026-06-13-bilibili-bv1rlvg6oeut-edge-recall-source/segments.md` 00:47-01:25：Edge Recall 不需要在笔记里添加特殊符号，避免污染原文。
- `raw/videos/2026-06-13-bilibili-bv1rlvg6oeut-edge-recall-source/segments.md` 01:25-01:45：状态栏打开待复习卡片，跳转到原笔记位置，不在弹窗中切换。
- `raw/videos/2026-06-13-bilibili-bv1rlvg6oeut-edge-recall-source/segments.md` 02:18-02:51：点击色条显示/隐藏答案，所有操作在原笔记位置完成，形成场景式记忆。
- `raw/videos/2026-06-13-bilibili-bv1rlvg6oeut-edge-recall-source/segments.md` 02:51-03:31：原文内复习支持二次编辑和 Obsidian 原生格式。
- `raw/videos/2026-06-13-bilibili-bv1rlvg6oeut-edge-recall-source/segments.md` 03:58-04:41：移动端可创建和复习卡片，支持随时随地复习。

## 最值得借鉴的点

### 1. Capture Completion != Learning Completion

VAKS 很容易陷入一个错觉：资料已经 capture、summary、candidate distillation 了，好像就“拥有”了这份知识。但这个视频提醒我们，收藏只是入口，记住和会用是另一个环节。

可吸收为候选原则：

```text
captured != understood
understood != remembered
remembered != reviewed truth
reviewed truth != action ready
```

这条非常适合用来解释 VAKS 的分层。

### 2. Source Anchored Recall Card

Edge Recall 不把复习卡做成脱离上下文的弹窗，而是跳回原笔记位置，在原文里显示/隐藏答案。这一点很适合 VAKS：

```text
recall card
-> source anchor
-> local context
-> answer reveal
-> difficulty feedback
-> next activation time
```

这样 recall 不只是背孤立卡片，而是重新激活 source context。

### 3. No Source Pollution

视频强调不在原文塞问号、冒号等特殊符号。这个和 VAKS 的 source boundary 很契合：source 记录应该尽量保持干净，派生复习卡、candidate point、review note 应该是叠加层，而不是污染原文。

候选借鉴：

```text
raw source stays clean
recall overlay stores card metadata
source anchor links back to original span/location
```

### 4. Difficulty Feedback Belongs To Use Ledger

用户选择记忆难度，本质上是 feedback event。VAKS 可以吸收，但必须加边界：

```text
easy / hard / forgot
-> update human reactivation schedule
-> maybe create review_due if the answer was corrected
-> never update truth confidence directly
```

记住得熟，不代表内容真；忘了，也不代表内容假。

### 5. Mobile Micro Reactivation

移动端随时复习很适合 VAKS 的 cold/warm 材料再激活。不是所有旧资料都要重新整理，但可以把某些候选点、模式、术语、流程做成轻量 recall 卡，在碎片时间里重新点亮。

这更像 UI/workbench，不是核心 schema。

## Candidate Points

### CP1 - VAKS 需要区分 capture 和 human retention

资料被保存、摘要、蒸馏，只代表系统拥有了候选材料；用户是否记住和会用，需要单独的人侧反馈闭环。

```yaml
candidate_status: review_due
fit: high
layer: Activation / Use Ledger
```

### CP2 - 复习卡应锚定 source/context

复习卡如果脱离原文，就容易变成孤立背诵。source-anchored recall 更适合 VAKS，因为它保留来源、上下文和后续审查路径。

```yaml
candidate_status: review_due
fit: high
possible_pattern: source-anchored-recall-card
```

### CP3 - 复习反馈不能改 truth

复习次数、难度、图表成绩都只能影响 activation / reactivation / usefulness，不能影响 evidence support、truth confidence 或 reviewed relation。

```yaml
candidate_status: review_due
fit: critical_boundary
hard_rule: dashboard_not_truth
```

### CP4 - 原文不污染适合 VAKS raw/source boundary

复习卡 metadata 应该作为 overlay 或 workbench record，而不是强行写入原始 source body。

```yaml
candidate_status: review_due
fit: high
layer: Capture / Overlay
```

### CP5 - 移动端复习是冷却再激活的自然入口

VAKS 可以把一些冷却资料通过移动端微复习重新激活，但这应是可选工作台，不是普通查询的负担。

```yaml
candidate_status: review_due
fit: medium_high
layer: Cooling / Reactivation
```

## Suggested Labels For VAKS

```yaml
architecture_tags:
  - human-memory-loop
  - contextual-active-recall
  - source-anchored-recall-card
  - no-source-pollution
  - difficulty-feedback-to-reactivation
  - mobile-micro-reactivation
  - review-dashboard-as-motivation
  - capture-is-not-learning
  - remembered-is-not-truth
  - dashboard-not-truth

vaks_layers:
  - Activation
  - Context Pack
  - Use Ledger / Feedback
  - Cooling / Reactivation
  - UI / Workbench

risk_tags:
  - proprietary-plugin-risk
  - recall-metric-not-evidence
  - reinforcing-wrong-memory
  - source-overlay-boundary
```

## Adoption Judgment

```yaml
borrow_value: strong
borrow_order: P2_candidate_for_human_memory_workbench
adoption_now: candidate_only
schema_change_now: no
recommended_shape:
  - optional Recall Workbench
  - source-anchored recall card overlay
  - difficulty feedback event
  - reactivation schedule
  - dashboard as motivation only
must_not_do:
  - do not change truth confidence from recall results
  - do not make ordinary capture/query heavier
  - do not depend on proprietary Modular OB plugin as core runtime
```

## Minimal Absorption Suggestion

先不改主架构。未来如果要吸收，最小形态可以是：

```text
recall_card:
  source_anchor:
  prompt:
  answer:
  card_group:
  last_reviewed_at:
  next_review_at:
  difficulty_feedback:
  context_note:
  truth_boundary: recall_only_not_evidence
```

这只是 UI/workbench record，不进入 `wiki/claims`，不改 reviewed relation，不作为 action basis。

## Boundary Statement

本文件是候选蒸馏，不是 reviewed knowledge。它可以用于后续讨论 VAKS 的人侧记忆/复习工作台，但不能作为正式架构变更、truth 判断、插件采纳决策或 action basis。
