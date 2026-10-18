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
project_id: verified-action-knowledge-system
target_ref: raw/repos/2026-06-06-beltromatti-get-it-source.md
target_selector: checked_commit:4ce88a2c0a242206d96bcd7221bdeda1efcba41c
target_hint: "Use as a VAKS source-intake, agent-gateway, feedback-ledger, and local-workbench reference, not as truth architecture."
tagging_decision: tagged
tag_level: strong-borrow
tag_level_reason: "Directly useful for VAKS source processability gates, source-anchored candidate overlays, typed agent gateway quarantine, health diagnostics, and append-only feedback/use-ledger design."
project_borrow_scope:
  - source-quality gate before agent/model work
  - source-anchored derived overlays for candidate comprehension
  - server-owned derived artifact jobs with status and idempotence
  - typed agent transport wrapper with read-only/no-approval defaults
  - agent health mailbox for auth/rate-limit/binary/generic failures
  - append-only work-context ledger and incremental evaluator cursor
  - progress/usefulness dimensions as feedback diagnostics only
project_non_borrow_scope:
  - mastery score as truth confidence
  - monotone non-decreasing scores for reviewed knowledge
  - schema-valid JSON as true claim
  - generated-code repair as adversarial sandbox
  - Codex CLI as mandatory VAKS core dependency
  - full PDF study app or mastery graph in VAKS core
project_reopen_trigger:
  - "VAKS implements source-type processability gates."
  - "VAKS adds an agent/tool gateway contract or query-run diagnostic mailbox."
  - "VAKS adds feedback-event or use-ledger evaluator cursors."
  - "VAKS builds a local workbench where derived artifacts have server-owned job states."
  - "VAKS considers running generated code or model-created scripts."
confirmation_basis:
  - user requested continuation of the same repository distillation/tagging lane
  - existing source card, candidate distillation, and architecture review were found locally
  - GitHub current main still matches checked commit 4ce88a2c0a242206d96bcd7221bdeda1efcba41c
  - snapshot hash verified locally
  - no runtime execution; no promotion to reviewed knowledge
last_checked_at: 2026-06-07
expires_at: 2026-07-07
borrow_value: strong
borrow_order:
  - "P1: source-quality gate before agent/model work"
  - "P1: typed agent gateway with health mailbox and read-only/no-approval defaults"
  - "P1: append-only work-context ledger feeding incremental feedback evaluator"
  - "P1: source-anchored derived overlays"
  - "P2: server-owned singleton jobs and atomic derived artifact writes"
  - "P2: progress dimensions as usefulness diagnostics, not truth"
  - "P3: local-first desktop packaging and learning workbench UX"
avoid:
  - "Do not promote this overlay into reviewed knowledge."
  - "Do not make mastery/progress score into VAKS truth confidence."
  - "Do not let schema-valid JSON, job success, or repair success count as evidence support."
  - "Do not use Get It's generated-code sandbox posture as VAKS agent safety approval."
  - "Do not hardcode Codex CLI as the only VAKS agent gateway."
tags:
  - VAKS
  - project-overlay
  - get-it
  - strong-borrow
  - source-intake
  - source-quality-gate
  - source-anchored-overlays
  - typed-agent-gateway
  - agent-health-mailbox
  - feedback-ledger
  - local-first-workbench
  - progress-not-truth
  - candidate-only
---

# VAKS Project Overlay: Get It.

## Boundary

This is a project-scoped sidecar.

It does not rewrite the source card, candidate distillation, reviewed note, decision, or pattern.

It can guide the active project, but it cannot act as reviewed knowledge or action basis.

## Target

```yaml
target_ref: raw/repos/2026-06-06-beltromatti-get-it-source.md
target_selector: checked_commit:4ce88a2c0a242206d96bcd7221bdeda1efcba41c
target_hint: source-intake / typed-agent-gateway / feedback-ledger / local-workbench
```

## 标签等级

```yaml
tagging_decision: tagged
tag_level: strong-borrow
borrow_value: strong
```

人话：

```text
有帮助，而且是强帮助。
但强的是工作流和边界，不是事实真值。
```

## Project Borrow Scope

VAKS 当前值得强借：

1. **先过 source gate 再跑 agent**：先确定材料能不能处理，再启动模型、摘要、抽取、蒸馏。
2. **候选 overlay 要贴回 source anchor**：tag / visual / candidate hint 不能漂成无出处解释。
3. **derived jobs 由服务端拥有状态**：浏览器只是看状态，不让 tab 临时记忆成为事实来源。
4. **typed agent gateway**：统一 agent wrapper、schema output、read-only/no-approval 默认值、health mailbox。
5. **agent health 单独记录**：auth lost、rate limit、binary missing、generic error 不要混进 knowledge status。
6. **Use Ledger / Feedback Ledger**：互动进入 append-only journal，evaluator 读 journal，输出 derived diagnostic。
7. **增量 evaluator cursor**：只看新交互，减少重复计算，但 raw trace 保留。

## Project Non-Borrow Scope

VAKS 当前不要误借：

- 不要把 mastery score 当 truth confidence。
- 不要把 monotone non-decreasing score 套到 reviewed knowledge。
- 不要把 schema-valid JSON 当 true claim。
- 不要把 generated-code repair / `new Function` shadowing 当安全沙箱。
- 不要把 Codex CLI 写死成 VAKS 唯一 agent gateway。
- 不要把完整 PDF 学习 App / mastery graph 塞进 VAKS core。

## Reopen Trigger

重新打开这条 overlay 的条件：

- VAKS 要做 source-type gate。
- VAKS 要做 agent gateway / query-run health mailbox。
- VAKS 要做 feedback-event / use-ledger evaluator。
- VAKS 要做 local workbench 的 derived artifact jobs。
- VAKS 要允许模型生成代码、脚本或可执行产物。

## Confirmation

```yaml
confirmation_basis:
  - user_requested: "继续"
  - checked_commit: 4ce88a2c0a242206d96bcd7221bdeda1efcba41c
  - current_github_main_checked: 2026-06-07
  - current_github_main_matches_snapshot: true
  - artifact_paths:
      - raw/repos/2026-06-06-beltromatti-get-it-source.md
      - outputs/review/2026-06-06-beltromatti-get-it-candidate-distillation.md
      - wiki/summaries/2026-06-06-beltromatti-get-it-architecture-review.md
      - outputs/review/project_overlays/VAKS-get-it-2026-06-07.md
      - raw/repos/_snapshots/beltromatti-get-it-4ce88a2c0a242206d96bcd7221bdeda1efcba41c.zip
  - runtime_executed: false
last_checked_at: 2026-06-07
expires_at: 2026-07-07
```

## 人话结论

打标签，等级是 `strong-borrow`。

最值得 VAKS 记住的是：

```text
先看材料能不能处理，再让 agent 工作。
agent 输出要 schema 化，但 schema 不是事实。
所有 derived artifact 要有状态、能重跑、能解释。
用户怎么用资料，要进 Use Ledger。
进度分数不是事实置信度。
```

## Forbidden

```text
decision outcome
review verdict
truth confidence
action basis
implementation decision
mandatory Codex transport
```

