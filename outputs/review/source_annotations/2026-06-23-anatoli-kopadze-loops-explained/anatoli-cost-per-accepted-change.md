---
record_kind: source_annotation
annotation_id: anatoli-cost-per-accepted-change
knowledge_status: candidate
processing_tier: medium
annotation_scope: source_local_anchor
source_ref: raw/articles/2026-06-23-anatoli-kopadze-loops-explained-source.md
working_copy_ref:
source_snapshot_ref: raw/articles/2026-06-23-anatoli-kopadze-loops-explained-source/pasted-text.txt
selector_type: line_range
selector_value: "pasted-text.txt:75-84"
selector_exact: "context re-sent every iteration; cost per accepted change matters; Ralph Wiggum loop silently bills without hard gate"
selector_prefix:
selector_suffix:
source_hash: 939BDC7966CDACAF8B9EE33B7128287697C06B61DB502ACA7F891EA120509D6E
content_hash:
anchor_status: exact_verified
anchor_checked_at: 2026-06-23
anchor_stale: false
anchor_match_count:
annotation_role: risk_signal
body_note: "This span anchors loop economics and silent-failure risk: track cost per accepted change, not just tokens or loop count."
blocked_reason:
next_action: inspect_source_span
support_checked: false
evidence_support_status: not_checked
evidence_packet_ref:
candidate_refs:
  - outputs/review/2026-06-23-anatoli-kopadze-loops-explained-candidate-distillation.md
project_overlay_refs:
  - outputs/review/project_lens_overlays/2026-06-23-anatoli-kopadze-loops-explained-vaks-loop-overlay.md
source_digest_required: false
source_digest_ref:
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: review_input_only
  action_basis_allowed: false
  warning_code: annotation_not_support
action_basis_allowed: false
truth_mutation_allowed: false
tags:
  - source-annotation
  - cost-control
  - accepted-change
---

# Source Annotation: Cost Per Accepted Change

## Locator

```yaml
source_snapshot_ref: raw/articles/2026-06-23-anatoli-kopadze-loops-explained-source/pasted-text.txt
selector_type: line_range
selector_value: pasted-text.txt:75-84
anchor_status: exact_verified
```

## Why This Span Matters

This span warns that loop cost compounds through repeated context reads, maker/checker passes, and parallel fleets.

Its best metric:

```text
cost per accepted change
```

For VAKS/MISA, this is a good loop health metric because rejected outputs still create review burden.

## Boundary

This annotation is a locator and review input only.

It is not evidence support, reviewed knowledge, a Project Overlay verdict, or action basis.

