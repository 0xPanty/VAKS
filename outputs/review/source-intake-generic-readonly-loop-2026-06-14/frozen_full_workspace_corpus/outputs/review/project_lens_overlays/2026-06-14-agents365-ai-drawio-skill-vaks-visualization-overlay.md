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
target_ref: outputs/review/2026-06-14-agents365-ai-drawio-skill-candidate-distillation.md
target_selector: "VAKS architecture/product visualization sidecar"
target_hint: "diagram/documentation/export layer"
project_borrow_scope: "For VAKS, borrow drawio-skill as an optional diagram/documentation sidecar for architecture explanation, workflow diagrams, product onboarding, and MISA codebase visualization; use its lint -> visual check -> feedback loop as generated-artifact QA."
project_non_borrow_scope: "For project VAKS, do not currently borrow drawio-skill as a truth layer, review engine, evidence support mechanism, source intake path, or action-basis validator, because generated diagrams are derived views and visual/self-test checks are diagnostics only. Reopen if a future publishing/diagram pipeline adds source anchors, derived-view labels, and explicit action_basis_allowed=false receipts."
project_reopen_trigger: "Reopen when VAKS starts a diagram/export/publishing sandbox, or when MISA needs codebase visualization for a specific implementation review."
confirmation_basis: "User explicitly requested distillation; overlay is limited to visualization/product documentation and does not imply core adoption."
last_checked_at: 2026-06-14
expires_at:
tags:
  - drawio
  - diagram-generation
  - architecture-documentation
---

# Project Overlay: drawio-skill for VAKS Visualization

## Boundary

This is a project-scoped sidecar.

It does not rewrite the source card, candidate distillation, reviewed note, decision, or pattern.

It can guide diagram/product documentation work, but it cannot act as reviewed knowledge or action basis.

## Target

```yaml
target_ref: outputs/review/2026-06-14-agents365-ai-drawio-skill-candidate-distillation.md
target_selector: VAKS architecture/product visualization sidecar
target_hint: diagram/documentation/export layer
```

## Project Borrow Scope

For VAKS, borrow drawio-skill as an optional sidecar for:

```text
architecture diagrams
source intake / review / action flow diagrams
context-pack and evidence-packet explanations
product onboarding visuals
MISA bridge diagrams
MISA codebase/module visualization
```

Borrow the workflow:

```text
source/spec/graph
-> generated .drawio
-> deterministic structural lint
-> visual check
-> human feedback
-> final editable export
```

## Project Non-Borrow Scope

For project VAKS, do not currently borrow drawio-skill as:

```text
truth layer
review engine
evidence support mechanism
source intake path
action-basis validator
required core dependency
```

Reason:

```text
Generated diagrams are derived views.
Visual self-checks and script tests are diagnostics only.
They cannot support a claim, change confidence, or approve action.
```

Reopen if:

```text
a future publishing/diagram pipeline stores source anchors,
derived-view labels,
source prompts/specs,
and action_basis_allowed=false receipts.
```

## Recommended Use Shape

```yaml
diagram_artifact:
  source_spec_ref:
  generated_from:
  diagram_path:
  export_paths:
  derived_view_only: true
  action_basis_allowed: false
  source_anchors_required_for_claims: true
  qa:
    structural_lint:
    visual_check:
    user_feedback:
```

## Confirmation

```yaml
confirmation_basis: user requested distillation of this repo
last_checked_at: 2026-06-14
```

## Forbidden

```text
decision outcome
review verdict
truth confidence
action basis
universal ban
diagram-as-evidence
```
