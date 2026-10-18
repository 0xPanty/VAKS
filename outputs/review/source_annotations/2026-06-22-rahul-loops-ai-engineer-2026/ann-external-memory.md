---
record_kind: source_annotation
status: captured
knowledge_status: candidate
processing_tier: light
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
annotation_id: ann-2026-06-22-rahul-loops-external-memory
source_ref: raw/articles/2026-06-22-rahul-loops-ai-engineer-2026-source.md
working_copy_ref: raw/articles/2026-06-22-rahul-loops-ai-engineer-2026-source/pasted-text.txt
source_snapshot_ref: raw/articles/2026-06-22-rahul-loops-ai-engineer-2026-source/pasted-text.txt
external_annotation_id:
selector_type: TextQuoteSelector
selector_exact: "A markdown file. A Linear board. Anything that lives outside the single conversation."
selector_prefix: "The spine of the whole loop."
selector_suffix: "The model forgets everything between runs."
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
annotation_role: candidate_seed
body_note: "Pins the external-memory idea as a candidate pattern for handoff, ledger, and project-visible artifact practice."
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
  - memory
  - handoff
  - review-input
---

# External Memory For Loops

## Boundary

This annotation is not evidence that a specific memory implementation is correct.

It is a locator for the article's claim that durable state outside the single conversation is central to long-running loops.

## Intended Use

Use when designing handoff, ledger, progress, or workflow-memory surfaces for agent loops.
