---
record_kind: source_annotation
annotation_id: als-spawn-or-degrade-boundary
knowledge_status: candidate
processing_tier: medium
annotation_scope: source_local_anchor
source_ref: raw/repos/2026-06-23-gaasher-Agent-Loop-Skills-source.md
working_copy_ref:
source_snapshot_ref: raw/repos/_snapshots/2026-06-23-gaasher-Agent-Loop-Skills-25dd18f-source.zip
selector_type: line_range
selector_value: "docs/compatibility.md:26-43; docs/compatibility.md:45-56; docs/skill-authoring-rules.md:163-171"
selector_exact: "spawn real isolated subagents where supported; otherwise degrade to inline roles"
selector_prefix:
selector_suffix:
source_hash: 25dd18fc93523c212addd46fad540c779b18515a
content_hash:
anchor_status: exact_verified
anchor_checked_at: 2026-06-23
anchor_stale: false
anchor_match_count:
annotation_role: scope_limit
body_note: "This span is a portability warning: runtime role-file subagent dispatch is Claude-Code-specific; Codex/Cursor should use inline fallback unless separately configured."
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
  - subagents
  - portability
---

# Source Annotation: Spawn-Or-Degrade Host Boundary

## Locator

```yaml
source_snapshot_ref: raw/repos/_snapshots/2026-06-23-gaasher-Agent-Loop-Skills-25dd18f-source.zip
selector_type: line_range
selector_value: docs/compatibility.md:26-43; docs/compatibility.md:45-56; docs/skill-authoring-rules.md:163-171
anchor_status: exact_verified
```

## Why This Span Matters

This span prevents a bad VAKS/MISA adoption:

```text
do not assume real role-file subagent isolation on every host
declare spawn-or-degrade explicitly
keep output contract the same in fallback mode
```

For Codex-oriented work, this is a risk/source-limit anchor.

## Boundary

This annotation is a locator and review input only.

It is not evidence support, reviewed knowledge, a Project Overlay verdict, or action basis.
