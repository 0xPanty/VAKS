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
target_ref: outputs/review/2026-06-23-anatoli-kopadze-loops-explained-candidate-distillation.md
target_selector: "VAKS/MISA loop-worthiness, cost-control, and light-vs-heavy loop sidecar"
target_hint: "verify/state/stop / four-condition test / cost per accepted change / manual-to-schedule order / everyday-loop UX"
source_annotation_refs:
  - outputs/review/source_annotations/2026-06-23-anatoli-kopadze-loops-explained/anatoli-loop-core-verify-state-stop.md
  - outputs/review/source_annotations/2026-06-23-anatoli-kopadze-loops-explained/anatoli-loop-worth-building-test.md
  - outputs/review/source_annotations/2026-06-23-anatoli-kopadze-loops-explained/anatoli-coding-loop-spec.md
  - outputs/review/source_annotations/2026-06-23-anatoli-kopadze-loops-explained/anatoli-five-building-blocks.md
  - outputs/review/source_annotations/2026-06-23-anatoli-kopadze-loops-explained/anatoli-cost-per-accepted-change.md
  - outputs/review/source_annotations/2026-06-23-anatoli-kopadze-loops-explained/anatoli-manual-skill-loop-schedule-order.md
  - outputs/review/source_annotations/2026-06-23-anatoli-kopadze-loops-explained/anatoli-self-checking-light-loop.md
  - outputs/review/source_annotations/2026-06-23-anatoli-kopadze-loops-explained/anatoli-mira-everyday-loop-claims.md
project_borrow_scope: "For VAKS, borrow this source as a candidate boundary and cost-control reference: verify/state/stop triad, the four-condition test for whether a loop is worth building, coding-loop spec shape, automation/skill/sub-agent/connector/verifier checklist, cost per accepted change, manual-run -> skill -> loop -> schedule order, and light self-checking loop patterns for ordinary use. Also borrow the everyday-loop UX shape only as product inspiration."
project_non_borrow_scope: "For project VAKS, do not currently borrow this source as evidence that Claude Code, Codex, Mira, Composio, 500+ apps, model routing, cost ranges, migration anecdotes, or productized automation examples are true. Do not treat model self-scoring as strong verification, and do not let productized everyday loops bypass VAKS evidence/action boundaries. Reopen only if official docs, local tests, receipts, and authority-boundary checks support a bounded pilot."
project_reopen_trigger: "Reopen when VAKS designs a real loop-run receipt, cost-per-accepted-change metric, light self-checking capture flow, or productized everyday-loop interface; require explicit verify/state/stop fields, budget/iteration caps, accepted/rejected output accounting, and action_basis_allowed=false boundaries."
confirmation_basis: "User explicitly requested distillation of this article/post; overlay is limited to project borrow/non-borrow boundaries and does not imply adoption."
last_checked_at: 2026-06-23
expires_at:
tags:
  - loop-engineering
  - cost-control
  - self-checking-loop
  - everyday-loops
---

# Project Overlay: Anatoli Loops Explained For VAKS

## Boundary

This is a project-scoped sidecar.

It does not rewrite the source card, candidate distillation, reviewed note, decision, or pattern.

It can guide future VAKS/MISA loop design and loop-worthiness decisions, but it cannot act as reviewed knowledge or action basis.

## Target

```yaml
target_ref: outputs/review/2026-06-23-anatoli-kopadze-loops-explained-candidate-distillation.md
target_selector: VAKS/MISA loop-worthiness, cost-control, and light-vs-heavy loop sidecar
target_hint: verify/state/stop / four-condition test / cost per accepted change / manual-to-schedule order / everyday-loop UX
```

## Project Borrow Scope

For VAKS, borrow this source as a candidate reference for:

```text
when to build a loop
when to keep a task manual
what a minimal loop receipt must contain
how to explain light vs heavy loops
how to track loop economics
how to avoid schedule-before-reliability failures
```

Borrow the minimum loop receipt shape:

```yaml
loop_receipt:
  goal:
  verify_gate:
  state_ref:
  stop_condition:
  iteration_cap:
  cost_budget:
  accepted_outputs:
  rejected_outputs:
  cost_per_accepted_change:
  final_status: diagnostic_only
  action_basis_allowed: false
```

## Project Non-Borrow Scope

For project VAKS, do not currently borrow:

```text
Claude/Codex/Mira platform claims as verified
Composio/app-count/model-routing claims as verified
Mira everyday examples as confirmed capability
model self-score as strong verification
productized action as action basis
loop popularity as adoption evidence
```

Reason:

```text
This source is a pasted social-post/article.
It provides useful orientation and UX framing.
It does not provide official docs, reproducible tests, receipts, or reviewed evidence.
```

## Reopen Trigger

Reopen this boundary when:

```text
VAKS designs a real loop-run receipt
or a cost-per-accepted-change metric
or a light self-checking capture flow
or a productized everyday-loop interface
and official/source checks exist where product claims matter
and accepted/rejected output accounting exists
and action_basis_allowed=false remains explicit
```

## Forbidden

```text
decision outcome
review verdict
truth confidence
action basis
self-score-as-verification
product-claim-as-evidence
scheduled-loop-before-manual-reliability
```

