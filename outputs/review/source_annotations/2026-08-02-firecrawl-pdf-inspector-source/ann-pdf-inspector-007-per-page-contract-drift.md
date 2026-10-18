---
record_kind: source_annotation
status: captured
knowledge_status: candidate
processing_tier: light
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
annotation_id: ann-pdf-inspector-007-per-page-contract-drift
source_ref: "raw/repos/2026-08-02-firecrawl-pdf-inspector-source.md"
working_copy_ref: "https://github.com/firecrawl/pdf-inspector/blob/a15ec2d68d51dbe6a39d1da688ec7a3f642d846c/src/lib.rs#L457-L576"
source_snapshot_ref: "raw/repos/_snapshots/firecrawl-pdf-inspector-a15ec2d.zip"
external_annotation_id: null
selector_type: file_line_range
selector_exact: "extract_pages_markdown_mem"
selector_prefix: "Per-page markdown extraction"
selector_suffix: "is_complex"
selector_position: "src/lib.rs:457-576"
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
body_note: "Layout metadata uses items/rects/lines, but per-page Markdown passes empty line/structure inputs. Page index and coordinate semantics also vary across APIs/bindings."
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
tags: "[source-annotation, api-contract, page-index, risk-signal]"
---

# Source Annotation：per-page metadata/rendering contract drift

## Boundary

This is a static source-review risk signal; runtime impact has not been tested.

## Source Span

```yaml
selector_position: src/lib.rs:457-576
related_positions:
  - src/lib.rs:5508-5585
  - src/types.rs:96-114
  - src/python.rs:618-640
  - napi/src/lib.rs:309-368
  - wasm/src/lib.rs:8-65
anchor_status: exact_verified
```

## Annotation Body

Metadata can identify a line-based table while page Markdown omits the line and
tagged-table inputs. A VAKS adapter should normalize page bases, coordinates,
reason codes, and renderer inputs behind one contract.

## Review Routing

Risk input for any future implementation sandbox.

## Forbidden

```text
automatic defect severity
binding parity assumption
action basis
```

