---
record_kind: source_annotation
status: captured
annotation_id: odysseus-external-context-effect-gate
knowledge_status: candidate
processing_tier: medium
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
source_ref: raw/repos/2026-08-24-odysseus-dev-odysseus-source.md
source_snapshot_ref: "https://github.com/odysseus-dev/odysseus/blob/b4d12932a953b3cdfc745b3525c7ecd5dffd8b3c/src/tool_capabilities.py"
selector_type: line_range
selector_value: "src/tool_capabilities.py:586-662"
selector_exact: "Server-owned integrity state for one agent run."
source_hash: b4d12932a953b3cdfc745b3525c7ecd5dffd8b3c
content_hash: 80e9a52de70c46076739fa1cb0cf592f5e316d500d5bb1c1838628750ee3667c
content_hash_scope: full_source_file
anchor_status: exact_verified
anchor_checked_at: 2026-08-24
anchor_stale: false
anchor_match_count: 1
annotation_role: candidate_seed
body_note: "External untrusted context becomes server-owned run state; high-impact or unknown tool effects require a separate user-authorized action before dispatch."
next_action: inspect_source_span
support_checked: false
evidence_support_status: not_checked
candidate_refs:
  - outputs/review/2026-08-24-odysseus-dev-odysseus-candidate-distillation.md
project_overlay_refs: []
source_digest_required: false
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
  - prompt-injection
  - tool-effect-gate
  - review-input
---

# Source Annotation: External Context Effect Gate

## Locator

```yaml
source_snapshot_ref: https://github.com/odysseus-dev/odysseus/blob/b4d12932a953b3cdfc745b3525c7ecd5dffd8b3c/src/tool_capabilities.py
selector_type: line_range
selector_value: src/tool_capabilities.py:586-662
anchor_status: exact_verified
```

## Why This Span Matters

这段把“外部内容已影响当前 run”从 prompt 提示语提升为服务端运行状态，再按 tool effect 决定是否阻止私有读取、写入、代码执行、网络出口、外部副作用、管理变更或破坏性动作。未知能力 fail high。

对 VAKS，可候选借鉴的是“外部检索/工具结果不自动授权”，不是把 taint 当作 truth、evidence support 或安全证明。

## Related Anchor

`src/prompt_security.py:8-26;64-99` 是对应的 untrusted message 包装入口。包装是 defense in depth，不替代本段确定性 dispatch gate。

## Boundary

This annotation is a locator and review input only. It is not evidence support, reviewed knowledge, a Project Overlay verdict, or action basis.
