---
fixture_id: ci05-pass-scope-dashboard
expected_result: PASS
record_type: scope-dashboard
scope_id: vaks-ci05
scope_name: VAKS CI-05 Trial
scope_type: project
not_truth_layer: true
not_evidence_support: true
not_action_basis: true
selection_status: candidate_only
core_candidates:
  - id: core-01
    path: architecture/DEV_CONTEXT.md
    reason: defines temporary dev context pack role
support_candidates:
  - id: support-01
    path: evidence/dusk/template-area-anchor-snapshot.md
    reason: shows area dashboard source anchor
risk_candidates:
  - id: risk-01
    path: architecture/wiki/patterns/scope-dashboard-live-context-surface.md
    reason: dashboard can be mistaken for truth authority
task_candidates:
  - id: task-01
    note: run one local dev-context selection trial
cold_reference_candidates:
  - id: cold-01
    path: raw/repos/2026-05-27-dusk-obsidian-vault-source.md
last_refreshed: 2026-06-08
---

# PASS: Scope Dashboard Candidate Surface

This dashboard surfaces candidates only. It does not select the final dev
context pack by itself.

