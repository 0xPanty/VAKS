---
record_kind: source_annotation
status: captured
knowledge_status: candidate
processing_tier: medium
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
annotation_id: opus5-direct-vault-write-mcp-risk
source_ref: raw/articles/2026-08-02-opus-5-obsidian-research-system-source.md
working_copy_ref:
source_snapshot_ref: raw/articles/2026-08-02-opus-5-obsidian-research-system-source/pasted-text.txt
external_annotation_id:
selector_type: line_range
selector_value: "pasted-text.txt:103-107"
selector_exact:
selector_prefix:
selector_suffix:
selector_position: "pasted-text.txt:103-107"
selector_timestamp_start:
selector_timestamp_end:
selector_page:
selector_rect:
source_hash: 63CCB9472E75A3D0CE099DD74A440C6816EEE8CEAADC9EDF3D89A0CF1406C73C
content_hash:
anchor_status: exact_verified
anchor_checked_at: 2026-08-02
anchor_stale: false
anchor_match_count: 1
annotation_role: risk_signal
body_note: "This passage moves from manual copy-paste to direct MCP/REST reads, writes, real-note edits, and unattended schedules; the official plugin surface is broader than the article's simple connectivity test suggests."
blocked_reason:
next_action: require_path_scope_tool_allowlist_key_isolation_rollback_and_receipts_before_any_pilot
support_checked: false
evidence_support_status: not_checked
evidence_packet_ref:
candidate_refs:
  - outputs/review/2026-08-02-opus-5-obsidian-research-system-candidate-distillation.md
project_overlay_refs:
  - outputs/review/project_overlays/VAKS/VAKS-opus-5-obsidian-research-system-2026-08-02.md
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
  - mcp
  - direct-write
  - risk-signal
---

# Source Annotation: Direct Vault Write / MCP Risk

## Locator

```yaml
source_snapshot_ref: raw/articles/2026-08-02-opus-5-obsidian-research-system-source/pasted-text.txt
selector_type: line_range
selector_value: pasted-text.txt:103-107
anchor_status: exact_verified
```

## Why This Span Matters

The article crosses an important authority boundary here:

```text
manual read/copy
-> direct API/MCP read and write
-> edits to real notes
-> unattended scheduled calls
```

The official plugin repository exposes tools beyond read/write, including append, patch, delete, move, and command execution. A successful list-files test confirms connectivity only; it does not establish least privilege, prompt-injection safety, rollback, or write authority.

## Boundary

This annotation is a locator and risk input only. It is not permission to install the plugin, expose an API key, connect MCP, schedule a task, or write to the vault.

