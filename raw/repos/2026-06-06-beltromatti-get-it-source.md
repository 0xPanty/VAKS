---
type: source
status: source-captured
title: "Get It."
source_id: 2026-06-06-beltromatti-get-it-source
source_uri: https://github.com/beltromatti/get-it
source_url: https://github.com/beltromatti/get-it
source_type: repository
author: beltromatti
publisher: GitHub
published_at:
updated_at: 2026-05-28
captured_at: 2026-06-06
captured_by: Codex
version_or_commit: 4ce88a2c0a242206d96bcd7221bdeda1efcba41c
commit_time: "2026-05-28 22:08:33 +0200"
commit_subject: "macOS builds: Developer ID signing + Apple notarization end to end"
default_branch: main
latest_release: v1.2.1
latest_release_published_at: 2026-05-28T20:16:41Z
source_status: active
license: Apache-2.0
dynamic_metadata_checked_at: 2026-06-07T02:32:22+08:00
dynamic_metadata:
  stars: 152
  forks: 27
  open_issues: 1
raw_location: raw/repos/2026-06-06-beltromatti-get-it-source.md
snapshot_location: raw/repos/_snapshots/beltromatti-get-it-4ce88a2c0a242206d96bcd7221bdeda1efcba41c.zip
snapshot_sha256: 2F4C1285C03D8A4BD36766B8383CE6B927D8CD3725ABD0D4D80A42338F26CFAD
processing_mode: immediate
processing_level: heavy
processing_tier: heavy
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
review_priority: high
review_owner: Codex
formalization_status: candidate-generated
topics:
  - local-first-agent-app
  - pdf-study-workbench
  - codex-cli-transport
  - source-quality-gate
  - typed-agent-output
  - server-owned-jobs
  - work-context-journal
  - mastery-graph
  - llm-code-sandbox
projects:
  - verified-action-knowledge-system
source_family:
  - agent-workbench
  - source-intake
  - feedback-ledger
  - local-first-desktop
upstream_sources: []
verification_status: primary-source-captured
candidate_relation_suggestions:
  - target: "[[Source Intake]]"
    relation_type: refines
    relation_state: candidate
    why_suggested: "The repository uses deterministic PDF quality gates before any model workflow starts."
  - target: "[[Feedback Ledger]]"
    relation_type: refines
    relation_state: candidate
    why_suggested: "The work-context journal and incremental evaluator are useful as feedback/use-ledger design inputs."
  - target: "[[Agent memory quarantine]]"
    relation_type: refines
    relation_state: candidate
    why_suggested: "Codex runs through a read-only, no-approval transport wrapper with health/error boundaries."
  - target: "[[Action Basis]]"
    relation_type: risk_of
    relation_state: candidate
    why_suggested: "Its mastery scores and monotone clamp are progress UX, not truth or action-readiness evidence."
tags:
  - get-it
  - codex-cli
  - pdf
  - local-first
  - candidate-only
---

# Get It. Source Record

## 为什么收录

`beltromatti/get-it` 是一个本地优先的 PDF 学习桌面应用：用户把数字文本 PDF 放进去，应用先做确定性的质量门，然后用 Codex CLI / Codex SDK 走用户自己的 ChatGPT 或 OpenAI API 账户，生成概念标签、可视化、知识图谱、学习工具和掌握度反馈。

对 VAKS 来说，它不是 truth layer 参考，也不是我们要 fork 的学习 App。它值得收录，是因为它把几个对我们很有用的工程边界写得比较清楚：

```text
先拒绝不适合处理的输入
agent 输出必须 schema 化
后台 job 拥有生成状态
互动记录落成本地 JSON journal
评价只读 journal，不改原始交互
用户自带模型账户，应用不持有共享 key
```

边界也要写硬：

```text
Get It. 的 mastery score 不是 truth confidence
monotone non-decreasing 适合学习进度，不适合 VAKS 的事实置信度
LLM 代码 sandbox 是防模型失误，不是对抗性安全边界
Codex CLI 作为用户账号 transport 是产品策略，不应变成 VAKS 的唯一 agent gateway
```

## 来源信息

- Repository: `beltromatti/get-it`
- URL: https://github.com/beltromatti/get-it
- Checked commit: `4ce88a2c0a242206d96bcd7221bdeda1efcba41c`
- Checked branch: `main`
- Tag at checked commit: `v1.2.1`
- Commit time: `2026-05-28 22:08:33 +0200`
- Commit subject: `macOS builds: Developer ID signing + Apple notarization end to end`
- License: Apache-2.0
- Snapshot: `raw/repos/_snapshots/beltromatti-get-it-4ce88a2c0a242206d96bcd7221bdeda1efcba41c.zip`
- Snapshot SHA256: `2F4C1285C03D8A4BD36766B8383CE6B927D8CD3725ABD0D4D80A42338F26CFAD`
- Files in checked tree: 138
- Inspected mode: source/docs/config read; no package install; no app execution; no model/Codex calls launched.

## Intake Boundary

```yaml
processing_tier: heavy
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

This source record is provenance and findability only. It does not create reviewed patterns, truth confidence, relation strength, or action basis.

## 文件 / 代码锚点

| Anchor | What exists | 初步看点 | Boundary |
|---|---|---|---|
| `README.md:42-57` | PDF gate, concept tags, visualization pane, KG, four tools, monotone evaluator. | Full loop from source document to interaction-derived progress signal. | README product claim is not independent quality evidence. |
| `README.md:63-70` | Bring-your-own ChatGPT / Codex CLI account, no server, no shared key pool, local journal. | Strong local-first / user-owned-credential pattern. | Does not remove OpenAI-side policy/privacy constraints. |
| `README.md:101-109` | Per-user storage under OS-native data dir, one folder per doc. | Simple file-first persistence surface. | Product storage layout is not VAKS schema. |
| `technical-writeup.md:87-109` | One Codex wrapper, read-only sandbox, JSON schemas, nine prompts. | Useful agent gateway consolidation and typed-output contract. | Codex transport is implementation-specific. |
| `technical-writeup.md:113-115` | Lazy visualization generation and server-owned singleton jobs. | Good lazy gate / server-owned derived artifact pattern. | Visualization readiness is not knowledge readiness. |
| `technical-writeup.md:127-129` | `new Function` sandbox with dangerous globals shadowed, plus repair loop. | Useful generated-code UX safety pattern. | It is explicitly not adversarial sandboxing. |
| `technical-writeup.md:135-148` | KG build/evaluate, four-axis scores, baseline + fresh interactions, monotone clamp. | Strong feedback/evaluation design input. | Monotone progress should not be copied to truth confidence. |
| `technical-writeup.md:156-164` | Chat, flashcards, quizzes, Feynman all feed one work-context JSON. | Good Use Ledger / append-only feedback input model. | The evaluator's summary is diagnostic, not reviewed evidence. |
| `technical-writeup.md:218-226` | No server-side OpenAI key or shared credit pool. | Good agent-account boundary and privacy posture. | VAKS should not hardcode one provider as architecture truth. |
| `technical-writeup.md:240-246` | Bundled Codex CLI lifecycle and boot guards. | Practical desktop-agent packaging notes. | Product packaging detail only. |
| `app/api/upload/route.ts:113-152` | Validate PDF magic, extract in memory, gate before writing disk or starting agents. | Source intake should reject impossible inputs before generating candidate records. | Samples bypass the real-upload gate; adapt carefully. |
| `lib/pdf-extract.ts:11-20` | `MAX_PDF_PAGES = 150` and explicit reason for hard cap. | Explicit cost/context gate beats silent truncation. | Threshold is product-specific. |
| `lib/pdf-extract.ts:160-195` | Deterministic no-text / image-dominant checks. | Strong model-free source quality gate. | Text-layer gate is PDF-specific. |
| `lib/jobs.ts:1-29` | Server-side detection and viz jobs, persisted tags, rate-limit retry, atomic writes. | Good derived-artifact job contract. | Do not turn every VAKS query into a background job. |
| `lib/jobs.ts:46-53` | Detection concurrency 3, batch size 5, max generic attempts. | Bounded concurrency and no infinite retry loops. | Constants are app-specific. |
| `lib/jobs.ts:274-312` | Concepts route back to page anchors, tags merge idempotently, pages marked analyzed. | Source-span anchored candidate overlays. | Tag anchor is UI location, not evidence support. |
| `lib/tags-store.ts:1-12`, `lib/tags-store.ts:58-70` | Server persisted tags, temp write then rename. | Simple atomic JSON write pattern. | Atomic file write is operational hygiene only. |
| `lib/codex.ts:49-62` | Codex thread options default to read-only, no approvals, scratch working dir, web off. | Good agent gateway quarantine default. | Still depends on Codex SDK behavior. |
| `lib/codex.ts:117-193` | Health mailbox and rate-limit preflight. | Good operator/user feedback for agent failures. | Health is diagnostic, not knowledge status. |
| `lib/codex.ts:251-287`, `lib/codex.ts:310-360` | `runJson` / `runJsonInThread`, parse retry, typed output, thread resume. | One transport API for all agents. | JSON parse success is not semantic truth. |
| `lib/work-context.ts:1-12`, `lib/work-context.ts:51-100` | One work-context file; evaluator summary only emits fresh interactions after `sinceTs`. | Strong append-only + incremental feedback summary model. | The saved file can still contain poor evidence. |
| `lib/kg-runner.ts:202-258`, `lib/kg-runner.ts:297-392` | Rubric, non-decreasing rule, queue, skip no-new-interaction, clamp. | Good evidence-of-learning loop. | Do not copy monotone clamp to reviewed knowledge. |
| `package.json:1-35` | Private Next/Electron app, Apache-2.0, Codex SDK dependency and scripts. | Confirms stack and local app intent. | Dependency versions may drift. |
| `.github/workflows/release.yml:1-25` | Tag-driven release pipeline, macOS signing/notarization notes. | Useful release hygiene reference. | Windows signing remains unresolved. |

## 初步看点

1. **模型前置质量门**：不是先让 LLM 摘要失败，再解释为什么失败，而是在入口就拒绝扫描件、图片主导 PDF、超长 PDF。
2. **source-centered UX**：可视化标签挂在原文位置旁边，不把摘要变成阅读对象的替代品。
3. **derived artifact owner**：tag/viz/KG/work-context 都有服务器侧状态文件，而不是浏览器 tab 自己“记得”。
4. **Use Ledger 原型**：聊天、卡片、测验、Feynman 都进同一个 work-context journal，评价器读 journal，不改 journal。
5. **agent gateway 边界**：所有模型调用进同一个 Codex wrapper，默认 read-only / no approval / scratch dir / schema output / health mailbox。
6. **评价维度拆分**：memory / comprehension / structure / application 比单一分数更适合暴露学习状态。

## 明显疑点

1. `new Function` sandbox 的边界是“防 LLM 失误”，不是安全执行不可信代码；VAKS 不应把它当 agent safety 证明。
2. mastery score 单调不下降适合学习鼓励和进度保留，但事实判断会被新证据推翻；这个机制不能迁移到 truth confidence。
3. BYO ChatGPT/Codex CLI 是很好的产品定位，但对 VAKS 来说 provider / gateway 应可替换，不应把某个 transport 写死成核心架构。
4. 文档说 Windows builds are not signed；桌面分发风险仍在。
5. 本次未安装依赖、未启动 App、未运行 smoke tests；源码锚点足够做 candidate distillation，不足以证明 runtime 质量。

## 可抽取 Candidate Points

- `source-quality-gate-before-agent-work`
- `source-anchored-derived-overlays`
- `server-owned-idempotent-derived-jobs`
- `typed-agent-transport-wrapper`
- `agent-health-mailbox`
- `append-only-work-context-ledger`
- `incremental-feedback-evaluator`
- `progress-score-not-truth-confidence`
- `llm-code-repair-is-ux-not-safety`
- `bring-your-own-account-agent-boundary`

## 当前处理等级

```text
heavy source/code read, candidate-only extraction
```

升级为 reviewed pattern / decision 的条件：

- 与至少 1-2 个相似 repo / paper / product pattern 做交叉验证。
- 对 VAKS 本地一个真实入口做小型 trial，例如 source intake gate、feedback-event journal、query-run health mailbox。
- 明确哪些字段进入模板，哪些只停留在 `outputs/review` 候选。

## 下一步

- 已写入候选蒸馏：`outputs/review/2026-06-06-beltromatti-get-it-candidate-distillation.md`
- 已写入 library review：`wiki/summaries/2026-06-06-beltromatti-get-it-architecture-review.md`
- 暂不写 `wiki/patterns` / `wiki/decisions`，因为还没有 reviewed adoption。
