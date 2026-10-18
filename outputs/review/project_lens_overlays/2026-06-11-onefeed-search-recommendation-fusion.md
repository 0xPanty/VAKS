---
record_kind: project_overlay
status: candidate
knowledge_status: candidate
processing_tier: heavy
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
promotion_gate: retrieval_layer_comparison_and_sandbox_required
action_basis_allowed: false
truth_mutation_allowed: false
project_id: VAKS
target_ref: outputs/review/2026-06-11-guoxun-onefeed-candidate-distillation.md
target_selector: "candidate source: arXiv:2606.07972 OneFeed"
target_hint:
  - type: workflow
    value: query-generation-assisted-retrieval
    status: conceptual
    anchor_version: 2026-06-11-source-review
  - type: workflow
    value: feedback-routing
    status: conceptual
    anchor_version: 2026-06-11-source-review
  - type: workspace
    value: outputs/review/vaks-retrieval-layer-design-2026-06-11
    status: active_candidate_workspace
    anchor_version: 2026-06-11-file-checked
project_borrow_scope: "Use OneFeed as a P2 design reference for controlled query generation, implicit/explicit intent fusion, and feedback-to-activation routing in the VAKS retrieval layer."
project_non_borrow_scope: "Do not use OneFeed's expected-performance tables as evidence; do not let generated queries bypass authority buckets; do not let feedback mutate truth confidence, reviewed relations, or action basis."
project_reopen_trigger: "Reopen if OneFeed publishes measured full-dataset results, code/data, or if a VAKS query-expansion sandbox shows improved recall without boundary violations."
confirmation_basis: "arXiv PDF/e-print captured 2026-06-11; source says results are expected estimates and full training is pending."
last_checked_at: 2026-06-11
expires_at: 2026-08-11
---

# Project Overlay: OneFeed Search-Recommendation Fusion

## Boundary

This is a VAKS project-scoped sidecar.

It does not adopt OneFeed, validate its results, change VAKS architecture, or
create reviewed knowledge.

## Project Borrow Scope

Borrow conceptually:

```text
explicit query + implicit active context
controlled query variants for candidate expansion
intent-anchor alignment
feedback routed to activation and query-rewrite quality
leakage checks for any future sandbox
```

## Project Non-Borrow Scope

Do not borrow:

```text
expected performance as benchmark evidence
weak pseudo-query labels as proof of real search quality
closed-loop feedback as truth mutation
generated semantic IDs as source authority
query generation that bypasses bucket filtering
recommendation business metrics as VAKS evidence sufficiency
```

## VAKS Placement

```text
Query Intent Router
-> Controlled Query Variants
-> Scope / Authority Bucket Filter
-> Hybrid Recall
-> Anchor Queue
-> Context Pack
-> Evidence / Action Gate
```

This source belongs in retrieval-layer design as a P2 reference, not in reviewed
truth, source reliability, or action-basis logic.

## Reopen Trigger

Reopen when either:

- OneFeed publishes measured full-dataset results or runnable code/data; or
- VAKS sandbox proves query variants improve recall while preserving bucket and
  source-anchor boundaries.
