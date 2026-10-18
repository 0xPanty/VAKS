---
type: candidate_distillation
status: draft
title: "VAKS 需要产品化 onboarding 和统一反馈入口"
created_at: "2026-06-08"
created_by: Codex
processing_level: medium
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
  - raw/videos/2026-06-08-bilibili-modular-obsidian-official-site-source.md
projects:
  - verified-action-knowledge-system
topics:
  - onboarding
  - official-site
  - feedback-loop
  - starter-vault
  - obsidian-workbench
  - use-ledger
borrow_value: medium
borrow_order: P2
evidence_strength: low-medium
tags:
  - candidate-only
  - source-distillation
  - design-only
  - vaks-borrow-P2
---

# 候选蒸馏：VAKS 需要产品化 onboarding 和统一反馈入口

## 一句话

这条视频对 VAKS 的借鉴是 P2：它不是核心知识审查材料，而是提醒 VAKS 未来要有一个产品化入口。用户不能一上来只面对 schema、handoff、review gate；他们需要官网/入口页、入门课程、上手任务、starter vault、反馈入口和持续维护的生态说明。

## Borrow Tag

```yaml
borrow_value: medium
borrow_order: P2
borrow_scope:
  - onboarding
  - official-site
  - starter-vault
  - feedback-loop
  - use-ledger-surface
  - course-entry
not_borrow_scope:
  - reviewed truth
  - evidence support
  - action basis
  - core schema
```

## Candidate Point

VAKS 的外层产品入口可以借鉴“模块化 Obsidian 官网”的形态：

```text
入口页:
  说明 VAKS 是什么、适合谁、最小闭环是什么。

入门课程:
  从 capture -> candidate -> review -> context pack 的最小路径开始。

上手任务:
  让用户完成一条真实资料入库，而不是先读完整架构。

starter vault:
  给出可复制的最小目录、模板和示例。

反馈入口:
  统一提交问题、需求、使用结果和改进建议。

维护跟踪:
  反馈进入 Use Ledger / Feedback，而不是散落在聊天里。
```

## 应该吸收

- 为 VAKS 准备“最小上手路径”，不是只给完整文档。
- 把反馈入口做成显式通道，让使用结果可追踪。
- 用课程/任务帮助用户一步步建立工作流。
- starter vault / starter template 可以降低从零搭建成本。
- 把反馈采纳状态和后续跟踪作为 Use Ledger 的外层表现。

## 不应该吸收

- 不要把某个 Obsidian 工作流变成 VAKS 唯一路径。
- 不要用插件数量或课程数量证明系统可靠。
- 不要让反馈直接改变 truth confidence。
- 不要把官网/课程写进 reviewed knowledge。
- 不要为了产品化入口改 core schema。

## 对 VAKS 的具体启发

```text
P2 but useful:
  VAKS core 可以保持严谨；
  外层必须变得可上手。
```

最小产品化入口可以长这样：

```text
1. 我为什么需要 VAKS
2. 10 分钟跑通第一条资料
3. raw / candidate / reviewed 是什么
4. 怎么让 Codex 做第一轮整理
5. 哪些东西不能当真
6. 怎么提交反馈或纠错
```

## 与现有 VAKS 层级的关系

```text
Capture:
  onboarding 解释如何轻量 capture。

Understand:
  课程解释 candidate comprehension。

Review:
  课程提醒初整理不是 review。

Connect:
  starter vault 展示关系和索引，但不创建 reviewed relation。

Activation / Context Pack:
  官网/课程是 activation surface。

Decision / Action:
  不直接进入 action basis。

Use Ledger / Feedback:
  统一反馈入口是最值得借鉴的产品点。
```

## Risk / Inhibition

```text
risk:
  产品化入口可能把复杂边界讲得太轻，导致用户误用。
  starter vault 可能被误当唯一正确结构。
  feedback 可能被误当 truth update。

inhibition:
  每个入口页都保留 raw/candidate/reviewed/action-basis 解释。
  feedback 默认进入 feedback-event / review pressure，不直接改 truth。
  starter vault 明确是入门模板，不是唯一架构。
```

## 融合判断

```text
fusion_decision: adapt / watch
borrow_value: medium
borrow_order: P2
evidence_strength: low-medium
implementation_cost: medium
integration_fit: medium
reversibility: high
```

## 后续行动

- 若未来要做 VAKS 对外入口，可把这条作为 onboarding / feedback 设计参考。
- 当前不建议改 schema，不建议新增核心模块。
- 最小吸收方式：在使用说明或未来官网草图里加入“课程 + 上手任务 + 反馈入口”。
