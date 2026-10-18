---
record_kind: source_annotation
status: captured
knowledge_status: candidate
processing_tier: light
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
annotation_id: ann-pdf-inspector-002-single-load-positioned-extraction
source_ref: "raw/repos/2026-08-02-firecrawl-pdf-inspector-source.md"
working_copy_ref: "https://github.com/firecrawl/pdf-inspector/blob/a15ec2d68d51dbe6a39d1da688ec7a3f642d846c/src/lib.rs#L3558-L3640"
source_snapshot_ref: "raw/repos/_snapshots/firecrawl-pdf-inspector-a15ec2d.zip"
external_annotation_id: null
selector_type: file_line_range
selector_exact: "fn process_document"
selector_prefix: "Core processing pipeline operating on a pre-loaded document"
selector_suffix: "result"
selector_position: "src/lib.rs:3558-3640"
selector_timestamp_start: null
selector_timestamp_end: null
selector_page: null
selector_rect: null
source_hash: "sha256:A15AE3C5CB4A290F6FA594A690AC3D3FA6E7B0473E7F7A1A962172B04A01A815"
content_hash: null
anchor_status: exact_verified
anchor_checked_at: "2026-08-02"
anchor_stale: false
anchor_match_count: 1
annotation_role: candidate_seed
body_note: "Detection and extraction reuse one loaded Document. Combined with TextItem page/position/font/MCID fields, this is a candidate retained-extraction shape."
blocked_reason: null
next_action: inspect_source_span
support_checked: false
evidence_support_status: not_checked
evidence_packet_ref: null
candidate_refs: "[outputs/review/2026-08-02-firecrawl-pdf-inspector-candidate-distillation.md]"
project_overlay_refs: "[outputs/review/project_overlays/VAKS/VAKS-firecrawl-pdf-inspector-2026-08-02.md]"
source_digest_required: false
source_digest_ref: null
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: review_input_only
  action_basis_allowed: false
  warning_code: annotation_not_support
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
tags: "[source-annotation, positioned-text, single-load, candidate-seed]"
---

# Source Annotation：single-load positioned extraction

## Boundary

This is a source locator and candidate seed only.

## Source Span

```yaml
selector_position: src/lib.rs:3558-3640
related_positions:
  - src/types.rs:96-132
  - src/extractor/content_stream.rs:131-220
anchor_status: exact_verified
```

## Annotation Body

The source shares one parsed document across detection and extraction, while the
public text item retains page and geometry. This may inform a VAKS extraction
receipt; it does not validate the extracted content.

## Review Routing

Route to the PDF adapter candidate only.

## Forbidden

```text
evidence support
truth mutation
dependency approval
```

