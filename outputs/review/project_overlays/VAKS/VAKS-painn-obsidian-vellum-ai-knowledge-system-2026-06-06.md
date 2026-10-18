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
source_distillation: outputs/review/2026-06-06-x-painn-obsidian-vellum-ai-knowledge-system-candidate-distillation.md
source_card: raw/articles/2026-06-06-x-painn-obsidian-vellum-ai-knowledge-system-source.md
truth_boundary: "Project overlay only; not truth; not ADR; not action basis; not reviewed knowledge."
tags:
  - project-overlay
  - project-vaks
  - obsidian
  - vellum
  - automation
  - capture-workflow
  - candidate-only
---

# VAKS Project Overlay: painn Obsidian + Vellum AI Knowledge System

## Boundary

This is a project-scoped borrowing list for VAKS.

It does not rewrite the source card, generic candidate points, or reviewed
knowledge. It only records how VAKS may temporarily read this source.

## Entries

### file-first-agent-workbench

- kp_ref: outputs/review/candidate_pattern_bank/file-first-agent-workbench.md
- stance: partial
- project_borrow_scope: Treat Obsidian folders, VELLUM.md, workflow files, connection notes, and brief files as visible workbench artifacts.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: File visibility is not tool safety, truth, or permission to automate.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - DEV_CONTEXT.md
  - outputs/review
  - future agent workbench
- updated_at: 2026-06-06

### source-structure-first-rag

- kp_ref: outputs/review/candidate_pattern_bank/source-structure-first-rag.md
- stance: watch
- project_borrow_scope: Type-based capture folders may be useful as an experiment for cross-domain candidate discovery.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not adopt the folder taxonomy as VAKS schema.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - SOURCE_INTAKE.md
  - raw/articles
  - outputs/review
- updated_at: 2026-06-06

### skills-and-prompts-as-visible-files

- kp_ref: outputs/review/candidate_pattern_bank/skills-and-prompts-as-visible-files.md
- stance: partial
- project_borrow_scope: Treat Vellum workflow prompts as visible operating procedures with explicit trigger, input, output, and quality constraints.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Workflow files are not reviewed procedures or automation approval.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - templates
  - future Codex / Vellum / Claude skills
  - outputs/review
- updated_at: 2026-06-06

### retrieval-is-activation-not-truth

- kp_ref: outputs/review/candidate_pattern_bank/retrieval-is-activation-not-truth.md
- stance: partial
- project_borrow_scope: Treat daily briefs, connection notes, pattern reports, and deep research prompts as activation and review-pressure surfaces.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not let Vellum-found connections, quotes, or patterns become evidence support, reviewed relations, confidence, or action basis.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - MEMORY_TIER.md
  - DEV_CONTEXT.md
  - REFERENCE_REVIEW_PROTOCOL.md
- updated_at: 2026-06-06

### memory-granularity-and-quarantine

- kp_ref: outputs/review/candidate_pattern_bank/memory-granularity-and-quarantine.md
- stance: partial
- project_borrow_scope: Keep raw inbox items, captures, connection notes, project notes, Vellum outputs, and close-loop feedback as separate grains.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not let synthesized connection notes enter reviewed truth without review.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - MEMORY_TIER.md
  - FEEDBACK.md
  - REVIEW_QUEUE.md
- updated_at: 2026-06-06

### operational-session-capture-loop

- kp_ref: wiki/patterns/operational-session-capture-loop.md
- stance: watch
- project_borrow_scope: Use daily ritual, weekly connection session, and monthly close-the-loop prompt as operational receipt ideas.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Operational receipts are not decisions, reviewed relations, truth updates, or action readiness.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - DEV_CONTEXT.md
  - FEEDBACK.md
  - outputs/feedback
- updated_at: 2026-06-06

### agent-tool-access-tiering

- kp_ref: wiki/patterns/agent-tool-access-tiering.md
- stance: watch
- project_borrow_scope: Treat Vellum vault access, Readwise sync, N8N file writes, Telegram bot capture, and Whisper transcripts as access-tier design inputs.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not connect cloud tools or automations to local vault content without separate review.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - future agent access rules
  - SOURCE_INTAKE.md
  - REFERENCE_REVIEW_PROTOCOL.md
- updated_at: 2026-06-06

### path-scoped-agent-output-writes

- kp_ref: wiki/patterns/path-scoped-agent-output-writes.md
- stance: watch
- project_borrow_scope: Put generated briefs and connection notes in bounded output/candidate folders before any writeback.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: A workflow prompt is not permission to move, create, or overwrite vault files.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - outputs/review
  - outputs/qa
  - future automation sandbox
- updated_at: 2026-06-06

### archive-first-lazy-reactivation

- kp_ref: wiki/patterns/archive-first-lazy-reactivation.md
- stance: watch
- project_borrow_scope: Archive old or inactive material out of active context while preserving reactivation paths.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Archive is not deletion, evidence rejection, or truth confidence change.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - MEMORY_TIER.md
  - SOURCE_INTAKE.md
  - DEV_CONTEXT.md
- updated_at: 2026-06-06

## Closeout Note

No entry here is action-ready.

If any entry is later used for a decision, architecture absorption, Vellum
setup, Readwise/N8N/Telegram/Whisper automation, cloud-vault access,
source-template adoption, or action basis, stop and run the v0.2.13 late-stage
review:

```text
claim + anchored evidence + non-circular warrant + scope + gaps + residual risk
```
