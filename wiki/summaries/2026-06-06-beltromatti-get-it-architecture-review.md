---
type: library_review
status: draft
library_name: "Get It."
repo_url: https://github.com/beltromatti/get-it
source_url: https://github.com/beltromatti/get-it
checked_commit: 4ce88a2c0a242206d96bcd7221bdeda1efcba41c
commit_time: "2026-05-28 22:08:33 +0200"
source_status: active
reviewed_at: 2026-06-06
domain: local-first PDF study agent workbench
related_projects:
  - verified-action-knowledge-system
current_branch:
  - source-intake
  - feedback-ledger
  - agent-gateway
  - local-first-workbench
extracted_patterns:
  - source-quality-gate-before-agent-work
  - source-anchored-derived-overlays
  - server-owned-idempotent-derived-jobs
  - typed-agent-transport-wrapper
  - append-only-work-context-ledger
  - incremental-feedback-evaluator
fusion_decision: adapt
borrow_value: strong
tag_level: strong-borrow
confidence: medium
evidence_count: 22
cross_validated_with:
  - DataChain
  - VAKS Source Intake Control Flow
negative_evidence:
  - LLM code sandbox is not adversarial safety
  - monotone progress scores do not transfer to truth confidence
  - runtime was not executed in this review
extension_potential: medium
relations: []
tags:
  - get-it
  - library-review
  - strong-borrow
  - source-intake
  - source-quality-gate
  - source-anchored-overlays
  - typed-agent-gateway
  - feedback-ledger
  - agent-health-mailbox
  - local-first-workbench
  - candidate-only
---

# 库分析：Get It.

## 它解决什么问题

`Get It.` 解决的是学生已有 PDF 之后的学习闭环问题：

```text
PDF 原文
-> 质量门
-> 概念标签 / 可视化
-> 知识图谱
-> chat / flashcards / quizzes / Feynman
-> work-context journal
-> mastery evaluator
```

它的设计重点不是“摘要 PDF”，而是把源文档旁边的理解辅助和学习反馈变成一个本地桌面工作台。

对 VAKS 来说，它最有价值的不是学习功能，而是：

```text
source gate
derived artifact persistence
agent transport boundary
append-only feedback trace
incremental evaluator
diagnostic health mailbox
```

## 核心设计

核心架构是 Next.js 16 + Electron 桌面壳 + 本地 JSON 文件存储 + Codex CLI/SDK 作为用户自带模型账户的 transport。

文档处理分两条并行线：

```text
upload
-> deterministic PDF gate
-> pdfjs extraction
-> concept detection + per-tag visualization
-> source-side visual overlay

upload
-> KG build
-> four learning tools feed workctx.json
-> KG evaluate reads fresh interactions
-> four-axis mastery scores
```

关键控制点：

- 入口先拒绝不适合的 PDF，避免 silent truncation。
- agent 输出通过 JSON schema 进 typed object。
- 检测和可视化是 server-owned jobs，viewer 只消费状态。
- 互动 journal append-only by convention。
- evaluator 只读新增交互，runtime clamp 保证学习分数不下降。
- Codex wrapper 默认 read-only / no approval / scratch dir / web off。

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md:42-57` | PDF gate, tags, visualizer, KG, four tools, monotone evaluator. | Source-to-feedback loop in one user-facing product. | Product README is not runtime proof. |
| `README.md:63-70` | User signs in with own ChatGPT/Codex; no Get It server/key pool/analytics. | User-owned credential and local-first posture. | OpenAI-side data/policy still applies. |
| `README.md:89-109` | Setup wizard and local data folder layout. | Practical local app recovery and storage surface. | Storage schema is app-specific. |
| `technical-writeup.md:87-109` | One Codex transport wrapper; JSON schemas; nine prompts. | Unified agent gateway + typed-output discipline. | JSON validity is not truth. |
| `technical-writeup.md:113-115` | Server-side singleton jobs; lazy on-click generation; state polling. | Lazy gate and derived artifact owner. | Ready tag is not reviewed knowledge. |
| `technical-writeup.md:127-129` | Dangerous globals shadowed; repair loop. | Generated-code preflight/repair pattern. | Explicitly not adversarial sandboxing. |
| `technical-writeup.md:135-148` | KG build/evaluate; fresh interactions; monotone clamp. | Incremental feedback evaluator. | Learning progress invariant does not fit truth confidence. |
| `technical-writeup.md:156-164` | Four tools feed one work-context JSON. | Use Ledger shape: one trace, many interaction types. | Evaluator summary is diagnostic. |
| `technical-writeup.md:218-226` | No server key, no shared credits, no app-side metering. | Agent credential ownership boundary. | Provider-specific product decision. |
| `app/api/upload/route.ts:113-152` | Extract in memory, quality gate before disk write and agent workflow. | Intake gate before candidate generation. | Gate is processability, not reliability. |
| `lib/pdf-extract.ts:11-20` | Hard 150-page cap with explicit rationale. | Context/cost gate should be explicit. | Threshold not portable. |
| `lib/pdf-extract.ts:160-195` | Deterministic no-text / image-dominant checks. | Model-free source suitability check. | PDF-specific. |
| `lib/jobs.ts:1-29` | Detection/viz jobs, incremental persistence, retry, atomic write. | Durable derived job contract. | Job success is not semantic correctness. |
| `lib/jobs.ts:46-53` | Bounded concurrency and max attempts. | Avoid burst overload and infinite retry. | Constants are app-specific. |
| `lib/jobs.ts:274-312` | Anchor located against extracted PDF items, tags merged idempotently. | Source-anchored derived overlays. | UI anchor is not evidence support. |
| `lib/tags-store.ts:58-70` | Temp file then rename. | Atomic JSON write habit. | Operational hygiene only. |
| `lib/codex.ts:49-62` | Read-only sandbox, no approvals, scratch working dir, web off by default. | Agent quarantine default. | Depends on Codex SDK semantics. |
| `lib/codex.ts:117-193` | Health mailbox, rate-limit preflight. | Diagnostic state separated from UI/jobs. | Health is not knowledge status. |
| `lib/codex.ts:251-287`, `lib/codex.ts:310-360` | `runJson` and `runJsonInThread`. | One transport wrapper for stateless and threaded calls. | Thread context is not evidence. |
| `lib/work-context.ts:1-12`, `lib/work-context.ts:51-100` | Work context file, append-only convention, incremental summary. | Feedback ledger and evaluator input. | Summary can omit context; raw trace must remain. |
| `lib/kg-runner.ts:202-258`, `lib/kg-runner.ts:297-392` | Rubric, monotone clamp, coalesced queue, skip no-new-interactions. | Efficient evaluator loop. | Monotone clamp must not apply to VAKS truth. |
| `.github/workflows/release.yml:1-25` | Tag release, signing/notarization notes. | Release hygiene and platform caveats. | Windows signing unresolved. |

## 当前支线价值

当前支线：

```text
Source Intake Control Flow / feedback-ledger / agent gateway / local workbench
```

它对当前支线：

```text
refines
```

具体价值：

- 强化 `SOURCE_INTAKE.md` 的 “processing_tier != authority” 口径：处理前可以有 gate，但 gate 不产生 truth。
- 给 `templates/query-run.md` / future agent health trace 一个参考：auth/rate-limit/binary/generic 应与 source/candidate/reviewed 状态分离。
- 给 `FEEDBACK.md` 一个工程样本：使用行为进 append-only journal，再由 evaluator 产出 derived diagnostic。
- 给 future local workbench 一个 UI/状态样本：viewer 消费 server-owned artifact，不让浏览器临时状态成为事实来源。

打标签等级：

```yaml
tag_level: strong-borrow
borrow_value: strong
```

强借用范围只限：

```text
source-intake / agent-gateway / feedback-ledger / local workbench diagnostics
```

不表示：

```text
reviewed knowledge / truth confidence / action basis / implementation decision
```

风险：

- 容易被误吸收成“学习分数也可以做知识置信度”。
- 容易把 repair loop / `new Function` shadowing 误读为 agent sandbox 安全方案。
- 容易把 Codex CLI transport 写成 VAKS core，而不是可替换 agent gateway 的一个实例。

## 全貌架构价值

| Architecture Zone | Value / Finding | Adopt? |
|---|---|---|
| Karpathy spine | 文件优先、本地 JSON、简单 index/store，非常贴近 light workflow。 | adapt |
| Dusk workbench | Library / viewer / right pane / job badges 是 scope workbench 的参考。 | watch |
| source ingest | PDF quality gate、processability reason、no silent truncation。 | adapt |
| review queue | 不直接提供 review queue，但 tag/state/journal 可作为 candidate inputs。 | watch |
| schema / reviewed knowledge | typed schemas 对 agent output 有用；mastery score 不适合 truth。 | adapt with boundary |
| memory / dev context | Per-doc persistent context 和 thread resume 是 activation/cost 优化。 | watch |
| feedback | Work-context journal + incremental evaluator 是高价值参考。 | adapt |
| retrieval / cache | 没有重点做 RAG 检索；主要是 per-doc extracted cache。 | no-clear-value |
| API / MCP / agent access | Codex wrapper + health mailbox 是 strong gateway reference。 | adapt |
| viewer / workbench | Source-anchored inline tags和右侧工具面板很有启发。 | watch |
| publishing | Tag-driven release / notarization 是产品发布参考，不是 VAKS publishing。 | watch |
| risk / anti-pattern | Monotone scores、LLM code sandbox、BYO account 都有误用风险。 | adapt carefully |

## 值得提炼的模式

1. `source-quality-gate-before-agent-work`
2. `server-owned-derived-artifact-jobs`
3. `typed-agent-gateway-with-health-mailbox`
4. `append-only-use-ledger-with-derived-evaluator`
5. `source-anchored-candidate-overlays`
6. `domain-specific-runtime-invariant`

这些目前只进入 candidate distillation，不直接写成 formal pattern。

## 标签与量化

- domain: local-first agent learning app
- problem: source-centered study workflow and measurable mastery feedback
- pattern: source gate + derived overlays + use ledger + incremental evaluator
- maturity: emerging
- complexity: medium
- problem_fit: 4
- reuse_value: 4
- implementation_cost: 3
- integration_fit: 4
- evidence_strength: 3
- reversibility: 5

## 交叉验证

- 相似设计来源：
  - DataChain: read-first compiled surface / typed derived artifacts / reuse before recompute。
  - VAKS Source Intake Control Flow sandbox: candidate not action basis、retrieval_policy 机器可过滤、derived artifacts 不越权。
- 用户历史项目里的相似问题/影子：
  - 视频 intake 要先保留 transcript/segments/metadata/ledger，再做 candidate distillation。
  - Project Overlay sidecar 只能 active-project activation，不能当 authority。
  - Feedback Ledger 只影响 usefulness/scope_fit/review_pressure，不改 truth。
- 支持证据：
  - Source/code anchors listed above.
- 反例或失败边界：
  - runtime 未执行。
  - LLM sandbox 不是 adversarial sandbox。
  - mastery monotone clamp 与 truth maintenance 的可降级/可推翻冲突。
- 最小验证方式：
  - 为 `templates/query-run.md` 或 `templates/maintenance-manifest.md` 增加一个可选 `agent_health` block 的 candidate trial。
  - 对一个 repo/article/PDF source intake 做 processability gate 小试验。
  - 用现有 `outputs/feedback` 跑一次 append-only feedback-event -> derived diagnostic 的 micro-trial。

## Knowledge Calibration / Point Collision

| Candidate Point | Local Reviewed Knowledge | Calibration Output | Review Question |
|---|---|---|---|
| `source-quality-gate-before-agent-work` | `SOURCE_INTAKE.md` says processing_tier != authority and strict checks are lazy gates. | candidate_relation | Which source_type gates are worth templating now? |
| `typed-agent-transport-wrapper` | Agent memory quarantine / future agent writes cannot mutate truth. | candidate_relation | Should VAKS have one agent gateway contract before MCP tools expand? |
| `append-only-work-context-ledger` | `FEEDBACK.md` / Use Ledger: feedback does not mutate truth. | refines | Should query-run and feedback-event share one append-only event family? |
| `progress-score-not-truth-confidence` | Truth confidence can change with evidence; feedback cannot directly mutate truth. | contradiction_candidate avoided by boundary | Where do we store progress/usefulness metrics so they do not look like truth? |
| `llm-code-repair-is-ux-not-safety` | Test/fixture/LLM-judge results are diagnostic, not truth or readiness. | risk_of | What sandbox level is required before generated code can execute in VAKS? |

边界：

- 相似不是支持。
- 冲突不是自动推翻。
- 重复出现不是自动真理。
- 校准输出是 review input，不是 reviewed relation。

## Support / Challenge Review

What supports it:

- The repo contains explicit code and docs for PDF gate, job state, Codex wrapper, work-context journal, KG evaluator, and packaging.
- The design aligns with existing VAKS boundaries: raw/source first, candidate output separate, feedback as derived diagnostic.

What challenges it:

- The repo is product-specific and education-specific.
- The app was not executed in this review.
- Some claims are from README / writeup rather than test evidence.
- The strongest-sounding mechanism, monotone scoring, is dangerous if copied to truth confidence.

Challenge severity:

```text
major for direct adoption
minor for design-only extraction
```

Scope limits:

- Only useful as source intake / feedback / local workbench / agent gateway reference.
- Not a truth maintenance engine.
- Not a verified knowledge system.
- Not an evidence support checker.

Known risks:

- Over-platforming ordinary source intake.
- Confusing progress UX with review state.
- Confusing provider transport with architecture core.
- Confusing generated-code repair with agent safety.

Review again when:

- VAKS starts implementing an agent gateway / desktop workbench.
- VAKS adds a query-run / feedback-event evaluator.
- A source-type-specific quality gate becomes necessary.

Action readiness:

```text
not_ready
```

Reason: this is a candidate design extraction. It can guide a micro-trial, not action-facing support.

## 关系边 / 关联强度

```yaml
relations:
  - target: "[[Source Intake]]"
    type: refines
    relation_state: candidate
    evidence:
      - "[[2026-06-06-beltromatti-get-it-source]]"
    rationale: "Model-free processability gates should run before agent extraction but remain separate from authority."
    created: 2026-06-06
    last_verified: 2026-06-06
  - target: "[[Feedback Ledger]]"
    type: refines
    relation_state: candidate
    evidence:
      - "[[2026-06-06-beltromatti-get-it-source]]"
    rationale: "Work-context journal plus incremental evaluator is a useful Use Ledger design input."
    created: 2026-06-06
    last_verified: 2026-06-06
  - target: "[[Agent memory quarantine]]"
    type: refines
    relation_state: candidate
    evidence:
      - "[[2026-06-06-beltromatti-get-it-source]]"
    rationale: "A single read-only Codex wrapper with health mailbox is a candidate agent gateway shape."
    created: 2026-06-06
    last_verified: 2026-06-06
  - target: "[[Truth confidence]]"
    type: risk_of
    relation_state: candidate
    evidence:
      - "[[2026-06-06-beltromatti-get-it-source]]"
    rationale: "Monotone mastery scores would be unsafe if translated into factual confidence."
    created: 2026-06-06
    last_verified: 2026-06-06
```

## 对当前项目的适配点

可以小规模适配：

- source intake gate reason fields:

```yaml
processability_gate:
  checked: true
  result: pass | fail | skipped
  reason_code:
  reason_note:
  agent_work_started: false
```

- agent health diagnostic:

```yaml
agent_health:
  status: ok | rate_limited | auth_lost | binary_missing | generic_error
  retry_at:
  source: tool | model | local_runtime
  action_basis_allowed: false
```

- feedback evaluator cursor:

```yaml
feedback_eval:
  last_evaluated_at:
  raw_trace_location:
  derived_summary_location:
  truth_mutation_allowed: false
```

暂不适配：

- mastery graph UI
- four-axis student scoring
- LLM-generated JS visualizer
- Codex CLI as mandatory product dependency
- monotone scoring for knowledge confidence

## 可拓展性

- 是否适合作为插件/适配层：适合做 agent gateway / local workbench / intake-gate 参考。
- 是否会绑定核心结构：如果直接搬产品结构，会绑定；如果只吸收模式，不会。
- 未来替换成本：低到中。gate / health / journal 都可用 Markdown/JSON artifact 承接。
- 可迁移路径：先 candidate template trial，再 Pro/reviewer 复核，再决定是否写入 `SOURCE_INTAKE.md` / `FEEDBACK.md` / `templates/query-run.md`。

## 复杂度和风险

复杂度：

- 工程复杂度中等，涉及 Electron、Next、local file store、Codex SDK、background jobs。
- 对 VAKS 当前 mainline 来说，只吸收小机制即可，不应复制产品栈。

风险：

- 误把 local-first 说成 no-data-leaves-device；实际模型调用仍走用户账户和 OpenAI 侧服务。
- 误把 schema 输出当 truth。
- 误把 evaluation score 当 review confidence。
- 误把 repair loop 当安全沙箱。

## 不可行点 / 避坑

- 不要 fork 这个 App 做 VAKS。
- 不要把 `memory/comprehension/structure/application` 分数写进 truth layer。
- 不要在普通 capture 上强制跑完整评价器。
- 不要让 source gate 失败直接生成 negative knowledge。
- 不要把 Codex CLI 账户状态写成 source reliability。
- 不要让 generated code 在 VAKS 里运行，除非另有真实 sandbox 和权限协议。

## 融合判断

- 结论：adapt
- 理由：它提供的是多个清晰的小型工程控制点，正好可以补 VAKS 的 source intake / feedback / agent gateway 操作层；但产品对象和学习分数不能直接搬。
- 验证方式：先做 1-2 个 candidate-only micro-trial，尤其是 `processability_gate` 和 `agent_health`。

## 直接判断

- Direct use: no
- Fork: no
- Design-only: yes
- Reject: no, but reject direct migration of mastery score / JS sandbox / mandatory Codex transport
- Current branch value: high for source-intake + feedback-ledger + agent-gateway candidate design
- Whole architecture value: medium-high as local-first workbench reference
- Risk: progress metrics and generated-code repair can easily be overread as truth/safety
- Next action: keep as candidate-only reference; do not promote until a narrow VAKS micro-trial passes review

## 后续行动

1. Keep source record and candidate distillation as review input.
2. If source intake gates are reopened, compare this against `SOURCE_INTAKE.md` and the Source Intake Control Flow sandbox.
3. If agent gateway work starts, use `lib/codex.ts` / health mailbox as one reference, not as the only transport model.
4. If feedback-ledger evaluator work starts, borrow the append-only journal + incremental cursor shape, but keep truth mutation blocked.
