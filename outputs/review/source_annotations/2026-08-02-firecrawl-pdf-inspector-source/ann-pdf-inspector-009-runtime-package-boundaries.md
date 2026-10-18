---
record_kind: source_annotation
status: captured
knowledge_status: candidate
processing_tier: light
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
annotation_id: ann-pdf-inspector-009-runtime-package-boundaries
source_ref: "raw/repos/2026-08-02-firecrawl-pdf-inspector-source.md"
working_copy_ref: "https://github.com/firecrawl/pdf-inspector/blob/a15ec2d68d51dbe6a39d1da688ec7a3f642d846c/src/lib.rs#L5746-L5772"
source_snapshot_ref: "raw/repos/_snapshots/firecrawl-pdf-inspector-a15ec2d.zip"
external_annotation_id: null
selector_type: file_line_range
selector_exact: "validate_pdf_bytes"
selector_prefix: "Validate that a byte buffer looks like a PDF"
selector_suffix: "validate_pdf_bytes(&buf[..n])"
selector_position: "src/lib.rs:5746-5772"
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
body_note: "Public validation checks PDF magic in the first 1024 bytes; path loading then reads the full file. Local caps exist, but host-level bytes/pages/time/memory/output budgets remain necessary."
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
tags: "[source-annotation, resource-budget, packaging, security-boundary]"
---

# Source Annotation：runtime and package boundaries

## Boundary

This is a static risk locator, not a vulnerability finding or legal conclusion.

## Source Span

```yaml
selector_position: src/lib.rs:5746-5772
related_positions:
  - src/lib.rs:3392-3450
  - src/extractor/content_stream.rs:233-254
  - src/structure_tree.rs:478-491
  - Cargo.toml:1-57
  - pyproject.toml:5-13
  - napi/package.json:1-55
anchor_status: exact_verified
```

## Annotation Body

The library has useful local caps but not one unified host budget. Future use
must record distribution/version/commit/binary hash, isolate untrusted inputs,
and verify bundled CMap packaging and notices in the actual artifact.

## Review Routing

Risk input for implementation preflight only.

## Forbidden

```text
confirmed vulnerability
legal advice
production approval
```
