---
record_kind: source_annotation
annotation_id: als-tournament-judge-calibration
knowledge_status: candidate
processing_tier: medium
annotation_scope: source_local_anchor
source_ref: raw/repos/2026-06-23-gaasher-Agent-Loop-Skills-source.md
working_copy_ref:
source_snapshot_ref: raw/repos/_snapshots/2026-06-23-gaasher-Agent-Loop-Skills-25dd18f-source.zip
selector_type: line_range
selector_value: "loops/tournament-autoresearch/SKILL.md:19-25; loops/tournament-autoresearch/SKILL.md:92-102; loops/tournament-autoresearch/SKILL.md:125-131; loops/tournament-autoresearch/SKILL.md:153-169"
selector_exact: "Judge predicts, run measures realized delta, calibration ledger updates judge lessons"
selector_prefix:
selector_suffix:
source_hash: 25dd18fc93523c212addd46fad540c779b18515a
content_hash:
anchor_status: exact_verified
anchor_checked_at: 2026-06-23
anchor_stale: false
anchor_match_count:
annotation_role: risk_signal
body_note: "This span is useful for measurable operator loops but risky for VAKS truth: judge calibration can improve selection, not create confidence or support."
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
  - tournament-autoresearch
  - judge-calibration
---

# Source Annotation: Tournament Judge Calibration

## Locator

```yaml
source_snapshot_ref: raw/repos/_snapshots/2026-06-23-gaasher-Agent-Loop-Skills-25dd18f-source.zip
selector_type: line_range
selector_value: loops/tournament-autoresearch/SKILL.md:19-25; loops/tournament-autoresearch/SKILL.md:92-102; loops/tournament-autoresearch/SKILL.md:125-131; loops/tournament-autoresearch/SKILL.md:153-169
anchor_status: exact_verified
```

## Why This Span Matters

This is a useful but risky mechanism:

```text
judge predicts which idea will improve a metric
real run measures the result
calibration ledger compares predicted vs realized
judge updates working lessons/rubric
```

For VAKS/MISA it may improve measurable selection heuristics. It must not become truth confidence, review approval, or action basis.

## Boundary

This annotation is a locator and review input only.

It is not evidence support, reviewed knowledge, a Project Overlay verdict, or action basis.
