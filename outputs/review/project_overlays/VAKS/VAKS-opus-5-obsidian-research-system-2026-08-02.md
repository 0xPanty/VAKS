---
record_kind: project_overlay
status: candidate
knowledge_status: candidate
processing_tier: medium
overlay_state: confirmed
review_pressure: none
overlay_scope: project_sidecar_only
overlay_storage: confirmed_persistent_project_bucket
retrieval_scope: active_project_only
default_retrieval: false
retrieval_policy:
  policy_kind: project_context_only
  default_scope: project_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: overlay_not_authority
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
project_id: verified-action-knowledge-system
target_ref: outputs/review/2026-08-02-opus-5-obsidian-research-system-candidate-distillation.md
target_selector: "VAKS project borrowing boundary for the pasted Opus 5 + Obsidian research-system article"
target_hint: "outcome calibration / unresolved-question queue / recent-delta digest / scope-first ingestion / workload-shaped evaluation / direct-write risk"
source_annotation_refs:
  - outputs/review/source_annotations/2026-08-02-opus-5-obsidian-research-system-source/workload-shaped-model-routing.md
  - outputs/review/source_annotations/2026-08-02-opus-5-obsidian-research-system-source/protocol-review-boundary-gap.md
  - outputs/review/source_annotations/2026-08-02-opus-5-obsidian-research-system-source/weekly-digest-bounded-pointer.md
  - outputs/review/source_annotations/2026-08-02-opus-5-obsidian-research-system-source/contradiction-review-and-audit-gap.md
  - outputs/review/source_annotations/2026-08-02-opus-5-obsidian-research-system-source/direct-vault-write-mcp-risk.md
  - outputs/review/source_annotations/2026-08-02-opus-5-obsidian-research-system-source/topic-scope-before-ingest.md
  - outputs/review/source_annotations/2026-08-02-opus-5-obsidian-research-system-source/outcome-calibration-manual-first.md
project_borrow_scope: "For VAKS, borrow as candidate project guidance: keep unresolved questions visible without guessing; use recent-delta digests as links to full notes; route contradictions to temporal/scope review with preserved history; decide project/topic scope before ingestion; evaluate research-system value with omissions, corrections, actual query use, cost, and stability; test any model route on representative VAKS tasks before choosing a default."
project_non_borrow_scope: "For VAKS, do not borrow raw-to-trusted-wiki writes, silent updates of old judgments, a new /raw-/wiki-/questions-/digests lane family, hard-coded Opus/Fable routing from vendor data, full-vault REST/MCP write authority, or unattended schedules. These mechanisms lack VAKS review, provenance, authority, rollback, receipt, and local-evaluation requirements."
project_reopen_trigger: "Reopen model routing after a representative VAKS evaluation; reopen REST/MCP only for an explicitly approved path-scoped candidate/output pilot with minimal tools, key isolation, prompt-injection controls, backup/rollback, operation receipts, and no reviewed-wiki writes; reopen scheduling only after two to three weeks of manual runs with omission, correction, cost, latency, and stability records."
confirmation_basis: "The user explicitly requested distillation inside the active VAKS project. This overlay records only project-scoped borrow/non-borrow boundaries and does not imply adoption."
last_checked_at: 2026-08-02
expires_at:
tags:
  - project-overlay
  - project-vaks
  - obsidian
  - research-workflow
  - candidate-only
---

# Project Overlay: Opus 5 + Obsidian Research System For VAKS

## Boundary

This is a project-scoped sidecar.

It does not rewrite the source card, candidate distillation, reviewed note, decision, or pattern. It can guide the active project, but it cannot act as reviewed knowledge or action basis.

## Target

```yaml
target_ref: outputs/review/2026-08-02-opus-5-obsidian-research-system-candidate-distillation.md
target_selector: VAKS project borrowing boundary for the pasted article
target_hint: outcome calibration / unresolved questions / recent-delta digest / topic scope / model evaluation / direct-write risk
```

## Entries

### outcome-calibrated-research-loop

- stance: partial
- project_borrow_scope: Measure a research loop with significant omissions, human corrections, actual cross-source query use, cost, latency, stability, and time saved. Start with manual receipts before considering a schedule.
- project_non_borrow_scope: Do not treat a short digest, subjective productivity feeling, or claimed hours saved as coverage or adoption evidence. Feedback cannot directly change truth confidence.
- project_reopen_trigger: Reopen for implementation when a concrete manual pilot has a defined input set, expected important points, omission log, correction log, use log, and stop condition.
- target_hint:
  - FEEDBACK.md
  - Use Ledger
  - decision outcome calibration
  - future bounded digest pilot

### unresolved-question-review-routing

- stance: partial
- project_borrow_scope: Keep unresolved questions persistent and visible, and route them to existing `missing_evidence`, `synthesis_needed`, or contradiction review items instead of guessing.
- project_non_borrow_scope: Do not add a new formal `/questions` lane or let an open question become a claim, reviewed relation, or action basis.
- project_reopen_trigger: Reopen if the existing review queue cannot preserve the source anchor, scope, owner, status, and later resolution link.
- target_hint:
  - REVIEW_QUEUE.md
  - SOURCE_INTAKE.md

### activity-scoped-bounded-digest

- stance: partial
- project_borrow_scope: Use a recent-delta digest with links to complete notes, contradictions, unresolved questions, and unusually active topics as an activation pointer.
- project_non_borrow_scope: Do not treat a 500-word budget as coverage proof, replace raw/reviewed notes with the digest, or schedule it before manual quality checks.
- project_reopen_trigger: Reopen scheduling only after manual runs show acceptable scope selection, omission rate, correction load, and stable output paths.
- target_hint:
  - DEV_CONTEXT.md
  - future activation workbench
  - outputs/feedback

### topic-scope-before-ingestion

- stance: partial
- project_borrow_scope: Make project/topic scope explicit before ingestion, make cross-scope links explicit, and generate routine digests inside the requested scope.
- project_non_borrow_scope: Do not make folders or vaults truth boundaries, create new module lanes, or isolate material that should remain retrievable through explicit project/context controls.
- project_reopen_trigger: Reopen a physical vault split only when explicit retrieval requirements show that accidental cross-topic activation is harmful and cross-pollination is not desired.
- target_hint:
  - Project Overlay
  - Context Pack
  - Temporal Applicability Check
  - retrieval_scope

### workload-shaped-model-routing

- stance: watch
- project_borrow_scope: Separate repeated volume work from high-risk deep synthesis and compare candidate models on representative VAKS tasks.
- project_non_borrow_scope: Do not hard-code Opus 5 for routine work or Fable for difficult work from vendor positioning, Frontier-Bench, or Harvey's legal evaluation alone.
- project_reopen_trigger: Reopen after a local comparison records source-anchor coverage, significant omissions, contradiction quality, human corrections, token/cost, latency, and run-to-run stability.
- target_hint:
  - future model evaluation manifest
  - source-intake task set
  - digest task set

### direct-vault-write-mcp

- stance: defer
- project_borrow_scope: Treat Local REST API/MCP only as a future transport option for a narrowly scoped candidate/output writer.
- project_non_borrow_scope: Do not install or connect it from this article; do not grant full-vault write, delete, move, command, or unattended schedule authority; do not write reviewed wiki directly.
- project_reopen_trigger: Reopen only with explicit user approval, candidate/output path scope, minimal tool allowlist, isolated key, prompt-injection controls, backup/rollback, operation preflight and receipts, and a tested recovery path.
- target_hint:
  - wiki/patterns/agent-tool-access-tiering.md
  - future operator cockpit
  - operation receipts

## Borrow Order

```text
P1:
  outcome/omission/use calibration
  contradiction temporal/scope judgment with audit history
  persistent unresolved-question routing

P2:
  recent-delta bounded digest
  visible protocol completion check
  scope-before-ingest
  manual-first pilot

P3 / reopen only:
  model routing after local evaluation
  path-scoped REST/MCP candidate writer
  unattended scheduling
```

## Forbidden

```text
decision outcome
review verdict
truth confidence
action basis
raw-to-trusted-wiki automation
silent overwrite of old judgments
full-vault direct write
vendor-benchmark-only model route
digest-as-coverage
```

