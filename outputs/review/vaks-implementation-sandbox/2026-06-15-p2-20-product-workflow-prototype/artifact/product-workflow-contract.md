---
record_kind: product_workflow_contract
slice_id: 2026-06-15-p2-20-product-workflow-prototype
status: drafted
truth_boundary: sandbox_contract_only
---

# Product Workflow Contract

## Purpose

Prototype the first usable VAKS product workflow in sandbox JSON form. The
workflow must make the strict system easier to operate without weakening any
authority boundary.

This is not production UI, not a real Obsidian Base, not reviewed knowledge, and
not action basis.

## Required Prototype Shape

The workflow artifact must be JSON with:

- `record_kind`: `vaks_product_workflow_prototype`
- `slice_id`: `2026-06-15-p2-20-product-workflow-prototype`
- `scope`: sandbox-only with no runtime, sync, dependency, MCP-write, commit, or
  push flags enabled
- `source_screening_ref`: P2-19 product experience screening prototype
- `workflow_questions`: the five P2 use-surface questions
- `steps`: ordered workflow steps
- `non_claims`: explicit authority boundaries

Every step must include:

- `id`
- `surface`
- `p2_px_ref`
- `purpose`
- `input_contract`
- `output_contract`
- `required_validators`
- `blocking_states`
- `boundary_copy`
- `allowed_user_value`
- `forbidden_implications`
- `authority_flags` with all authority-changing flags explicitly `false`

## Required Steps

```text
WF-01 capability_boundary
WF-02 onboarding
WF-03 home_status
WF-04 layer_badge
WF-05 quick_capture
WF-06 candidate_funnel
WF-07 review_due
WF-08 context_export
WF-09 hash_receipt
WF-10 dirty_guardrail
WF-11 action_boundary_exit
```

`WF-11` is an explicit exit guard: it does not create action basis, but shows
that action basis requires separate action readiness and evidence sufficiency.

## Hard Boundaries

The workflow must not:

- write reviewed truth;
- approve review;
- promote wiki claims, patterns, or decisions;
- infer action readiness;
- mutate truth confidence;
- create evidence support or reviewed relations;
- treat status, badge, activity, hash, export, navigation, onboarding, or
  dashboard display as authority;
- create production UI, real Bases, sync, runtime, dependency install, MCP write
  tools, commit, push, or hooks.

## Non-Claims

Passing this workflow validator only proves internal sandbox consistency. It is
not Product Acceptance, reviewed knowledge, evidence support, action basis,
mainline readiness, product release approval, commit, push, or sync.
