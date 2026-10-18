---
record_kind: source_annotation
annotation_id: anatoli-loop-worth-building-test
knowledge_status: candidate
processing_tier: medium
annotation_scope: source_local_anchor
source_ref: raw/articles/2026-06-23-anatoli-kopadze-loops-explained-source.md
working_copy_ref:
source_snapshot_ref: raw/articles/2026-06-23-anatoli-kopadze-loops-explained-source/pasted-text.txt
selector_type: line_range
selector_value: "pasted-text.txt:41-47"
selector_exact: "loop is worth building only when task repeats, bad output can be automatically rejected, agent can do work end-to-end, and done is objective"
selector_prefix:
selector_suffix:
source_hash: 939BDC7966CDACAF8B9EE33B7128287697C06B61DB502ACA7F891EA120509D6E
content_hash:
anchor_status: exact_verified
anchor_checked_at: 2026-06-23
anchor_stale: false
anchor_match_count:
annotation_role: risk_signal
body_note: "This span anchors a useful anti-overengineering gate: most tasks should not become heavy loops unless all four conditions pass."
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
  - loop-worthiness
  - anti-overengineering
---

# Source Annotation: Loop Worth Building Test

## Locator

```yaml
source_snapshot_ref: raw/articles/2026-06-23-anatoli-kopadze-loops-explained-source/pasted-text.txt
selector_type: line_range
selector_value: pasted-text.txt:41-47
anchor_status: exact_verified
```

## Why This Span Matters

This span gives a practical loop go/no-go test:

```text
task repeats at least weekly
bad output can be rejected automatically
agent can do the work end-to-end
done is objective
```

For VAKS, this prevents ordinary capture from becoming a needless heavy loop.

## Boundary

This annotation is a locator and review input only.

It is not evidence support, reviewed knowledge, a Project Overlay verdict, or action basis.

