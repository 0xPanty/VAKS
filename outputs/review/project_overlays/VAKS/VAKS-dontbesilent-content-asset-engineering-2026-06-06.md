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
source_distillation: outputs/review/2026-06-06-x-dontbesilent-content-asset-engineering-candidate-distillation.md
source_card: raw/articles/2026-06-06-x-dontbesilent-content-asset-engineering-source.md
truth_boundary: "Project overlay only; not truth; not ADR; not action basis; not reviewed knowledge."
tags:
  - project-overlay
  - project-vaks
  - content-engineering
  - agent-workflow
  - obsidian
  - candidate-only
---

# VAKS Project Overlay: dontbesilent 内容资产工程系统

## Boundary

This is a project-scoped borrowing list for VAKS.

It does not rewrite the source card, generic candidate points, or reviewed
knowledge. It only records how VAKS may temporarily read this source.

## Entries

### source-structure-first-rag

- kp_ref: outputs/review/candidate_pattern_bank/source-structure-first-rag.md
- stance: partial
- project_borrow_scope: Use copied raw material, source candidates, original indexes, and structured extraction before asking agents to synthesize large content archives.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not treat extracted units as reviewed knowledge or replace source provenance with summaries.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - SOURCE_INTAKE.md
  - raw/articles
  - raw/videos
  - outputs/review
- updated_at: 2026-06-06

### file-first-agent-workbench

- kp_ref: outputs/review/candidate_pattern_bank/file-first-agent-workbench.md
- stance: partial
- project_borrow_scope: Treat rules, state, templates, scripts, unit libraries, topic maps, assembly drafts, indexes, and status overviews as visible project files.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: A well-structured project folder is not proof of correctness or review.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - outputs/review
  - DEV_CONTEXT.md
  - future content workbench
- updated_at: 2026-06-06

### skills-and-prompts-as-visible-files

- kp_ref: outputs/review/candidate_pattern_bank/skills-and-prompts-as-visible-files.md
- stance: watch
- project_borrow_scope: Treat `/dbs-content-system` as a visible repeatable workflow shape: inputs, exclusions, priority order, constraints, acceptance counts.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not run or adopt the skill without verifying the package, commands, permissions, and fit.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - templates
  - future Codex skills
  - outputs/review
- updated_at: 2026-06-06

### memory-granularity-and-quarantine

- kp_ref: outputs/review/candidate_pattern_bank/memory-granularity-and-quarantine.md
- stance: partial
- project_borrow_scope: Keep raw materials, extracted content units, topic maps, assembly drafts, relation indexes, dedupe candidates, and status ledgers in separate grains.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not let content units, topic maps, or assembly drafts enter reviewed truth by shape alone.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - MEMORY_TIER.md
  - SOURCE_INTAKE.md
  - REVIEW_QUEUE.md
- updated_at: 2026-06-06

### retrieval-is-activation-not-truth

- kp_ref: outputs/review/candidate_pattern_bank/retrieval-is-activation-not-truth.md
- stance: partial
- project_borrow_scope: Treat topic maps, Obsidian links, relation indexes, and assembly drafts as activation and production surfaces.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not treat production links as evidence support, reviewed relation, confidence, or action basis.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - MEMORY_TIER.md
  - DEV_CONTEXT.md
  - REFERENCE_REVIEW_PROTOCOL.md
- updated_at: 2026-06-06

### path-scoped-agent-output-writes

- kp_ref: wiki/patterns/path-scoped-agent-output-writes.md
- stance: partial
- project_borrow_scope: Process old content in a new copy/output project rather than directly modifying the original archive.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not grant agents direct write authority over original content archives or formal VAKS truth files.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - outputs/review
  - outputs/qa
  - future content engineering sandbox
- updated_at: 2026-06-06

### agent-tool-access-tiering

- kp_ref: wiki/patterns/agent-tool-access-tiering.md
- stance: watch
- project_borrow_scope: Treat large content engineering skills as needing explicit read/write scope, exclusions, sample gates, and owner review.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not let a skill decide its own authority, exclusions, or completion standard.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - future agent access rules
  - SOURCE_INTAKE.md
  - REFERENCE_REVIEW_PROTOCOL.md
- updated_at: 2026-06-06

### operational-session-capture-loop

- kp_ref: wiki/patterns/operational-session-capture-loop.md
- stance: watch
- project_borrow_scope: Use processed/skipped/unit/map/draft/relation/dedupe counts as closeout receipts for a content engineering run.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Counts are not quality, support, or truth.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - DEV_CONTEXT.md
  - FEEDBACK.md
  - outputs/feedback
- updated_at: 2026-06-06

## Closeout Note

No entry here is action-ready.

If any entry is later used for a decision, architecture absorption, content
engineering module, skill installation, source-template adoption, or action
basis, stop and run the v0.2.13 late-stage review:

```text
claim + anchored evidence + non-circular warrant + scope + gaps + residual risk
```
