---
record_kind: source_annotation
status: captured
knowledge_status: candidate
processing_tier: light
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
annotation_id: ann-pdf-inspector-003-text-quality-ocr-reasons
source_ref: "raw/repos/2026-08-02-firecrawl-pdf-inspector-source.md"
working_copy_ref: "https://github.com/firecrawl/pdf-inspector/blob/a15ec2d68d51dbe6a39d1da688ec7a3f642d846c/src/text_quality.rs#L250-L300"
source_snapshot_ref: "raw/repos/_snapshots/firecrawl-pdf-inspector-a15ec2d.zip"
external_annotation_id: null
selector_type: file_line_range
selector_exact: "analyze_text_quality"
selector_prefix: "pub(crate) fn"
selector_suffix: "reasons_by_page"
selector_position: "src/text_quality.rs:250-300"
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
body_note: "The parser accumulates page-level decoding evidence and emits explicit OCR reasons. Treat these as routing warnings, not semantic correctness or source trust."
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
tags: "[source-annotation, text-quality, ocr-routing, warning-code]"
---

# Source Annotation：page-level text quality and OCR reasons

## Boundary

This record identifies a routing mechanism, not a verified quality score.

## Source Span

```yaml
selector_position: src/text_quality.rs:250-300
related_positions:
  - src/text_quality.rs:1-25
  - src/lib.rs:125-157
  - src/lib.rs:3774-3874
anchor_status: exact_verified
```

## Annotation Body

Localized decoding signals accumulate into page-level OCR reasons. VAKS may
borrow the explicit warning shape, while keeping the original page and adapter
receipt available for review.

## Review Routing

Candidate input for PDF routing design.

## Forbidden

```text
semantic correctness
truth confidence
action basis
```

