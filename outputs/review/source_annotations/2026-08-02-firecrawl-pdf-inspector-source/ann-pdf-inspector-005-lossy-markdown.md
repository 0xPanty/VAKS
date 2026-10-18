---
record_kind: source_annotation
status: captured
knowledge_status: candidate
processing_tier: light
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
annotation_id: ann-pdf-inspector-005-lossy-markdown
source_ref: "raw/repos/2026-08-02-firecrawl-pdf-inspector-source.md"
working_copy_ref: "https://github.com/firecrawl/pdf-inspector/blob/a15ec2d68d51dbe6a39d1da688ec7a3f642d846c/src/markdown/mod.rs#L848-L907"
source_snapshot_ref: "raw/repos/_snapshots/firecrawl-pdf-inspector-a15ec2d.zip"
external_annotation_id: null
selector_type: file_line_range
selector_exact: "impl Default for MarkdownOptions"
selector_prefix: "Options for markdown conversion"
selector_suffix: "strip_headers_footers: true"
selector_position: "src/markdown/mod.rs:848-907"
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
body_note: "Default Markdown removes page numbers, omits page markers and images, and strips repeated headers/footers. It is an activation artifact, not the original source."
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
tags: "[source-annotation, markdown, transformed-evidence, risk-signal]"
---

# Source Annotation：default Markdown is lossy

## Boundary

This is a risk locator, not evidence that every conversion loses critical text.

## Source Span

```yaml
selector_position: src/markdown/mod.rs:848-907
related_positions:
  - src/markdown/mod.rs:1584-1599
  - src/markdown/convert.rs:520-625
  - src/markdown/mod.rs:1644-1655
anchor_status: exact_verified
```

## Annotation Body

The default output is optimized presentation/activation material. Cross-page
table merging and image placeholders add further transformation. Preserve the
original PDF and page/region mapping.

## Review Routing

Risk input for transformed-evidence review.

## Forbidden

```text
original-source equivalence
no-omission guarantee
action basis
```

