---
record_kind: source_annotation
annotation_id: let-artifact-kind-domain-field
knowledge_status: candidate
processing_tier: medium
annotation_scope: source_local_anchor
source_ref: raw/repos/2026-06-23-AI-Builder-Club-loop-engineer-template-source.md
working_copy_ref:
source_snapshot_ref: raw/repos/_snapshots/2026-06-23-AI-Builder-Club-loop-engineer-template-a226735-source.zip
selector_type: line_range
selector_value: "ARCHITECTURE.md:16-25; ARCHITECTURE.md:27-37; ARCHITECTURE.md:39-52; ARCHITECTURE.md:54-59; ARCHITECTURE.md:78-83"
selector_exact: "artifacts are global by kind; domain is a field; domains are loops that link artifacts; new kinds must be earned"
selector_prefix:
selector_suffix:
source_hash: a2267355209713a2184eaeef3b276ec680219d2b
content_hash:
anchor_status: exact_verified
anchor_checked_at: 2026-06-23
anchor_stale: false
anchor_match_count:
annotation_role: candidate_seed
body_note: "This span is the best anchor for the template's anti-sprawl data model: store by artifact kind, route by domain field, and add new kinds only when a status machine, fields, and body shape justify them."
blocked_reason:
next_action: inspect_source_span
support_checked: false
evidence_support_status: not_checked
evidence_packet_ref:
candidate_refs:
  - outputs/review/2026-06-23-AI-Builder-Club-loop-engineer-template-candidate-distillation.md
project_overlay_refs:
  - outputs/review/project_lens_overlays/2026-06-23-AI-Builder-Club-loop-engineer-template-vaks-loop-engineering-overlay.md
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
  - schema-discipline
  - domain-field
---

# Source Annotation: Artifact Kind, Domain Field

## Locator

```yaml
source_snapshot_ref: raw/repos/_snapshots/2026-06-23-AI-Builder-Club-loop-engineer-template-a226735-source.zip
selector_type: line_range
selector_value: ARCHITECTURE.md:16-25; ARCHITECTURE.md:27-37; ARCHITECTURE.md:39-52; ARCHITECTURE.md:54-59; ARCHITECTURE.md:78-83
anchor_status: exact_verified
```

## Why This Span Matters

This span contains the cleanest schema discipline in the repo:

```text
artifact storage = by kind
loop routing = domain field and links
domain folder = live loop state and machinery
new kind = only after status machine + query fields + body shape
```

For VAKS, this is useful as a candidate anti-sprawl rule, not as a replacement for VAKS's stricter authority layers.

## Boundary

This annotation is a locator and review input only.

It is not evidence support, reviewed knowledge, a Project Overlay verdict, or action basis.

