---
record_kind: candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: none
derived_from:
  - raw/repos/2026-06-06-beltromatti-get-it-source.md
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
  - source-intake
  - feedback-ledger
  - agent-gateway
  - local-first-workbench
possible_project_refs:
  - verified-action-knowledge-system
point_anchor_refs:
  - snapshot_ref: raw/repos/_snapshots/beltromatti-get-it-4ce88a2c0a242206d96bcd7221bdeda1efcba41c.zip
    selector_type: source_code
    selector_value: README.md:42-57
  - snapshot_ref: raw/repos/_snapshots/beltromatti-get-it-4ce88a2c0a242206d96bcd7221bdeda1efcba41c.zip
    selector_type: source_code
    selector_value: technical-writeup.md:87-115
  - snapshot_ref: raw/repos/_snapshots/beltromatti-get-it-4ce88a2c0a242206d96bcd7221bdeda1efcba41c.zip
    selector_type: source_code
    selector_value: lib/kg-runner.ts:202-392
tagging_decision: tagged
tag_level: strong-borrow
tag_level_reason: "Strong VAKS fit for source processability gates, source-anchored candidate overlays, typed agent gateway, health diagnostics, and feedback/use-ledger design; not a truth-layer adoption."
borrow_value: strong
borrow_order:
  - "P1: source-quality gate before agent/model work"
  - "P1: source-anchored derived overlays that stay tied to original PDF/text anchors"
  - "P1: typed agent transport wrapper with read-only/no-approval defaults and health mailbox"
  - "P1: append-only work-context ledger feeding a derived incremental evaluator"
  - "P2: server-owned singleton jobs, idempotent derived artifacts, and atomic JSON writes"
  - "P2: progress dimensions as usefulness/learning diagnostics, not truth confidence"
  - "P3: local-first desktop workbench and release packaging as later product reference"
avoid:
  - "Do not copy monotone mastery score into VAKS truth confidence; VAKS facts must be able to go down, become stale, or be contradicted."
  - "Do not treat source processability gates as source reliability or evidence sufficiency."
  - "Do not treat schema-valid agent JSON as semantically true."
  - "Do not treat LLM code repair or new Function shadowing as adversarial sandbox safety."
  - "Do not make Codex CLI the mandatory VAKS core transport; keep agent gateway provider-replaceable."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "approved VAKS task implements source intake gates, agent gateway quarantine, feedback/use-ledger events, or local workbench job status."
  support_when: "designing source-type processability checks, source-anchored overlays, query-run diagnostics, derived artifact jobs, or feedback evaluator cursors."
  risk_when: "mastery/progress score could be confused with truth confidence, schema-valid output could be confused with evidence, or generated-code repair could be confused with sandbox safety."
  cold_references:
    - raw/repos/2026-06-06-beltromatti-get-it-source.md
    - raw/repos/_snapshots/beltromatti-get-it-4ce88a2c0a242206d96bcd7221bdeda1efcba41c.zip
tags:
  - candidate
  - provisional
  - get-it
  - codex-cli
  - local-first
  - strong-borrow
  - source-intake
  - source-quality-gate
  - source-anchored-overlays
  - typed-agent-gateway
  - feedback-ledger
  - agent-health-mailbox
  - candidate-only
---

# Get It. Candidate Distillation

## Boundary

This note is provisional orientation.

It can help route attention, compare ideas, or suggest project overlays. It is not reviewed knowledge, not a decision, not a formal pattern, and not action basis.

## Source

```yaml
derived_from:
  - raw/repos/2026-06-06-beltromatti-get-it-source.md
checked_commit: 4ce88a2c0a242206d96bcd7221bdeda1efcba41c
snapshot: raw/repos/_snapshots/beltromatti-get-it-4ce88a2c0a242206d96bcd7221bdeda1efcba41c.zip
snapshot_sha256: 2F4C1285C03D8A4BD36766B8383CE6B927D8CD3725ABD0D4D80A42338F26CFAD
```

## 人话压缩

`Get It.` 最值得借的不是“学习 App 功能”，而是这条小闭环：

```text
source gate
-> source-anchored generated overlays
-> server-owned derived artifacts
-> local append-only interaction journal
-> incremental evaluator reads only fresh evidence
-> UI shows progress / repair / rate-limit state
```

对 VAKS 的说人话版本：

```text
先判断材料能不能处理。
能处理，再生成候选。
候选生成物要落文件、可恢复、可重跑、可解释。
用户怎么用它，也要留下 Use Ledger。
但这些都不是 truth；它们只是让 review 和 action basis 更有材料。
```

## 打标签结论

```yaml
tagging_decision: tagged
tag_level: strong-borrow
borrow_value: strong
```

强在哪里：

```text
source gate / source anchor / agent gateway / health mailbox / feedback ledger
```

不强在哪里：

```text
不是 truth layer
不是 reviewed pattern
不是 action basis
不是 VAKS core transport 决策
```

## Candidate Points

### 1. `source-quality-gate-before-agent-work`

候选结论：VAKS 的 source intake 可以借鉴 `Get It.` 的入口门：先用确定性检查判断输入是否适合当前处理路径，再启动 agent、摘要、抽取、candidate distillation。

锚点：

- `app/api/upload/route.ts:113-152`
- `lib/pdf-extract.ts:11-20`
- `lib/pdf-extract.ts:160-195`

对 VAKS 的适配：

- PDF / video / repo / article 都可以有最小 gate。
- gate 只能决定“当前路径是否适合处理”，不能决定 source 是否可靠。
- gate 失败应该产生清楚的 reason，而不是静默截断或生成低质候选。

边界：

```text
input quality gate != truth review
processable != trustworthy
unprocessable != false
```

### 2. `source-anchored-derived-overlays`

候选结论：`Get It.` 把概念 tag 落在 PDF 文本位置旁边，而不是把摘要变成原文替代品。VAKS 可以借这个思想：candidate overlay / context-pack hint / project sidecar 应该尽量回到 source anchor 或 reviewed node，不要漂成无锚点解释。

锚点：

- `README.md:42-46`
- `lib/jobs.ts:274-312`
- `lib/pdf-extract.ts:196-260`

对 VAKS 的适配：

- 文章 / repo / paper / video 的候选点应保留可回钻 anchor。
- overlay 可以帮助阅读，但不能成为 evidence support。
- UI tag / route hint 是 activation，不是 support。

边界：

```text
anchor location != evidence support
overlay visibility != reviewed relation
```

### 3. `server-owned-idempotent-derived-jobs`

候选结论：检测和可视化不是 browser tab 的临时循环，而是 server-side singleton jobs，状态写入 JSON，viewer 只轮询消费。VAKS 的 source extraction、candidate distillation、query-run、context-pack 生成也应该有明确 owner、状态、receipt 和重入规则。

锚点：

- `technical-writeup.md:113-115`
- `lib/jobs.ts:1-29`
- `lib/jobs.ts:91-134`
- `lib/tags-store.ts:58-70`

对 VAKS 的适配：

- 长任务要有 `in_progress / done / failed / retry_after` 之类状态。
- derived artifact 要落 repo-visible 或 vault-visible 文件，不留在隐形 scratch。
- 重跑要 idempotent，不能 silent overwrite。

边界：

```text
job success != semantic correctness
atomic write != reviewed knowledge
```

### 4. `typed-agent-transport-wrapper`

候选结论：所有 agent 调用进同一个 `runJson` / `runJsonInThread` wrapper，默认 read-only sandbox、no approval、web off、schema output、health mailbox。这是一个很好的 agent gateway quarantine 形状。

锚点：

- `technical-writeup.md:87-109`
- `lib/codex.ts:49-62`
- `lib/codex.ts:251-287`
- `lib/codex.ts:310-360`

对 VAKS 的适配：

- 未来 agent / MCP / tool 调用应有统一入口和权限默认值。
- schema 解析失败可以重试，但语义判断必须走 review。
- chat thread resume 是成本优化，不是证据保留。

边界：

```text
schema-valid JSON != true claim
read-only sandbox != proof of no side effect outside provider
Codex CLI transport != VAKS core dependency
```

### 5. `agent-health-mailbox`

候选结论：`Get It.` 不把 auth / rate limit / binary missing 混成 generic failure，而是写入 health mailbox，让 UI 和后台 queue 有一致的恢复口径。VAKS 可以借成 operator cockpit / query-run / source-intake 的 diagnostic surface。

锚点：

- `README.md:69-70`
- `technical-writeup.md:197-214`
- `lib/codex.ts:117-193`
- `lib/kg-runner.ts:331-348`

对 VAKS 的适配：

- agent/tool failure 应进入 diagnostic / maintenance manifest。
- `retry_at`、`auth_lost`、`rate_limited`、`binary_missing` 应与 knowledge status 分离。
- 失败恢复可以自动重试，但不能自动改变 truth/candidate 状态。

边界：

```text
health status != source reliability
retry success != review pass
```

### 6. `append-only-work-context-ledger`

候选结论：聊天、卡片、测验、Feynman 全进一个 `workctx.json`；评价器读它，但不改它。这很接近 VAKS 的 Use Ledger / Feedback Event：使用过程留下轨迹，后续从轨迹里提取 usefulness、scope fit、review pressure。

锚点：

- `technical-writeup.md:152-164`
- `lib/work-context.ts:1-12`
- `lib/work-context.ts:51-100`

对 VAKS 的适配：

- query-run / feedback-event / action outcome 可以统一成 append-only trace。
- evaluator / reviewer 可以读 trace，产出 candidate feedback。
- 原始使用记录应保留，summary 只是 derived view。

边界：

```text
feedback trace != truth mutation
positive feedback is weak
negative feedback creates review pressure
explicit correction creates review_due
```

### 7. `incremental-feedback-evaluator`

候选结论：评价器拿当前 graph baseline，只看 `lastEvaluatedAt` 之后的新交互；没新交互就不花模型调用。VAKS 的 feedback / query-run / source dashboard 也可以借这个“新证据增量读取”的思路。

锚点：

- `technical-writeup.md:146-148`
- `lib/work-context.ts:60-100`
- `lib/kg-runner.ts:361-392`

对 VAKS 的适配：

- 反馈总结不必每次重读全历史。
- baseline 应该是 derived state，原始 trace 仍保留。
- 增量 evaluator 输出只能是 diagnostic / review input。

边界：

```text
incremental summary may miss old context
derived baseline cannot replace raw trace
```

### 8. `progress-score-not-truth-confidence`

候选结论：`Get It.` 的四轴分数是学习进度 UX：memory、comprehension、structure、application。它对 VAKS 有启发：不同维度的“使用表现”比一个总分更有用。但它不能迁移为 truth confidence。

锚点：

- `README.md:50-59`
- `technical-writeup.md:137-148`
- `lib/kg-runner.ts:202-258`

对 VAKS 的适配：

- feedback 可以拆成 usefulness、scope_fit、retrieval_hit_quality、evidence_gap_detected。
- action outcome 可以拆成 did_work、missing_context、wrong_scope、risk_missed。
- 不要把这些维度变成 truth score。

边界：

```text
progress score != evidence support
usefulness != truth
high interaction volume != confidence
```

### 9. `monotone-clamp-is-domain-specific`

候选结论：`Get It.` runtime clamp 确保学生进度不下降，这对学习产品很合理，因为它避免模型一次误判抹掉过去成果。但 VAKS 恰恰需要允许新证据降低 confidence、标记 stale、触发 contradiction。

锚点：

- `README.md:57`
- `technical-writeup.md:146`
- `lib/kg-runner.ts:297-303`

对 VAKS 的适配：

- 可以借“engine-side guard enforces invariant”的做法。
- 不能借“所有分数只升不降”的具体 invariant。
- VAKS 的 invariant 应该是：reviewed truth 不能被 feedback 直接改；source/candidate/reviewed 边界不能被 derived artifacts 绕过。

边界：

```text
monotone learning progress != monotone truth confidence
```

### 10. `llm-code-repair-is-ux-not-safety`

候选结论：可视化代码生成失败时，应用把错误送回 agent 修复，用户看到 repairing。这是很好的产品体验和生成物修复 loop，但安全边界不能高估。

锚点：

- `README.md:45`
- `technical-writeup.md:127-129`
- `lib/agents/viz.ts:1-16`
- `lib/viz-runtime.ts:1-62`

对 VAKS 的适配：

- LLM 输出可以有 syntax preflight / repair attempt / retry budget。
- 失败应留下 diagnostic，而不是让用户看不懂。
- 如果未来 agent 写脚本，必须另有真实 sandbox / permission gate。

边界：

```text
repair loop != adversarial sandbox
syntax preflight != semantic correctness
```

### 11. `bring-your-own-account-agent-boundary`

候选结论：产品选择“不持有 server-side OpenAI key”，而是让用户用自己的 ChatGPT/Codex 账户。这给 VAKS 一个重要提醒：agent access 应透明、可归属、可撤回，避免共享黑箱 key pool。

锚点：

- `README.md:61-72`
- `technical-writeup.md:218-226`
- `technical-writeup.md:240-246`

对 VAKS 的适配：

- future tool/agent surface 应区分 user-owned credential、project credential、service credential。
- 每类 credential 的数据流、权限、审计责任要清楚。
- Provider choice 应保持可替换。

边界：

```text
user-owned credential != no data leaves device
transport transparency != reviewed knowledge
```

## Open Questions

1. VAKS 是否需要一个最小 `agent_health_event` 模板，还是先把这类内容放进 `maintenance-manifest` / `query-run`？
2. Source intake 的 gate 是否应该按 source_type 拆：article / repo / video / paper / PDF？
3. Use Ledger 是否需要类似 `last_evaluated_at` 的增量 cursor，还是现阶段保留人工读全 trace 更稳？
4. 如果未来要运行 agent 生成脚本，真实 sandbox 是 Vercel sandbox / local container / Windows sandbox，还是只允许 dry-run artifact？
5. BYO account 模式在我们的桌面/Obsidian workflow 中是否值得作为默认解释层，还是只作为外部产品参考？

## Routing Hint

```yaml
route_to:
  - SOURCE_INTAKE.md
  - FEEDBACK.md
  - DEV_CONTEXT.md
  - templates/query-run.md
  - templates/maintenance-manifest.md
  - future agent gateway / operator cockpit notes
do_not_route_to:
  - wiki/claims
  - wiki/patterns
  - wiki/decisions
unless:
  - later reviewed adoption passes v0_2_13 gate
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
