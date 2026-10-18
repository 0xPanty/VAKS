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
target_ref: outputs/review/2026-06-07-curiouslychase-ai-native-obsidian-vault-setup-guide-candidate-distillation.md
source_card: raw/articles/2026-06-07-curiouslychase-ai-native-obsidian-vault-setup-guide-source.md
target_selector: ai_native_obsidian_workbench
target_hint: "Use for VAKS workbench UX, AI logs, skill/command organization, and optional review cadence."
borrow_tags:
  - P1/agent_os_folder_for_commands_scripts_skills
  - P1/ai_log_as_operation_trace
  - P2/north_star_dashboard_quick_links_workbench
  - P2/periodic_review_cadence
  - P2/tag_taxonomy_for_ai_feedback_and_limitations
do_not_borrow_tags:
  - avoid/life_os_as_vaks_core_schema
  - avoid/plugin_runtime_as_truth_layer
  - avoid/agent_write_access_default
  - avoid/sensitive_life_modules_in_core
project_reopen_trigger:
  - "When designing VAKS daily dashboard or operation cockpit."
  - "When organizing commands/scripts/skills in the vault."
  - "When designing AI session log and feedback review cadence."
confirmation_basis: "Public page observed on 2026-06-07 with HTTP 200 and HTML hash."
last_checked_at: 2026-06-07
expires_at:
---

# VAKS Overlay: Curiously Chase AI-Native Obsidian Vault

## Boundary

Project workbench reference only. Do not treat personal OS structure, plugins, or dashboards as VAKS truth core.

## Project Borrow Scope

- Visible operating layer for commands, scripts, skills, and templates.
- AI Log as trace/use-ledger input.
- North Star / Dashboard / Quick Links as UX entrypoints.
- Optional periodic review cadence.
- Tag categories for AI workflow, limitation, and feedback signals.

## Project Non-Borrow Scope

- No life OS schema in VAKS core.
- No plugin runtime as truth layer.
- No default agent write access.
- No sensitive personal modules in the shared core.
