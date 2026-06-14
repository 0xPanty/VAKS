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
project_id:
target_ref:
target_selector:
target_hint:
source_annotation_refs: []
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
source_annotation_refs:
```

`source_annotation_refs` can point to useful source-local locators, but they do
not replace `project_borrow_scope`, `project_non_borrow_scope`, or
`project_reopen_trigger`.

## Project Borrow Scope

```text
For this project, what may be borrowed from the target?
```

## Project Non-Borrow Scope

```text
For project <project_id>, do not currently borrow <X> as <Y> because <reason>.
Reopen if <goal/scope/tooling/evidence> changes.
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
source annotation as project verdict
action basis
universal ban
```
