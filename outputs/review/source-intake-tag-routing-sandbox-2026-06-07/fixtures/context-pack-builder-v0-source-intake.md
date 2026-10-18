---
record_kind: context_pack_manifest_candidate
status: candidate
created_at: 2026-06-07
pack_id: CPACK-source-intake-routing-fixture
mode: research
action_facing: false
truth_boundary: activation_pack_not_truth
artifact_registry_refs:
  - fixtures/artifact-registry-source-intake.md
allowed_use:
  - orientation
  - context_activation
  - drilldown
forbidden_use:
  - truth
  - reviewed_relation
  - action_basis
---

# Fixture: Context Pack Builder v0

## Pack Items

```yaml
items:
  - item_id: PI-001
    display_label: Current source intake rule
    lane: mainline_current
    source_ref: SOURCE_INTAKE.md
    selector_or_offset: "Retrieval Bucket Policy"
    snippet: "Current source intake retrieval boundary."
    snippet_status: navigation_snippet_not_evidence
    citable_status: drilldown_required
    action_basis_allowed: false
    why_included: "Defines current source intake retrieval boundary."

  - item_id: PI-002
    display_label: DataChain registry-before-recompute candidate
    lane: candidate_orientation
    source_ref: outputs/review/2026-06-06-datachain-ai-datachain-detailed-candidate-distillation.md
    selector_or_offset: "registry before recompute"
    snippet: "Suggests read-first registry UX."
    snippet_status: navigation_snippet_not_evidence
    citable_status: activation_only
    action_basis_allowed: false
    why_included: "Suggests read-first registry UX."

  - item_id: PI-003
    display_label: Mainline merge audit
    lane: audit_evidence
    source_ref: outputs/review/source-intake-control-flow-sandbox-2026-06-06/checks/mainline-merge-audit.md
    selector_or_offset: "Round2 mainline audit"
    snippet: "Audit evidence explains guardrail merge context."
    snippet_status: navigation_snippet_not_evidence
    citable_status: activation_only
    action_basis_allowed: false
    why_included: "Explains why the current guardrails were merged."
```

## Coverage Overview

```yaml
coverage_overview:
  supported: 0
  weakly_supported: 0
  challenged: 0
  missing_evidence:
    - evidence_support_check_not_run
  out_of_scope: 0
  risk_flags:
    - research_pack_not_action_basis
action_readiness:
  state: not_ready
  reason: "Research pack only; no action-facing evidence support check."
context_pack_trace:
  used_sources:
    - SOURCE_INTAKE.md
    - outputs/review/2026-06-06-datachain-ai-datachain-detailed-candidate-distillation.md
  ignored_sources:
    - old sandbox/package copies unless audit mode is requested
  ignored_reason: "Default noise control."
```
