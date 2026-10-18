---
record_kind: source_annotation
status: captured
knowledge_status: candidate
processing_tier: light
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
annotation_id: ann-pdf-inspector-008-benchmark-diagnostic-gates
source_ref: "raw/repos/2026-08-02-firecrawl-pdf-inspector-source.md"
working_copy_ref: "https://github.com/firecrawl/pdf-inspector/blob/a15ec2d68d51dbe6a39d1da688ec7a3f642d846c/docs/benchmarking.md#L3-L62"
source_snapshot_ref: "raw/repos/_snapshots/firecrawl-pdf-inspector-a15ec2d.zip"
external_annotation_id: null
selector_type: file_line_range
selector_exact: "The paired harness runs two pdf2md binaries"
selector_prefix: "Benchmarking against OpenDataLoader"
selector_suffix: "backend disagreement as automatically correct"
selector_position: "docs/benchmarking.md:3-62"
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
body_note: "Same-corpus paired evaluation exposes overall, missing-output, and per-document regressions; alternate-backend disagreement opens inspection instead of declaring the alternate correct."
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
tags: "[source-annotation, benchmark, regression-gate, diagnostic]"
---

# Source Annotation：paired parser regression gates

## Boundary

This locator identifies a diagnostic method, not a readiness or truth gate.

## Source Span

```yaml
selector_position: docs/benchmarking.md:3-62
related_positions:
  - scripts/bench_opendataloader.py:64-167
  - scripts/probe_backend_evidence.py:171-212
anchor_status: exact_verified
```

## Annotation Body

The useful shape is fixed-envelope comparison plus worst-case inspection. The
published 200-document benchmark remains scoped to its corpus, evaluator,
hardware, versions, and OCR-disabled configuration.

## Review Routing

Candidate input for parser maintenance manifests.

## Forbidden

```text
truth confidence
mainline readiness
automatic promotion
```

