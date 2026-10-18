---
record_kind: source_annotation
status: captured
knowledge_status: candidate
processing_tier: medium
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
annotation_id: opus5-outcome-calibration-manual-first
source_ref: raw/articles/2026-08-02-opus-5-obsidian-research-system-source.md
working_copy_ref:
source_snapshot_ref: raw/articles/2026-08-02-opus-5-obsidian-research-system-source/pasted-text.txt
external_annotation_id:
selector_type: line_range
selector_value: "pasted-text.txt:122-131"
selector_exact:
selector_prefix:
selector_suffix:
selector_position: "pasted-text.txt:122-131"
selector_timestamp_start:
selector_timestamp_end:
selector_page:
selector_rect:
source_hash: 63CCB9472E75A3D0CE099DD74A440C6816EEE8CEAADC9EDF3D89A0CF1406C73C
content_hash:
anchor_status: exact_verified
anchor_checked_at: 2026-08-02
anchor_stale: false
anchor_match_count: 1
annotation_role: implementation_note
body_note: "This passage checks value against missed important items and actual cross-source query use, not only reading time, and delays scheduling until manual ingestion and digest runs have demonstrated acceptable behavior."
blocked_reason:
next_action: define_use_ledger_metrics_and_manual_pilot_receipts_before_automation
support_checked: false
evidence_support_status: not_checked
evidence_packet_ref:
candidate_refs:
  - outputs/review/2026-08-02-opus-5-obsidian-research-system-candidate-distillation.md
project_overlay_refs:
  - outputs/review/project_overlays/VAKS/VAKS-opus-5-obsidian-research-system-2026-08-02.md
source_digest_required: false
source_digest_ref:
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: review_input_only
  action_basis_allowed: false
  warning_code: annotation_not_support
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
tags:
  - source-annotation
  - outcome-calibration
  - omission
  - manual-first
---

# Source Annotation: Outcome Calibration And Manual-First Rollout

## Locator

```yaml
source_snapshot_ref: raw/articles/2026-08-02-opus-5-obsidian-research-system-source/pasted-text.txt
selector_type: line_range
selector_value: pasted-text.txt:122-131
anchor_status: exact_verified
```

## Why This Span Matters

This is the strongest incremental borrow in the article:

```text
time saved
+ significant omissions
+ human corrections
+ actual cross-source query use
+ manual pilot before scheduling
```

For VAKS, these belong in outcome calibration and the Use Ledger. Positive feedback remains weak; omissions and explicit corrections create review pressure but do not directly mutate truth confidence.

## Boundary

This annotation is a locator and implementation input only. It is not a measured result, an automation approval, a truth update, or action basis.

