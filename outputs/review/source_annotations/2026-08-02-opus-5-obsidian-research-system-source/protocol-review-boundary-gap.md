---
record_kind: source_annotation
status: captured
knowledge_status: candidate
processing_tier: medium
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
annotation_id: opus5-protocol-review-boundary-gap
source_ref: raw/articles/2026-08-02-opus-5-obsidian-research-system-source.md
working_copy_ref:
source_snapshot_ref: raw/articles/2026-08-02-opus-5-obsidian-research-system-source/pasted-text.txt
external_annotation_id:
selector_type: line_range
selector_value: "pasted-text.txt:28-48"
selector_exact:
selector_prefix:
selector_suffix:
selector_position: "pasted-text.txt:28-48"
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
body_note: "The protocol usefully encodes duplicate checks, links, contradictions, unresolved questions, and a completion check, but incorrectly treats model-processed wiki notes as a trustworthy layer without a review boundary."
blocked_reason:
next_action: map_protocol_steps_to_candidate_and_review_queue_boundaries
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
  - ingestion-protocol
  - review-boundary
  - scope-limit
---

# Source Annotation: Protocol Review-Boundary Gap

## Locator

```yaml
source_snapshot_ref: raw/articles/2026-08-02-opus-5-obsidian-research-system-source/pasted-text.txt
selector_type: line_range
selector_value: pasted-text.txt:28-48
anchor_status: exact_verified
```

## Why This Span Matters

The visible protocol is operationally useful: it requires duplicate inspection, linked claims, explicit contradictions, persistent unanswered questions, and a final check that existing material was actually inspected.

The boundary failure is equally important:

```text
model-processed != trustworthy
candidate comprehension != reviewed standing
```

For VAKS, the protocol can route raw material into candidates and review-queue inputs. It cannot make wiki notes reviewed merely by processing them.

## Boundary

This annotation is a locator and review input only. It is not evidence support, a review verdict, or permission to modify reviewed knowledge.

