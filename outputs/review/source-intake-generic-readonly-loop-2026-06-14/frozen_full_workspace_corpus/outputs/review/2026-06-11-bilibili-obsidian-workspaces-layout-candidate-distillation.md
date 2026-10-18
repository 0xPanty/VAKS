---
type: candidate_distillation
record_kind: candidate_distillation
status: draft
title: "VAKS 可以借鉴 Obsidian Workspaces 的场景化工作区"
created_at: "2026-06-11"
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
  - raw/videos/2026-06-11-bilibili-bv13ndqbtehs-source.md
projects:
  - verified-action-knowledge-system
topics:
  - obsidian
  - workspaces
  - activation-surface
  - context-pack
  - dev-context
  - retrieval-workbench
borrow_value: medium
borrow_order: P2
evidence_strength: low-medium
tags:
  - candidate-only
  - source-distillation
  - design-only
  - vaks-borrow-P2
provisional: true
---

# 候选蒸馏：VAKS 可以借鉴 Obsidian Workspaces 的场景化工作区

## 一句话

这条视频对 VAKS 的借鉴是 P2：它不影响真理核心，但很适合启发 VAKS 的检索层、Dev Context 和 Context Pack workbench。

说人话：用户不只是要“找到一堆资料”，还要“一键回到某个工作场景”。Obsidian Workspaces 保存的是界面布局；VAKS 将来可以保存的是任务场景：该打开哪些 source、candidate、review queue、ledger、索引和上下文包。

## Borrow Tag

```yaml
borrow_value: medium
borrow_order: P2
borrow_scope:
  - activation-surface
  - retrieval-workbench
  - context-pack-view
  - dev-context-recovery
  - user-workspace-presets
not_borrow_scope:
  - reviewed truth
  - evidence support
  - reviewed relation
  - action basis
  - core schema
```

## Candidate Point

VAKS 可以把“检索结果”从单纯列表，扩展成“场景化工作区恢复”：

```text
检索某个任务时，不只返回资料：
  还返回一组应该打开/激活的文件、视图和检查点。

比如：
  source card
  transcript / raw text
  candidate distillation
  review queue item
  related decisions
  risk notes
  current task_plan / findings
```

这不是让 UI 布局变成知识，而是让 VAKS 的 activation 更像真实工作流。

## 应该吸收

- 按任务场景保存工作区，而不是每次手动重建上下文。
- 给常见场景预设入口：Capture、Distill、Review、Retrieval Design、Decision。
- Context Pack 可以有两种形态：文本上下文包 + workspace preset。
- Dev Context 可以记录“当前任务文件集合”，帮助下一窗口恢复。
- 快捷入口很重要：命令、快捷键、按钮、固定 workspace 都能减少上下文切换成本。

## 不应该吸收

- 不要把 workspace layout 当作知识结构。
- 不要把 dashboard / graph / opened files 当 reviewed relation。
- 不要让“已打开资料”变成“证据充分”。
- 不要为了工作区体验改核心 schema。
- 不要让快捷恢复跳过 Evidence Sufficiency Gate 或 action-basis 边界。

## 与 VAKS 检索层的关系

```text
普通检索:
  找到可能相关材料。

VAKS 检索层:
  找材料 + 标边界 + 组上下文包 + 暴露风险/缺口。

Workspaces 借鉴:
  在“组上下文包”之后，提供可恢复工作区，让用户继续干活。
```

这能补一个体验缺口：VAKS 现在很会讲边界，但用户最终还是要进入一个具体工作状态。工作区预设可以把“检索到材料”变成“可继续工作的桌面”。

## 对 VAKS 的具体启发

```text
Capture Workspace:
  inbox、source template、raw/videos、raw/articles。

Distillation Workspace:
  raw source、transcript、segments、candidate distillation。

Review Workspace:
  candidate point、evidence packet、review queue、challenge notes。

Retrieval Design Workspace:
  task_plan、findings、frontier-source-ledger、north-star。

Decision Workspace:
  relevant reviewed notes、scope/risk、action checklist、use ledger。
```

## Risk / Inhibition

```text
risk:
  漂亮工作区会制造“系统已经完成”的错觉。
  Graph / dashboard 容易被用户误读成知识关系。
  一键恢复可能让人跳过证据检查。

inhibition:
  workspace preset 只能是 activation surface。
  每个 preset 都显示 knowledge_status 和 action_basis_allowed。
  进入 decision/action workspace 时必须经过 sufficiency / scope / risk gate。
```

## 融合判断

```text
fusion_decision: adapt / later
borrow_value: medium
borrow_order: P2
evidence_strength: low-medium
implementation_cost: medium
integration_fit: medium
reversibility: high
```

## 后续行动

- 当前只作为 P2 候选设计点保留。
- 不改 `SCHEMA.md`。
- 如果之后开发 VAKS 检索层 UI / Obsidian workbench，可把它并入“workspace preset / context-pack view”设计。
