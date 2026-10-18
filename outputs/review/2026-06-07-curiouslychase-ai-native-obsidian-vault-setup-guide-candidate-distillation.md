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
  - raw/articles/2026-06-07-curiouslychase-ai-native-obsidian-vault-setup-guide-source.md
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
scope: curiouslychase-ai-native-obsidian-vault-setup-distillation
source_checked_at: 2026-06-07
borrow_value: medium
borrow_order:
  - "P1: visible agent OS folder for commands, scripts, and skills"
  - "P1: AI Log as operation trace rather than reviewed knowledge"
  - "P2: North Star, Dashboard, and Quick Links as workbench entrypoints"
  - "P2: periodic review cadence as optional cooling/reactivation reference"
  - "P2: tag taxonomy for AI feedback and limitations"
  - "P3: Dataview/plugin templates as tool references"
avoid:
  - "Do not copy a life OS folder tree as VAKS core schema."
  - "Do not make Dataview, Kanban, or plugins required truth infrastructure."
  - "Do not default agent write access."
  - "Do not put sensitive life/health/finance/people modules into VAKS core."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "Designing VAKS daily workbench UX or AI operation trace conventions."
  support_when: "Discussing commands/scripts/skills organization, AI logs, dashboards, or review cadence."
  risk_when: "Any proposal imports personal life OS structure or plugin runtime into core."
  cold_references:
    - raw/articles/2026-06-07-curiouslychase-ai-native-obsidian-vault-setup-guide-source.md
routing_hint:
  - runtime-workbench
  - use-ledger
  - feedback
  - dev-context
tags:
  - candidate
  - provisional
  - article-distillation
  - obsidian
  - workbench
borrow_tags:
  - P1/agent_os_folder_for_commands_scripts_skills
  - P1/ai_log_as_operation_trace
  - P2/north_star_dashboard_quick_links_workbench
  - P2/periodic_review_cadence
  - P2/tag_taxonomy_for_ai_feedback_and_limitations
  - P3/dataview_plugin_templates_as_tool_reference
do_not_borrow_tags:
  - avoid/life_os_as_vaks_core_schema
  - avoid/plugin_runtime_as_truth_layer
  - avoid/agent_write_access_default
  - avoid/sensitive_life_modules_in_core
---

# Curiously Chase AI-Native Obsidian Vault Candidate Distillation

## Boundary

Candidate-only UX/workbench reference. Not reviewed knowledge, not schema, not action basis.

## Plain-Language Takeaway

说人话：这篇能补“用户每天怎么操作这个库”。它不是解决 VAKS 怎么判断真假，而是给 commands、skills、AI Log、dashboard 和周期复盘一个可借鉴的摆法。

## Candidate Points

### 1. Agent operating layer should be visible

Commands, scripts, skills, templates, and steering files should be findable as files, not hidden only in chat or app settings.

### 2. AI Log is a trace layer

AI conversation records can help recovery, feedback, and use-ledger analysis, but they remain operation trace, not reviewed knowledge.

### 3. Dashboard is entrypoint, not authority

North Star / Dashboard / Quick Links can help orient action, but cannot decide truth, priority, or review state.

### 4. Cadence is optional infrastructure

Daily/weekly/monthly review cadence can support cooling and reactivation, but should not burden ordinary source intake.
