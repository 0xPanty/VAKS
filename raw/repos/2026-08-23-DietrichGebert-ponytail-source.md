---
type: source
record_kind: source_card
status: source-captured
title: "DietrichGebert/ponytail"
source_id: github-DietrichGebert-ponytail
source_uri: https://github.com/DietrichGebert/ponytail
source_url: https://github.com/DietrichGebert/ponytail
source_type: repository
source_identity:
  schema_version: 1
  source_id: github-DietrichGebert-ponytail
  kind: repository
  canonical_locator: https://github.com/DietrichGebert/ponytail
  identity_profile: github-repository
  aliases:
    - kind: git_locator
      value: "git+https://github.com/DietrichGebert/ponytail.git"
author: Dietrich Gebert
publisher: GitHub
updated_at: 2026-08-08T00:44:01+03:00
captured_at: 2026-08-23T23:00:23+08:00
captured_by: Codex
version_or_commit: 2ed6c52c9d7e5e56942508591085fd45dea277d3
adapter_ingest:
  adapter_name: git-clone-and-archive
  adapter_version: git 2.52.0.windows.1
  capture_method: "git ls-remote; git clone --depth 1 --branch main; git archive HEAD"
  extraction_trace: "Local inspection of README, AGENTS/SKILL rules, lifecycle hooks, cross-host manifests, rule-copy checker, debt skill, tests, CI configuration, benchmark harness, and benchmark reports; repository tests and drift checks executed in a normal host environment."
  known_limits:
    - "Repository tests and drift checks passed, but these are project-authored diagnostics and do not independently validate Ponytail's behavioral, benchmark, security, or host-integration claims."
    - "No live Ponytail plugin, lifecycle hook, MCP session, skill invocation, paid-model benchmark, or real host end-to-end session was executed during intake."
    - "Repository-authored benchmark results were inspected as source claims and diagnostic artifacts, not independently reproduced evidence."
    - "GitHub popularity and issue metadata are volatile and were not used as quality or authority signals."
    - "The archive is a git tree snapshot, not a Source Capture Envelope v1 bundle."
source_status: active
raw_location: raw/repos/_snapshots/2026-08-23-DietrichGebert-ponytail-2ed6c52-source.zip
processing_tier: medium
knowledge_status: raw
overlay_state: none
review_pressure: none
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
review_priority: normal
review_owner: Codex
formalization_status: raw-only
why_saved: "User explicitly requested VAKS distillation of DietrichGebert/ponytail as a repository reference."
topics:
  - ai-coding-agents
  - yagni
  - minimal-implementation
  - agent-skills
  - lifecycle-hooks
  - cross-host-portability
  - benchmark-discipline
projects:
  - verified-action-knowledge-system
source_family:
  - repository
  - agent-skill
  - coding-discipline
upstream_sources: []
verification_status: unverified
candidate_relation_suggestions: []
tags:
  - repo-intake
  - candidate-only
  - agent-skills
  - minimalism
---

# 来源记录：DietrichGebert/ponytail

## 为什么收录

用户明确要求蒸馏 `DietrichGebert/ponytail`。

这个仓库把“避免 AI 编码过度工程”做成一套可跨多个 agent host 分发的规则、skill、hook、review 命令和 benchmark。它可能为 VAKS 的轻量架构纪律、实现复核、规则漂移检查和风险标注提供候选设计，但本记录只保存来源身份、可追溯快照和初步看点。

## 来源信息

- 作者 / 维护者：Dietrich Gebert / GitHub contributors
- 发布方：GitHub
- 原始链接：https://github.com/DietrichGebert/ponytail
- 默认分支：`main`
- checked commit：`2ed6c52c9d7e5e56942508591085fd45dea277d3`
- remote `main` rechecked：`2026-08-24`，HEAD unchanged
- commit time：`2026-08-08T00:44:01+03:00`
- commit subject：`feat: add Grok Build native skills adapter (revive #561) (#661)`
- package / plugin version：`4.9.0`
- license：MIT
- source_status：active
- 采集方式：`git ls-remote` + shallow clone + `git archive HEAD`
- 本地快照：`raw/repos/_snapshots/2026-08-23-DietrichGebert-ponytail-2ed6c52-source.zip`
- 快照 SHA256：`f8ad777666c82cabe7a5c80e0b8d213e27677ddb67adf41efd781eb4d22c7d89`
- 快照大小：`1,148,195` bytes
- archive entries：`212`

## Intake Boundary

```yaml
processing_tier: medium
knowledge_status: raw
overlay_state: none
review_pressure: none
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
```

Source Card 只负责 provenance、findability 和后续 drilldown。它不携带采纳 / 拒绝结论、truth score、项目借鉴裁决或 action basis。

## Inspected Repository Areas

| Area | Anchor | Why inspected |
|---|---|---|
| Core compact rule | `AGENTS.md:1-28` | 确认 YAGNI / reuse / stdlib / native / minimum ladder 与不可削减底线。 |
| Full skill | `skills/ponytail/SKILL.md:20-120` | 确认常驻模式、decision ladder、root-cause rule、ceiling comment、test boundary。 |
| Codex packaging | `.codex-plugin/plugin.json:1-31` | 确认 v4.9.0、MIT、skills 与 lifecycle hooks 能力声明。 |
| Hook map | `hooks/claude-codex-hooks.json:1-41` | 确认 SessionStart、SubagentStart、UserPromptSubmit 三类 hook。 |
| Activation hook | `hooks/ponytail-activate.js:1-84` | 确认 mode state 写入、隐藏上下文注入和 statusline nudge。 |
| Cross-host drift check | `scripts/check-rule-copies.js:15-76` | 确认 canonical compact copy equality 与 load-bearing invariant canary。 |
| Deferred simplification ledger | `skills/ponytail-debt/SKILL.md:11-44` | 确认 ceiling / upgrade trigger 的只读扫描与 no-trigger 风险。 |
| Agentic benchmark method | `benchmarks/results/2026-06-18-agentic.md:1-219` | 检查 benchmark 设计、污染修复、汇总结果与限制。 |
| Comprehension follow-up | `benchmarks/results/2026-06-22-issue-245-217-comprehension.md:1-86` | 检查 root-cause wording 的后续测试和 reuse rung 未复现边界。 |
| Benchmark harness | `benchmarks/agentic/run.py`, `judge.py`, `complete.py`, `tasks.py` | 确认 fresh workspaces、deterministic scorers 与 LLM-judge 辅助层。 |
| Test surface | `tests/*.test.js`, `pi-extension/test/`, `ponytail-mcp/test/` | 确认 hooks、package、host adapters、uninstall、rule copies 等测试面。 |
| CI | `.github/workflows/test.yml`, `.github/workflows/publish.yml` | 确认 Node / Python 版本矩阵、测试与发布路径。 |

## 初步看点

- 核心不是“少写代码”一句口号，而是一个按顺序执行、在首个足够方案停止的实现决策梯。
- 规则明确要求先理解真实调用链，再决定最小解；这修正了“最小 diff = 最近症状补丁”的风险。
- 多宿主分发采用 compact canonical copy + long-form invariant canary，能暴露规则副本漂移。
- 故意接受的简化要写明 ceiling 与 upgrade trigger，并可被只读 ledger 汇总。
- 仓库公开记录了 benchmark baseline 被自身 SessionStart hook 污染的错误，说明常驻 agent 指令会破坏实验隔离。
- 仓库自己的 benchmark 有明确限制：单模型 / 单仓库 / 小样本 / deterministic safety floor；这些是适用范围，不是独立安全证明。

## 明显疑点

- `ACTIVE EVERY RESPONSE`、SessionStart 注入、全 subagent 注入和本地 mode state 会扩大隐藏上下文与副作用面。
- “最短 working diff”容易被误读成 LOC 目标；仓库本身用安全 carve-out 和 comprehension-first 规则约束，但宿主模型未必稳定执行。
- `ONE runnable check` / no fixtures 是该 skill 的局部编码偏好，不足以覆盖高风险、schema、迁移、兼容性或 assurance 测试。
- 自有 benchmark 透明度较好，但仍由项目作者设计、执行和解释；未经独立复验不能作为普适效果或安全结论。
- 跨宿主适配数量很大，带来 manifest、hook、skill、rule copy 和卸载残留的长期维护面。
- Hermes adapter 的活动 mode 是进程级变量，不是 session / user 隔离状态；共享 gateway 存在跨会话影响风险。
- 不同 host 对 `review` mode、session persistence 和 flag fallback 的语义并不完全一致；现有 copy/version checks 不覆盖全部运行语义。
- 多处配置 / state / hook I/O 采用 best-effort silent failure，优先不阻塞宿主，但会降低“是否真正注入 / 关闭 / 持久化”的可观测性。
- CI 只跑 Ubuntu；发布 workflow 未显式依赖 test job。MCP 子包使用范围依赖且无 lockfile，分发与复现性弱于主包。
- `ponytail-review` 明确只审过度工程，不审 correctness、security 或 performance，不能替代正常 code review。

## 可抽取 Candidate Points

1. 将“是否需要、能否复用、平台是否已覆盖、最后才新增”压成显式 sufficiency ladder。
2. 最小实现必须建立在真实调用链理解之上；root-cause fix 往往也是更小、更稳定的 fix。
3. 故意简化要绑定 ceiling 与可观察的 reopen / upgrade trigger。
4. 多处重复的关键规则可以使用 canonical source + exact-copy check + invariant canary，漂移只报告、不自动修。
5. 常驻 hook 可能污染 benchmark、baseline 和 agent 行为；实验与生产比较必须隔离注入源。
6. 更少代码、测试通过和 benchmark 改善都是诊断信号，不能自动变成 VAKS truth、review 或 action readiness。

## Source Annotation Sidecars

```yaml
source_annotation_refs:
  - annotation_id: ponytail-sufficiency-ladder
    path: outputs/review/source_annotations/2026-08-23-DietrichGebert-ponytail/ponytail-sufficiency-ladder.md
    anchor_status: exact_verified
  - annotation_id: ponytail-root-cause-and-ceiling
    path: outputs/review/source_annotations/2026-08-23-DietrichGebert-ponytail/ponytail-root-cause-and-ceiling.md
    anchor_status: exact_verified
  - annotation_id: ponytail-safety-test-boundary
    path: outputs/review/source_annotations/2026-08-23-DietrichGebert-ponytail/ponytail-safety-test-boundary.md
    anchor_status: exact_verified
  - annotation_id: ponytail-canonical-rule-canary
    path: outputs/review/source_annotations/2026-08-23-DietrichGebert-ponytail/ponytail-canonical-rule-canary.md
    anchor_status: exact_verified
  - annotation_id: ponytail-trigger-bearing-debt-ledger
    path: outputs/review/source_annotations/2026-08-23-DietrichGebert-ponytail/ponytail-trigger-bearing-debt-ledger.md
    anchor_status: exact_verified
  - annotation_id: ponytail-benchmark-isolation-risk
    path: outputs/review/source_annotations/2026-08-23-DietrichGebert-ponytail/ponytail-benchmark-isolation-risk.md
    anchor_status: exact_verified
  - annotation_id: ponytail-benchmark-scope-limit
    path: outputs/review/source_annotations/2026-08-23-DietrichGebert-ponytail/ponytail-benchmark-scope-limit.md
    anchor_status: exact_verified
  - annotation_id: ponytail-always-on-hook-state
    path: outputs/review/source_annotations/2026-08-23-DietrichGebert-ponytail/ponytail-always-on-hook-state.md
    anchor_status: exact_verified
```

## 当前处理等级

```text
medium
```

升级到 heavy 的条件：

- VAKS 准备把 sufficiency ladder 变成正式 implementation / architecture gate。
- VAKS 出现真实多宿主 agent runtime，需要规范 canonical rule 与 adapter parity。
- Ponytail 插件或 hooks 被提议直接安装到 VAKS 工作流。
- 仓库自有 benchmark 被用于 action-facing 结论，需要独立复验和 Evidence Packet。

## 本地验证

已执行：

```text
git ls-remote ... refs/heads/main
git clone --depth 1 --branch main ...
git rev-parse HEAD
git show -s --format=...
git archive --format=zip ... HEAD
Get-FileHash -Algorithm SHA256 <snapshot>
tar -tf <snapshot>
npm test
node scripts/check-rule-copies.js
node scripts/check-versions.js
```

测试结果：

```text
root Node tests: 84/84 passed
Pi extension:     23/23 passed
MCP package:       3/3 passed
total:           110/110 passed
rule-copy check: passed; 9 invariants present
version check:   passed; 8 version locations aligned at 4.9.0
```

受限沙箱首次运行时，10 个需要启动 Python 子进程的测试因环境不可执行而失败；在正常宿主环境完整重跑后全部通过，因此不记录为仓库测试失败。测试通过仍只是该提交的 repository diagnostic，不验证 README 效果数字、真实 host 集成或安全证明。

未执行：

- Ponytail 安装、live skill、lifecycle hook、MCP session 或 statusline。
- 付费模型 benchmark、模型调用或独立 benchmark reproduction。
- 真实 Claude / Codex / OpenCode / Gemini / Hermes host end-to-end run。
- 外部发布流程。

## 下一步

- 通过候选蒸馏、架构 review 和 Project Overlay 保留设计价值与不借边界。
- 任何主线吸收、正式 pattern、工具实现或插件安装，仍需后续明确确认和 evidence-aware review。
