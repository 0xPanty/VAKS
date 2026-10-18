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
target_ref: outputs/review/2026-06-07-ferreira-obsidian-second-brains-case-study-candidate-distillation.md
source_card: raw/papers/2026-06-07-ferreira-obsidian-second-brains-case-study-source.md
target_selector: obsidian_pkm_case_study
target_hint: "Use as empirical candidate reference for source-intake/retrieval co-design."
borrow_tags:
  - P1/retrieval_strategy_shapes_note_structure
  - P1/organization_and_retrieval_must_be_designed_together
  - P1/blank_page_needs_starter_structure_but_structure_must_change
  - P1/tags_folders_links_search_as_real_user_retrieval_modes
  - P2/inbox_then_periodic_processing_as_user_observed_workflow
do_not_borrow_tags:
  - avoid/small_sample_as_universal_rule
  - avoid/folder_tag_retrieval_as_truth_signal
  - avoid/obsidian_feature_behavior_as_vaks_schema
  - avoid/ai_suggestions_as_implemented_system
project_reopen_trigger:
  - "When redesigning SOURCE_INTAKE fields or retrieval hints."
  - "When arguing for context-pack/retrieval design from empirical Obsidian use."
confirmation_basis: "arXiv abstract and PDF observed on 2026-06-07; PDF hash recorded."
last_checked_at: 2026-06-07
expires_at:
---

# VAKS Overlay: Obsidian Second Brains Case Study

## Boundary

Project-side empirical reference only. It cannot create a universal VAKS rule without review.

## Project Borrow Scope

- Retrieval strategy should influence intake structure.
- Starter structure should exist but remain flexible.
- Real retrieval modes include folder browsing, tags, links, and search.
- Inbox then periodic processing is a useful observed workflow.
- PKB can reflect domain mental models, which supports context-pack thinking.

## Project Non-Borrow Scope

- No universal rule from a small sample.
- No folder/tag/search as truth signal.
- No Obsidian feature behavior as VAKS schema.
