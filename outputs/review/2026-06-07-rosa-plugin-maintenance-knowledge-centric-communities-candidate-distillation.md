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
  - raw/papers/2026-06-07-rosa-plugin-maintenance-knowledge-centric-communities-source.md
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
scope: rosa-plugin-maintenance-knowledge-centric-communities-distillation
source_checked_at: 2026-06-07
borrow_value: strong
borrow_order:
  - "P1: plugin ecosystem belongs in runtime capability layer"
  - "P1: plugin taxonomy can guide VAKS tool/skill routing"
  - "P1: plugin health requires maintenance metrics, not popularity alone"
  - "P1: knowledge tools live between coding and thinking"
  - "P2: PR, issue, commit, contributor, and release cadence as adoption gates"
  - "P2: non-developer ecosystems can still show engineering structure"
  - "P2: Obsidian plugin categories as workbench map"
avoid:
  - "Do not treat plugin output as authority."
  - "Do not treat PR activity as safety, quality, or truth."
  - "Do not treat LLM topic model output as final taxonomy."
  - "Do not import full Obsidian plugin runtime into VAKS core."
  - "Do not install community plugins by default."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "Designing VAKS plugin/skill registry, tool adoption gate, or runtime workbench."
  support_when: "Comparing plugin ecosystems, skill ecosystems, MCP/API surfaces, or workbench capabilities."
  risk_when: "Any plugin output, dashboard, or maintenance metric is treated as reviewed knowledge."
  cold_references:
    - raw/papers/2026-06-07-rosa-plugin-maintenance-knowledge-centric-communities-source.md
routing_hint:
  - plugin-ecosystem
  - skill-registry
  - runtime-workbench
  - tool-adoption-gate
tags:
  - candidate
  - provisional
  - paper-distillation
  - obsidian
  - plugin-ecosystem
borrow_tags:
  - P1/plugin_ecosystem_as_runtime_capability_layer
  - P1/plugin_taxonomy_for_vaks_tool_routing
  - P1/plugin_health_requires_maintenance_metrics
  - P1/knowledge_tools_live_between_coding_and_thinking
  - P2/pr_issue_commit_release_as_plugin_adoption_gate
  - P2/non_developer_ecosystem_can_still_have_engineering_structure
  - P2/obsidian_plugin_categories_as_workbench_map
do_not_borrow_tags:
  - avoid/plugin_output_as_authority
  - avoid/pr_activity_as_safety_or_truth
  - avoid/llm_topic_model_as_final_taxonomy
  - avoid/full_obsidian_plugin_runtime_as_vaks_core
  - avoid/community_plugin_install_as_default
---

# Rosa et al. Plugin Maintenance Candidate Distillation

## Boundary

Candidate-only plugin ecosystem reference. It is not a plugin adoption decision and not reviewed VAKS truth.

## Plain-Language Takeaway

说人话：这篇说明 Obsidian 插件生态不是小玩具，它已经像一个知识工作插件生态。但对 VAKS 来说，插件永远是 runtime/workbench 能力，不是知识本体。

## Candidate Points

### 1. Plugins are runtime capability, not truth

Plugins can help write, organize, sync, link, script, visualize, and automate, but cannot bypass review.

### 2. Plugin taxonomy can guide tool routing

The six broad categories can become a future VAKS tool/skill map:

```text
dynamic editing and organization
interface and layouts
creative writing and productivity
knowledge sync solutions
linking and script tools
workflow enhancement tools
```

### 3. Adoption needs maintenance signals

Before relying on a plugin/tool, inspect issues, commits, releases, contributors, and PR flow, not only stars or claims.

### 4. Knowledge work and coding tools are converging

VAKS skill/plugin design should assume tools support thinking workflows, not only software production.

## Open Questions

- What minimal plugin/skill adoption checklist should VAKS use?
- Should VAKS maintain its own tool taxonomy before adding more helpers?
- Which plugin categories are safe as read-only workbench first?
