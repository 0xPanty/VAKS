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
source_distillation: outputs/review/2026-06-06-x-cyrilxbt-obsidian-from-scratch-candidate-distillation.md
source_card: raw/articles/2026-06-06-x-cyrilxbt-obsidian-from-scratch-source.md
truth_boundary: "Project overlay only; not truth; not ADR; not action basis; not reviewed knowledge."
tags:
  - project-overlay
  - project-vaks
  - obsidian
  - simple-setup
  - capture-workflow
  - candidate-only
---

# VAKS Project Overlay: CyrilXBT Obsidian From Scratch

## Boundary

This is a project-scoped borrowing list for VAKS.

## Entries

### simple-first-retrieval-baseline

- kp_ref: outputs/review/candidate_pattern_bank/simple-first-retrieval-baseline.md
- stance: partial
- project_borrow_scope: Prefer minimum viable structure and add complexity only after real friction appears.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not adopt the article's folder structure or plugin list as VAKS schema.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - SOURCE_INTAKE.md
  - MEMORY_TIER.md
  - future Obsidian workbench
- updated_at: 2026-06-06

### archive-first-lazy-reactivation

- kp_ref: wiki/patterns/archive-first-lazy-reactivation.md
- stance: partial
- project_borrow_scope: Use weekly review and random note reactivation as lightweight ways to resurface older context.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Reactivation does not create support, confidence, or reviewed relation.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - MEMORY_TIER.md
  - DEV_CONTEXT.md
  - SOURCE_INTAKE.md
- updated_at: 2026-06-06

### retrieval-is-activation-not-truth

- kp_ref: outputs/review/candidate_pattern_bank/retrieval-is-activation-not-truth.md
- stance: partial
- project_borrow_scope: Treat links, related fields, note names, and graph visibility as retrieval and activation aids.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not let links, graph position, or names become evidence support or action basis.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - MEMORY_TIER.md
  - DEV_CONTEXT.md
  - REFERENCE_REVIEW_PROTOCOL.md
- updated_at: 2026-06-06

### memory-granularity-and-quarantine

- kp_ref: outputs/review/candidate_pattern_bank/memory-granularity-and-quarantine.md
- stance: watch
- project_borrow_scope: Preserve different handling for Inbox captures, developed notes, active projects, resources, and daily operational notes.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not treat all note types as equal truth or equal activation priority.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - MEMORY_TIER.md
  - SOURCE_INTAKE.md
  - REVIEW_QUEUE.md
- updated_at: 2026-06-06

### operational-session-capture-loop

- kp_ref: wiki/patterns/operational-session-capture-loop.md
- stance: watch
- project_borrow_scope: Daily notes and weekly reviews can act as operational receipts for what happened and what needs reactivation.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Operational receipts are not reviewed knowledge or decisions.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - DEV_CONTEXT.md
  - FEEDBACK.md
  - outputs/feedback
- updated_at: 2026-06-06

## Closeout Note

No entry here is action-ready. Any use for architecture absorption, action
basis, template adoption, or plugin adoption must run the v0.2.13 late-stage
review.
