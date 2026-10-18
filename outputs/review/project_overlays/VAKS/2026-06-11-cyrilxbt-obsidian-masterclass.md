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
target_ref: outputs/review/2026-06-11-cyrilxbt-obsidian-masterclass-candidate-distillation.md
target_selector: whole-file
target_hint:
  - type: workflow
    value: future-obsidian-user-surface
    status: conceptual
    anchor_version: 2026-06-11-candidate-source
  - type: workflow
    value: daily-source-intake-and-review
    status: conceptual
    anchor_version: 2026-06-11-candidate-source
  - type: doc
    value: AGENTS.md
    status: healthy
    anchor_version: 2026-06-11-file-read
  - type: doc
    value: SOURCE_INTAKE.md
    status: healthy
    anchor_version: 2026-06-11-file-read
project_borrow_scope: "For VAKS, borrow this as a P1 Obsidian usage/workbench reference: root operating manual, daily capture front door, visible candidate compound outputs, manual query prompts, vault audit prompts, and staged onboarding."
project_non_borrow_scope: "For VAKS, do not borrow the exact folder taxonomy, scheduled automation, plugin stack, or whole-vault AI authority as architecture. Do not let Claude summaries, compound notes, links, MOCs, Bases, or audit reports become reviewed knowledge or action basis."
project_reopen_trigger: "Reopen when designing the formal Obsidian HOME, daily note/intake templates, candidate synthesis folder, audit dashboard/Base views, or agent permission model; also reopen if the original URL and stronger source anchors are later captured."
confirmation_basis: "User explicitly requested strong distillation with '强蒸馏' in the VAKS workspace; local AGENTS.md authorizes formal Obsidian target H:\\Obsidian\\资料库."
last_checked_at: "2026-06-11 04:02:34 +08:00"
expires_at:
borrow_value: strong
borrow_order: P1
avoid:
  - exact-folder-taxonomy-adoption
  - scheduled-automation-without-permission-design
  - ai-summary-as-reviewed-knowledge
  - whole-vault-access-as-action-basis
---

# Project Overlay：VAKS 借鉴 CyrilXBT Obsidian Masterclass

## Boundary

This is a project-scoped sidecar.

It does not rewrite the source card, candidate distillation, reviewed note, decision, or pattern.

It can guide the active project, but it cannot act as reviewed knowledge or action basis.

## Target

```yaml
target_ref: outputs/review/2026-06-11-cyrilxbt-obsidian-masterclass-candidate-distillation.md
target_selector: whole-file
target_hint:
  - future-obsidian-user-surface
  - daily-source-intake-and-review
  - AGENTS.md
  - SOURCE_INTAKE.md
```

## Project Borrow Scope

For VAKS, borrow this source as a strong usage/workbench reference:

- 把 root manual / `CLAUDE.md` 思路转成更友好的 Obsidian read-first surface。
- 把 daily note 借鉴成低摩擦 capture front door，而不是 promotion gate。
- 把 AI connection / pattern / synthesis outputs 设计成可见候选文件。
- 把 manual prompts 借鉴成 VAKS query modes。
- 把 vault audit 借鉴成 maintenance lint / dashboard / Base view。
- 把三个月搭建计划借鉴成“先 habit，后 automation”的上线节奏。

## Project Non-Borrow Scope

For VAKS, do not currently borrow:

- 不照抄 00-10 folder taxonomy。VAKS 已有 `raw / wiki / outputs / templates / tools` 项目结构。
- 不把 `YYYY-MM-DD-[TYPE]-[TOPIC]` 变成全局强制命名法。
- 不把 two-link rule、15-note MOC threshold 或插件清单变成 reviewed rule。
- 不启动 6AM / 8PM / 11PM 自动化调度。
- 不让 Claude / Filesystem MCP 获得默认全 vault 写入权。
- 不让 AI compound output、MOC、Base、链接图谱或审计报告成为 truth confidence、review pass、reviewed relation 或 action basis。

## Reopen Trigger

Reopen this overlay when VAKS is actively designing:

- Obsidian HOME / landing page
- daily note or source-intake templates
- candidate synthesis / compound output folder
- query-mode prompt library
- audit dashboard or `.base` views
- Claude/Codex/agent filesystem permission model

Also reopen if the original URL, publication date, and stable source anchors are later captured.

## Confirmation

```yaml
confirmation_basis: explicit user request: 强蒸馏
last_checked_at: "2026-06-11 04:02:34 +08:00"
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
