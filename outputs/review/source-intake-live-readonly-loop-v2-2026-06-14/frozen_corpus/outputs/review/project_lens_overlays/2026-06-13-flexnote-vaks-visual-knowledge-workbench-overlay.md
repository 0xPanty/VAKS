---
record_kind: project_overlay
status: candidate
knowledge_status: candidate
processing_tier: medium
overlay_state: confirmed
review_pressure: review_due
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
project_id: VAKS
target_ref: outputs/review/2026-06-13-flexnote-docs-candidate-distillation.md
target_selector: visual-knowledge-workbench
target_hint: "Future VAKS visual workbench, source annotation surface, context-pack viewer, or review dashboard."
borrow_value: strong
borrow_order:
  - "P1: reusable card atom separated from whiteboard/view contexts"
  - "P1: annotation-to-card for PDF/video/web source anchors"
  - "P2: whiteboard as context-pack/review/project workbench"
  - "P2: tag database as dashboard/view layer"
  - "P3: journal/tabs/shortcuts/local-first sync as UX references"
project_borrow_scope: "For VAKS, borrow FlexNote as a design reference for visual workbench and source-annotation UX: source anchors, candidate points, evidence packets, review items, and context-pack items can be displayed as cards on boards while Markdown/YAML remains authoritative."
project_non_borrow_scope: "For project VAKS, do not currently borrow FlexNote's visual arrows, backlinks, tags, or board placement as reviewed relations or evidence support because VAKS relations require evidence-aware review. Reopen if a later workbench design stores relation proposals as candidate_relation objects with source anchors, warrants, scope, and review state."
project_reopen_trigger: "Reopen when building a VAKS visual workbench, source annotation adapter, context-pack viewer, review dashboard, or Obsidian Canvas/Bases integration."
confirmation_basis: "User explicitly requested distillation of FlexNote for VAKS; overlay remains candidate and project-scoped."
last_checked_at: 2026-06-13
expires_at:
tags:
  - project-overlay
  - vaks
  - flexnote
  - visual-workbench
  - annotation-to-card
  - source-anchor
  - context-pack-viewer
  - candidate-only
---

# Project Overlay: FlexNote for VAKS

## Boundary

This is a project-scoped sidecar.

It does not rewrite the source card, candidate distillation, reviewed note, decision, or pattern.

It can guide the active project, but it cannot act as reviewed knowledge or action basis.

## Target

```yaml
target_ref: outputs/review/2026-06-13-flexnote-docs-candidate-distillation.md
target_selector: visual-knowledge-workbench
target_hint: Future VAKS visual workbench, source annotation surface, context-pack viewer, or review dashboard.
```

## Project Borrow Scope

For VAKS, FlexNote is useful as a visual UI and source-annotation reference.

Borrow:

- card as UI-level information atom;
- one content object appearing in multiple views/boards;
- whiteboard as project/review/context-pack workbench;
- PDF/video/web annotation becoming source-location cards;
- tag database as dashboard and filter layer;
- journal as daily capture / session entry;
- tabs as active working set;
- shortcuts/import/export/sync as UX inspiration.

Safe VAKS translation:

```text
source material
-> source anchor card
-> candidate point card
-> evidence packet card
-> review queue board
-> reviewed relation only after review
```

## Project Non-Borrow Scope

For project VAKS, do not currently borrow FlexNote's visual arrows, backlinks, tags, or board placement as reviewed relations or evidence support because VAKS relations require evidence-aware review.

Do not borrow:

- canvas relation as truth;
- visual adjacency as support;
- tag fields as VAKS schema authority;
- annotation card as reviewed evidence by itself;
- cloud sync status as provenance integrity;
- generated card count as coverage or confidence.

Reopen if a later workbench design stores relation proposals as candidate_relation objects with source anchors, warrants, scope, and review state.

## Reopen Trigger

Reopen this overlay when one of these happens:

- user asks for VAKS visual workbench;
- user asks for Obsidian Canvas/Bases integration;
- user asks for PDF/video/web annotation intake;
- user asks for context-pack viewer;
- user asks for review dashboard;
- FlexNote publishes implementation/schema details.

## Confirmation

```yaml
confirmation_basis: User explicitly requested distillation for VAKS.
last_checked_at: 2026-06-13
```

## Forbidden

```text
decision outcome
review verdict
truth confidence
action basis
universal ban
```
