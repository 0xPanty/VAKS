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
  - raw/papers/2026-06-07-ferreira-obsidian-second-brains-case-study-source.md
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
scope: ferreira-obsidian-second-brains-case-study-distillation
source_checked_at: 2026-06-07
borrow_value: strong
borrow_order:
  - "P1: retrieval strategy shapes note structure and maintenance"
  - "P1: organization and retrieval must be designed together"
  - "P1: blank page needs starter structure, but structure must remain changeable"
  - "P1: tags, folders, links, and search are real user retrieval modes"
  - "P2: inbox then periodic processing as observed workflow"
  - "P2: PKB as externalized mental model for domain work"
  - "P2: AI support should cover create, organize, retrieve, and use loop"
avoid:
  - "Do not generalize a 7-participant CS researcher case study into universal rule."
  - "Do not treat folders, tags, or search retrieval as truth signals."
  - "Do not turn Obsidian feature behavior into VAKS schema."
  - "Do not treat AI feature suggestions as implemented evidence."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "Designing VAKS source intake or retrieval/context-pack behavior."
  support_when: "Arguing why intake structure and future retrieval should be co-designed."
  risk_when: "Any proposal treats user retrieval habits as reviewed truth or universal behavior."
  cold_references:
    - raw/papers/2026-06-07-ferreira-obsidian-second-brains-case-study-source.md
routing_hint:
  - source-intake
  - retrieval
  - activation
  - context-pack
  - workbench-ux
tags:
  - candidate
  - provisional
  - paper-distillation
  - obsidian
  - pkm
borrow_tags:
  - P1/retrieval_strategy_shapes_note_structure
  - P1/organization_and_retrieval_must_be_designed_together
  - P1/blank_page_needs_starter_structure_but_structure_must_change
  - P1/tags_folders_links_search_as_real_user_retrieval_modes
  - P2/inbox_then_periodic_processing_as_user_observed_workflow
  - P2/pkb_as_externalized_mental_model_for_domain_work
  - P2/ai_support_should_cover_create_organize_retrieve_use_loop
do_not_borrow_tags:
  - avoid/small_sample_as_universal_rule
  - avoid/folder_tag_retrieval_as_truth_signal
  - avoid/obsidian_feature_behavior_as_vaks_schema
  - avoid/ai_suggestions_as_implemented_system
  - avoid/researcher_pkb_as_general_user_truth
---

# Ferreira et al. Obsidian Second Brains Case Study Candidate Distillation

## Boundary

Candidate-only empirical reference. It can support design discussion, but it is not reviewed VAKS truth or action basis.

## Plain-Language Takeaway

说人话：这篇最硬的价值是证明“以后怎么找”会反过来塑造“现在怎么写”。所以 VAKS 不能只设计资料怎么存，还要从 intake 时就考虑未来怎么查、怎么回到来源、怎么用于 context pack。

## Candidate Points

### 1. Retrieval strategy shapes note construction

Users organize folders, tags, links, and note content according to how they expect to find material later.

### 2. Starter structure helps, but must stay flexible

Blank vaults overwhelm users, but fixed folder taxonomies become wrong as knowledge grows.

### 3. Multiple retrieval modes coexist

Real Obsidian users retrieve by folder browsing, search, tags, links, and in-note pointers.

### 4. Inbox plus periodic processing is observed behavior

Raw capture and later processing is not only theory; it appears in observed user workflows.

### 5. PKB mirrors domain mental model

Personal knowledge bases externalize expert mental models and discovery work, but this is still personal/contextual.

## Open Questions

- Should VAKS source cards include a lightweight "future retrieval route" hint?
- Which retrieval modes should the first VAKS workbench support before vector search?
- How much starter structure is helpful before it becomes schema bloat?
