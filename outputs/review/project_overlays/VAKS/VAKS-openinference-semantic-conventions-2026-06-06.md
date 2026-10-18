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
source_distillation: outputs/review/2026-06-06-openinference-semantic-conventions-candidate-distillation.md
source_card: raw/repos/2026-06-06-openinference-semantic-conventions-source.md
truth_boundary: "Project overlay only; not truth; not ADR; not action basis; not reviewed knowledge."
tags:
  - project-overlay
  - project-vaks
  - openinference
  - tracing
  - agent-receipts
  - retrieval-diagnostics
  - candidate-only
---

# VAKS Project Overlay: OpenInference Semantic Conventions

## Boundary

This is a project-scoped borrowing list for VAKS.

It does not rewrite the source card, generic candidate points, or reviewed
knowledge. It only records how VAKS may temporarily read this source.

## Entries

### operational-session-capture-loop

- kp_ref: wiki/patterns/operational-session-capture-loop.md
- stance: partial
- project_borrow_scope: Use span kinds, session id, input/output, prompt template/version, token/cost, and tool-call fields as candidate vocabulary for operation receipts.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not treat trace presence, cost, token count, or evaluator runs as proof of quality, review, or action readiness.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - DEV_CONTEXT.md
  - FEEDBACK.md
  - outputs/feedback
  - future run receipts
- updated_at: 2026-06-06

### retrieval-is-activation-not-truth

- kp_ref: outputs/review/candidate_pattern_bank/retrieval-is-activation-not-truth.md
- stance: partial
- project_borrow_scope: Use `retrieval.documents`, `reranker.*`, `document.id`, `document.metadata`, and `document.score` as retrieval activation receipts.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not treat retrieval score, rerank order, or activated document presence as evidence support or reviewed relation.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - MEMORY_TIER.md
  - REFERENCE_REVIEW_PROTOCOL.md
  - future context-pack receipts
- updated_at: 2026-06-06

### source-structure-first-rag

- kp_ref: outputs/review/candidate_pattern_bank/source-structure-first-rag.md
- stance: watch
- project_borrow_scope: Use document id/content/metadata fields to preserve source identity in retrieval and context-pack pipelines.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not replace source cards or source anchors with backend trace attributes.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - SOURCE_INTAKE.md
  - raw/repos
  - outputs/review
- updated_at: 2026-06-06

### agent-tool-access-tiering

- kp_ref: wiki/patterns/agent-tool-access-tiering.md
- stance: partial
- project_borrow_scope: Use tool schema, tool name, tool id, tool-call id, and tool-call arguments as audit vocabulary for future tool use.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Trace visibility is not authorization; tool access still needs separate tiers, path boundaries, intent confirmation, and review gates.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - future agent access rules
  - DEV_CONTEXT.md
  - REFERENCE_REVIEW_PROTOCOL.md
- updated_at: 2026-06-06

### path-scoped-agent-output-writes

- kp_ref: wiki/patterns/path-scoped-agent-output-writes.md
- stance: watch
- project_borrow_scope: If future tool traces include file operations, record target paths and operation kind as operational receipt fields.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: A recorded write path does not make the write appropriate, reviewed, or reversible.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - tools
  - outputs/review
  - future run receipts
- updated_at: 2026-06-06

### file-first-agent-workbench

- kp_ref: outputs/review/candidate_pattern_bank/file-first-agent-workbench.md
- stance: watch
- project_borrow_scope: Treat trace fields as a possible bridge between invisible runtime events and visible Markdown receipts.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not replace file-first handoffs, source cards, review records, or project overlays with an external trace backend.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - 00_handoff
  - outputs/review
  - future Codex skill receipts
- updated_at: 2026-06-06

### skills-and-prompts-as-visible-files

- kp_ref: outputs/review/candidate_pattern_bank/skills-and-prompts-as-visible-files.md
- stance: watch
- project_borrow_scope: Use prompt template, variables, and version fields to make prompt/skill-driven outputs more reproducible.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Prompt trace is not workflow approval, review, or correctness.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - templates
  - future Codex skills
  - outputs/review
- updated_at: 2026-06-06

### memory-granularity-and-quarantine

- kp_ref: outputs/review/candidate_pattern_bank/memory-granularity-and-quarantine.md
- stance: partial
- project_borrow_scope: Treat session id, user id, metadata, tags, prompt variables, and tool-call details as operational memory that may need quarantine or redaction.
- project_non_borrow_scope: For project VAKS, keep this boundary project-scoped: Do not let session metadata become reviewed memory or global truth by default.
- project_reopen_trigger: Reopen if VAKS later needs this source for architecture, decision, action basis, cross-project reuse, or formal negative knowledge.
- target_hint:
  - MEMORY_TIER.md
  - FEEDBACK.md
  - future privacy/scope rules
- updated_at: 2026-06-06

## Project Reading

For VAKS, the source reads like this:

```text
OpenInference gives us a clean vocabulary for "what happened during the run".
VAKS still decides "what counts as support, review, risk, and action basis".
```

Most valuable candidates:

```text
1. operation trace taxonomy
2. retrieval/rerank/document activation receipts
3. tool-call audit fields
4. prompt template/version receipts
5. token/cost/session accounting
6. evaluator/guardrail as diagnostics only
```

## Closeout Note

No entry here is action-ready.

If any entry is later used for schema/template changes, official run receipts,
tool instrumentation, privacy/session logging, runtime adoption, or action
basis, stop and run the v0.2.13 late-stage review:

```text
claim + anchored evidence + non-circular warrant + scope + gaps + residual risk
```

