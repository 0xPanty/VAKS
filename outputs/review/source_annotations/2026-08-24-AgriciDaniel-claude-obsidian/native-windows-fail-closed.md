---
record_kind: source_annotation
status: captured
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
annotation_id: claude-obsidian-native-windows-fail-closed
source_ref: raw/repos/2026-08-24-AgriciDaniel-claude-obsidian-source.md
working_copy_ref:
source_snapshot_ref: raw/repos/_snapshots/2026-08-24-AgriciDaniel-claude-obsidian-1c1bc49-source.zip
external_annotation_id:
selector_type: line_range
selector_value: "docs/windows-wsl.md:7-33"
selector_exact: "## Platform support"
selector_prefix:
selector_suffix:
selector_position: "docs/windows-wsl.md:7-33"
source_hash: 1c1bc49c03a685ee8f5d09c99efe52b42d6673f5
content_hash: "sha256:99125545b58009ef18ee549c17051b1aba5bc755936f510de91715d63d4eb954"
anchor_status: exact_verified
anchor_checked_at: 2026-08-24
anchor_stale: false
anchor_match_count: 1
annotation_role: risk_flag
body_note: "Pin the platform contract: native Windows is read-only, supported mutation requires WSL/Linux semantics and stable file identity, and unsupported writes fail before side effects."
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
  - risk-flag
  - windows-wsl
---

# Source Annotation：Native Windows Fail-Closed

## Locator

    selector_value: docs/windows-wsl.md:7-33
    anchor_status: exact_verified

## Why This Span Matters

上游明确 native Windows 只读，写事务要求稳定文件身份和 WSL/Linux 语义，缺失时在副作用前拒绝。它直接限制当前 Windows + H: vault 的集成可行性。

## Boundary

这个风险 locator 不授权迁移 vault、启用 WSL、安装插件或试运行写路径。

