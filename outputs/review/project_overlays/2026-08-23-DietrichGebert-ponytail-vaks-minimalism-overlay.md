---
record_kind: project_overlay
status: candidate
knowledge_status: candidate
processing_tier: medium
overlay_state: confirmed
review_pressure: none
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
project_id: verified-action-knowledge-system
target_ref: outputs/review/2026-08-23-DietrichGebert-ponytail-candidate-distillation.md
target_selector: "VAKS implementation discipline and maintenance-lint sidecar"
target_hint: "comprehension-first sufficiency ladder / rule-drift canary / trigger-bearing simplification / benchmark isolation"
source_annotation_refs:
  - outputs/review/source_annotations/2026-08-23-DietrichGebert-ponytail/ponytail-sufficiency-ladder.md
  - outputs/review/source_annotations/2026-08-23-DietrichGebert-ponytail/ponytail-root-cause-and-ceiling.md
  - outputs/review/source_annotations/2026-08-23-DietrichGebert-ponytail/ponytail-safety-test-boundary.md
  - outputs/review/source_annotations/2026-08-23-DietrichGebert-ponytail/ponytail-canonical-rule-canary.md
  - outputs/review/source_annotations/2026-08-23-DietrichGebert-ponytail/ponytail-trigger-bearing-debt-ledger.md
  - outputs/review/source_annotations/2026-08-23-DietrichGebert-ponytail/ponytail-benchmark-isolation-risk.md
  - outputs/review/source_annotations/2026-08-23-DietrichGebert-ponytail/ponytail-benchmark-scope-limit.md
  - outputs/review/source_annotations/2026-08-23-DietrichGebert-ponytail/ponytail-always-on-hook-state.md
project_borrow_scope: "For VAKS, keep Ponytail as a design-only implementation-discipline reference. Future significant schema, tool, adapter, and runtime proposals may use a comprehension-first sufficiency ladder, shared-root fix check, canonical-rule invariant canaries, trigger-bearing deliberate simplifications, and explicit instruction/plugin isolation in evaluations."
project_non_borrow_scope: "For project VAKS, do not currently install or fork Ponytail, enable always-on lifecycle hooks or default subagent injection, add mode/statusline/MCP runtime, optimize for LOC or file count, cap verification at one test, treat self-authored benchmarks as independent validation, or let minimal code imply epistemic confidence, review status, mainline readiness, or action basis."
project_reopen_trigger: "Reopen direct integration only when VAKS has a real multi-host agent runtime or repeated observed over-building that an on-demand checklist does not prevent, and a controlled VAKS-specific comparison demonstrates benefit without weakening authority, provenance, safety, fixtures, rollback, or instruction-isolation boundaries."
confirmation_basis: "User explicitly requested VAKS distillation of this repository; this confirmed overlay persists project-scoped borrow/non-borrow routing only and does not imply adoption."
last_checked_at: 2026-08-23
expires_at:
tags:
  - implementation-discipline
  - yagni
  - maintenance-lint
  - agent-tool-safety
---

# Project Overlay：Ponytail 对 VAKS 的项目借鉴边界

## Boundary

这是 project-scoped candidate sidecar。

它不改写 source card、candidate、reviewed note、decision 或 pattern；也不构成安装许可、架构采纳、review verdict 或 action basis。

## Target

```yaml
target_ref: outputs/review/2026-08-23-DietrichGebert-ponytail-candidate-distillation.md
target_selector: VAKS implementation discipline and maintenance-lint sidecar
target_hint: comprehension-first sufficiency ladder / rule-drift canary / trigger-bearing simplification / benchmark isolation
```

## Project Borrow Scope

对 VAKS，当前只借四个 design-only 候选：

```text
1. Comprehension-first sufficiency ladder
   先理解真实端到端流，再在首个足够方案停止。

2. Shared-root fix check
   修改共享契约前检查全部 consumers，在共同根部修一次。

3. Canonical rule + invariant canary
   exact-copy 做 parity；long/short variant 只钉关键不变量；漂移只报告。

4. Ceiling / reopen trigger + eval isolation
   故意简化写明上限与复查触发器；agent eval 隔离 plugins、hooks、global instructions 和 state。
```

推荐最小使用形状：

```text
只在重大架构 / 实现 review 中按需打开
-> 不新增 formal lane
-> 不常驻注入
-> 不自动修文件
-> 检查数量按风险决定
```

## Project Non-Borrow Scope

当前明确不借：

```text
Ponytail plugin / fork
SessionStart / SubagentStart / UserPromptSubmit always-on injection
mode flag / statusline / MCP runtime
all-host adapter surface
LOC / file-count quality score
self-authored benchmark as independent proof
ONE runnable check as universal test cap
ponytail comments as formal ledger or reviewed state
minimal code as truth / review / action readiness
```

原因：

```text
Ponytail 解决的是 coding behavior。
VAKS 仍必须单独维护 provenance、authority、evidence、review、rollback 和 action gates。
```

## Reopen Trigger

只有同时满足以下条件才重新讨论直接集成：

1. VAKS 已有真实、多宿主 agent runtime 或反复出现的实证性 over-building。
2. 一次性 on-demand checklist 无法解决该问题。
3. VAKS-specific controlled comparison 隔离了 hooks、plugins、global instructions、state 和 subagents。
4. 结果证明收益不靠削弱 provenance、authority、security、rollback、fixtures 或 negative cases 获得。
5. 用户明确批准后续 implementation / installation scope。

## Confirmation

```yaml
confirmation_basis: user explicitly requested VAKS distillation; overlay is routing only
last_checked_at: 2026-08-23
```

## Forbidden

```text
decision outcome
review verdict
truth confidence
action basis
universal ban outside VAKS
plugin installation authority
benchmark-as-proof
```
