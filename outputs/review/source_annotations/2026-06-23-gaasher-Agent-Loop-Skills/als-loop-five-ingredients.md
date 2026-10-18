---
record_kind: source_annotation
annotation_id: als-loop-five-ingredients
knowledge_status: candidate
processing_tier: medium
annotation_scope: source_local_anchor
source_ref: raw/repos/2026-06-23-gaasher-Agent-Loop-Skills-source.md
working_copy_ref:
source_snapshot_ref: raw/repos/_snapshots/2026-06-23-gaasher-Agent-Loop-Skills-25dd18f-source.zip
selector_type: line_range
selector_value: "README.md:46-49; README.md:72-77; docs/skill-authoring-rules.md:28-37"
selector_exact: "loop = program + artifact slot + feedback signal + run ledger + termination/budget"
selector_prefix:
selector_suffix:
source_hash: 25dd18fc93523c212addd46fad540c779b18515a
content_hash:
anchor_status: exact_verified
anchor_checked_at: 2026-06-23
anchor_stale: false
anchor_match_count:
annotation_role: candidate_seed
body_note: "This is the main reusable source span: a loop is a skill/program with an artifact slot, real feedback signal, append-only ledger, and explicit stop/budget."
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
  - agentic-loops
  - loop-contract
---

# Source Annotation: Loop Five Ingredients

## Locator

```yaml
source_snapshot_ref: raw/repos/_snapshots/2026-06-23-gaasher-Agent-Loop-Skills-25dd18f-source.zip
selector_type: line_range
selector_value: README.md:46-49; README.md:72-77; docs/skill-authoring-rules.md:28-37
anchor_status: exact_verified
```

## Why This Span Matters

This span defines the source's core reusable abstraction:

```text
program
artifact slot
feedback signal
run ledger
termination / budget
```

For VAKS, this is a candidate seed for future bounded `loop_run` artifacts.

## Boundary

This annotation is a locator and review input only.

It is not evidence support, reviewed knowledge, a Project Overlay verdict, or action basis.
