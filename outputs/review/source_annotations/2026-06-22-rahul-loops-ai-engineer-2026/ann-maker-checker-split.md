---
record_kind: source_annotation
status: captured
knowledge_status: candidate
processing_tier: light
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
annotation_id: ann-2026-06-22-rahul-loops-maker-checker-split
source_ref: raw/articles/2026-06-22-rahul-loops-ai-engineer-2026-source.md
working_copy_ref: raw/articles/2026-06-22-rahul-loops-ai-engineer-2026-source/pasted-text.txt
source_snapshot_ref: raw/articles/2026-06-22-rahul-loops-ai-engineer-2026-source/pasted-text.txt
external_annotation_id:
selector_type: TextQuoteSelector
selector_exact: "Keep the maker away from the checker."
selector_prefix: "5. SUBAGENTS"
selector_suffix: "The model that wrote the code is too nice grading its own homework."
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
annotation_role: implementation_note
body_note: "Pins the maker/checker split as a candidate verification hygiene principle for agent workflows."
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
  - subagents
  - review-input
---

# Maker / Checker Split

## Boundary

This is not evidence that a checker agent is sufficient for review.

It is a locator for a candidate implementation hygiene idea: separate the agent that makes an artifact from the agent or process that verifies it.

## Intended Use

Use when comparing review-loop designs, subagent delegation, or multi-agent execution patterns.
