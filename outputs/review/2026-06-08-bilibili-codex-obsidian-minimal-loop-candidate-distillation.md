---
type: candidate_distillation
record_kind: candidate_distillation
status: draft
title: "Obsidian + Codex 知识库先跑通最小闭环"
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
  - raw/videos/2026-06-08-bilibili-codex-obsidian-knowledge-loop-source.md
projects:
  - verified-action-knowledge-system
topics:
  - obsidian
  - codex
  - web-clipper
  - source-intake
  - minimal-loop
  - onboarding
  - candidate-routing
borrow_value: strong
borrow_order: P1
evidence_strength: low-medium
tags:
  - candidate-only
  - source-distillation
  - design-only
  - vaks-borrow-P1
provisional: true
---

# 候选蒸馏：Obsidian + Codex 知识库先跑通最小闭环

## 一句话

这条视频对 VAKS 的借鉴是 P1，但不是因为它提供了复杂技术，而是因为它击中了 VAKS 最容易出错的第一步：不要一上来做全自动知识库，先跑通一个能每天用的最小闭环。

```text
浏览器内容
-> Obsidian Web Clipper
-> 本地 Markdown
-> Obsidian 素材文件夹
-> Codex 第一轮整理
-> 标出哪些值得后续处理
```

## 为什么是 P1

它直接影响 VAKS 的普通用户入口和 source intake 默认体验：

```text
P1 reason:
  普通 capture 必须轻。
  AI 初整理只能是 candidate routing。
  先接住内容，再谈分类、标签、自动化和 review。
```

这不是 reviewed truth，也不是 action basis。它是 workflow/onboarding 级别的 P1：先让系统动起来，避免 VAKS 变成用户还没开始就被结构劝退的重系统。

## Candidate Point

VAKS 最小闭环应该先长这样：

```text
Capture:
  Web Clipper / 手动保存 / 粘贴链接，把内容变成本地 raw Markdown。

Raw Buffer:
  进入素材文件夹或 raw source buffer，不直接进 wiki/claims。

AI First Pass:
  Codex 做标签、目录建议、摘要、后续处理价值判断。

Review Queue:
  只有值得继续处理的内容进入候选点或 review queue。

Later:
  再慢慢补标签体系、分类规则、自动化流程。
```

## 对 VAKS 的借鉴标签

```yaml
borrow_value: strong
borrow_order: P1
borrow_scope:
  - source-intake
  - onboarding
  - capture-workflow
  - candidate-routing
  - anti-overautomation
not_borrow_scope:
  - reviewed truth
  - evidence confidence
  - action basis
  - automatic promotion
```

## 应该吸收

- 把 `Web Clipper -> local md -> Codex 初整理` 定义成 VAKS 新用户的最小可用路径。
- 让 AI 先做轻量 triage：标签、目录、摘要、是否值得后续处理。
- 把“素材文件夹”明确为 raw/candidate buffer。
- 对用户说清楚：先跑通闭环，再谈自动化。

## 不应该吸收

- 不要一开始就做全自动分类。
- 不要把 Codex 的整理结果当成 truth。
- 不要把所有来源都丢进一个无边界大池子。
- 不要为了追求完美 schema 让 capture 变重。

## 与本地 VAKS 的关系

这条资料支持已有主线，而不是要求新增核心模块：

```text
Capture -> Understand -> Review -> Connect -> Act and Learn
```

对应关系：

```text
Web Clipper:
  Capture

素材文件夹:
  raw/source buffer

Codex 第一轮整理:
  Understand / candidate routing

值得后续处理:
  Review Queue input

标签和目录:
  candidate organization, not reviewed relation
```

## Risk / Inhibition

```text
risk:
  用户可能把 AI 初整理当正式知识。
  用户可能把 capture 入口开太多，变成材料垃圾堆。
  用户可能过早追求全自动，反而看不懂自己的库。

inhibition:
  初始入口只保留少数。
  AI 输出默认 candidate。
  后续处理必须显式进入 review queue。
  标签 / 目录只是候选组织，不是知识关系。
```

## 最小吸收建议

```text
Do:
  在 VAKS 使用说明 / onboarding 中加入“一条最小闭环”：
  Web Clipper -> raw md -> Codex 初整理 -> worth-review queue。

Do not:
  不改 SCHEMA。
  不新增模块。
  不自动提升任何材料。
  不把视频当证据权威。
```

## Support / Challenge Review

- What supports it: 视频直接描述 Obsidian + Codex 的最小闭环；与 VAKS 当前 source intake 边界一致。
- What challenges it: 视频很短，没有实际配置模板；ASR 有轻微错字；没有展示失败案例。
- Challenge severity: minor
- Scope limits: 只适用于 onboarding / source intake / capture workflow。
- Known risks: 过度 clip、过度自动化、AI 初整理污染 truth core。
- Review again when: 准备写 VAKS 普通用户使用说明或 Web Clipper 具体模板时。
- Action readiness: not_ready

## 融合判断

```text
fusion_decision: adapt
borrow_value: strong
borrow_order: P1
evidence_strength: low-medium
implementation_cost: low
integration_fit: high
reversibility: high
```
