---
record_kind: source_annotation
annotation_id: anatoli-self-checking-light-loop
knowledge_status: candidate
processing_tier: medium
annotation_scope: source_local_anchor
source_ref: raw/articles/2026-06-23-anatoli-kopadze-loops-explained-source.md
working_copy_ref:
source_snapshot_ref: raw/articles/2026-06-23-anatoli-kopadze-loops-explained-source/pasted-text.txt
selector_type: line_range
selector_value: "pasted-text.txt:92-124"
selector_exact: "self-checking loop prompt uses task, strict criteria, plan/do/verify/decide, score threshold, weakest-point repair, but lacks trigger/schedule/event autonomy"
selector_prefix:
selector_suffix:
source_hash: 939BDC7966CDACAF8B9EE33B7128287697C06B61DB502ACA7F891EA120509D6E
content_hash:
anchor_status: exact_verified
anchor_checked_at: 2026-06-23
anchor_stale: false
anchor_match_count:
annotation_role: implementation_note
body_note: "This span anchors a useful lightweight loop prompt and its boundary: model self-checking is not the same as autonomous scheduled execution or external verification."
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
  - self-checking-loop
  - light-loop
---

# Source Annotation: Self-Checking Light Loop

## Locator

```yaml
source_snapshot_ref: raw/articles/2026-06-23-anatoli-kopadze-loops-explained-source/pasted-text.txt
selector_type: line_range
selector_value: pasted-text.txt:92-124
anchor_status: exact_verified
```

## Why This Span Matters

This span gives a lightweight loop prompt:

```text
TASK
SUCCESS CRITERIA
PLAN
DO
VERIFY
DECIDE
threshold to stop
fix weakest point first
```

For VAKS, this is a useful low-friction pattern, but weaker than external gates because the model still grades itself.

## Boundary

This annotation is a locator and review input only.

It is not evidence support, reviewed knowledge, a Project Overlay verdict, or action basis.

