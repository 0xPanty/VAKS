---
record_kind: source_card
status: fixture_blocked
truth_boundary: source freshness fixture only; not reviewed knowledge; not action basis
lifecycle_state: source_registered
processing_tier: medium
knowledge_status: raw
overlay_state: none
review_pressure: blocked
source_type: repository_spec_file
source_url: https://example.invalid/spec.md
raw_location: raw/repos/example/spec.md
snapshot_ref_or_source_date: missing_or_changed
source_change_signal: upstream_changed_or_anchor_broken
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: false
  action_basis_allowed: false
  warning_code: anchor_broken_or_source_changed
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
---

# Source Changed Blocked Fixture

This fixture represents a source whose anchor or version changed.

It must be blocked from action-facing use until the source is recaptured or the
anchor is repaired.

