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
source_distillation: outputs/review/2026-06-06-x-zaimiri-hermes-obsidian-vault-ai-brain-candidate-distillation.md
source_card: raw/articles/2026-06-06-x-zaimiri-hermes-obsidian-vault-ai-brain-source.md
truth_boundary: "Project overlay only; not truth; not ADR; not action basis; not reviewed knowledge."
tags:
  - project-overlay
  - project-vaks
  - hermes
  - obsidian
  - agent-access
  - candidate-only
---

# VAKS Project Overlay: Zaimiri Hermes + Obsidian Agent Vault X Article

## Boundary

This is a project-scoped borrowing list for VAKS.

It does not rewrite the source card, generic candidate points, or any reviewed
knowledge node. It only records how VAKS may temporarily read this source.

## Entries

### file-first-agent-workbench

- kp_ref: outputs/review/candidate_pattern_bank/file-first-agent-workbench.md
- stance: partial
- project_borrow_scope: Keep agent context, workflow instructions, outputs, and receipts visible as Markdown or other readable files.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not treat file visibility as review, truth, safety, or permission to automate writes.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - DEV_CONTEXT.md
  - MEMORY_TIER.md
  - outputs/review
  - future agent workbench
- updated_at: 2026-06-06

### path-scoped-agent-output-writes

- kp_ref: wiki/patterns/path-scoped-agent-output-writes.md
- stance: partial
- project_borrow_scope: Start agent writes in a narrow output zone before allowing direct edits to project folders or durable notes.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not give broad write access to `wiki/`, decisions, schema, templates, or reviewed knowledge from this source.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - outputs/review
  - outputs/qa
  - future agent access rules
- updated_at: 2026-06-06

### agent-tool-access-tiering

- kp_ref: wiki/patterns/agent-tool-access-tiering.md
- stance: watch
- project_borrow_scope: Use read / suggest / write / approve separation when thinking about Hermes-like vault tools.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not treat a prompt instruction, MCP registration, or cron schedule as sufficient permission control.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - future agent access rules
  - SOURCE_INTAKE.md
  - REFERENCE_REVIEW_PROTOCOL.md
- updated_at: 2026-06-06

### skills-and-prompts-as-visible-files

- kp_ref: outputs/review/candidate_pattern_bank/skills-and-prompts-as-visible-files.md
- stance: partial
- project_borrow_scope: Treat Hermes skills and scheduled prompts as explicit workflow files with process steps, quality bars, and output paths.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: A skill file is not reviewed knowledge and should not self-approve its own changes.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - templates
  - future Codex / Hermes skills
  - outputs/review
- updated_at: 2026-06-06

### claude-md-index-md-navigation-layer

- kp_ref: wiki/patterns/claude-md-index-md-navigation-layer.md
- stance: partial
- project_borrow_scope: Use a short read-first steering file to orient agents to vault rules, active priorities, and review boundaries.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: A stale steering file can mislead; it routes context but does not become truth or action basis.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - AGENTS.md
  - 00_handoff
  - wiki/indexes
  - future Obsidian workbench
- updated_at: 2026-06-06

### memory-granularity-and-quarantine

- kp_ref: outputs/review/candidate_pattern_bank/memory-granularity-and-quarantine.md
- stance: partial
- project_borrow_scope: Keep agent-generated briefs, inbox proposals, project health reports, and research conversions quarantined until reviewed.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not let clean Markdown output, repeated cron success, or user convenience promote content into reviewed truth.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - MEMORY_TIER.md
  - FEEDBACK.md
  - REVIEW_QUEUE.md
- updated_at: 2026-06-06

### operational-session-capture-loop

- kp_ref: wiki/patterns/operational-session-capture-loop.md
- stance: watch
- project_borrow_scope: Read scheduled briefs, inbox proposals, project health reports, and weekly syntheses as possible operational receipts.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Scheduled receipts are not facts, decisions, reviewed relations, or action readiness.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - DEV_CONTEXT.md
  - FEEDBACK.md
  - outputs/feedback
- updated_at: 2026-06-06

### retrieval-is-activation-not-truth

- kp_ref: outputs/review/candidate_pattern_bank/retrieval-is-activation-not-truth.md
- stance: partial
- project_borrow_scope: Treat source-path references and vault reads as activation/provenance surfaces that help humans inspect outputs.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: A referenced note path is not point-specific evidence support unless later reviewed against the claim.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - MEMORY_TIER.md
  - DEV_CONTEXT.md
  - REFERENCE_REVIEW_PROTOCOL.md
- updated_at: 2026-06-06

## Closeout Note

No entry here is action-ready.

If any entry is later used for a decision, architecture absorption, action
basis, Hermes setup, automation, agent write access, or risk-sensitive answer,
stop and run the v0.2.13 late-stage review:

```text
claim + anchored evidence + non-circular warrant + scope + gaps + residual risk
```
