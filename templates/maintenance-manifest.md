---
record_type: maintenance-manifest
status: open
created:
updated:
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
  - item_type: missing_required_field | unsupported_claim | stale_dependency | validity_window_mismatch | confidence_cap_violation | missing_intent_confirmation | missing_outcome_calibration | orphan_review_candidate | missing_relation_target
    target_ref:
    severity: low | medium | high
    reason:
    suggested_action: add_source_anchor | add_evidence_support | mark_review_due | add_intent_confirmation | record_outcome | narrow_scope | ask_user | needs_review
    status: open | resolved | parked
```

## Boundary

```text
Maintenance manifest is lint.
It may create review pressure.
It must not rewrite reviewed knowledge automatically.
```
