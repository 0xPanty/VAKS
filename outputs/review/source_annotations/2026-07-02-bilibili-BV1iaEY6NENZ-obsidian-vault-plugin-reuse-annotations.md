---
type: source_annotation
record_kind: source_annotation
source_id: bilibili-BV1iaEY6NENZ
source_card: raw/videos/2026-07-02-bilibili-BV1iaEY6NENZ-obsidian-vault-plugin-reuse-source.md
created: 2026-07-02
created_by: Codex
knowledge_status: candidate
processing_tier: medium
annotation_scope: source_local_anchor
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: review_input_only
  action_basis_allowed: false
  warning_code: annotation_not_support
anchor_status: exact_verified
anchor_checked_at: 2026-07-02
anchor_stale: false
next_action: inspect_source_span
support_checked: false
evidence_support_status: not_checked
action_basis_allowed: false
truth_mutation_allowed: false
---

# Source Annotations: BV1iaEY6NENZ Obsidian Vault Plugin Reuse

These annotations are locators for later inspection only. They are not evidence support, adoption decisions, reviewed truth, or action basis.

## A1: Vault-local configuration explains repeated plugin setup

- source_anchor: `segments.md` 00:23-00:48
- locator: `raw/videos/2026-07-02-bilibili-BV1iaEY6NENZ-obsidian-vault-plugin-reuse-source/segments.md`
- why_pin: Explains the root cause: `.obsidian` configuration is per vault, so plugins/themes/hotkeys do not automatically carry over.
- candidate_use: background for configuration-layer separation.
- next_action: verify against Obsidian local folder behavior if used in docs.

## A2: Copy only plugin folder, not whole `.obsidian`

- source_anchor: `segments.md` 00:51-01:10
- locator: `raw/videos/2026-07-02-bilibili-BV1iaEY6NENZ-obsidian-vault-plugin-reuse-source/segments.md`
- why_pin: Useful caution against copying workspace/local UI state across vaults.
- candidate_use: operational warning for beginners.
- next_action: check which plugin settings are stored under plugin folders before presenting as complete migration.

## A3: Symlink / shared configuration vault

- source_anchor: `segments.md` 02:02-04:12
- locator: `raw/videos/2026-07-02-bilibili-BV1iaEY6NENZ-obsidian-vault-plugin-reuse-source/segments.md`
- why_pin: Main reusable pattern: separate real configuration storage from multiple consuming vaults.
- candidate_use: VAKS sandbox / disposable-vault setup idea.
- next_action: test in a disposable vault before any formal recommendation.

## A4: Agent skills central directory analogy

- source_anchor: `segments.md` 04:12-04:36
- locator: `raw/videos/2026-07-02-bilibili-BV1iaEY6NENZ-obsidian-vault-plugin-reuse-source/segments.md`
- why_pin: Suggests the same pattern for multiple agent tools sharing Skills.
- candidate_use: possible future tooling reference.
- next_action: treat as analogy until specific tools and path semantics are verified.
