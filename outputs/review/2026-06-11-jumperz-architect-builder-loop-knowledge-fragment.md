---
record_kind: candidate_distillation
fragment_kind: knowledge_fragment
status: candidate
title: "Architect-Builder-Handoff Loop：架构师裁决、构建者执行、仓库记忆、人类 gate"
created_at: "2026-06-11 04:16:49 +08:00"
created_by: Codex
provisional: true
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: none
derived_from:
  - raw/articles/2026-06-11-jumperz-architect-builder-loop-source.md
  - raw/articles/2026-06-11-jumperz-architect-builder-loop-source/pasted-text.txt
  - raw/articles/2026-06-11-jumperz-architect-builder-loop-source/architect-loop.png
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
v0_2_13_trigger: no
routing_hint:
  - agentic-development-loop
  - handoff-memory
  - goal-mode
  - reviewer-agent
  - frozen-gates
possible_project_refs:
  - verified-action-knowledge-system
  - misa-runtime-development
  - casttune-development
point_anchor_refs:
  - snapshot_ref: raw/articles/2026-06-11-jumperz-architect-builder-loop-source/pasted-text.txt
    selector_type: section
    selector_value: "步骤 1 / docs/HANDOFF.md"
  - snapshot_ref: raw/articles/2026-06-11-jumperz-architect-builder-loop-source/pasted-text.txt
    selector_type: section
    selector_value: "步骤 2 / Fable architect prompt"
  - snapshot_ref: raw/articles/2026-06-11-jumperz-architect-builder-loop-source/pasted-text.txt
    selector_type: section
    selector_value: "步骤 3 / Codex /goal phases"
  - snapshot_ref: raw/articles/2026-06-11-jumperz-architect-builder-loop-source/architect-loop.png
    selector_type: image
    selector_value: "diagram text: fable thinks / codex builds / repo remembers / you judge"
verification_refs:
  - https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex
  - https://developers.openai.com/codex/use-cases/follow-goals
  - https://developers.openai.com/codex/changelog
  - https://openai.com/index/introducing-gpt-5-5/
  - https://www.anthropic.com/claude/fable
borrow_value: strong
borrow_order: P1
evidence_strength: medium_for_workflow_shape_low_for_cost_claim
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "future task is specifically about multi-agent development SOP, Codex goal workflow, handoff template, or reviewer-agent gate"
  support_when: "planning long-running Codex work, split-lane implementation, architect/builder collaboration, or handoff discipline"
  risk_when: "commit/push, frozen contracts, success criteria, reviewer approval, or cost/plan assumptions affect action"
  cold_references:
    - raw/articles/2026-06-11-jumperz-architect-builder-loop-source.md
    - raw/articles/2026-06-11-jumperz-architect-builder-loop-source/pasted-text.txt
    - raw/articles/2026-06-11-jumperz-architect-builder-loop-source/architect-loop.png
tags:
  - candidate
  - knowledge-fragment
  - agentic-coding
  - codex-goal
  - handoff
  - reviewer-gate
---

# 知识碎片：Architect-Builder-Handoff Loop

## Boundary

This note is provisional orientation.

It can help route attention, compare ideas, or suggest project overlays. It is not reviewed knowledge, not a decision, not a formal pattern, and not action basis.

## 一句话

把长时间 agentic development 拆成四个角色：

```text
架构师负责判断
构建者负责执行
仓库负责记忆
人类负责 gate
```

这条碎片对 VAKS / Misa / CastTune 都很有借鉴价值，因为它把“多模型协作”从聊天技巧变成了文件化流程：handoff、frozen gates、分歧、raw results、reviewer approval。

## 核心循环

```text
Architect reads repo state
-> rules on disagreements
-> writes next slice spec
-> Builder executes with /goal
-> Builder records raw results in repo handoff
-> Reviewer checks frozen docs + tests + spec
-> Human / Architect gates continue, stop, or revise
```

## Candidate Points

### 1. Repo memory is the shared state, not chat memory

最强点是 `docs/HANDOFF.md`：跨模型、跨 session、跨时间的共同状态必须在仓库文件中，而不是靠对话残影。

好的 handoff 不是流水账，而是：

```text
built
decided
why
open disagreements
next slice
raw results
frozen gates
```

VAKS 现有“文件为准、对话为辅”与这点高度一致。

### 2. Architect should judge, not implement

架构师模型的价值是裁决：

- accept / reject / modify disagreements
- judge raw results against docs gates
- write next small slice
- mark scope creep
- make kill / continue calls

这可以降低“同一个 agent 既做题又批改自己”的风险。

### 3. Builder must surface disagreements before coding

`PHASE 0` 的价值很高：编码前先说计划、分歧和原因，并引用真实文件。

这条能防两个常见失败：

```text
silent obedience
silent scope addition
```

也就是：agent 看似听话，其实没有提出关键冲突；或者悄悄加范围，最后变成不可审查的大包。

### 4. Freeze contracts before implementation

先冻结 docs 里的 schemas/interfaces/gates，再写代码。冻结后连构建者也不能随手改。

这和 VAKS 的证据/成功标准前置原则相同：

```text
success criteria before result
no moving goalposts after output exists
```

### 5. Reviewer agent can only approve or list defects

很适合借鉴的是 reviewer agent 的权限边界：

```text
does not write feature code
checks spec + tests + frozen docs
returns APPROVE or numbered defects
```

这比“reviewer 顺手修掉问题”更干净，因为它保护了审查角色的独立性。

### 6. Raw results should beat builder narration

构建者的解释不应被当成成果。架构师和人类应看 raw results：

- diff
- tests
- logs
- frozen docs
- reviewer defect list
- handoff table

这直接对应 VAKS 的边界：summary / dashboard / model narration 不能成为 truth 或 action basis。

## Borrow Gradient

```yaml
borrow_value: strong
borrow_order: P1
P1:
  - docs/HANDOFF.md as repo memory
  - disagreements mandatory before coding
  - success criteria frozen before results
  - architect judges raw results, not builder narration
  - reviewer agent cannot write feature code
P2:
  - multi-lane implementation with max 3-4 independent lanes
  - one-PR-sized next slice spec
  - commit/push per slice only when user/project policy allows
P3:
  - using Fable specifically as architect and GPT-5.5 Codex specifically as builder
avoid:
  - treating subscription cost claims as verified
  - letting builder self-grade
  - editing success criteria after seeing results
  - using handoff as prose optimism instead of raw tables and numbers
  - auto commit/push without explicit project permission
```

## 对 VAKS 的映射

| Source term | VAKS-safe mapping | Boundary |
|---|---|---|
| architect | reviewer / advisor / human gate / planning model | does not write implementation |
| builder | Codex implementation lane | cannot self-approve |
| repo remembers | project-local handoff and docs | chat memory is secondary |
| frozen gates | pre-result success criteria | not edited after result |
| raw results | diffs, tests, logs, hash checks | narration is not evidence |
| reviewer | defect-list gate | no feature code |

## Suggested Fragment Name

```text
architect-builder-handoff-loop
```

## Open Questions

- VAKS 是否要把 `docs/HANDOFF.md` 模式推广成项目级模板，还是继续使用当前 `00_handoff/`？
- 对 Misa / CastTune 这类 runtime 项目，哪些 docs 可以在 slice 前冻结？
- reviewer agent 的输出格式是否应固定为 `APPROVE` 或编号缺陷？
- commit + push per slice 是否适合当前用户习惯，还是应拆成 commit-only / push-with-confirmation？
- 多 lane 并行什么时候收益大于协调成本？

## Judgment

```yaml
direct_use: no
fork: no
design_only: yes
fusion_decision: adapt_with_boundaries
architecture_change: no
workflow_value: strong
cost_claim_value: low
implementation_cost: low_to_medium
reversibility: high
action_readiness: not_ready
suggested_project_overlay: yes
```

## Forbidden

```text
project_borrow_scope
project_non_borrow_scope
decision outcome
formal pattern
action basis
truth confidence
```

Project-specific borrowing is recorded separately in the VAKS project overlay.
