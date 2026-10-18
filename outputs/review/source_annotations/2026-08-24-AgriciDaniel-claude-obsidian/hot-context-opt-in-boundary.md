---
record_kind: source_annotation
status: captured
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
annotation_id: claude-obsidian-hot-context-opt-in-boundary
source_ref: raw/repos/2026-08-24-AgriciDaniel-claude-obsidian-source.md
working_copy_ref:
source_snapshot_ref: raw/repos/_snapshots/2026-08-24-AgriciDaniel-claude-obsidian-1c1bc49-source.zip
external_annotation_id:
selector_type: line_range
selector_value: "claude_obsidian/hook_adapter.py:172-214"
selector_exact: "def session_start_context("
selector_prefix:
selector_suffix:
selector_position: "claude_obsidian/hook_adapter.py:172-214"
source_hash: 1c1bc49c03a685ee8f5d09c99efe52b42d6673f5
content_hash: "sha256:544f998113957a9b12b78839c767e387f3c1f0c3004e4067ebec0b638c57a99e"
anchor_status: exact_verified
anchor_checked_at: 2026-08-24
anchor_stale: false
anchor_match_count: 1
annotation_role: candidate_seed
body_note: "Pin the SessionStart context path: default off, exact opt-in, vault resolution, bounded hot.md read and untrusted-data envelope."
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
  - hot-context
  - untrusted-data
---

# Source Annotation：Hot Context Opt-In Boundary

## Locator

    selector_value: claude_obsidian/hook_adapter.py:172-214
    anchor_status: exact_verified

## Why This Span Matters

这个 span 证明 SessionStart 注入不是默认自治记忆：它必须显式 opt-in，先解析 vault，只读 hot.md，再把内容放入禁止执行指令的 untrusted envelope。

## Boundary

hot 只能做 orientation。这个 locator 不证明 hot 内容正确，也不允许其进入 evidence 或 action basis。

