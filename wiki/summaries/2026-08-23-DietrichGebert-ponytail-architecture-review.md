---
type: library_review
record_kind: library_review
status: draft
knowledge_status: candidate
processing_tier: medium
library_name: DietrichGebert/ponytail
repo_url: https://github.com/DietrichGebert/ponytail
source_url: https://github.com/DietrichGebert/ponytail
checked_commit: 2ed6c52c9d7e5e56942508591085fd45dea277d3
commit_time: 2026-08-08T00:44:01+03:00
source_status: active
reviewed_at: 2026-08-23
domain:
  - ai-coding-agent-discipline
  - yagni
  - agent-skills
  - cross-host-plugin-packaging
related_projects:
  - verified-action-knowledge-system
current_branch: "master / Source Capture Store v1 + Fragment Candidate"
extracted_patterns:
  - comprehension-first-sufficiency-ladder
  - canonical-rule-invariant-canary
  - trigger-bearing-deliberate-simplification
  - benchmark-instruction-isolation
fusion_decision: adapt
confidence: medium
evidence_count: 20
cross_validated_with:
  - ARCHITECTURE_PRINCIPLES.md
  - SOURCE_INTAKE.md
  - templates/maintenance-manifest.md
  - wiki/anti-patterns/overgrown-always-on-instructions.md
negative_evidence:
  - "Repository-authored benchmark only; not independently reproduced in this intake."
  - "Always-on hooks and mode-state writes expand hidden context and side effects."
  - "One-check/no-fixtures guidance is too narrow for high-assurance VAKS changes."
  - "Project tests and drift checks passed, but real host integration and behavioral effects were not independently validated."
extension_potential: "On-demand design checklist or future read-only lint input; no current runtime integration."
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: review_input_only
  action_basis_allowed: false
  warning_code: candidate_review_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
relations: []
tags:
  - library-review
  - candidate
  - implementation-discipline
  - agent-tool-safety
---

# 库分析：DietrichGebert/ponytail

Remote `main` was rechecked on `2026-08-24`; HEAD remained `2ed6c52c9d7e5e56942508591085fd45dea277d3`.

## Boundary

这是候选架构 review，不是正式 pattern、decision、review pass 或 action basis。Source/code anchors 证明“仓库里有什么”，不自动证明其规则对 VAKS 普适有效。

## 它解决什么问题

Ponytail 试图解决 AI coding agent 的常见过度工程：

```text
把可复用 / 标准库 / 原生平台能解决的问题
扩成新抽象、新依赖、新文件和大量样板代码。
```

它把解决方案包装成：

```text
compact AGENTS rule
+ long-form skill
+ lifecycle hooks / mode state
+ diff review / audit / debt commands
+ cross-host adapters
+ test and benchmark harness
```

## 核心设计

```text
Comprehension first
-> stop at the first sufficient rung
-> protect trust boundaries and explicit requirements
-> leave a runnable check for non-trivial logic
-> mark deliberate ceilings with upgrade triggers
-> keep host-specific copies aligned
```

仓库包含 instruction-only 与 plugin-tier 两种运行面：前者靠 `AGENTS.md` / host rule file，后者通过 SessionStart、SubagentStart、UserPromptSubmit 等 hooks 注入规则和维护 mode state。

## Runtime / Persistence Notes

Ponytail 不是统一 runtime，而是 canonical skill body 外加多套薄适配器：

```text
canonical SKILL.md / compact AGENTS.md
-> host-specific manifest or adapter
-> mode resolution
-> instruction filtering / injection
-> optional session state and status surface
```

默认 mode 解析顺序是 `PONYTAIL_DEFAULT_MODE -> config.json -> full`（`hooks/ponytail-config.js:54-100`）。活动状态随宿主而不同：Claude / Codex / Copilot / Qoder / OpenCode 主要写 `.ponytail-active`；Pi 写 session custom entry；Hermes 使用 Python 模块级 `_current_mode`；MCP 按请求返回指令而不保存 active session state。

这带来三个重要边界：

1. Hermes mode 是 process-global，不是 session/user isolated。
2. `review` mode、session persistence 和 fallback location 在不同 host 上存在语义漂移。
3. 配置 / flag / hook 输出多处 silent fail，优先保证宿主不被阻塞，但降低运行状态可观测性。

仓库没有数据库或知识持久化；正常运行主要写 mode/config/statusline 状态，不应被误认为 target repository knowledge write。

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `AGENTS.md:1-28` | Compact canonical coding rule. | Short, host-portable policy surface. | Instruction text, not enforced authority. |
| `skills/ponytail/SKILL.md:32-48` | Ordered ladder and comprehension-first guard. | First-sufficient-stop is the strongest reusable idea. | Depends on model following instructions. |
| `skills/ponytail/SKILL.md:50-64` | Root-cause rule and ceiling/upgrade comments. | Smallest correct fix may live at a shared root. | Grep/caller scan is a heuristic, not formal proof. |
| `skills/ponytail/SKILL.md:90-112` | Safety carve-outs and one-check guidance. | Minimalism must not remove trust/safety basics. | One check/no fixtures is not enough for all VAKS risks. |
| `.codex-plugin/plugin.json:1-31` | v4.9.0 manifest; skills + lifecycle hooks. | Clear package boundary and declared capabilities. | Manifest does not prove host behavior or safety. |
| `hooks/claude-codex-hooks.json:1-41` | Session, subagent, prompt hooks. | Always-on injection is explicit and testable. | Expands hidden-context and side-effect surface. |
| `hooks/ponytail-activate.js:4-41` | Writes mode state and emits hidden context. | Operational activation mechanism. | Not suitable as VAKS default without a real runtime need. |
| `scripts/check-rule-copies.js:15-69` | Exact compact-copy parity plus invariant canaries. | Canonical source + bounded drift checks. | String canaries can miss semantic drift. |
| `skills/ponytail-debt/SKILL.md:11-43` | Read-only marker harvest with no-trigger flag. | Ceiling + reopen trigger can prevent silent rot. | Comments remain routing hints, not formal records. |
| `benchmarks/results/2026-06-18-agentic.md:40-47` | Records contaminated baseline and isolation fix. | Always-on agent context must be isolated in evals. | Author-reported correction, not independent audit. |
| `benchmarks/results/2026-06-18-agentic.md:186-198` | One-model, safety-floor, n=4, timeout limits. | Claims need narrow scope and explicit caveats. | No universal performance or safety conclusion. |
| `benchmarks/results/2026-06-22-issue-245-217-comprehension.md:15-59` | Root-cause wording helped capable models; reuse benefit did not reproduce. | Operational wording can matter; model ceiling remains. | Mixed evidence, small controlled setting. |
| `benchmarks/agentic/run.py:36-47, 184-217, 283-339` | Isolated arms, selftests, fresh workspaces. | Better eval hygiene than single-shot prompt comparison. | Harness not executed in this intake. |
| `hooks/ponytail-config.js:54-100` | Default mode and config path resolution. | Small shared config core. | Silent fallback can hide malformed config or missing state. |
| `pi-extension/index.js:24-58,183-210` | Pi session entry and prompt injection. | Host-native session persistence. | Different semantics from file-flag hosts. |
| `__init__.py:105-128,153-217` | Hermes process hooks and module-level mode. | Thin Python adapter. | Process-global mode can cross session/user boundaries. |
| `ponytail-mcp/index.js:23-52` | Stdio prompt and read-only instruction tool. | On-demand alternative to always-on injection. | Private subpackage, no active-session state. |
| `skills/ponytail-review/SKILL.md:50-56` | Review excludes correctness, security, performance. | Good separation of complexity review from normal review. | Must never replace full code review. |
| `tests/*.test.js`, `.github/workflows/test.yml:9-36` | Host adapters, hooks, packaging, uninstall, behavior tests. | 110/110 tests plus rule/version checks passed in a normal host environment. | Project-authored diagnostics; CI is Ubuntu-only and not real-host E2E. |
| `.github/workflows/publish.yml:3-24` | Tag-triggered npm publish workflow. | Small release surface. | Publish is not explicitly gated by the separate test workflow. |

## 当前支线价值

当前支线：

```text
master
-> Source Capture Envelope / Source Capture Store v1
-> deterministic Source Snapshot Index
-> Fragment Candidate / source-missing inbox
```

它对当前支线：

```text
refines / pressure-tests
```

具体价值：

- 在新增 capture object、field、adapter 或 runtime 前，先检查现有 Source Card / Annotation / Fragment / Candidate / Overlay / Store 是否已覆盖；第一个足够方案就停止。
- 修改共享 schema、enum、store invariant 时，先找全部 consumers，在共同契约处一次修正。
- 当前 Source Capture Store 的 optional、read-only verify、derived/rebuildable index，已经比照搬 Ponytail runtime 更符合 VAKS。
- Fragment Candidate 复用 existing candidate spine，而不是新增一条来源缺失 lane，正好符合 Ponytail ladder 的“already in this codebase”。

风险：

- Ponytail 不提供 source ingest、provenance、evidence review、promotion 或 action gate；不能把它误当当前分支实现参考。
- `ONE runnable check` 不能削弱 Store / Envelope / Guard 已有 fixture、negative cases、schema validation 和 replay。
- 当前支线不需要因本仓库新增 schema、script、hook 或 runtime。

## 全貌架构价值

| Architecture Zone | Value / Finding | Adopt? |
|---|---|---|
| Karpathy spine | 将“保持简单”变成有顺序、有停止条件的 operational ladder。 | adapt |
| Dusk workbench | 可作为一次性复杂度复核输入；无需新 dashboard、mode 或 statusline。 | watch |
| source ingest | 没有直接 ingest 能力；只能阻止不必要 object / adapter 膨胀。 | no direct use |
| review queue | 复杂度、规则漂移、无 trigger 简化可进入 maintenance/review input。 | adapt as diagnostic |
| schema / reviewed knowledge | 没有 epistemic schema；短代码不等于可信。 | reject as authority |
| memory / dev context | 短 skill 可做按需 Support；常驻全局注入与默认 subagent 注入相冲突。 | adapt on-demand only |
| feedback | ceiling 触发后可制造 `review_due`；不能改 truth。 | adapt |
| retrieval / cache | 无明显增量。 | no |
| API / MCP / agent access | 多宿主包装和只读 MCP 可作未来 Agent Tool Safety 参考。 | watch / parked |
| viewer / workbench | mode badge / statusline 对当前 VAKS 没有足够价值。 | reject now |
| publishing | 无直接价值。 | no |
| risk / anti-pattern | 强：暴露 over-abstraction、hidden instruction、baseline contamination、test underfit。 | keep as candidate risk |

## 值得提炼的模式

### 1. Comprehension-First Sufficiency Ladder

最小融合版：在架构 / 实现 review 时按顺序问“需要吗、已有吗、原生能否覆盖、最后才扩展”，但不新增 formal lane 或独立 gate object。

### 2. Canonical Rule + Invariant Canary

对能完全等值的规则副本做 parity；对 long/short variant 只钉关键 boundary invariants；drift 进入 lint，不自动修。

### 3. Trigger-Bearing Deliberate Simplification

故意简化必须带 ceiling 和 reopen trigger。VAKS 复用现有 overlay / review_due / maintenance 字段，不建立第二套 debt authority。

### 4. Instruction Isolation In Agent Evaluation

baseline 与 treatment 必须隔离 global skills、plugins、hooks、state 和 subagent context。这个风险点比 README 的效果数字更可迁移。

## 标签与量化

- domain: AI coding agent discipline / cross-host skills
- problem: over-engineering, unnecessary dependencies, rule-copy drift
- pattern: comprehension-first sufficiency ladder
- maturity: emerging
- complexity: low for design borrowing / high for cross-host runtime maintenance
- problem_fit: 4/5 for implementation governance; 1/5 for knowledge authority
- reuse_value: 4/5 as on-demand review principle
- implementation_cost: 1/5 for checklist; 4/5 for plugin/runtime
- integration_fit: 4/5 as design-only; 1/5 as always-on runtime
- evidence_strength: 3/5 for code/design extraction; 1/5 for unreplicated performance claims
- reversibility: 5/5 if kept candidate-only

## 交叉验证

- 相似设计来源：Karpathy-simple spine、YAGNI、stdlib/native-first、maintenance lint。
- 本地相似机制：`ARCHITECTURE_PRINCIPLES.md` adoption gates、`templates/maintenance-manifest.md`、Project Overlay reopen trigger、`wiki/anti-patterns/overgrown-always-on-instructions.md`。
- 支持证据：固定 commit 的 rules、skills、hooks、tests、benchmark harness 与 limitation notes。
- 反例 / 失败边界：baseline contamination、reuse rung 未复现、小模型 ceiling、单模型 agentic benchmark、Windows timeout cells。
- 最小验证方式：未来只在一个批准的 architecture/implementation review 中用 on-demand checklist，对比是否减少无必要变更且不削弱 boundary / tests。

## Knowledge Calibration / Point Collision

| Candidate Point | Local Reviewed Knowledge | Calibration Output | Review Question |
|---|---|---|---|
| First sufficient rung stops expansion. | `ARCHITECTURE_PRINCIPLES.md:509-533` 已要求 smallest useful version。 | refines | 是否只需加入 review prompt，而不改主架构？ |
| Reuse existing codebase contract first. | Source Capture Store / Fragment Candidate 已复用现有 Raw/Candidate spine。 | candidate_relation | 哪些未来提案可被现有对象直接覆盖？ |
| Canonical copies need drift checks. | Markdown is source of truth；lint reports but does not repair. | candidate_relation / missing_evidence | 当前是否有真实 rule drift recurrence？ |
| Ceiling needs reopen trigger. | Project Overlay / review_due / maintenance manifest 已有承载面。 | refines | 能否完全复用现有字段？ |
| Always-on hook can contaminate eval. | Test/benchmark/LLM-judge are diagnostics only. | risk_signal | future eval receipt 是否要记录 instruction/plugin isolation？ |
| One runnable check is enough. | VAKS assurance uses multiple fixtures and negative cases by risk. | scope_mismatch | 哪些任务允许 one-check，哪些禁止？ |

## Support / Challenge Review

- What supports it:
  - 规则、skill、hook、复制检查、tests 和 benchmark harness 在固定 commit 内彼此可追踪。
  - 仓库公开记录了污染 bug 和 benchmark 局限，降低了隐藏 cherry-pick 风险。
  - comprehension follow-up 同时报告成功与未复现结果。
  - 本轮正常宿主环境实跑 `npm test`：root 84/84、Pi 23/23、MCP 3/3，合计 110/110；rule-copy 9 invariants 与 8 个版本位置检查也通过。
- What challenges it:
  - 所有效果结论仍来自仓库自身，未由本轮独立复现。
  - instruction following 随模型与 host 变化；小模型存在明确 ceiling。
  - always-on lifecycle hooks 与多宿主复制面增加长期维护、隐式上下文和实验污染风险。
  - 最少代码可能与高 assurance 的冗余验证、迁移、兼容性要求冲突。
  - 测试以 mock / contract 为主；CI 仅 Ubuntu，没有真实 Codex / Claude / OpenCode / Hermes 或 Windows host E2E。
  - Hermes process-global mode、跨宿主 persistence 语义漂移和 silent failure 仍是未被 copy/version checks 覆盖的运行风险。
- Challenge severity: minor for design-only borrowing; major for direct runtime adoption.
- Scope limits: implementation / architecture sufficiency review only; not truth, support, promotion, or action approval.
- Known risks: LOC proxy, self-benchmark bias, hook contamination, rule-copy drift, test underfit, model noncompliance.
- Review again when: VAKS has repeated over-building, real multi-host runtime, or a proposal to install Ponytail.
- Action readiness: not_ready

## 关系边 / 关联强度

```yaml
relations:
  - target: "[[2026-05-27-karpathy-simple-verified-strict-ux-principle]]"
    type: refines
    relation_state: candidate
    strength: 3
    confidence: medium
    evidence:
      - "skills/ponytail/SKILL.md:32-48"
    rationale: "Adds an explicit first-sufficient-stop order to an existing simplicity principle."
  - target: "[[static-wiki-health-lint-before-auto-rewrite]]"
    type: refines
    relation_state: candidate
    strength: 2
    confidence: medium
    evidence:
      - "scripts/check-rule-copies.js:15-69"
    rationale: "Shows exact-copy and invariant-canary checks that report drift without repairing truth."
  - target: "[[overgrown-always-on-instructions]]"
    type: supports
    relation_state: candidate
    strength: 3
    confidence: medium
    evidence:
      - "hooks/ponytail-activate.js:4-41"
      - "benchmarks/results/2026-06-18-agentic.md:40-47"
    rationale: "Always-on injection created a concrete baseline-contamination failure mode."
```

这些仍是 candidate relation suggestions，不是 reviewed relations。

## 对当前项目的适配点

最小适配：

```text
future significant VAKS proposal
-> comprehension-first sufficiency questions
-> existing contract / native surface check
-> risk boundary check
-> smallest reversible extension
-> one or more checks proportional to risk
```

不新增正式文件类型、不新增 runtime、不常驻注入。

## 可拓展性

- 是否适合作为插件 / 适配层：技术上是；当前 VAKS 不需要。
- 是否会绑定核心结构：直接安装会绑定 hooks、state、mode 和 host adapters；design-only 不会。
- 未来替换成本：checklist 很低；多宿主 plugin 较高。
- 可迁移路径：candidate reference -> one on-demand pilot -> maintenance evidence -> later explicit review only if recurrence exists.

## 复杂度和风险

Ponytail 的“规则很短”并不代表系统很小。其真实维护面包含多个 host manifest、规则副本、hook、state、skill、MCP、statusline、tests 和 uninstall behavior。

本轮仓库测试结果为：

```text
root 84/84 + Pi 23/23 + MCP 3/3 = 110/110 passed
rule-copy check: 9 invariants passed
version check: 8 locations aligned at 4.9.0
```

这证明固定提交的 repository contracts 在正常宿主环境内自洽，但不证明：

```text
真实 host integration 已验证
prompt behavior 对所有模型有效
self-benchmark 已独立复现
安全性或成本收益可外推
发布一定被测试成功阻断
```

对 VAKS 的 alpha 正好是反过来：

```text
只借 decision order
不借 runtime surface
```

## 不可行点 / 避坑

- 把更少 LOC 当质量分数。
- 用自有 benchmark 直接宣称安全或普适收益。
- 用一个 test / no fixtures 替代高风险验证。
- 在 VAKS 普通 intake 中常驻注入编码规则。
- 让 mode 强度影响 authority、review 或 action gate。
- 复制全部 host adapters，只为“兼容性看起来完整”。
- 新建 Ponytail-specific debt ledger，而不复用 overlay / review_due / maintenance manifest。
- 把 Hermes process-global mode 带入共享多用户 gateway。
- 把 `ponytail-review` 当 correctness / security / performance review。
- 假设跨宿主 mode / persistence / uninstall 语义已被统一验证。
- 让 publish workflow 在未建立显式 test dependency 时承担 release gate。

## 融合判断

- 结论：adapt / design-only
- 理由：对 implementation governance 有清晰增量；对 knowledge architecture 几乎无直接能力；runtime 成本与隐式副作用不匹配当前需求。
- 验证方式：未来在一个用户批准的 VAKS 方案 review 中以一次性 checklist 使用，比较是否减少无必要对象 / 字段 / adapter，同时保留全部 authority、rollback 和 test boundary。

## 直接判断

- Direct use: no.
- Fork: no.
- Design-only: yes.
- Reject: reject current always-on integration, not the source as a design reference.
- Current branch value: medium，主要是 refinement / pressure-test。
- Whole architecture value: medium-high for implementation governance; low for truth/review architecture.
- Risk: hidden instruction injection, LOC proxy, self-benchmark bias, verification underfit.
- Next action: keep source card + snapshot + candidate + annotations + confirmed project overlay; no pattern/decision/mainline change.

## 后续行动

- 默认放在 Cold Reference / on-demand Support。
- 如果未来出现重复 over-building，再考虑一次受控、可回滚、按风险验证的 VAKS-specific pilot。
- 未经后续明确确认，不实现 lint、不装插件、不修改主线文档和索引。
