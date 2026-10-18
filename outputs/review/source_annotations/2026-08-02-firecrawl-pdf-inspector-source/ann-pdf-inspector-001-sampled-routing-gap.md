---
record_kind: source_annotation
status: captured
knowledge_status: candidate
processing_tier: light
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
annotation_id: ann-pdf-inspector-001-sampled-routing-gap
source_ref: "raw/repos/2026-08-02-firecrawl-pdf-inspector-source.md"
working_copy_ref: "https://github.com/firecrawl/pdf-inspector/blob/a15ec2d68d51dbe6a39d1da688ec7a3f642d846c/src/detector.rs#L80-L88"
source_snapshot_ref: "raw/repos/_snapshots/firecrawl-pdf-inspector-a15ec2d.zip"
external_annotation_id: null
selector_type: file_line_range
selector_exact: "strategy: ScanStrategy::Sample(8)"
selector_prefix: "EarlyExit is too aggressive"
selector_suffix: "text_page_ratio_threshold: 0.6"
selector_position: "src/detector.rs:80-88"
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
annotation_role: risk_signal
body_note: "The actual default samples eight pages, while README says EarlyExit is default. Related logic at src/detector.rs:379-445 shows unsampled image pages are not a complete-document OCR guarantee."
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
tags: "[source-annotation, pdf-routing, sampling, risk-signal]"
---

# Source Annotation：default sampling and routing gap

## Boundary

This record says “inspect this span.” It does not prove a defect across all PDFs,
an extraction omission, or a VAKS design decision.

## Source Span

```yaml
source_snapshot_ref: raw/repos/_snapshots/firecrawl-pdf-inspector-a15ec2d.zip
selector_type: file_line_range
selector_position: src/detector.rs:80-88
related_positions:
  - README.md:215-231
  - src/detector.rs:379-445
anchor_status: exact_verified
```

## Annotation Body

The code default is `Sample(8)`, not the documented `EarlyExit`. For important
intake, inspect the full routing logic before interpreting an empty OCR list as
complete page coverage.

## Review Routing

This is a `risk_signal`; support has not been checked.

## Forbidden

```text
truth confidence
automatic bug verdict
action basis
```

