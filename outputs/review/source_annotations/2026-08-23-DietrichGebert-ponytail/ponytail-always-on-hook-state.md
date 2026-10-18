---
record_kind: source_annotation
status: captured
knowledge_status: candidate
processing_tier: medium
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
annotation_id: ponytail-always-on-hook-state
source_ref: raw/repos/2026-08-23-DietrichGebert-ponytail-source.md
working_copy_ref:
source_snapshot_ref: raw/repos/_snapshots/2026-08-23-DietrichGebert-ponytail-2ed6c52-source.zip
external_annotation_id:
selector_type: line_range
selector_value: "hooks/ponytail-activate.js:4-41"
selector_exact: "Runs on every session start"
selector_prefix:
selector_suffix:
selector_position: "hooks/ponytail-activate.js:4-41"
source_hash: 2ed6c52c9d7e5e56942508591085fd45dea277d3
content_hash: "sha256:6d16ab136a5e790a3b7f07c8a86725df1ddec9cf0cfeb6aaed28b9665f7105f3"
anchor_status: exact_verified
anchor_checked_at: 2026-08-23
anchor_stale: false
anchor_match_count: 1
annotation_role: risk_signal
body_note: "Pin the runtime side effects: session-start mode-state write and hidden ruleset injection; this is not appropriate as a VAKS default without a demonstrated runtime need."
blocked_reason:
next_action: inspect_source_span
support_checked: false
evidence_support_status: not_checked
evidence_packet_ref:
candidate_refs:
  - outputs/review/2026-08-23-DietrichGebert-ponytail-candidate-distillation.md
project_overlay_refs:
  - outputs/review/project_overlays/2026-08-23-DietrichGebert-ponytail-vaks-minimalism-overlay.md
source_digest_required: false
source_digest_ref:
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: review_input_only
  action_basis_allowed: false
  warning_code: annotation_not_support
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
tags:
  - source-annotation
  - lifecycle-hook
  - hidden-context
  - state-write
---

# Source Annotation：Always-On Hook State And Hidden Context

## Locator

```yaml
source_snapshot_ref: raw/repos/_snapshots/2026-08-23-DietrichGebert-ponytail-2ed6c52-source.zip
selector_type: line_range
selector_value: hooks/ponytail-activate.js:4-41
anchor_status: exact_verified
```

## Why This Span Matters

该 hook 在 session start 写 mode state，并把 ruleset 作为隐藏上下文发出。对当前 VAKS，这属于 future Agent Tool Safety / runtime risk reference，而不是默认应该安装的能力。

## Boundary

这是 source-local risk locator，不是 Project Overlay verdict、security finding、安装指令或 action basis。
