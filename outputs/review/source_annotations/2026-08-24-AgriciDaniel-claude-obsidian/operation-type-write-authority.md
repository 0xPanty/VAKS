---
record_kind: source_annotation
status: captured
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
annotation_id: claude-obsidian-operation-type-write-authority
source_ref: raw/repos/2026-08-24-AgriciDaniel-claude-obsidian-source.md
working_copy_ref:
source_snapshot_ref: raw/repos/_snapshots/2026-08-24-AgriciDaniel-claude-obsidian-1c1bc49-source.zip
external_annotation_id:
selector_type: line_range
selector_value: "claude_obsidian/transaction.py:3130-3235"
selector_exact: "def _validate_operation_write_scope("
selector_prefix:
selector_suffix:
selector_position: "claude_obsidian/transaction.py:3130-3235"
source_hash: 1c1bc49c03a685ee8f5d09c99efe52b42d6673f5
content_hash: "sha256:a64a762704f7a7e7ccdff5334d28ba92a4cf4e7129be48eb570d23f56649e58d"
anchor_status: exact_verified
anchor_checked_at: 2026-08-24
anchor_stale: false
anchor_match_count: 1
annotation_role: candidate_seed
body_note: "Pin the mechanical mapping from operation type to allowed write paths; the label acts as a capability boundary rather than descriptive metadata."
blocked_reason:
next_action: inspect_source_span
support_checked: false
evidence_support_status: not_checked
evidence_packet_ref:
candidate_refs:
  - outputs/review/2026-08-24-AgriciDaniel-claude-obsidian-candidate-distillation.md
project_overlay_refs:
  - outputs/review/project_overlays/2026-08-24-AgriciDaniel-claude-obsidian-vaks-transaction-and-evidence-overlay.md
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
  - write-scope
  - capability-boundary
---

# Source Annotation：Operation Type as Write Authority

## Locator

    selector_value: claude_obsidian/transaction.py:3130-3235
    anchor_status: exact_verified

## Why This Span Matters

该 span 让 operation type 真正限制 setup、migration、mode、fold、capture、ingest 等操作的写域。VAKS 可借这一不变量，避免 receipt 字段只记录却不约束 write-set。

## Boundary

这不是 action authority；它只描述通过该 core 执行时的路径能力限制。

