---
record_kind: source_annotation
status: captured
knowledge_status: candidate
processing_tier: light
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
annotation_id: ann-2026-06-22-rahul-loops-closed-loop-first
source_ref: raw/articles/2026-06-22-rahul-loops-ai-engineer-2026-source.md
working_copy_ref: raw/articles/2026-06-22-rahul-loops-ai-engineer-2026-source/pasted-text.txt
source_snapshot_ref: raw/articles/2026-06-22-rahul-loops-ai-engineer-2026-source/pasted-text.txt
external_annotation_id:
selector_type: TextQuoteSelector
selector_exact: "Start with closed loops."
selector_prefix: "Which one should you use?"
selector_suffix: "Build a tight system that works reliably."
selector_position:
selector_timestamp_start:
selector_timestamp_end:
selector_page:
selector_rect:
source_hash: 4FD4D5E0FDBC016365447E96DDD55B79802F01C104FD8D3532D9CA857BBE89B5
content_hash:
anchor_status: exact_verified
anchor_checked_at: 2026-06-22
anchor_stale: false
anchor_match_count: 1
annotation_role: risk_signal
body_note: "Pins the practical advice to start bounded and gated before widening autonomy."
blocked_reason:
next_action: inspect_source_span
support_checked: false
evidence_support_status: not_checked
evidence_packet_ref:
candidate_refs:
  - outputs/review/2026-06-22-rahul-loops-ai-engineer-2026-candidate-distillation.md
project_overlay_refs: []
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
  - closed-loop
  - review-input
---

# Closed Loop First

## Boundary

This annotation is a source-local locator only.

It does not create a universal ban on open loops and does not authorize an automated loop.

## Intended Use

Use this span as a review-input reminder when someone proposes broad autonomy before there is a quality gate, scope boundary, or stop condition.
