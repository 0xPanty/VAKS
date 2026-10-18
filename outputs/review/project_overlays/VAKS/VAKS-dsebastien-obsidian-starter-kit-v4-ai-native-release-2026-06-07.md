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
target_ref: outputs/review/2026-06-07-dsebastien-obsidian-starter-kit-v4-ai-native-release-candidate-distillation.md
source_card: raw/articles/2026-06-07-dsebastien-obsidian-starter-kit-v4-ai-native-release-source.md
target_selector: ai_native_starter_kit_runtime
target_hint: "Use for VAKS skill registry, typed workbench schema, AI conversation log, and generated content boundary."
borrow_tags:
  - P1/typed_vault_schema_plugin
  - P1/skill_registry_and_skill_router
  - P1/fewer_agents_more_skills
  - P1/ai_conversation_log_as_memory_source
  - P2/ai_generated_content_isolation
  - P2/bases_graph_explorer_as_workbench
do_not_borrow_tags:
  - avoid/commercial_template_as_core_architecture
  - avoid/mcp_write_access_default
  - avoid/ai_maintained_wiki_as_reviewed_truth
  - avoid/identity_health_layer_as_vaks_core
project_reopen_trigger:
  - "When designing VAKS skills registry or helper routing."
  - "When designing typed workbench records."
  - "When deciding how to store AI conversation logs."
confirmation_basis: "Public page observed on 2026-06-07 with HTTP 200 and HTML hash."
last_checked_at: 2026-06-07
expires_at:
---

# VAKS Overlay: dSebastien Obsidian Starter Kit v4

## Boundary

Project-side borrowing only. This does not adopt the commercial template, plugins, MCP tools, or AI-maintained wiki.

## Project Borrow Scope

- Typed vault schema as workbench design reference.
- Skill registry and skill router.
- Fewer agents, more explicit skills.
- AI conversation log as memory/use-ledger input.
- AI-generated content isolation.
- Bases/Graph Explorer as workbench view only.

## Project Non-Borrow Scope

- No commercial template as VAKS architecture.
- No default write-enabled MCP/CLI/agent.
- No AI-maintained wiki as reviewed truth.
- No identity/health/life tracking in VAKS core.
