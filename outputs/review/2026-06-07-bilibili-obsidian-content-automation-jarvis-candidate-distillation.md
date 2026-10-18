---
record_kind: candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: review_due
derived_from:
  - raw/videos/2026-06-07-bilibili-obsidian-content-automation-jarvis-source.md
  - raw/videos/2026-06-07-bilibili-obsidian-content-automation-jarvis-source/transcript.txt
  - raw/videos/2026-06-07-bilibili-obsidian-content-automation-jarvis-source/segments.md
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
v0_2_13_trigger: yes
routing_hint:
  - project_overlay
  - workflow_automation
  - feedback_ledger
  - activation_tier
possible_project_refs:
  - verified-action-knowledge-system
point_anchor_refs:
  - raw/videos/2026-06-07-bilibili-obsidian-content-automation-jarvis-source/segments.md#0000-0075
  - raw/videos/2026-06-07-bilibili-obsidian-content-automation-jarvis-source/segments.md#0136-0258
  - raw/videos/2026-06-07-bilibili-obsidian-content-automation-jarvis-source/segments.md#0300-0426
  - raw/videos/2026-06-07-bilibili-obsidian-content-automation-jarvis-source/segments.md#0430-0480
  - raw/videos/2026-06-07-bilibili-obsidian-content-automation-jarvis-source/segments.md#0510-0576
  - raw/videos/2026-06-07-bilibili-obsidian-content-automation-jarvis-source/segments.md#0590-0906
borrow_value: strong
borrow_tags:
  - P1/project_operating_manual_as_ai_entrypoint
  - P1/feedback_to_constraints_not_truth
  - P1/local_markdown_as_executable_context
  - P2/version_control_required_for_ai_file_work
  - P2/publishing_pipeline_as_tool_layer
  - P3/content_creation_preview_workflow
do_not_borrow_tags:
  - avoid/auto_publish_default
  - avoid/feedback_as_truth_confidence
  - avoid/asr_as_reviewed_evidence
  - avoid/project_style_as_global_default
  - avoid/private_account_routes_default
borrow_order:
  - "P1: project operating manual as AI entrypoint"
  - "P1: feedback becomes reusable workflow constraints, not truth"
  - "P2: Git/version control as safety net for AI file edits"
  - "P2: local Markdown-to-publishing connectors as tool layer"
  - "P3: content-creation UI ideas and preview/publish workflow"
avoid:
  - "Do not borrow automatic truth mutation from feedback or ASR."
  - "Do not connect auto-publish or external accounts to VAKS mainline by default."
  - "Do not let project-specific style rules become global skill defaults."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "approved work on VAKS project-local operating manuals, skill routing, or feedback-to-constraint design"
  support_when: "designing ordinary capture, project workbench, activation context, or local-file automation"
  risk_when: "AI file writes, external publishing, version control, or feedback promotion are being discussed"
  cold_references:
    - raw/videos/2026-06-07-bilibili-obsidian-content-automation-jarvis-source.md
tags:
  - candidate
  - provisional
  - video-intake
  - obsidian
  - automation
  - feedback-ledger
  - borrow-p1-project-manual
  - borrow-p1-feedback-constraints
  - borrow-p1-executable-markdown
  - borrow-p2-version-control
  - borrow-p2-tool-layer-publishing
---

# Candidate Distillation: Obsidian Content Automation / Jarvis Workflow

## Boundary

This note is candidate orientation. It can help route VAKS design attention, but it is not reviewed knowledge, not a decision, not a formal pattern, and not action basis.

Transcript source: local ASR with OpenAI Whisper `small` on CUDA. Proper nouns, plugin names, repository names, and commands need visual/source confirmation before operational use.

## Human Summary

The video's automation logic is:

```text
local materials
-> project-specific Markdown structure
-> AI reads the project manual first
-> AI creates work products
-> human feedback marks like/dislike/forbidden
-> feedback is written back as style/workflow constraints
-> version control protects file changes
-> optional publishing connectors push finished content outward
```

The useful lesson for VAKS is not "install more plugins." The useful lesson is that a knowledge base becomes productive when it tells the AI what each folder means, what rules apply, what state the project is in, what has already been tried, what feedback matters, and what must not be touched.

## 借鉴标签

```yaml
borrow_value: strong
P1:
  - project_operating_manual_as_ai_entrypoint
  - feedback_to_constraints_not_truth
  - local_markdown_as_executable_context
P2:
  - version_control_required_for_ai_file_work
  - publishing_pipeline_as_tool_layer
P3:
  - content_creation_preview_workflow
avoid:
  - auto_publish_default
  - feedback_as_truth_confidence
  - asr_as_reviewed_evidence
  - project_style_as_global_default
  - private_account_routes_default
```

人话拆开：

- **P1 / 项目说明书入口**：AI 每次开工先读项目入口文件，知道资料、状态、权限和停手规则。
- **P1 / 反馈变约束**：喜欢、不喜欢、禁止项要写回项目文件，指导下一次，但不能变成 truth。
- **P1 / Markdown 变执行上下文**：本地 Markdown 不只是笔记，还写清楚文件夹用途、工作流和可调用边界。
- **P2 / Git 安全网**：AI 能批量改文件时，必须能回退。
- **P2 / 发布工具层**：公众号、飞书、预览、配图这些可以做工具连接，但不能进 VAKS 主真理层。
- **P3 / 创作工作台体验**：预览、排版、插图密度、风格选择这些 UI 思路以后可参考。

## Automation Logic

1. **Resource capture**

   The project starts from source material such as a PDF, book, article, script, or notes. In the example, a novel source becomes the seed for manga creation.

2. **Structural decomposition**

   AI is asked to create durable Markdown files: character profiles, chapter summaries, scene descriptions, key dialogue, storyboard suggestions, and character state tracking.

3. **Project-local operating manual**

   A README/workflow manual becomes the "central brain" of the project. Every AI session should read it first. It links to required files and records important rules, progress, and constraints.

4. **Project-specific skill**

   Repeated prompts become a dedicated skill/trigger. Saying "create the manga" should cause AI to read the workflow manual, inspect project progress, and run the right sequence.

5. **Feedback loop**

   Human feedback is not left in chat. Liked pages, forbidden styles, bad outputs, and quality standards are written back into reference files. Future runs use them as constraints.

6. **Safety net**

   When AI can edit many files, Git/GitHub style version control is the recovery layer. It protects against accidental deletion, overwrite, and unsatisfactory edits.

7. **Publishing connectors**

   Finished Markdown can be routed into image generation, article formatting, preview tools, WeChat draft publishing, or Feishu document sync. These are downstream tool connectors, not knowledge authority.

## Candidate Points

### candidate: project_operating_manual_as_ai_entrypoint

A project-level operating manual can be treated as the first activation file for AI work. It should explain folder roles, allowed operations, current progress, required references, and stop rules.

VAKS fit: strong. This matches local `AGENTS.md`, handoffs, `DEV_CONTEXT.md`, and skill routing.

### candidate: local_markdown_as_executable_context

Markdown files can describe not only content, but permissions, workflow state, dependencies, style rules, and reusable prompts. This makes the vault a workbench rather than a static archive.

VAKS fit: strong, but only if authority fields remain machine-readable.

### candidate: feedback_to_constraints_not_truth

Human likes/dislikes can become style constraints, usefulness hints, or review pressure. They must not become truth confidence or reviewed knowledge without evidence-aware review.

VAKS fit: strong. This reinforces Feedback Ledger boundaries.

### candidate: version_control_required_for_ai_file_work

When AI can write/delete/move files, version control is not optional. It is the rollback layer for file operations, especially when output assets are expensive or hard to reproduce.

VAKS fit: medium/strong. Use for repo workspace hygiene; do not confuse Git commit with reviewed truth.

### candidate: publishing_pipeline_as_tool_layer

Obsidian-to-WeChat/Feishu style publishing is valuable as a downstream connector. It should sit outside the truth core and require explicit user intent before account/platform actions.

VAKS fit: medium, tool-layer only.

## What VAKS Should Borrow

- Keep project-local entry files as AI operating manuals.
- Let repeated workflows become skills only after their boundaries are clear.
- Convert feedback into next-run constraints and review pressure, not truth mutation.
- Use Git/hash/sync checks for file safety.
- Treat local Markdown as an executable context surface: state, rules, sources, and allowed actions.

## What VAKS Should Not Borrow

- Do not make automatic publishing part of ordinary capture.
- Do not let a project-specific content style become a global VAKS default.
- Do not treat ASR/video claims as reviewed knowledge.
- Do not use external account connections, cookies, private repos, or API keys without explicit authorization.
- Do not let a skill auto-write reviewed claims, decisions, or action basis.

## Risk Notes

- ASR is good enough for the logic, but several proper nouns are unreliable.
- The video is optimized for creative production, not evidence review.
- The creator's "AI learns me" framing maps to VAKS only as activation/feedback, not as truth or confidence.
- Auto-push every few minutes may be convenient for a personal vault, but VAKS should keep sync, commit, push, and reviewed promotion as separate gates.

## Routing Hint

Use this source when working on:

- project-local operating manuals;
- skill routing and trigger boundaries;
- feedback ledger / use ledger;
- activation tier and context pack design;
- local file automation safety;
- publishing/export connectors as optional tool layer.

Do not use this source as direct evidence for factual claims about specific tools, repositories, commands, pricing, or plugin availability without a separate source check.
