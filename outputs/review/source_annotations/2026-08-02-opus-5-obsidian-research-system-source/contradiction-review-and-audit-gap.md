---
record_kind: source_annotation
status: captured
knowledge_status: candidate
processing_tier: medium
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
annotation_id: opus5-contradiction-review-audit-gap
source_ref: raw/articles/2026-08-02-opus-5-obsidian-research-system-source.md
working_copy_ref:
source_snapshot_ref: raw/articles/2026-08-02-opus-5-obsidian-research-system-source/pasted-text.txt
external_annotation_id:
selector_type: line_range
selector_value: "pasted-text.txt:88-95"
selector_exact:
selector_prefix:
selector_suffix:
selector_position: "pasted-text.txt:88-95"
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
annotation_role: scope_limit
body_note: "The source correctly requires human judgment over error, temporal change, or contextual scope, but its example directly updates an old note without explicit superseding links, retained prior judgment, review receipt, or downstream review_due."
blocked_reason:
next_action: preserve_superseding_and_temporal_scope_semantics_in_any_future_use
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
  - contradiction
  - temporal-applicability
  - audit-gap
---

# Source Annotation: Contradiction Review And Audit Gap

## Locator

```yaml
source_snapshot_ref: raw/articles/2026-08-02-opus-5-obsidian-research-system-source/pasted-text.txt
selector_type: line_range
selector_value: pasted-text.txt:88-95
anchor_status: exact_verified
```

## Why This Span Matters

The strong part is the human decision frame:

```text
was the earlier source wrong?
did reality change?
are both statements valid under different scope?
```

The worked example exposes an audit gap: directly updating the old note can erase the prior judgment and its downstream consequences. VAKS needs explicit superseding, reason, scope, retained history, and review pressure.

## Boundary

This annotation is a locator and review input only. It does not resolve the contradiction, declare either source true, or authorize updating reviewed notes.

