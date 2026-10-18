---
record_kind: project_overlay
status: candidate
knowledge_status: candidate
processing_tier: medium
overlay_state: confirmed
overlay_scope: project_sidecar_only
overlay_storage: confirmed_persistent_project_bucket
retrieval_scope: active_project_only
default_retrieval: false
retrieval_policy:
  policy_kind: project_context_only
  default_scope: project_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: overlay_not_authority
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
project_id: VAKS
target_ref: outputs/review/2026-06-11-jumperz-architect-builder-loop-knowledge-fragment.md
target_selector: whole-file
target_hint:
  - type: workflow
    value: multi-agent-development-loop
    status: conceptual
    anchor_version: 2026-06-11-candidate-source
  - type: doc
    value: 00_handoff/
    status: healthy
    anchor_version: 2026-06-11-directory-known
  - type: workflow
    value: reviewer-agent-gate
    status: conceptual
    anchor_version: 2026-06-11-candidate-source
project_borrow_scope: "For VAKS, borrow the architect/builder/repo/human split as a project-workflow candidate: repo-visible handoff, mandatory disagreements, frozen gates before implementation, raw-result review, and reviewer-agent no-feature-code boundary."
project_non_borrow_scope: "For VAKS, do not borrow the cost claim, automatic commit/push, builder self-grading, or any rule that lets a candidate workflow become reviewed process without a real trial. Do not replace existing 00_handoff discipline until a user-approved pilot proves the template."
project_reopen_trigger: "Reopen when designing a formal multi-agent development SOP, Codex /goal recovery prompt, handoff template, reviewer-agent output format, or a Misa/CastTune long-running build lane."
confirmation_basis: "User explicitly requested '蒸馏进去 知识碎片' in the VAKS workspace; the source directly targets Codex/Fable development handoff workflow."
last_checked_at: "2026-06-11 04:16:49 +08:00"
expires_at:
borrow_value: strong
borrow_order: P1
avoid:
  - subscription-cost-as-action-basis
  - automatic-commit-push
  - builder-self-approval
  - moving-goalposts-after-results
  - handoff-as-optimistic-summary
---

# Project Overlay：VAKS 借鉴 Architect-Builder-Handoff Loop

## Boundary

This is a project-scoped sidecar.

It does not rewrite the source card, candidate distillation, reviewed note, decision, or pattern.

It can guide the active project, but it cannot act as reviewed knowledge or action basis.

## Target

```yaml
target_ref: outputs/review/2026-06-11-jumperz-architect-builder-loop-knowledge-fragment.md
target_selector: whole-file
target_hint:
  - multi-agent-development-loop
  - 00_handoff/
  - reviewer-agent-gate
```

## Project Borrow Scope

For VAKS, borrow the workflow shape:

- `repo remembers`: 继续强化“文件为准、对话为辅”，handoff 必须能让下一窗口恢复。
- `architect judges`: 规划/审查模型或人类 gate 做裁决，不写实现。
- `builder builds`: Codex 负责执行、测试、修复，但不能自评通过。
- `disagreements mandatory`: 编码前必须列出分歧和原因。
- `frozen gates`: 结果出现前冻结 success criteria、schemas/interfaces、scope out。
- `reviewer gate`: reviewer agent 只给 `APPROVE` 或编号缺陷，不写功能代码。
- `raw results`: handoff 记录 raw result、测试、hash、diff、编号，而不是“有前景”的叙述。

## Project Non-Borrow Scope

For VAKS, do not currently borrow:

- 不借 `20 dollar subscription` 成本论证作为 action basis。
- 不自动 commit/push；VAKS 仍需用户明确授权。
- 不让 builder 自己写“我通过了”。
- 不在结果出现后修改成功标准。
- 不把 `docs/HANDOFF.md` 立刻替换现有 `00_handoff/` 习惯。
- 不把多 lane 并行作为默认；先看任务是否真的可独立拆分。

## Reopen Trigger

Reopen when:

- 设计正式 multi-agent development SOP。
- 写 Codex `/goal` 恢复 prompt。
- 需要统一 handoff 模板。
- 要做 reviewer-agent 输出格式。
- Misa / CastTune 进入长时间并行构建。
- 用户授权一次真实 pilot 来验证这套 loop。

## Confirmation

```yaml
confirmation_basis: explicit user request: 蒸馏进去 知识碎片
last_checked_at: "2026-06-11 04:16:49 +08:00"
expires_at:
```

## Forbidden

```text
decision outcome
review verdict
truth confidence
action basis
universal ban
```
