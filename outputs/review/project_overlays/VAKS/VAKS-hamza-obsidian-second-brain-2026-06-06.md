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
source_distillation: outputs/review/2026-06-06-x-hamza-obsidian-second-brain-candidate-distillation.md
source_card: raw/articles/2026-06-06-x-hamza-obsidian-second-brain-source.md
truth_boundary: "Project overlay only; not truth; not ADR; not action basis; not reviewed knowledge."
tags:
  - project-overlay
  - project-vaks
  - obsidian
  - candidate-only
---

# VAKS Project Overlay: Hamza Obsidian Second Brain X Article

## Boundary

This is a project-scoped borrowing list for VAKS.

It does not rewrite the source card, generic candidate points, or any reviewed
knowledge node. It only records how VAKS may temporarily read this source.

## Entries

### retrieval-is-activation-not-truth

- kp_ref: outputs/review/candidate_pattern_bank/retrieval-is-activation-not-truth.md
- stance: partial
- project_borrow_scope: Treat Obsidian links, backlinks, graph view, search, and tags as activation surfaces that help resurface possible context.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not let links, graph position, tag presence, or search hits become support, confidence, reviewed relations, or action basis.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - MEMORY_TIER.md
  - DEV_CONTEXT.md
  - ARCHITECTURE_PRINCIPLES.md
- updated_at: 2026-06-06

### file-first-agent-workbench

- kp_ref: outputs/review/candidate_pattern_bank/file-first-agent-workbench.md
- stance: partial
- project_borrow_scope: Keep source text, candidate distillation, prompts, templates, and handoffs visible as files.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: File visibility is not review, adoption, or permission to automate writes.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - raw/articles
  - outputs/review
  - templates
- updated_at: 2026-06-06

### skills-and-prompts-as-visible-files

- kp_ref: outputs/review/candidate_pattern_bank/skills-and-prompts-as-visible-files.md
- stance: watch
- project_borrow_scope: Use the prompt pack as a reminder that AI note processors should be explicit, file-visible, and easy to audit.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not treat Claude prompt output as reviewed knowledge or automatic vault write authority.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - templates
  - outputs/review
  - future Codex skill design
- updated_at: 2026-06-06

### visual-workbench-for-retrieval-diagnostics

- kp_ref: outputs/review/candidate_pattern_bank/visual-workbench-for-retrieval-diagnostics.md
- stance: defer
- project_borrow_scope: Revisit graph, backlink, and dashboard ideas when VAKS needs a human-facing context or review workbench.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not add dashboard authority, graph truth, or visual readiness scores to the truth layer.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - future Obsidian workbench
  - templates/maintenance-manifest.md
- updated_at: 2026-06-06

### archive-first-lazy-reactivation

- kp_ref: wiki/patterns/archive-first-lazy-reactivation.md
- stance: partial
- project_borrow_scope: Use inbox review and archive/cooling ideas to keep capture light while preventing permanent clutter.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not turn Inbox/Notes/Projects/Archive into VAKS truth schema or required root folders.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - SOURCE_INTAKE.md
  - MEMORY_TIER.md
  - DEV_CONTEXT.md
- updated_at: 2026-06-06

## Closeout Note

No entry here is action-ready.

If any entry is later used for a decision, architecture absorption, action
basis, or risk-sensitive answer, stop and run the v0.2.13 late-stage review:

```text
claim + anchored evidence + non-circular warrant + scope + gaps + residual risk
```
