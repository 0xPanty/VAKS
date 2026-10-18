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
  - raw/articles/2026-06-07-dsebastien-obsidian-starter-kit-v4-ai-native-release-source.md
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
scope: dsebastien-obsidian-starter-kit-v4-ai-native-release-distillation
source_checked_at: 2026-06-07
borrow_value: strong
borrow_order:
  - "P1: typed vault, note type, property schema, allowed values, folders, and templates"
  - "P1: skills registry and skill router for natural-language task routing"
  - "P1: fewer agents, more explicit skills"
  - "P1: AI conversation log as memory source and operation trace"
  - "P2: AI-generated content isolation"
  - "P2: LLM Wiki with source trace and contradiction/confidence hints"
  - "P2: Bases and Graph Explorer as workbench, not authority"
  - "P3: Time Machine, journal, life tracker, and plugin ecosystem as UX references"
avoid:
  - "Do not import commercial template/runtime as VAKS core architecture."
  - "Do not default MCP, CLI, or agent write access."
  - "Do not treat AI-maintained wiki as reviewed truth."
  - "Do not mix identity, health, habits, or life tracking into VAKS core."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "Designing VAKS skill registry, typed workbench schema, or AI conversation logging."
  support_when: "Comparing AI-native Obsidian runtime organization and skill routing."
  risk_when: "Any proposal imports a full plugin stack, commercial template, or AI-maintained wiki as authority."
  cold_references:
    - raw/articles/2026-06-07-dsebastien-obsidian-starter-kit-v4-ai-native-release-source.md
routing_hint:
  - skill-registry
  - runtime-workbench
  - agent-access
  - generated-content-boundary
tags:
  - candidate
  - provisional
  - article-distillation
  - obsidian
  - skill-registry
borrow_tags:
  - P1/typed_vault_schema_plugin
  - P1/skill_registry_and_skill_router
  - P1/fewer_agents_more_skills
  - P1/ai_conversation_log_as_memory_source
  - P2/ai_generated_content_isolation
  - P2/llm_wiki_with_source_trace_claim
  - P2/bases_graph_explorer_as_workbench
  - P3/plugin_ecosystem_ux_reference
do_not_borrow_tags:
  - avoid/commercial_template_as_core_architecture
  - avoid/mcp_write_access_default
  - avoid/ai_maintained_wiki_as_reviewed_truth
  - avoid/identity_health_layer_as_vaks_core
---

# dSebastien Obsidian Starter Kit v4 Candidate Distillation

## Boundary

Candidate-only architecture/workbench reference. No plugin/runtime adoption, no reviewed knowledge, no action basis.

## Plain-Language Takeaway

说人话：这篇像一个 AI-native Obsidian 操作系统产品说明。对 VAKS 有用的是 skill registry、typed vault、AI conversation log 和少 agent 多 skill 的组织思路；不该借的是整套商业模板和插件 runtime。

## Candidate Points

### 1. Typed vault schema can make workbench safer

Note types, properties, allowed values, folders, and templates can reduce ambiguous records, but they remain UX/schema assistance unless reviewed.

### 2. Skill registry beats agent sprawl

Few agents plus many narrow skills is cleaner than many overlapping agents.

### 3. AI conversations should be separable

AI conversation logs can become memory/use-ledger input without being confused with durable truth.

### 4. AI-generated content needs isolation

Generated wiki or generated notes must stay marked as generated/candidate until reviewed.

## Open Questions

- Should VAKS have a skill index that maps task phrases to helper scripts?
- What minimal typed schema helps without turning every note into a form?
- Where should AI conversation logs live relative to feedback-event and query-run?
