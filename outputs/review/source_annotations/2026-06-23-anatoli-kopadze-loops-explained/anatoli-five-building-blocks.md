---
record_kind: source_annotation
annotation_id: anatoli-five-building-blocks
knowledge_status: candidate
processing_tier: medium
annotation_scope: source_local_anchor
source_ref: raw/articles/2026-06-23-anatoli-kopadze-loops-explained-source.md
working_copy_ref:
source_snapshot_ref: raw/articles/2026-06-23-anatoli-kopadze-loops-explained-source/pasted-text.txt
selector_type: line_range
selector_value: "pasted-text.txt:63-73"
selector_exact: "five building blocks: automation, skill, sub-agents, connectors, verifier"
selector_prefix:
selector_suffix:
source_hash: 939BDC7966CDACAF8B9EE33B7128287697C06B61DB502ACA7F891EA120509D6E
content_hash:
anchor_status: exact_verified
anchor_checked_at: 2026-06-23
anchor_stale: false
anchor_match_count:
annotation_role: candidate_seed
body_note: "This span anchors the source's checklist of loop components, while product-specific capability claims remain unverified."
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
  - loop-building-blocks
  - verifier
---

# Source Annotation: Five Building Blocks

## Locator

```yaml
source_snapshot_ref: raw/articles/2026-06-23-anatoli-kopadze-loops-explained-source/pasted-text.txt
selector_type: line_range
selector_value: pasted-text.txt:63-73
anchor_status: exact_verified
```

## Why This Span Matters

This span gives a compact loop checklist:

```text
automation
skill
sub-agents
connectors
verifier
```

For VAKS, this is useful for comparing loop designs across sources. Product claims in the same span remain unverified.

## Boundary

This annotation is a locator and review input only.

It is not evidence support, reviewed knowledge, a Project Overlay verdict, or action basis.

