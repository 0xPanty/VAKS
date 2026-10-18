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
source_distillation: outputs/review/2026-06-06-x-khairallah-obsidian-claude-workflows-candidate-distillation.md
source_card: raw/articles/2026-06-06-x-khairallah-obsidian-claude-workflows-source.md
truth_boundary: "Project overlay only; not truth; not ADR; not action basis; not reviewed knowledge."
tags:
  - project-overlay
  - project-vaks
  - obsidian
  - claude
  - tool-catalog
  - agent-access
  - candidate-only
---

# VAKS Project Overlay: Khairallah Obsidian + Claude Workflow Catalog

## Boundary

This is a project-scoped borrowing list for VAKS.

## Entries

### retrieval-is-activation-not-truth

- kp_ref: outputs/review/candidate_pattern_bank/retrieval-is-activation-not-truth.md
- stance: partial
- project_borrow_scope: Treat vault chat, Smart Connections, Copilot, graph analysis, and idea cross-pollination as activation surfaces.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not let RAG answers, graph hubs, search matches, or suggested links become evidence support, confidence, reviewed relations, or action basis.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - MEMORY_TIER.md
  - DEV_CONTEXT.md
  - REFERENCE_REVIEW_PROTOCOL.md
- updated_at: 2026-06-06

### source-structure-first-rag

- kp_ref: outputs/review/candidate_pattern_bank/source-structure-first-rag.md
- stance: partial
- project_borrow_scope: Use templates and ingestion workflow ideas as support for structured candidate/source notes.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Structured notes and generated summaries are not reviewed knowledge.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - SOURCE_INTAKE.md
  - raw/articles
  - raw/videos
  - outputs/review
- updated_at: 2026-06-06

### skills-and-prompts-as-visible-files

- kp_ref: outputs/review/candidate_pattern_bank/skills-and-prompts-as-visible-files.md
- stance: watch
- project_borrow_scope: Treat official skills, custom skills, routines, and workflow prompts as visible workflow files that require review.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not treat official branding, star count, or skill existence as fit or safety evidence.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - templates
  - future Codex / Claude skills
  - outputs/review
- updated_at: 2026-06-06

### agent-tool-access-tiering

- kp_ref: wiki/patterns/agent-tool-access-tiering.md
- stance: watch
- project_borrow_scope: Treat MCP servers, Obsidian CLI, Claude Code routines, and vault-powered Projects as access-tier design inputs.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not grant broad read/write/delete/schedule authority from a tool catalog.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - future agent access rules
  - SOURCE_INTAKE.md
  - REFERENCE_REVIEW_PROTOCOL.md
- updated_at: 2026-06-06

### path-scoped-agent-output-writes

- kp_ref: wiki/patterns/path-scoped-agent-output-writes.md
- stance: watch
- project_borrow_scope: Put generated workflows, health checks, meeting processors, and ingestion outputs into bounded candidate/output paths.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: A workflow output is not permission to edit formal wiki, schema, decisions, or reviewed nodes.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - outputs/review
  - outputs/qa
  - future maintenance reports
- updated_at: 2026-06-06

### memory-granularity-and-quarantine

- kp_ref: outputs/review/candidate_pattern_bank/memory-granularity-and-quarantine.md
- stance: partial
- project_borrow_scope: Treat AI-generated summaries, project kickoffs, decision journal analyses, and feedback-loop notes as quarantined candidate or feedback artifacts.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not let #ai-generated notes compound into reviewed truth without review.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - MEMORY_TIER.md
  - FEEDBACK.md
  - REVIEW_QUEUE.md
- updated_at: 2026-06-06

### operational-session-capture-loop

- kp_ref: wiki/patterns/operational-session-capture-loop.md
- stance: watch
- project_borrow_scope: Read morning synthesis, weekly automation, decision journals, and periodic notes as operational receipts.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Operational receipts are not decisions, reviewed relations, or action readiness.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - DEV_CONTEXT.md
  - FEEDBACK.md
  - outputs/feedback
- updated_at: 2026-06-06

### simple-first-retrieval-baseline

- kp_ref: outputs/review/candidate_pattern_bank/simple-first-retrieval-baseline.md
- stance: partial
- project_borrow_scope: Use the source as a reminder that tool abundance needs a problem-fit filter.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not turn a 30-item catalog into roadmap, default stack, or automation backlog.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - MEMORY_TIER.md
  - DEV_CONTEXT.md
  - future automation policy
- updated_at: 2026-06-06

### visual-workbench-for-retrieval-diagnostics

- kp_ref: outputs/review/candidate_pattern_bank/visual-workbench-for-retrieval-diagnostics.md
- stance: defer
- project_borrow_scope: Graph analysis may help diagnose hubs, clusters, and bridge candidates in a future workbench.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not treat graph structure as truth, coverage, or evidence support.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - future Obsidian workbench
  - templates/maintenance-manifest.md
- updated_at: 2026-06-06

## Closeout Note

No entry here is action-ready. Any use for tool adoption, MCP/CLI access,
automation, architecture absorption, or action basis must run the v0.2.13
late-stage review.
