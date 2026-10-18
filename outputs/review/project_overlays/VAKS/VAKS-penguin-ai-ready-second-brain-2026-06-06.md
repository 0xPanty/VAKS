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
source_distillation: outputs/review/2026-06-06-x-penguin-ai-ready-second-brain-candidate-distillation.md
source_card: raw/articles/2026-06-06-x-penguin-ai-ready-second-brain-source.md
truth_boundary: "Project overlay only; not truth; not ADR; not action basis; not reviewed knowledge."
tags:
  - project-overlay
  - project-vaks
  - obsidian
  - ai-context
  - second-brain
  - candidate-only
---

# VAKS Project Overlay: Penguin AI-Ready Second Brain

## Boundary

This is a project-scoped borrowing list for VAKS.

It does not rewrite the source card, generic candidate points, or reviewed
knowledge. It only records how VAKS may temporarily read this source.

## Entries

### retrieval-is-activation-not-truth

- kp_ref: outputs/review/candidate_pattern_bank/retrieval-is-activation-not-truth.md
- stance: partial
- project_borrow_scope: Treat AI-readable patterns, repeated ideas, related notes, and context prompts as activation surfaces.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not let pattern detection, related-note lists, or AI memory become support, confidence, reviewed relations, or action basis.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - MEMORY_TIER.md
  - DEV_CONTEXT.md
  - REFERENCE_REVIEW_PROTOCOL.md
- updated_at: 2026-06-06

### memory-granularity-and-quarantine

- kp_ref: outputs/review/candidate_pattern_bank/memory-granularity-and-quarantine.md
- stance: partial
- project_borrow_scope: Keep decisions, mistakes, prompts, workflows, personal rules, examples, and repeated patterns as distinct context grains.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not treat context grain labels as truth categories or reviewed knowledge.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - MEMORY_TIER.md
  - FEEDBACK.md
  - REVIEW_QUEUE.md
- updated_at: 2026-06-06

### skills-and-prompts-as-visible-files

- kp_ref: outputs/review/candidate_pattern_bank/skills-and-prompts-as-visible-files.md
- stance: watch
- project_borrow_scope: Use context prompts as visible workflow candidates for repeated pattern, contradiction, project-next-step, and missing-knowledge scans.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Prompt output is not reviewed workflow, decision, or knowledge.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - templates
  - future Codex / Claude skills
  - outputs/review
- updated_at: 2026-06-06

### claude-md-index-md-navigation-layer

- kp_ref: wiki/patterns/claude-md-index-md-navigation-layer.md
- stance: watch
- project_borrow_scope: Treat identity, goals, style, constraints, history, and taste as context that can reduce repeated re-explanation.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Steering context does not authorize actions or prove facts.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - AGENTS.md
  - 00_handoff
  - wiki/indexes
- updated_at: 2026-06-06

### operational-session-capture-loop

- kp_ref: wiki/patterns/operational-session-capture-loop.md
- stance: watch
- project_borrow_scope: Weekly loops can surface repeated patterns, mistakes, unanswered questions, and candidate next actions.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Operational loop output is review pressure, not reviewed decision or action readiness.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - DEV_CONTEXT.md
  - FEEDBACK.md
  - outputs/feedback
- updated_at: 2026-06-06

### archive-first-lazy-reactivation

- kp_ref: wiki/patterns/archive-first-lazy-reactivation.md
- stance: partial
- project_borrow_scope: Archive low-value noise out of active context while preserving the option to reactivate later.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Archive is not deletion, evidence rejection, or truth confidence change.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - MEMORY_TIER.md
  - SOURCE_INTAKE.md
  - DEV_CONTEXT.md
- updated_at: 2026-06-06

### simple-first-retrieval-baseline

- kp_ref: outputs/review/candidate_pattern_bank/simple-first-retrieval-baseline.md
- stance: partial
- project_borrow_scope: Keep the weekly loop simple: capture, route, link obvious relations, ask for patterns, convert useful patterns into candidates.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not turn the article's folder list or prompt list into a mandatory workflow.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - MEMORY_TIER.md
  - DEV_CONTEXT.md
  - future Obsidian workbench
- updated_at: 2026-06-06

## Closeout Note

No entry here is action-ready.

If any entry is later used for a decision, architecture absorption, template
adoption, automation, archive policy, or action basis, stop and run the v0.2.13
late-stage review:

```text
claim + anchored evidence + non-circular warrant + scope + gaps + residual risk
```
