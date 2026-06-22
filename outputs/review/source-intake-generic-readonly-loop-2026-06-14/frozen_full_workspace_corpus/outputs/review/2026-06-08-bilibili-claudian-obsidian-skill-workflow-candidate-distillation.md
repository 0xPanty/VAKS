---
type: candidate_distillation
record_kind: candidate_distillation
status: draft
title: "Claudian skill 演示提醒 VAKS：skill 应该是实际工作动作包，不是 reviewed truth"
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
  - raw/videos/2026-06-08-bilibili-claudian-obsidian-skill-workflow-source.md
projects:
  - verified-action-knowledge-system
topics:
  - claudian
  - obsidian
  - skills
  - agent-workbench
  - publishing-gate
  - style-extraction
  - workflow-skill-pack
borrow_value: low
borrow_order: P3
evidence_strength: low-medium
tags:
  - candidate-only
  - source-distillation
  - design-only
  - vaks-borrow-P3
provisional: true
---

# 候选蒸馏：Claudian skill 演示提醒 VAKS：skill 应该是实际工作动作包，不是 reviewed truth

## 一句话

这条视频对 VAKS 是 `P3 / borrow_value: low`。

它有用，但不是因为它讲了什么新架构，而是因为它提醒了一句很朴素的话：

```text
skill 好不好，不看功能多不多；
看它能不能真的进入实际工作流。
```

视频里的 skill 多数是内容生产场景：公众号爆款、敏感词检测、选题评分、风格萃取、对标拆解。对 VAKS 来说，这些只能作为 workflow skill / publishing gate 的候选参考，不能进入 truth/review core。

## Borrow Tag

```yaml
borrow_value: low
borrow_order: P3
borrow_scope:
  - workflow-skill-pack
  - project-workbench
  - publishing-precheck
  - style-extraction-helper
  - content-production-support
  - use-ledger-feedback
not_borrow_scope:
  - reviewed truth
  - evidence support
  - truth confidence
  - reviewed relation
  - action basis without human approval
  - compliance guarantee
  - automatic publishing
  - agent write access to VAKS core
```

## 为什么是 P3

不是 P1/P2 的原因：

```text
视频太短；
没有展示 skill 文件；
没有展示 prompt；
没有展示执行日志；
没有展示失败案例；
没有展示权限、回滚、证据、审批边界。
```

它只是一个“这些 skill 好用”的主观演示。

但仍然值得留作 P3，因为它提醒 VAKS：

```text
不要只设计抽象能力；
要把 skill 设计成实际任务的小闭环。
```

## Candidate Point

VAKS skills 可以按“真实工作动作包”来设计：

```text
input:
  link / draft / idea / transcript / source card / old style sample

skill action:
  inspect / extract / score / rewrite / check / compare / package

output:
  candidate suggestion / publishing precheck / style note / review input

gate:
  human confirmation
  action_basis_allowed remains false unless later review passes
```

关键是：

```text
skill 输出是建议；
不是知识真相。
```

## 可以借

- skill 应该服务真实任务，而不是只展示功能名。
- 发布前检查可以做成 skill：敏感词、风险词、平台限制、标题/选题风险。
- 风格萃取可以做成 tone/context helper，让 AI 更贴近用户过往表达。
- 爆款拆解 / 对标拆解可以作为 candidate analysis，而不是结论。
- skill 调用结果应进入 Use Ledger：用了没有、改了多少、最后有没有发布。

## 不能借

- 不借“评分高 = 爆款概率高”的确定性表达。
- 不把敏感词检测当合规保证。
- 不把风格萃取当用户授权发布。
- 不让 Claudian 或任何 agent 直接写 `wiki/claims`、`wiki/decisions`、reviewed relation。
- 不把短视频里的 skill 名称当精确来源实体。
- 不把视频主观体验当成 VAKS 采用依据。

## 对 VAKS 的最小吸收

现在不改 schema。

可以在未来 skill 设计清单里记一条：

```text
每个 VAKS skill 都要写清楚：
  - 解决哪个真实任务
  - 输入是什么
  - 输出属于 raw / candidate / review_input / action_suggestion 哪一层
  - 是否允许写文件
  - 是否允许进入 action basis
  - 需要什么人工确认
  - 失败或撤销怎么记入 Use Ledger
```

如果做 publishing gate，可以先从低风险开始：

```text
draft -> sensitive-word candidate check -> user revision -> publish decision note
```

而不是：

```text
draft -> AI 判断可发 -> 自动发布
```

## 与 VAKS 现有设计的关系

```text
Capture:
  从想法、对话、链接、视频中生成候选输入。

Understand:
  拆解、风格萃取、文案生成都属于 candidate comprehension/action suggestion。

Review:
  敏感词和选题评分只能作为 review input，不是 reviewed evidence。

Connect:
  对标拆解可产生 candidate associations。

Activation / Context Pack:
  Skill pack 可以作为 project workbench 的快捷动作。

Decision / Action:
  发布类 skill 必须经过人工确认；不能自动成为 action basis。

Use Ledger / Feedback:
  记录 skill 输出是否被采纳、被修改、被拒绝和实际效果。
```

## Risk / Inhibition

```text
risk:
  Agent/skill 在 Obsidian vault 内具备写入能力，可能越过 VAKS 边界。
  用户容易把 AI 评分当成可靠判断。
  内容生产 skill 容易推动“为了产出而跳过证据检查”。
  风格萃取可能制造像用户本人写的内容，但未经过用户确认。

inhibition:
  skill 输出默认 candidate。
  发布或行动前必须 human approval。
  对外内容必须保留 source/provenance/revision trace。
  agent write access 需要另做权限和路径隔离。
```

## 融合判断

```text
fusion_decision: watch / adapt-lightly
borrow_value: low
borrow_order: P3
evidence_strength: low-medium
implementation_cost: low for prompt checklist, medium-high for safe agent integration
integration_fit: medium
reversibility: high if kept as design note
```

## 后续行动

- 当前不研究 Claudian 源码，不安装插件，不启用 agent 写 vault。
- 当前不改 `SCHEMA.md`，不新增 reviewed pattern。
- 如果后续要评估 Claudian 本体，应另开 repo/plugin source review，重点看：

```text
agent write boundary
skills storage and invocation
slash commands
provider/session storage
MCP integration
plan mode / approval mode
permission isolation
VAKS raw/reviewed/action 路径保护
```
