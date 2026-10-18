---
record_kind: project_overlay
status: candidate
knowledge_status: candidate
processing_tier: medium
overlay_state: confirmed
overlay_scope: project_sidecar_only
overlay_storage: confirmed_persistent_project_bucket
retrieval_scope: active_project_only
default_retrieval: false
retrieval_policy:
  policy_kind: project_context_only
  default_scope: project_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: overlay_not_authority
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
project_id: verified-action-knowledge-system
target_ref: outputs/review/2026-06-07-trustedsec-obsidian-vault-structure-candidate-distillation.md
source_card: raw/repos/2026-06-07-trustedsec-obsidian-vault-structure-source.md
target_selector: team_operational_vault_template
target_hint: "Use as low-priority reference for team capture friction, template routing, and Git/personal boundary."
borrow_tags:
  - P1/team_operational_knowledge_needs_low_friction_capture
  - P1/master_template_routes_note_type_and_destination
  - P1/content_type_tags_for_ttp_tool_idea_documentation
  - P2/primary_secondary_categories_as_moc_navigation
  - P2/git_managed_vault_with_personal_gitignore_boundary
do_not_borrow_tags:
  - avoid/security_team_vault_as_general_vaks_schema
  - avoid/emoji_tags_as_authority
  - avoid/graph_view_as_truth_or_relation
  - avoid/obsidian_git_auto_sync_as_default
  - avoid/plugin_template_runtime_as_core_architecture
project_reopen_trigger:
  - "When designing low-friction team capture or template-based source creation."
  - "When designing shared vault Git/personal-data boundaries."
confirmation_basis: "GitHub repo and companion blog observed on 2026-06-07; main commit c408d4914a7bd98f1a5628e0067c84ab4b3a0a1a."
last_checked_at: 2026-06-07
expires_at:
---

# VAKS Overlay: TrustedSec Obsidian Vault Structure

## Boundary

Legacy team-vault reference only. It cannot define VAKS schema, plugin runtime, sync policy, or reviewed relations.

## Project Borrow Scope

- Low-friction capture for team operational knowledge.
- Master template that routes note type and destination.
- TTP / Tool / Idea / Documentation as example capture types.
- MoC categories as navigation.
- Personal files excluded from shared Git.

## Project Non-Borrow Scope

- No security-team folder tree as VAKS schema.
- No emoji tag authority.
- No graph view as truth.
- No default auto-sync.
