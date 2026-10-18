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
source_distillation: outputs/review/2026-06-06-x-cyrilxbt-claude-obsidian-90-days-candidate-distillation.md
source_card: raw/articles/2026-06-06-x-cyrilxbt-claude-obsidian-90-days-source.md
truth_boundary: "Project overlay only; not truth; not ADR; not action basis; not reviewed knowledge."
tags:
  - project-overlay
  - project-vaks
  - claude
  - obsidian
  - longitudinal-retrospective
  - candidate-only
---

# VAKS Project Overlay: CyrilXBT Claude + Obsidian 90-Day Retrospective

## Boundary

This is a project-scoped borrowing list for VAKS.

It does not rewrite the source card, generic candidate points, or any reviewed
knowledge node. It only records how VAKS may temporarily read this source.

## Entries

### retrieval-is-activation-not-truth

- kp_ref: outputs/review/candidate_pattern_bank/retrieval-is-activation-not-truth.md
- stance: partial
- project_borrow_scope: Treat Claude-surfaced forgotten notes and connection suggestions as activation candidates that help humans inspect relevant context.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not let surfaced notes, semantic matches, or connection-finder output become evidence support, reviewed relations, confidence, or action basis.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - MEMORY_TIER.md
  - DEV_CONTEXT.md
  - REFERENCE_REVIEW_PROTOCOL.md
- updated_at: 2026-06-06

### claude-md-index-md-navigation-layer

- kp_ref: wiki/patterns/claude-md-index-md-navigation-layer.md
- stance: partial
- project_borrow_scope: Keep a short, specific, frequently refreshed steering file for active priorities, project status, next actions, voice, and review boundaries.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not treat CLAUDE.md / AGENTS.md / handoff text as truth authority or permission to act without review.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - AGENTS.md
  - 00_handoff
  - wiki/indexes
  - future Obsidian workbench
- updated_at: 2026-06-06

### operational-session-capture-loop

- kp_ref: wiki/patterns/operational-session-capture-loop.md
- stance: watch
- project_borrow_scope: Read morning briefs, weekly reviews, project health reports, and decision logs as operational receipts that may reveal patterns over time.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Operational receipts are not facts, decisions, reviewed relations, truth updates, or action readiness.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - DEV_CONTEXT.md
  - FEEDBACK.md
  - outputs/feedback
- updated_at: 2026-06-06

### memory-granularity-and-quarantine

- kp_ref: outputs/review/candidate_pattern_bank/memory-granularity-and-quarantine.md
- stance: partial
- project_borrow_scope: Keep generated briefs, health reports, meeting note drafts, writing briefs, and weekly reviews quarantined until reviewed or manually accepted.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not let repeated generation, clean formatting, or apparent usefulness promote content into reviewed truth.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - MEMORY_TIER.md
  - FEEDBACK.md
  - REVIEW_QUEUE.md
- updated_at: 2026-06-06

### file-first-agent-workbench

- kp_ref: outputs/review/candidate_pattern_bank/file-first-agent-workbench.md
- stance: partial
- project_borrow_scope: Use visible Markdown briefs, reviews, and steering files as inspectable workbench artifacts.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: File visibility is not review, safety, adoption, or evidence support.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - DEV_CONTEXT.md
  - outputs/review
  - outputs/feedback
  - future agent workbench
- updated_at: 2026-06-06

### skills-and-prompts-as-visible-files

- kp_ref: outputs/review/candidate_pattern_bank/skills-and-prompts-as-visible-files.md
- stance: partial
- project_borrow_scope: Treat the five core workflow prompts as examples of small visible skills that can be tested before scheduling.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not adopt the five workflows as mandatory VAKS automation or let skills self-approve output.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - templates
  - future Codex / Claude / Hermes skills
  - outputs/review
- updated_at: 2026-06-06

### simple-first-retrieval-baseline

- kp_ref: outputs/review/candidate_pattern_bank/simple-first-retrieval-baseline.md
- stance: partial
- project_borrow_scope: Keep scheduled workflows few and valuable enough that humans actually read the outputs.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not add scheduled synthesis, dashboards, or connection reports just because the tool can generate them.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - MEMORY_TIER.md
  - DEV_CONTEXT.md
  - future automation policy
- updated_at: 2026-06-06

### agent-tool-access-tiering

- kp_ref: wiki/patterns/agent-tool-access-tiering.md
- stance: watch
- project_borrow_scope: Treat broad vault read access as an explicit access-boundary decision, especially for sensitive notes or production vaults.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not infer broad write, delete, schedule, or sensitive-data access from this self-report.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - future agent access rules
  - SOURCE_INTAKE.md
  - REFERENCE_REVIEW_PROTOCOL.md
- updated_at: 2026-06-06

## Closeout Note

No entry here is action-ready.

If any entry is later used for a decision, architecture absorption, action
basis, Claude/MCP setup, automation, agent write access, or risk-sensitive
answer, stop and run the v0.2.13 late-stage review:

```text
claim + anchored evidence + non-circular warrant + scope + gaps + residual risk
```
