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
project_id: VAKS
target_ref: fixture-source-confirmed-metadata
target_hint: source-intake metadata routing
project_borrow_scope: "For project VAKS, borrow the separation between hard filters and recall tags as a source-intake design pressure."
project_non_borrow_scope: "For project VAKS, do not borrow a generic tag-heavy taxonomy as a truth or action-basis mechanism."
project_reopen_trigger: "Reopen if VAKS adopts a dedicated retrieval UI or a reviewed topic registry."
confirmation_basis: sandbox fixture
last_checked_at: 2026-06-07
expires_at:
---

# Fixture: Confirmed Project Overlay

## Expected Behavior

This overlay can guide VAKS project exploration.

It cannot:

```text
rewrite source metadata
create reviewed knowledge
create action basis
be used outside active project by default
```
