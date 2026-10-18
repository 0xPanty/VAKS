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
project_id:
target_ref:
target_selector:
target_hint:
project_borrow_scope:
project_non_borrow_scope:
project_reopen_trigger:
confirmation_basis:
last_checked_at:
expires_at:
---

# Project Overlay

## Boundary

This is a project-scoped sidecar.

It does not rewrite the source card, candidate distillation, reviewed note,
decision, or pattern.

It can guide the active project, but it cannot act as reviewed knowledge or
action basis.

## Target

```yaml
target_ref:
target_selector:
target_hint:
```

## Project Borrow Scope

```text
For this project, what may be borrowed from the target?
```

## Project Non-Borrow Scope

```text
For this project, what should not currently be borrowed, and why?
Use project-local language. Do not write a universal ban.
```

## Reopen Trigger

```text
When should this boundary be reconsidered?
```

## Confirmation

```yaml
confirmation_basis:
last_checked_at:
expires_at:
```

## Forbidden

```text
decision outcome
review verdict
truth confidence
action basis
universal ban
```
