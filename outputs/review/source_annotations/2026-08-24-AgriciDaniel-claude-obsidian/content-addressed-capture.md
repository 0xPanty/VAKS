---
record_kind: source_annotation
status: captured
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
annotation_id: claude-obsidian-content-addressed-capture
source_ref: raw/repos/2026-08-24-AgriciDaniel-claude-obsidian-source.md
working_copy_ref:
source_snapshot_ref: raw/repos/_snapshots/2026-08-24-AgriciDaniel-claude-obsidian-1c1bc49-source.zip
external_annotation_id:
selector_type: line_range
selector_value: "claude_obsidian/capture.py:908-1029"
selector_exact: "def plan_filesystem_batch("
selector_prefix:
selector_suffix:
selector_position: "claude_obsidian/capture.py:908-1029"
source_hash: 1c1bc49c03a685ee8f5d09c99efe52b42d6673f5
content_hash: "sha256:f5a000d28ca949981439d4426dbbbde5b2144d1d272a096e7e4f5fd93d9656b5"
anchor_status: exact_verified
anchor_checked_at: 2026-08-24
anchor_stale: false
anchor_match_count: 1
annotation_role: candidate_seed
body_note: "Pin filesystem batch planning and execution for content-addressed captured sources, including content-unchanged handling and transaction application."
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
  - source-capture
  - content-addressing
---

# Source Annotation：Content-Addressed Capture

## Locator

    selector_value: claude_obsidian/capture.py:908-1029
    anchor_status: exact_verified

## Why This Span Matters

这个 span 固定 filesystem batch 从 content hash 规划到 transaction apply 的主链。与前置 budget、symlink 和 TOCTOU 检查结合后，它是上游最适合 VAKS Capture 层的工程参考。

## Boundary

捕获成功只证明字节被固定，不证明来源权威、内容真实、候选点受支持或可用于行动。

