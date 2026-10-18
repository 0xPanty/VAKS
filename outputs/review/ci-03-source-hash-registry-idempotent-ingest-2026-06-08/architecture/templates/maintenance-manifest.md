---
record_type: maintenance-manifest
status: open
created:
updated: 2026-05-31
scope:
generated_by:
tags:
  - maintenance
  - lint
---

# Maintenance Manifest

## Scope


## Items

```yaml
items:
  - item_type: missing_required_field | unsupported_claim | stale_dependency | validity_window_mismatch | confidence_cap_violation | missing_intent_confirmation | missing_outcome_calibration | orphan_review_candidate | missing_relation_target | missing_source_anchor | missing_evidence_packet | missing_omission_check | missing_context_pack_trace | agent_memory_quarantine_violation
    target_ref:
    severity: low | medium | high
    reason:
    suggested_action: add_source_anchor | add_evidence_support | add_evidence_packet | add_omission_check | add_context_pack_trace | quarantine_agent_memory | mark_review_due | add_intent_confirmation | record_outcome | narrow_scope | ask_user | needs_review
    status: open | resolved | parked
```

## Boundary

```text
Maintenance manifest is lint.
It may create review pressure.
It must not rewrite reviewed knowledge automatically.
Test, benchmark, fixture, and LLM-judge results are lint / diagnostic input.
They may report what was measured, what was not measured, negative coverage, side-effect scope, and forbidden interpretations.
They must not create truth confidence, benchmark authority, reviewer status, runtime readiness, mainline readiness, or a new eval/test template family.
```
