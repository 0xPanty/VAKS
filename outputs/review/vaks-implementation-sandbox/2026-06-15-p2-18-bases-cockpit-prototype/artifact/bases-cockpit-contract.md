---
record_kind: sandbox_contract
slice_id: 2026-06-15-p2-18-bases-cockpit-prototype
status: implemented_pending_review
truth_boundary: sandbox_contract_only
---

# Bases Cockpit Contract

## Intent

Describe a Bases-style cockpit package that makes VAKS review, context,
feedback, and operator status visible without creating a real Obsidian Bases
implementation or authority-changing workflow.

## Required Bases

| Base | Purpose | Required columns | Boundary |
|---|---|---|---|
| `review-candidates.base` | review queue visibility | `review_status`, `review_object_state`, `body_hash`, `promotion_target`, `missing_evidence`, `risk_flags` | cannot approve |
| `context-packs.base` | context/action visibility | `query_mode`, `evidence_sufficiency.state`, `action_readiness.state`, `warnings`, `gaps` | cannot infer ready |
| `feedback-events.base` | feedback pressure | `event_kind`, `target_ref`, `project_ref`, `review_pressure_effect`, `query_run_ref` | cannot mutate truth |
| `operator-cockpit.base` | total cockpit | `blocked`, `stale`, `missing_anchor`, `hash_mismatch`, `action_not_ready` | cannot replace validators |

## Manifest Inputs

A valid cockpit prototype has:

- `scope`: sandbox-only write and runtime boundaries.
- `bases`: four required base definitions.
- `navigation`: links among cockpit surfaces and source artifacts.
- `operator_states`: display-only blocked/stale/missing-anchor/hash/action
  readiness states.
- `non_claims`: explicit non-authority declarations.

## Non-Claims

Passing this sandbox is not:

- real Obsidian Bases implementation;
- reviewed knowledge;
- evidence support;
- reviewer approval;
- action basis;
- promotion readiness;
- mainline readiness;
- production UI approval;
- Obsidian sync permission;
- commit or push permission.
