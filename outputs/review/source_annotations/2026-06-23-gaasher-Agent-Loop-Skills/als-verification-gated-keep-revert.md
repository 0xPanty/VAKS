---
record_kind: source_annotation
annotation_id: als-verification-gated-keep-revert
knowledge_status: candidate
processing_tier: medium
annotation_scope: source_local_anchor
source_ref: raw/repos/2026-06-23-gaasher-Agent-Loop-Skills-source.md
working_copy_ref:
source_snapshot_ref: raw/repos/_snapshots/2026-06-23-gaasher-Agent-Loop-Skills-25dd18f-source.zip
selector_type: line_range
selector_value: "README.md:51-55; loops/karpathy/SKILL.md:89-99; loops/optimize-loop/SKILL.md:16-31; loops/optimize-loop/SKILL.md:65-81"
selector_exact: "keep only if the bound signal says better; otherwise discard or revert"
selector_prefix:
selector_suffix:
source_hash: 25dd18fc93523c212addd46fad540c779b18515a
content_hash:
anchor_status: exact_verified
anchor_checked_at: 2026-06-23
anchor_stale: false
anchor_match_count:
annotation_role: implementation_note
body_note: "The strongest implementation pattern is verification-gated iteration: one change, same gate, same metric, keep only if valid/better, else revert and log."
blocked_reason:
next_action: inspect_source_span
support_checked: false
evidence_support_status: not_checked
evidence_packet_ref:
candidate_refs:
  - outputs/review/2026-06-23-gaasher-Agent-Loop-Skills-candidate-distillation.md
project_overlay_refs:
  - outputs/review/project_lens_overlays/2026-06-23-gaasher-Agent-Loop-Skills-vaks-agent-loop-overlay.md
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
  - verification-gate
  - keep-revert
---

# Source Annotation: Verification-Gated Keep/Revert

## Locator

```yaml
source_snapshot_ref: raw/repos/_snapshots/2026-06-23-gaasher-Agent-Loop-Skills-25dd18f-source.zip
selector_type: line_range
selector_value: README.md:51-55; loops/karpathy/SKILL.md:89-99; loops/optimize-loop/SKILL.md:16-31; loops/optimize-loop/SKILL.md:65-81
anchor_status: exact_verified
```

## Why This Span Matters

This is the operational core worth borrowing:

```text
one focused change
same gate
same metric
keep only if valid and better
otherwise discard/revert
append ledger row
```

For VAKS/MISA this can inform bounded operator loops, but the gate remains diagnostic until later review.

## Boundary

This annotation is a locator and review input only.

It is not evidence support, reviewed knowledge, a Project Overlay verdict, or action basis.
