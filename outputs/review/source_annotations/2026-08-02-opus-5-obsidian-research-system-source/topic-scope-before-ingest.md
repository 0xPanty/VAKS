---
record_kind: source_annotation
status: captured
knowledge_status: candidate
processing_tier: medium
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
annotation_id: opus5-topic-scope-before-ingest
source_ref: raw/articles/2026-08-02-opus-5-obsidian-research-system-source.md
working_copy_ref:
source_snapshot_ref: raw/articles/2026-08-02-opus-5-obsidian-research-system-source/pasted-text.txt
external_annotation_id:
selector_type: line_range
selector_value: "pasted-text.txt:108-121"
selector_exact:
selector_prefix:
selector_suffix:
selector_position: "pasted-text.txt:108-121"
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
annotation_role: candidate_seed
body_note: "This passage makes topic scope an ingestion input, asks cross-topic links to be explicit, and distinguishes scoped subfolders from fully isolated vaults according to desired cross-retrieval."
blocked_reason:
next_action: map_to_project_overlay_context_scope_and_applicability_without_new_lane
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
  - topic-scope
  - cross-topic-link
  - candidate-seed
---

# Source Annotation: Topic Scope Before Ingest

## Locator

```yaml
source_snapshot_ref: raw/articles/2026-08-02-opus-5-obsidian-research-system-source/pasted-text.txt
selector_type: line_range
selector_value: pasted-text.txt:108-121
anchor_status: exact_verified
```

## Why This Span Matters

This is a genuinely incremental control:

```text
decide topic/project scope before ingestion
make cross-topic connections explicit
generate routine digests inside scope
preserve cross-pollination only where desired
```

For VAKS, scope belongs to Project Overlay, context-pack selection, and applicability. Folder/vault placement is an implementation detail, not a truth boundary or reviewed relation.

## Boundary

This annotation is a locator and review input only. It does not create a new VAKS lane, prescribe a vault split, or establish a cross-topic relation.

