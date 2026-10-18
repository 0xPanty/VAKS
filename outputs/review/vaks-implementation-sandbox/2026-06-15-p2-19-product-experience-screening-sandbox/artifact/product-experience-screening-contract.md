---
record_kind: product_experience_screening_contract
slice_id: 2026-06-15-p2-19-product-experience-screening-sandbox
status: drafted
truth_boundary: sandbox_contract_only
---

# Product Experience Screening Contract

## Purpose

Screen the P2 product-experience backlog into a ranked, reusable sandbox
artifact before P2-20 product workflow work starts.

This contract intentionally does not create product UI, real Obsidian Bases,
reviewed knowledge, evidence support, action basis, or promotion.

## Required Output Shape

The screening artifact must be JSON with:

- `record_kind`: `vaks_product_experience_screening`
- `slice_id`: `2026-06-15-p2-19-product-experience-screening-sandbox`
- `scope`: sandbox-only and no runtime / sync / dependency / MCP-write /
  commit / push flags enabled
- `forbidden_import_controls`: product anti-patterns explicitly set to false
- `p2_20_handoff`: selected candidates for the next product workflow slice
- `candidates`: exactly P2-PX-01 through P2-PX-15
- `non_claims`: authority boundaries explicitly preserved

Each candidate must include:

- `id`
- `rank`
- `candidate`
- `decision`: one of `keep`, `park`, `reject`
- `source_inspiration`
- `target_layer`
- `required_validators`
- `boundary_warning`
- `minimal_wireflow`
- `rationale`
- `p2_20_role` for kept candidates
- `authority_flags` with all authority-changing flags set to false

Authority flags must be explicit. A candidate cannot rely on only a summary
switch; each authority-changing flag must be present and exactly `false`.

`required_validators` must use known validator names and include the
candidate-specific checks needed for its boundary warning.

## Candidate Set

```text
P2-PX-01 Capability Circle / Boundary Page
P2-PX-02 Quick Capture Inbox
P2-PX-03 Candidate Inbox / Review Funnel
P2-PX-04 Activation Timeline / Activity Calendar
P2-PX-05 Review Due Calendar
P2-PX-06 Context Pack / Evidence Packet Export
P2-PX-07 Mobile Capture Shell
P2-PX-08 Thin MCP / LLM Entry Surface
P2-PX-09 Product Onboarding
P2-PX-10 MISA Read-Only Context Entry
P2-PX-11 Home / Operator Status Surface
P2-PX-12 Total Research Map / MOC
P2-PX-13 One-Click Sync + Hash Receipt View
P2-PX-14 Layer Badge System
P2-PX-15 Worktree / Dirty-State Guardrail
```

## Screening Decisions

- `keep`: useful for P2-20 workflow design and can be expressed as a
  sandbox-only product flow without weakening VAKS.
- `park`: potentially useful but should wait for later product/runtime/tooling
  work or a stronger safety envelope.
- `reject`: bad fit or direct boundary violation for VAKS.

The P2-20 handoff must exactly match screening decisions:

- `selected_candidate_ids` equals all `keep` candidates;
- `parked_candidate_ids` equals all `park` candidates;
- `rejected_candidate_ids` equals all `reject` candidates;
- kept / selected candidates must carry a non-empty `p2_20_role`.

## Hard Boundaries

The screening artifact must not:

- approve candidates or reviewed knowledge;
- write reviewed truth;
- promote wiki claims/patterns/decisions;
- infer action readiness;
- mutate truth confidence;
- treat retrieval, graph, dashboard, rank, activity, heatmap, badge, hash,
  sync, export, or AI summary as evidence support;
- create real Obsidian Bases;
- build production UI;
- install dependencies;
- start runtime/server/background services;
- use MCP write tools;
- commit, push, sync, or run hooks.

## Verification

`artifact/product_experience_screening_validator.py` validates one screening
artifact. `artifact/verify_product_experience_screening.py` runs the prototype,
positive fixtures, and independent failure-case oracle.

The verifier reads expected failure codes from
`artifact/failure-case-oracle.json`; failure case files do not carry their own
expected result.

## Non-Claims

Passing this contract only proves the P2-19 sandbox screen is internally
consistent. It is not Product Acceptance, reviewer approval, reviewed knowledge,
evidence support, action basis, mainline readiness, or product release approval.
