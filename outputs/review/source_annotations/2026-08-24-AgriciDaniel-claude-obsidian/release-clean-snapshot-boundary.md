---
record_kind: source_annotation
status: captured
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
annotation_id: claude-obsidian-release-clean-snapshot-boundary
source_ref: raw/repos/2026-08-24-AgriciDaniel-claude-obsidian-source.md
working_copy_ref:
source_snapshot_ref: raw/repos/_snapshots/2026-08-24-AgriciDaniel-claude-obsidian-1c1bc49-source.zip
external_annotation_id:
selector_type: line_range
selector_value: "claude_obsidian/release.py:732-834"
selector_exact: "def _git_snapshot("
selector_prefix:
selector_suffix:
selector_position: "claude_obsidian/release.py:732-834"
source_hash: 1c1bc49c03a685ee8f5d09c99efe52b42d6673f5
content_hash: "sha256:6eb7471d597a88ab8342dd4ae4baa2124a1a5cf10f147e0a16051609cc3548db"
anchor_status: exact_verified
anchor_checked_at: 2026-08-24
anchor_stale: false
anchor_match_count: 1
annotation_role: candidate_seed
body_note: "Pin the sanitized Git snapshot routine used to bind release inputs to a fixed HEAD/index state and reject dirty or ambiguous payload sources."
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
  - release
  - clean-snapshot
---

# Source Annotation：Release Clean Snapshot Boundary

## Locator

    selector_value: claude_obsidian/release.py:732-834
    anchor_status: exact_verified

## Why This Span Matters

release 输入被绑定到清洁的 Git HEAD/index，而不是任意 worktree。未来 VAKS product/export 可借 fixed-snapshot contract，但当前 publishing surface 仍 parked。

## Boundary

这是 release hygiene locator，不是完整隐私、安全、供应链或发布批准证明。

