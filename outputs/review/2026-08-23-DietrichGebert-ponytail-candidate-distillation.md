---
record_kind: candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: none
source_ref: raw/repos/2026-08-23-DietrichGebert-ponytail-source.md
derived_from:
  - raw/repos/2026-08-23-DietrichGebert-ponytail-source.md
  - raw/repos/_snapshots/2026-08-23-DietrichGebert-ponytail-2ed6c52-source.zip
  - wiki/summaries/2026-08-23-DietrichGebert-ponytail-architecture-review.md
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
  - implementation-discipline
  - architecture-sufficiency-check
  - maintenance-lint
  - agent-tool-safety
  - benchmark-isolation
possible_project_refs:
  - verified-action-knowledge-system
source_annotation_refs:
  - outputs/review/source_annotations/2026-08-23-DietrichGebert-ponytail/ponytail-sufficiency-ladder.md
  - outputs/review/source_annotations/2026-08-23-DietrichGebert-ponytail/ponytail-root-cause-and-ceiling.md
  - outputs/review/source_annotations/2026-08-23-DietrichGebert-ponytail/ponytail-safety-test-boundary.md
  - outputs/review/source_annotations/2026-08-23-DietrichGebert-ponytail/ponytail-canonical-rule-canary.md
  - outputs/review/source_annotations/2026-08-23-DietrichGebert-ponytail/ponytail-trigger-bearing-debt-ledger.md
  - outputs/review/source_annotations/2026-08-23-DietrichGebert-ponytail/ponytail-benchmark-isolation-risk.md
  - outputs/review/source_annotations/2026-08-23-DietrichGebert-ponytail/ponytail-benchmark-scope-limit.md
  - outputs/review/source_annotations/2026-08-23-DietrichGebert-ponytail/ponytail-always-on-hook-state.md
point_anchor_refs:
  - snapshot_ref: raw/repos/_snapshots/2026-08-23-DietrichGebert-ponytail-2ed6c52-source.zip
    selector_type: file_line
    selector_value: skills/ponytail/SKILL.md:32-48
  - snapshot_ref: raw/repos/_snapshots/2026-08-23-DietrichGebert-ponytail-2ed6c52-source.zip
    selector_type: file_line
    selector_value: scripts/check-rule-copies.js:15-69
  - snapshot_ref: raw/repos/_snapshots/2026-08-23-DietrichGebert-ponytail-2ed6c52-source.zip
    selector_type: file_line
    selector_value: benchmarks/results/2026-06-18-agentic.md:40-47
borrow_value: medium
borrow_order:
  - "P1: comprehension-first sufficiency ladder for architecture and implementation proposals"
  - "P2: canonical rule copies with exact parity and load-bearing invariant canaries"
  - "P3: trigger-bearing deliberate simplifications and benchmark-isolation warning"
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "An approved VAKS task is explicitly reviewing implementation scope, architecture bloat, cross-host rule drift, or a direct Ponytail integration proposal."
  support_when: "Reviewing a schema/tool/adapter/runtime proposal for the smallest sufficient reversible shape."
  risk_when: "LOC, a test result, self-authored benchmark, hidden hook, or persistent agent instruction is being treated as quality, truth, or action readiness."
  cold_references:
    - raw/repos/2026-08-23-DietrichGebert-ponytail-source.md
    - raw/repos/_snapshots/2026-08-23-DietrichGebert-ponytail-2ed6c52-source.zip
avoid:
  - "Do not install or fork Ponytail for VAKS from this candidate intake."
  - "Do not enable always-on lifecycle hooks, statusline mutation, or default subagent injection."
  - "Do not turn LOC, file count, shortest diff, tests, or self-authored benchmark results into truth or readiness signals."
  - "Do not cap VAKS verification at one check or prohibit fixtures where assurance requires more."
  - "Do not add a Ponytail lane, truth layer, review object, runtime, or dashboard."
tags:
  - candidate
  - provisional
  - yagni
  - agent-skills
  - implementation-discipline
---

# 候选蒸馏：DietrichGebert/ponytail

## Boundary

This note is provisional orientation.

It can route attention, compare ideas, and support a project overlay. It is not reviewed knowledge, not a decision, not a formal pattern, and not action basis.

## 一句话结论

Ponytail 值得作为“实现与架构克制”的候选参考，但不值得直接装进 VAKS：

```text
它最有价值的不是插件和 LOC 数字，
而是“先理解全链路，再在首个足够方案停止”的显式 sufficiency ladder。
```

融合判断暂定：

```text
adapt / design-only
```

## Source

```yaml
derived_from:
  - raw/repos/2026-08-23-DietrichGebert-ponytail-source.md
  - raw/repos/_snapshots/2026-08-23-DietrichGebert-ponytail-2ed6c52-source.zip
source_annotation_refs:
  - outputs/review/source_annotations/2026-08-23-DietrichGebert-ponytail/ponytail-sufficiency-ladder.md
  - outputs/review/source_annotations/2026-08-23-DietrichGebert-ponytail/ponytail-root-cause-and-ceiling.md
  - outputs/review/source_annotations/2026-08-23-DietrichGebert-ponytail/ponytail-safety-test-boundary.md
  - outputs/review/source_annotations/2026-08-23-DietrichGebert-ponytail/ponytail-canonical-rule-canary.md
  - outputs/review/source_annotations/2026-08-23-DietrichGebert-ponytail/ponytail-trigger-bearing-debt-ledger.md
  - outputs/review/source_annotations/2026-08-23-DietrichGebert-ponytail/ponytail-benchmark-isolation-risk.md
  - outputs/review/source_annotations/2026-08-23-DietrichGebert-ponytail/ponytail-benchmark-scope-limit.md
  - outputs/review/source_annotations/2026-08-23-DietrichGebert-ponytail/ponytail-always-on-hook-state.md
```

## Candidate Points

### Candidate Point 1: Comprehension-First Sufficiency Ladder

仓库把最小实现从一句价值观变成一个有顺序和停止条件的决策过程：

```text
先理解任务与真实调用链
-> 不需要就不建
-> 代码库已有就复用
-> 标准库 / 原生平台已覆盖就使用
-> 已装依赖可覆盖就复用
-> 最后才写最小新实现
```

对 VAKS 的真正增量不是“更简单”三个字，而是把已有 `smallest useful version`、Karpathy-simple 和 lazy gates 变成一个可复核顺序。

### Candidate Point 2: Root-Cause Fix Can Also Be The Smaller Fix

Ponytail 后续补丁明确反对“在最近症状处做最小 diff”。它要求先找所有调用者，在共同路径修一次。

这与 VAKS 当前 canonical schema / enum / source-intake contract 的维护方式相容：共享约束应在共同契约处修正，而不是在每个消费者处累积补丁。

### Candidate Point 3: Deliberate Simplification Needs A Ceiling And Reopen Trigger

故意接受的简化必须说清：

```text
当前省掉了什么
可接受上限 / 失败边界是什么
出现什么可观察条件时升级
```

VAKS 不需要新债务系统；最小吸收是复用现有 `project_reopen_trigger`、`review_due_when`、risk note 和 maintenance manifest。

### Candidate Point 4: Canonical Rule Plus Invariant Canary

跨宿主规则副本分两类检查：

```text
能完全相同的 compact copy：做等值检查
无法完全相同的 long-form skill：只钉 load-bearing invariants
```

这对 VAKS 分散在 `AGENTS.md`、schema、intake、templates 和 skills 的关键边界有候选价值，但当前只需保留设计点，不新建自动化。

### Candidate Point 5: Always-On Instructions Are Experimental Contamination Risk

仓库公开承认早期 agentic benchmark 的 baseline 被 Ponytail 自己的 SessionStart hook 污染。这个失败记录比宣传数字更值得保留：

```text
常驻 hook / 全局 plugin / 隐藏 context
会使 baseline 不再是 baseline
```

任何 future VAKS agent runtime 对比都必须隔离 instruction source、plugin source、state directory 和 subagent injection。

### Candidate Point 6: Minimal Code Is Not Epistemic Reliability

仓库通过安全 carve-out、可执行检查和 benchmark 约束“少写代码”，但这仍是编码质量纪律，不是知识权威模型。

对 VAKS 必须保持：

```text
fewer LOC != truth
test pass != evidence support
self-benchmark != independent validation
shortest diff != action readiness
```

## Knowledge Calibration / Point Collision

| Candidate Point | Local Reviewed / Standing Contract | Calibration Output | Review Question |
|---|---|---|---|
| 在首个足够方案停止。 | `ARCHITECTURE_PRINCIPLES.md` 已要求 smallest useful version；README 已有 Karpathy-simple / lazy gates。 | candidate_relation / refines | 是否需要把顺序压成未来 review prompt，而不是新增 formal gate？ |
| 先理解真实流，再做最小改动。 | AGENTS 要求不 overdesign；当前 Source Capture Store / Fragment Candidate 复用已有 spine。 | refines | 哪些高风险共享契约必须强制 caller/consumer scan？ |
| 简化带 ceiling 与 reopen trigger。 | Project Overlay 已有 `project_reopen_trigger`；Evidence discipline 已有 `review_due_when`。 | candidate_relation | 是否只需复用现有字段，而不创建新的 debt schema？ |
| canonical copy + invariant canary。 | VAKS 有多份边界文档，但 Markdown source of truth 仍优先。 | missing_evidence / candidate_relation | 重复边界何时产生真实 drift，值得实现 lint？ |
| 常驻 hook 会污染 benchmark。 | Test / benchmark / LLM judge 仅为 maintenance diagnostic。 | risk_signal / scope_mismatch | 未来 agent eval 如何证明 baseline 未加载全局 instructions？ |
| 一个 runnable check 足够。 | VAKS Guard、schema、migration、negative fixtures 需要按风险扩展测试。 | scope_mismatch | 哪些低风险改动可用 one-check，哪些 assurance 任务必须多层验证？ |

所有 calibration output 都是 review input，不是 reviewed relation、truth mutation 或 action basis。

## 借鉴顺序

### P1 — VAKS Sufficiency Ladder

```text
先理解端到端真实流
-> 真的需要存在吗
-> 现有 VAKS 对象 / 契约 / 工具已覆盖吗
-> Markdown / Obsidian / Git / 原生平台已覆盖吗
-> 已有模块或依赖已覆盖吗
-> 最后才做最小、可回退扩展
```

不可削减：provenance、authority boundary、数据损失保护、安全、用户明确要求、回退与可执行验证。

### P2 — Canonical Rule + Invariant Canary

作为未来 lint 候选：能 exact-copy 的做 parity；不能 exact-copy 的只检查少量关键不变量；只报告 drift，不自动修。

### P3 — Trigger-Bearing Simplification + Benchmark Isolation

将 ceiling / reopen trigger 留在现有 overlay、risk、review_due 或 maintenance 记录中；同时把 always-on instruction contamination 保留为实验设计风险。

## Open Questions

- 是否真实存在 VAKS 多文档边界漂移，还是现有 AGENTS + source-of-truth 文件已足够？
- VAKS 将来是否需要一个 on-demand“复杂度复核”提示，而不是常驻规则？
- 哪些 runtime / schema 改动适合 one-check，哪些必须保留 fixture、negative cases 和 replay？
- 如果未来比较 agent workflows，如何记录 plugin、hook、global skill、system prompt 与 state isolation？
- Ponytail 在其他仓库、其他模型、其他 host 上的效果是否能由独立主体复现？

## Routing Hint

```text
Default: Cold Reference + Support-with-required-risk
Use when: architecture review, implementation scope review, cross-host rule packaging, benchmark isolation
Do not use when: ordinary capture, truth review, source support, action-basis approval
```

## 明确不吸收

- 不安装或 fork Ponytail。
- 不启用 SessionStart / SubagentStart / UserPromptSubmit 常驻注入。
- 不引入 mode / statusline / MCP / 跨宿主 adapter runtime。
- 不把 LOC、文件数、最短 diff 或自有 benchmark 变成质量 / truth / mainline readiness 指标。
- 不把 `ONE runnable check` 当高风险测试上限。
- 不新增 Ponytail lane、truth layer、review object、dashboard 或 debt database。
- 不让“少写代码”削掉 provenance、证据边界、回退、审计、安全或可访问性。

## Forbidden

```text
project_borrow_scope in this candidate note
formal architecture decision
formal pattern
source annotation as final support
reviewed relation
action basis
truth confidence
```
