---
type: project_overlay_note
status: candidate_sidecar
record_kind: project_overlay
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: confirmed
review_pressure: none
overlay_scope: project_sidecar_only
retrieval_policy: project_context_only
overlay_storage: confirmed_persistent_project_bucket
retrieval_scope: active_project_only
default_retrieval: false
archive_policy: exclude_from_default_retrieval_when_project_closed
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
mount_basis: active_project_intake_context
project_id: VAKS
created_at: 2026-06-06
source_distillation: outputs/review/2026-06-06-x-cyrilxbt-obsidian-hermes-life-system-candidate-distillation.md
source_card: raw/articles/2026-06-06-x-cyrilxbt-obsidian-hermes-life-system-source.md
truth_boundary: "Project overlay only; not truth; not ADR; not action basis; not reviewed knowledge."
tags:
  - project-overlay
  - project-vaks
  - obsidian
  - hermes
  - agent-access
  - scheduled-automation
  - candidate-only
---

# VAKS Project Overlay: CyrilXBT Obsidian + Hermes Life System

## Boundary

This is a project-scoped borrowing list for VAKS.

It does not rewrite the source card, generic candidate points, or reviewed
knowledge. It only records how VAKS may temporarily read this source.

## Entries

### file-first-agent-workbench

- kp_ref: outputs/review/candidate_pattern_bank/file-first-agent-workbench.md
- stance: partial
- project_borrow_scope: Treat Obsidian Markdown files, CLAUDE.md, skill docs, output notes, reports, and summaries as visible workbench artifacts.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: File visibility is not truth, safety, or permission to automate writes.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - DEV_CONTEXT.md
  - outputs/review
  - future agent workbench
- updated_at: 2026-06-06

### path-scoped-agent-output-writes

- kp_ref: wiki/patterns/path-scoped-agent-output-writes.md
- stance: partial
- project_borrow_scope: Use a dedicated agent-output folder for scheduled briefs, analyses, syntheses, and reviews.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not let Hermes or any agent write directly to formal wiki, schema, templates, decisions, or reviewed nodes.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - outputs/review
  - outputs/qa
  - future agent output zone
- updated_at: 2026-06-06

### agent-tool-access-tiering

- kp_ref: wiki/patterns/agent-tool-access-tiering.md
- stance: watch
- project_borrow_scope: Treat Filesystem MCP, scheduler, inbox processor, research converter, and CLAUDE.md update steps as access-tier design inputs.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not grant broad read/write/delete/schedule authority from this article.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - future agent access rules
  - SOURCE_INTAKE.md
  - REFERENCE_REVIEW_PROTOCOL.md
- updated_at: 2026-06-06

### skills-and-prompts-as-visible-files

- kp_ref: outputs/review/candidate_pattern_bank/skills-and-prompts-as-visible-files.md
- stance: partial
- project_borrow_scope: Use the seven skill descriptions as examples of explicit process, trigger, output path, and quality-standard documentation.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Skill text is not reviewed policy, implementation proof, or permission to run automation.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - templates
  - future Codex / Hermes skills
  - outputs/review
- updated_at: 2026-06-06

### memory-granularity-and-quarantine

- kp_ref: outputs/review/candidate_pattern_bank/memory-granularity-and-quarantine.md
- stance: partial
- project_borrow_scope: Keep Hermes memory, vault notes, agent outputs, daily notes, project reports, connection reports, and research conversions in separate grains.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not let generated outputs compound into reviewed truth without tagging, quarantine, and review.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - MEMORY_TIER.md
  - FEEDBACK.md
  - REVIEW_QUEUE.md
- updated_at: 2026-06-06

### retrieval-is-activation-not-truth

- kp_ref: outputs/review/candidate_pattern_bank/retrieval-is-activation-not-truth.md
- stance: partial
- project_borrow_scope: Treat connection finder, vault search, project health reports, and thinking-partner tensions as activation or review-pressure surfaces.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not let search hits, connection labels, or diagnostic reports become support, confidence, reviewed relations, or action basis.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - MEMORY_TIER.md
  - DEV_CONTEXT.md
  - REFERENCE_REVIEW_PROTOCOL.md
- updated_at: 2026-06-06

### source-structure-first-rag

- kp_ref: outputs/review/candidate_pattern_bank/source-structure-first-rag.md
- stance: watch
- project_borrow_scope: Research-to-notes conversion can inspire candidate literature-note extraction with source metadata and reaction fields.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: A generated literature note is not reviewed knowledge or promotion.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - SOURCE_INTAKE.md
  - raw/articles
  - outputs/review
- updated_at: 2026-06-06

### operational-session-capture-loop

- kp_ref: wiki/patterns/operational-session-capture-loop.md
- stance: watch
- project_borrow_scope: Read morning briefs, weekly synthesis, project health reports, and thinking-partner sessions as operational receipts.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Operational receipts are not decisions, reviewed relations, truth updates, or action readiness.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - DEV_CONTEXT.md
  - FEEDBACK.md
  - outputs/feedback
- updated_at: 2026-06-06

### claude-md-index-md-navigation-layer

- kp_ref: wiki/patterns/claude-md-index-md-navigation-layer.md
- stance: partial
- project_borrow_scope: Read-first CLAUDE.md can orient skills to priorities, project status, vault structure, and output rules.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not auto-update steering files without human review.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - AGENTS.md
  - 00_handoff
  - wiki/indexes
- updated_at: 2026-06-06

## Closeout Note

No entry here is action-ready.

If any entry is later used for a decision, architecture absorption, Hermes
setup, Filesystem MCP access, scheduled automation, direct note writes,
CLAUDE.md updates, or action basis, stop and run the v0.2.13 late-stage review:

```text
claim + anchored evidence + non-circular warrant + scope + gaps + residual risk
```
