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
source_distillation: outputs/review/2026-06-06-x-damidefi-obsidian-signal-density-cleanup-candidate-distillation.md
source_card: raw/articles/2026-06-06-x-damidefi-obsidian-signal-density-cleanup-source.md
truth_boundary: "Project overlay only; not truth; not ADR; not action basis; not reviewed knowledge."
tags:
  - project-overlay
  - project-vaks
  - obsidian
  - vault-health
  - signal-density
  - candidate-only
---

# VAKS Project Overlay: Dami-Defi Obsidian Signal Density Cleanup

## Boundary

This is a project-scoped borrowing list for VAKS.

It does not rewrite the source card, generic candidate points, or any reviewed
knowledge node. It only records how VAKS may temporarily read this source.

## Entries

### memory-granularity-and-quarantine

- kp_ref: outputs/review/candidate_pattern_bank/memory-granularity-and-quarantine.md
- stance: partial
- project_borrow_scope: Use different handling for raw captures, processed thinking, duplicate thoughts, rare facts, archive candidates, and review candidates.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not delete raw sources, transcripts, ledgers, source cards, or review artifacts just because they are low activation value.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - MEMORY_TIER.md
  - SOURCE_INTAKE.md
  - REVIEW_QUEUE.md
- updated_at: 2026-06-06

### retrieval-is-activation-not-truth

- kp_ref: outputs/review/candidate_pattern_bank/retrieval-is-activation-not-truth.md
- stance: partial
- project_borrow_scope: Treat signal-density cleanup as an activation/context-selection issue: keep low-signal material out of hot context.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not treat exclusion from activation as deletion, falsification, or lower truth confidence.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - MEMORY_TIER.md
  - DEV_CONTEXT.md
  - REFERENCE_REVIEW_PROTOCOL.md
- updated_at: 2026-06-06

### archive-first-lazy-reactivation

- kp_ref: wiki/patterns/archive-first-lazy-reactivation.md
- stance: partial
- project_borrow_scope: Prefer archive/cooling before deletion for unprocessed or low-signal captures, with the possibility of later reactivation.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not turn an aggressive personal cleanup story into a VAKS deletion workflow.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - MEMORY_TIER.md
  - SOURCE_INTAKE.md
  - DEV_CONTEXT.md
- updated_at: 2026-06-06

### source-structure-first-rag

- kp_ref: outputs/review/candidate_pattern_bank/source-structure-first-rag.md
- stance: watch
- project_borrow_scope: Keep the distinction between raw source material and extracted thinking visible, so context packs can use concise processed points without losing provenance.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not strip source anchors needed for evidence-aware review just to reduce apparent vault size.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - SOURCE_INTAKE.md
  - raw/articles
  - raw/videos
  - outputs/review
- updated_at: 2026-06-06

### simple-first-retrieval-baseline

- kp_ref: outputs/review/candidate_pattern_bank/simple-first-retrieval-baseline.md
- stance: partial
- project_borrow_scope: Prefer small, high-signal context packs over broad vault dumps when answering or briefing.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Smaller context is not automatically more correct; it must still include necessary support, challenge, scope, and risk.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - MEMORY_TIER.md
  - DEV_CONTEXT.md
  - future context-pack policy
- updated_at: 2026-06-06

### agent-tool-access-tiering

- kp_ref: wiki/patterns/agent-tool-access-tiering.md
- stance: watch
- project_borrow_scope: Cleanup agents may suggest KEEP / archive / review candidates, but destructive actions require owner review.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not grant AI delete authority over project files, Obsidian notes, source records, or reviewed knowledge.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - future agent access rules
  - SOURCE_INTAKE.md
  - REFERENCE_REVIEW_PROTOCOL.md
- updated_at: 2026-06-06

### path-scoped-agent-output-writes

- kp_ref: wiki/patterns/path-scoped-agent-output-writes.md
- stance: watch
- project_borrow_scope: Put cleanup reports in outputs/review or outputs/qa as suggestions before any archive or deletion decision.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: A cleanup report is not permission to move or delete files.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - outputs/review
  - outputs/qa
  - future maintenance reports
- updated_at: 2026-06-06

### operational-session-capture-loop

- kp_ref: wiki/patterns/operational-session-capture-loop.md
- stance: watch
- project_borrow_scope: If a cleanup or cooling trial happens later, record what changed, what stayed useful, what was missed, and whether outputs improved.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Daily brief improvement is diagnostic feedback, not evidence of truth or correctness.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - DEV_CONTEXT.md
  - FEEDBACK.md
  - outputs/feedback
- updated_at: 2026-06-06

## Closeout Note

No entry here is action-ready.

If any entry is later used for a decision, architecture absorption, action
basis, cleanup, archive policy, deletion, source retention, or risk-sensitive
answer, stop and run the v0.2.13 late-stage review:

```text
claim + anchored evidence + non-circular warrant + scope + gaps + residual risk
```
