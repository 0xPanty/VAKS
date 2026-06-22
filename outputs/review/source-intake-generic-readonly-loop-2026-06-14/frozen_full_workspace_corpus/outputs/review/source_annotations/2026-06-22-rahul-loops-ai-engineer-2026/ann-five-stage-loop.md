---
record_kind: source_annotation
status: captured
knowledge_status: candidate
processing_tier: light
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
annotation_id: ann-2026-06-22-rahul-loops-five-stage-loop
source_ref: raw/articles/2026-06-22-rahul-loops-ai-engineer-2026-source.md
working_copy_ref: raw/articles/2026-06-22-rahul-loops-ai-engineer-2026-source/pasted-text.txt
source_snapshot_ref: raw/articles/2026-06-22-rahul-loops-ai-engineer-2026-source/pasted-text.txt
external_annotation_id:
selector_type: TextQuoteSelector
selector_exact: "Every loop — no matter how simple or complex — moves through"
selector_prefix: "At its simplest, one agent works on itself:"
selector_suffix: "the same 5 stages:"
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
annotation_role: term_definition
body_note: "Pins the article's five-stage loop skeleton as a candidate workflow vocabulary for later inspection."
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
  - loop-engineering
  - review-input
---

# Five-Stage Loop Skeleton

## Boundary

This annotation is a locator and review input only.

It does not prove that the five-stage loop is correct, complete, reviewed, or action-ready.

## Intended Use

Inspect this source span when designing or comparing agent workflow templates:

```text
Discover -> Plan -> Execute -> Verify -> Iterate
```
