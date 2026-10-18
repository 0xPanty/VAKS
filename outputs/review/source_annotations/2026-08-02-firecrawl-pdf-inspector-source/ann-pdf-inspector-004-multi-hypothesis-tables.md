---
record_kind: source_annotation
status: captured
knowledge_status: candidate
processing_tier: light
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
annotation_id: ann-pdf-inspector-004-multi-hypothesis-tables
source_ref: "raw/repos/2026-08-02-firecrawl-pdf-inspector-source.md"
working_copy_ref: "https://github.com/firecrawl/pdf-inspector/blob/a15ec2d68d51dbe6a39d1da688ec7a3f642d846c/src/lib.rs#L4042-L4108"
source_snapshot_ref: "raw/repos/_snapshots/firecrawl-pdf-inspector-a15ec2d.zip"
external_annotation_id: null
selector_type: file_line_range
selector_exact: "select_table_candidate"
selector_prefix: "A line grid that visibly collapses"
selector_suffix: "heuristic_substantially_better"
selector_position: "src/lib.rs:4042-4108"
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
body_note: "Table candidates carry source and issue information; suspicious vector fragments can be replaced by a substantially better clean heuristic or rejected."
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
tags: "[source-annotation, table-extraction, multi-hypothesis, candidate-seed]"
---

# Source Annotation：multi-hypothesis table selection

## Boundary

This locator does not establish that any detected table is semantically correct.

## Source Span

```yaml
selector_position: src/lib.rs:4042-4108
related_positions:
  - src/markdown/mod.rs:1247-1402
  - src/lib.rs:928-1093
anchor_status: exact_verified
```

## Annotation Body

The useful idea is to compare structural hypotheses and reject a tidy-looking
fragment when another clean candidate has materially more structure. Original
page and cell anchors remain required.

## Review Routing

Candidate implementation note for document/table adapters.

## Forbidden

```text
reviewed table semantics
automatic evidence support
action basis
```

