---
record_kind: project_overlay
status: candidate
knowledge_status: candidate
processing_tier: medium
artifact_kind: live_readonly_test_fixture
retrieval_exclusion: true
overlay_state: confirmed
review_pressure: review_due
retrieval_scope: active_project_only
default_retrieval: false
retrieval_policy:
  policy_kind: project_context_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: overlay_not_authority
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
project_id: VAKS
target_ref: outputs/review/2026-06-13-flexnote-docs-candidate-distillation.md
project_borrow_scope: For VAKS runtime testing, borrow FlexNote only as a canonical overlay fixture for visual workbench review-input
  routing.
project_non_borrow_scope: For project VAKS, do not borrow this runtime fixture as reviewed knowledge, evidence support, decision,
  or action basis.
project_reopen_trigger: Reopen only when testing canonical project_overlay support-gate behavior.
created_at: '2026-06-14T01:42:43+00:00'
tags:
- runtime-test-fixture
- project-overlay
- canonical-overlay
- candidate-only
---

# Canonical Project Overlay Runtime Fixture

This is a sandbox test fixture for Source Intake runtime validation.

It exists only to test that a canonical `outputs/review/project_overlays/` overlay cannot become final support even if an errant pack assembler labels it as `support`.

It is not reviewed knowledge, not a decision, not action basis, and not default retrieval material.
