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
target_ref: outputs/review/2026-06-23-gaasher-Agent-Loop-Skills-candidate-distillation.md
target_selector: "VAKS/MISA agentic loop operational sidecar"
target_hint: "loop-run template / operator workflow / source-intake loop design"
source_annotation_refs:
  - outputs/review/source_annotations/2026-06-23-gaasher-Agent-Loop-Skills/als-loop-five-ingredients.md
  - outputs/review/source_annotations/2026-06-23-gaasher-Agent-Loop-Skills/als-verification-gated-keep-revert.md
  - outputs/review/source_annotations/2026-06-23-gaasher-Agent-Loop-Skills/als-spawn-or-degrade-boundary.md
  - outputs/review/source_annotations/2026-06-23-gaasher-Agent-Loop-Skills/als-literature-evidence-matrix.md
  - outputs/review/source_annotations/2026-06-23-gaasher-Agent-Loop-Skills/als-tournament-judge-calibration.md
project_borrow_scope: "For VAKS, borrow Agent-Loop-Skills as an operational-loop design reference: loop-as-skill packaging, five-ingredient loop contract, append-only run ledger, one-change-per-iteration attribution, verification-gated keep/revert/refute, measured stop/budget/patience, spawn-or-degrade role fallback, and best-iteration reporting. Use it for future bounded source-intake, operator, MISA work-order, evaluator-optimizer, and research survey loop designs."
project_non_borrow_scope: "For project VAKS, do not currently borrow Agent-Loop-Skills as a truth layer, reviewed knowledge model, evidence support mechanism, action-basis validator, background automation authority, or default ordinary-intake behavior, because loop signals, metrics, ledgers, judges, and showcase results are diagnostics/trace only unless later checked through VAKS evidence-aware review. Reopen if a future loop-run pilot stores authority labels, source anchors, receipts, stop conditions, and explicit action_basis_allowed=false boundaries."
project_reopen_trigger: "Reopen when VAKS designs a real loop-run template, source-intake loop, operator cockpit loop, or MISA evaluator-optimizer workflow; require a bounded sandbox pilot and evidence/action boundary audit before any mainline adoption."
confirmation_basis: "User explicitly requested distillation of this repo for VAKS knowledge coverage; overlay is limited to project borrow/non-borrow boundaries and does not imply adoption."
last_checked_at: 2026-06-23
expires_at:
tags:
  - agentic-loops
  - agent-skills
  - operator-loop
  - source-intake
---

# Project Overlay: Agent-Loop-Skills for VAKS Agentic Loops

## Boundary

This is a project-scoped sidecar.

It does not rewrite the source card, candidate distillation, reviewed note, decision, or pattern.

It can guide future VAKS/MISA loop design, but it cannot act as reviewed knowledge or action basis.

## Target

```yaml
target_ref: outputs/review/2026-06-23-gaasher-Agent-Loop-Skills-candidate-distillation.md
target_selector: VAKS/MISA agentic loop operational sidecar
target_hint: loop-run template / operator workflow / source-intake loop design
source_annotation_refs:
  - outputs/review/source_annotations/2026-06-23-gaasher-Agent-Loop-Skills/als-loop-five-ingredients.md
  - outputs/review/source_annotations/2026-06-23-gaasher-Agent-Loop-Skills/als-verification-gated-keep-revert.md
  - outputs/review/source_annotations/2026-06-23-gaasher-Agent-Loop-Skills/als-spawn-or-degrade-boundary.md
  - outputs/review/source_annotations/2026-06-23-gaasher-Agent-Loop-Skills/als-literature-evidence-matrix.md
  - outputs/review/source_annotations/2026-06-23-gaasher-Agent-Loop-Skills/als-tournament-judge-calibration.md
```

## Project Borrow Scope

For VAKS, borrow Agent-Loop-Skills as an optional operational sidecar for:

```text
source-intake loop design
operator cockpit / loop status surfaces
MISA work-order evaluator-optimizer loops
research survey / evidence matrix loops
red-team find-only loops
bounded prompt/data/code optimization loops
```

Borrow the workflow contract:

```text
program / skill
-> artifact slot
-> real feedback signal
-> one focused iteration
-> keep / discard / refute rule
-> append-only ledger
-> stop by threshold / plateau / dry rounds / budget / human interrupt
```

Borrow the host boundary:

```text
spawn roles only when supported
degrade inline otherwise
never let host capability change authority status
```

## Project Non-Borrow Scope

For project VAKS, do not currently borrow Agent-Loop-Skills as:

```text
truth layer
review engine
evidence support mechanism
action-basis validator
background automation authority
default ordinary-intake behavior
reviewed relation generator
```

Reason:

```text
Loop signals are diagnostics.
Metrics can be gamed.
Judges are selectors, not reviewers.
Ledgers are traces, not evidence packets.
Showcase results are source claims unless reproduced.
```

Reopen if:

```text
a future loop-run pilot stores source anchors,
authority labels,
receipts,
stop conditions,
bounded user scope,
and action_basis_allowed=false boundaries.
```

## Recommended Use Shape

```yaml
loop_run:
  record_kind: loop_run
  knowledge_status: candidate
  processing_tier: medium
  source_ref:
  task_scope:
  artifact_slot:
  feedback_signal:
  ledger_ref:
  stop_condition:
  best_iteration:
  result_status: diagnostic_only
  retrieval_policy:
    policy_kind: orientation_only
    pack_allowed: review_input_only
    action_basis_allowed: false
    warning_code: loop_signal_not_support
  truth_mutation_allowed: false
  action_basis_allowed: false
```

## Confirmation

```yaml
confirmation_basis: user requested distillation of this repo for VAKS knowledge coverage
last_checked_at: 2026-06-23
```

## Forbidden

```text
decision outcome
review verdict
truth confidence
action basis
universal ban
loop-output-as-evidence
metric-as-truth
judge-score-as-review
```
