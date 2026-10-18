---
record_kind: candidate_distillation
type: review-candidate
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: confirmed
review_pressure: none
derived_from:
  - raw/repos/2026-06-07-trustedsec-obsidian-vault-structure-source.md
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
v0_2_13_trigger: no
project: verified-action-knowledge-system
scope: trustedsec-obsidian-vault-structure-distillation
source_checked_at: 2026-06-07
borrow_value: low
borrow_order:
  - "P1: team operational knowledge needs low-friction capture"
  - "P1: master template routes note type and destination"
  - "P1: content type tags for TTP, Tool, Idea, and Documentation"
  - "P2: primary/secondary categories as MoC navigation"
  - "P2: Git-managed shared vault with personal .gitignore boundary"
  - "P2: organic link growth for shared navigation"
  - "P3: graph view and search tags as workbench navigation"
avoid:
  - "Do not use a security-team vault as general VAKS schema."
  - "Do not treat emoji tags as authority."
  - "Do not treat graph view as truth or reviewed relation."
  - "Do not default Obsidian Git auto-sync."
  - "Do not make plugin/template runtime core architecture."
dev_context_hint:
  default_layer: cold_reference
  core_only_when: "Designing low-friction team capture templates or personal/team workspace boundaries."
  support_when: "Comparing old team-vault practices for templates, Git, and MoC navigation."
  risk_when: "Any proposal treats legacy Obsidian plugin/template behavior as VAKS authority."
  cold_references:
    - raw/repos/2026-06-07-trustedsec-obsidian-vault-structure-source.md
routing_hint:
  - source-intake
  - team-workbench
  - template-routing
  - git-boundary
tags:
  - candidate
  - provisional
  - repo-distillation
  - obsidian
  - team-knowledge
borrow_tags:
  - P1/team_operational_knowledge_needs_low_friction_capture
  - P1/master_template_routes_note_type_and_destination
  - P1/content_type_tags_for_ttp_tool_idea_documentation
  - P2/primary_secondary_categories_as_moc_navigation
  - P2/git_managed_vault_with_personal_gitignore_boundary
  - P2/organic_link_growth_for_shared_navigation
  - P3/graph_view_and_search_tags_as_workbench_navigation
do_not_borrow_tags:
  - avoid/security_team_vault_as_general_vaks_schema
  - avoid/emoji_tags_as_authority
  - avoid/graph_view_as_truth_or_relation
  - avoid/obsidian_git_auto_sync_as_default
  - avoid/plugin_template_runtime_as_core_architecture
---

# TrustedSec Obsidian Vault Structure Candidate Distillation

## Boundary

Candidate-only legacy repository distillation. Not a VAKS schema, not a plugin adoption decision, and not action basis.

## Plain-Language Takeaway

说人话：这个老仓库有用的地方是“团队怎么愿意把操作知识写进来”。它不是 AI-native，也不是 verified knowledge system，但它抓住了协作知识库的摩擦：写入太麻烦，大家就不写。

## Candidate Points

### 1. Low-friction capture matters

If contribution feels like publishing a finished article, shared operational knowledge stalls.

### 2. Master template can reduce ambiguity

Prompting for title and type at note creation can route content into repeatable structures.

### 3. MoC categories are navigation, not truth

Primary/secondary category pages are maps of links. A note can appear in several maps.

### 4. Personal/team boundary must be explicit

Git-managed shared vaults need personal exclusions, plugin/workspace exclusions, and conflict policy.

## Open Questions

- Should VAKS light intake ask for a simple source type at creation time?
- What current-run files should never be synced or indexed?
- Is a small team-capture template useful later, separate from review templates?
