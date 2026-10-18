---
record_kind: project_overlay
status: candidate
knowledge_status: candidate
processing_tier: medium
overlay_state: confirmed
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
title: "sync-embeds Obsidian workbench overlay"
target_ref: "outputs/review/2026-06-12-uthvah-sync-embeds-candidate-distillation.md"
source_ref: "raw/repos/2026-06-12-uthvah-sync-embeds-source.md"
target_selector: "candidate source: uthvah/sync-embeds"
target_hint:
  - obsidian-workbench
  - editable-dashboard
  - source-card-ui
  - review-queue-ui
project_borrow_scope: "For VAKS, borrow sync-embeds only as a P2 design reference for editable Obsidian workbench surfaces: source inbox, candidate review queue, project scratch, and feedback triage."
project_non_borrow_scope: "For VAKS, do not borrow sync-embeds as a truth architecture, review authority, source provenance mechanism, evidence support layer, action-basis engine, or default editor for reviewed notes."
project_reopen_trigger: "Reopen when VAKS starts a real Obsidian workbench/Bases/plugin sandbox or when the user asks to test/install editable embeds in a disposable vault."
confirmation_basis: "User explicitly requested 蒸馏 for this repo in the VAKS workspace; source card and candidate distillation were created as candidate-only project material."
last_checked_at: 2026-06-12
expires_at:
borrow_value: medium
borrow_order: P2
avoid:
  - "reviewed-file edit-through"
  - "dynamic path as provenance"
  - "DOM section hiding as security"
  - "monkey-patched active view as authority"
tags:
  - project-overlay
  - candidate
  - obsidian
  - workbench
  - editable-dashboard
---

# Project Overlay: sync-embeds Obsidian Workbench

## Boundary

This is a project-scoped sidecar.

It does not rewrite the source card, candidate distillation, reviewed note, decision, or pattern. It can guide the active project, but it cannot act as reviewed knowledge or action basis.

```yaml
knowledge_status: candidate
overlay_scope: project_sidecar_only
retrieval_scope: active_project_only
action_basis_allowed: false
truth_mutation_allowed: false
```

## Target

```yaml
target_ref: outputs/review/2026-06-12-uthvah-sync-embeds-candidate-distillation.md
source_ref: raw/repos/2026-06-12-uthvah-sync-embeds-source.md
snapshot_ref: raw/repos/_snapshots/2026-06-12-uthvah-sync-embeds-10703d39548a-source.zip
target_selector: "candidate source: uthvah/sync-embeds"
```

## Project Borrow Scope

For VAKS, borrow `sync-embeds` as a design reference for one narrow problem:

```text
How can an Obsidian dashboard edit the underlying source/candidate/project note
without duplicating content or forcing the user to leave the dashboard?
```

Good VAKS uses:

- `raw/repos` / `raw/articles` source card inbox: edit "why captured", "obvious doubts", or "next step" sections from a dashboard.
- `outputs/review` candidate queue: edit candidate point notes or open questions from a queue page.
- `outputs/feedback` feedback triage: edit scoped feedback events from an active project view.
- project scratch / DEV_CONTEXT support notes: edit working context from project overview.

The useful pattern is:

```text
dashboard view
-> embedded real editor for allowed source/candidate section
-> file write remains in the original note
-> dashboard does not become the source of truth
```

## Project Non-Borrow Scope

For VAKS, do not currently borrow `sync-embeds` in these directions:

- Do not use it as the mechanism that makes knowledge reviewed.
- Do not expose reviewed `wiki/claims`, `wiki/decisions`, or adopted `wiki/patterns` to direct edit-through.
- Do not let dynamic paths decide source identity, source anchors, or evidence support.
- Do not treat section viewport boundaries as enforcement for permission/security.
- Do not build VAKS core around Obsidian monkey patches.
- Do not install in the formal vault before a disposable sandbox proves rollback and path-scoped editing.

Plain-language rule:

```text
It can make the workbench nicer.
It cannot make a candidate safer, truer, reviewed, or action-ready.
```

## Reopen Trigger

Reopen this overlay when one of these becomes true:

- VAKS starts designing an Obsidian workbench/Bases page that needs inline editing.
- The user asks to test this plugin in a disposable vault.
- A future implementation needs a source-card or review-queue UI.
- A comparable plugin offers a safer API-level editable embed without monkey-patching workspace state.

## Minimal Safe Adoption Shape

If tested later, start with this narrower setup:

```text
allowed:
  - raw source-card note sections
  - candidate distillation notes
  - feedback events
  - project scratch/support notes

blocked:
  - reviewed claims
  - reviewed patterns
  - decisions
  - indexes treated as authority
  - action-basis packets
```

Each edit-through should ideally leave:

```yaml
edit_receipt:
  edited_file:
  edited_section:
  project_ref:
  edited_at:
  edited_by:
  prior_hash:
  after_hash:
  layer:
  action_basis_allowed: false
```

This receipt idea is not in `sync-embeds`; it is the VAKS boundary needed if we borrow the UX.

## Confirmation

```yaml
confirmation_basis: "Explicit 蒸馏 request for this repository in the VAKS workspace."
last_checked_at: 2026-06-12
borrow_value: medium
borrow_order: P2
```

## Forbidden

```text
decision outcome
review verdict
truth confidence
action basis
universal ban
```
