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
target_ref: outputs/review/2026-06-13-Xinghongia-Kova-candidate-distillation.md
target_selector: local-ai-note-client
target_hint: Future VAKS local capture client, candidate-only agent gateway, or quick
  intake sidecar.
borrow_value: strong
borrow_order:
- 'P1: hotkey cursor quick-capture surface'
- 'P1: visible AI tool operation event stream'
- 'P2: candidate-only note/folder tool schema after approval gate'
- 'P2: local sidecar SQLite for cache/state, not authority'
- 'P3: backup/restore and import/export UX'
project_borrow_scope: For VAKS, borrow Kova as a design reference for local quick
  capture, visible AI tool execution, and local sidecar ergonomics. The safe target
  is raw/candidate intake, not reviewed knowledge.
project_non_borrow_scope: For project VAKS, do not currently borrow Kova's direct
  AI note mutation as reviewed knowledge mutation because VAKS requires raw/candidate/review/action-basis
  boundaries. Reopen if a later agent gateway task adds path-scoped tools, diff preview,
  user approval, action receipts, and reviewed-layer write protection.
project_reopen_trigger: Reopen when building a real VAKS desktop sidecar, Obsidian
  plugin, or agent gateway write API.
confirmation_basis: User explicitly requested strong distillation for VAKS; overlay
  remains candidate and project-scoped.
last_checked_at: 2026-06-13
expires_at: null
tags:
- project-overlay
- vaks
- kova
- quick-capture
- agent-gateway
- candidate-only
- risk-direct-ai-mutation
legacy_overlay_compatibility: true
canonical_p0_included: false
canonical_current_lint_scope: false
legacy_storage: outputs/review/_legacy_project_lens
truth_boundary: legacy project lens compatibility artifact only; not canonical overlay;
  not reviewed knowledge; not action basis
---

# Project Overlay: Kova for VAKS

## Boundary

This is a project-scoped sidecar.

It does not rewrite the source card, candidate distillation, reviewed note, decision, or pattern.

It can guide the active project, but it cannot act as reviewed knowledge or action basis.

## Target

```yaml
target_ref: outputs/review/2026-06-13-Xinghongia-Kova-candidate-distillation.md
target_selector: local-ai-note-client
target_hint: Future VAKS local capture client, candidate-only agent gateway, or quick intake sidecar.
```

## Project Borrow Scope

For VAKS, Kova is useful as a local client / entry-layer reference.

Borrow:

- hotkey-triggered quick capture;
- cursor-position small window;
- always-on-top capture mode;
- write/browse quick note modes;
- `tool_call` / `tool_done` / `data_changed` style visible agent operation events;
- local sidecar DB for UI state, queue, cache, conversation state;
- ZIP backup/restore thinking for sidecar state;
- OpenAI-compatible tool schema shape, but only for candidate-layer operations.

Safe VAKS translation:

```text
quick capture
-> raw/source stub or candidate note
-> proposed AI operation
-> diff preview
-> explicit approval
-> append receipt
-> review queue if durable
```

## Project Non-Borrow Scope

For project VAKS, do not currently borrow Kova's direct AI note mutation as reviewed knowledge mutation because VAKS requires raw/candidate/review/action-basis boundaries.

Do not borrow:

- AI directly creating reviewed claims;
- AI directly editing reviewed patterns;
- AI directly deleting reviewed files;
- SQLite as the reviewed source of truth;
- tool execution success as evidence support;
- conversation summary as reviewed context;
- plaintext secret storage as acceptable default;
- broad file commands exposed to agent paths without path scope.

Reopen if the project goal changes to building a local app shell, or if a later gateway design includes path-scoped permissions, diff preview, approval, action receipts, and reviewed-layer write protection.

## Reopen Trigger

Reopen this overlay when one of these happens:

- user asks for a VAKS desktop sidecar;
- user asks for Obsidian plugin / tray / quick capture implementation;
- user asks for agent write API or MCP tool layer;
- user asks to reduce friction in source intake UX;
- a future Kova release adds permissions, tests, security hardening, or review gates.

## Confirmation

```yaml
confirmation_basis: User explicitly requested strong distillation for VAKS.
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
