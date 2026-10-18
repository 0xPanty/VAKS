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
source_distillation: outputs/review/2026-06-06-x-damidefi-obsidian-claude-research-stack-candidate-distillation.md
source_card: raw/articles/2026-06-06-x-damidefi-obsidian-claude-research-stack-source.md
truth_boundary: "Project overlay only; not truth; not ADR; not action basis; not reviewed knowledge."
tags:
  - project-overlay
  - project-vaks
  - obsidian
  - claude
  - research-stack
  - capture-workflow
  - candidate-only
---

# VAKS Project Overlay: Dami-Defi Obsidian + Claude Research Stack

## Boundary

This is a project-scoped borrowing list for VAKS.

It does not rewrite the source card, generic candidate points, or any reviewed
knowledge node. It only records how VAKS may temporarily read this source.

## Entries

### source-structure-first-rag

- kp_ref: outputs/review/candidate_pattern_bank/source-structure-first-rag.md
- stance: partial
- project_borrow_scope: Use consistent source-note structure to help later candidate extraction, synthesis, contradiction routing, and source comparison.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: A filled source template is not reviewed knowledge, evidence support, or action readiness.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - SOURCE_INTAKE.md
  - raw/articles
  - raw/videos
  - outputs/review
- updated_at: 2026-06-06

### retrieval-is-activation-not-truth

- kp_ref: outputs/review/candidate_pattern_bank/retrieval-is-activation-not-truth.md
- stance: partial
- project_borrow_scope: Treat source-template connection fields and weekly synthesis connections as activation candidates for human review.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not let connection suggestions, semantic matches, or Claude Project context become reviewed relations, support, confidence, or action basis.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - MEMORY_TIER.md
  - DEV_CONTEXT.md
  - REFERENCE_REVIEW_PROTOCOL.md
- updated_at: 2026-06-06

### file-first-agent-workbench

- kp_ref: outputs/review/candidate_pattern_bank/file-first-agent-workbench.md
- stance: partial
- project_borrow_scope: Read the single-vault research setup as support for visible source, idea, project, output, prompt, and session-log artifacts.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: One environment is a workbench convenience, not truth, safety, or adoption proof.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - raw/articles
  - outputs/review
  - DEV_CONTEXT.md
  - future agent workbench
- updated_at: 2026-06-06

### memory-granularity-and-quarantine

- kp_ref: outputs/review/candidate_pattern_bank/memory-granularity-and-quarantine.md
- stance: partial
- project_borrow_scope: Preserve the distinction between Inbox captures, Source notes, Ideas, Projects, Outputs, and Claude support files as different memory/workflow grains.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not let Inbox items, AI-processed source notes, weekly syntheses, or output drafts enter reviewed truth without review.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - MEMORY_TIER.md
  - SOURCE_INTAKE.md
  - REVIEW_QUEUE.md
- updated_at: 2026-06-06

### skills-and-prompts-as-visible-files

- kp_ref: outputs/review/candidate_pattern_bank/skills-and-prompts-as-visible-files.md
- stance: partial
- project_borrow_scope: Treat the source template and weekly synthesis prompt as visible workflow instructions that can be tested and revised.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not make prompt output authoritative or let a prompt template approve its own results.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - templates
  - outputs/review
  - future Codex / Claude skills
- updated_at: 2026-06-06

### simple-first-retrieval-baseline

- kp_ref: outputs/review/candidate_pattern_bank/simple-first-retrieval-baseline.md
- stance: partial
- project_borrow_scope: Prefer simple capture and manual weekly synthesis testing before adding automation.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not add bots, sync plugins, n8n/Zapier/Make automation, or Claude Project setup just because the source mentions them.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - SOURCE_INTAKE.md
  - DEV_CONTEXT.md
  - future automation policy
- updated_at: 2026-06-06

### operational-session-capture-loop

- kp_ref: wiki/patterns/operational-session-capture-loop.md
- stance: watch
- project_borrow_scope: Read weekly synthesis, highest-value source selection, and output notes as possible operational receipts for later review.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Weekly synthesis is not a decision, reviewed relation, resolved contradiction, or action basis.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - DEV_CONTEXT.md
  - FEEDBACK.md
  - outputs/feedback
- updated_at: 2026-06-06

### claude-md-index-md-navigation-layer

- kp_ref: wiki/patterns/claude-md-index-md-navigation-layer.md
- stance: watch
- project_borrow_scope: Treat CLAUDE.md and project/source seed notes as context-routing aids for reducing fresh-start tax.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Claude Project context is not truth authority and should not receive broad access by default.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - AGENTS.md
  - 00_handoff
  - wiki/indexes
  - future Obsidian workbench
- updated_at: 2026-06-06

### agent-tool-access-tiering

- kp_ref: wiki/patterns/agent-tool-access-tiering.md
- stance: watch
- project_borrow_scope: Treat Readwise, Telegram bot, Zapier, Make, n8n, and Claude Projects as possible capture/context tools that need explicit access boundaries.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Capture adapters are not review layers, truth layers, or permission to automate writes.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - future agent access rules
  - SOURCE_INTAKE.md
  - REFERENCE_REVIEW_PROTOCOL.md
- updated_at: 2026-06-06

## Closeout Note

No entry here is action-ready.

If any entry is later used for a decision, architecture absorption, action
basis, capture automation, source-template adoption, Claude Project setup, or
risk-sensitive answer, stop and run the v0.2.13 late-stage review:

```text
claim + anchored evidence + non-circular warrant + scope + gaps + residual risk
```
