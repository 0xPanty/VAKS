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
target_ref: outputs/review/2026-06-07-rosa-plugin-maintenance-knowledge-centric-communities-candidate-distillation.md
source_card: raw/papers/2026-06-07-rosa-plugin-maintenance-knowledge-centric-communities-source.md
target_selector: obsidian_plugin_ecosystem_study
target_hint: "Use for VAKS skill/plugin ecosystem, tool adoption gates, and runtime workbench taxonomy."
borrow_tags:
  - P1/plugin_ecosystem_as_runtime_capability_layer
  - P1/plugin_taxonomy_for_vaks_tool_routing
  - P1/plugin_health_requires_maintenance_metrics
  - P1/knowledge_tools_live_between_coding_and_thinking
  - P2/pr_issue_commit_release_as_plugin_adoption_gate
  - P2/obsidian_plugin_categories_as_workbench_map
do_not_borrow_tags:
  - avoid/plugin_output_as_authority
  - avoid/pr_activity_as_safety_or_truth
  - avoid/llm_topic_model_as_final_taxonomy
  - avoid/full_obsidian_plugin_runtime_as_vaks_core
  - avoid/community_plugin_install_as_default
project_reopen_trigger:
  - "When adding VAKS plugin/skill registry or tool adoption policy."
  - "When evaluating Obsidian plugins, MCP servers, or helper runtimes."
confirmation_basis: "arXiv abstract/PDF observed on 2026-06-07; accepted-to-SANER2026 note recorded."
last_checked_at: 2026-06-07
expires_at:
---

# VAKS Overlay: Obsidian Plugin Maintenance Study

## Boundary

Project-side plugin ecosystem reference only. It cannot justify installing or trusting plugins.

## Project Borrow Scope

- Plugin ecosystem as runtime capability layer.
- Tool/skill routing taxonomy.
- Maintenance metrics as adoption input.
- Coding/thinking workflow convergence.
- Obsidian plugin categories as workbench map.

## Project Non-Borrow Scope

- Plugin output is not authority.
- PR activity is not safety or truth.
- LLM topic labels are not final taxonomy.
- Community plugins are not default dependencies.
