---
record_kind: action_readiness_check
action_id: AR-FAIL-025
expected_failure_reason: AR_SCHEMA_CHANGE_MISSING_OWNER_FINAL
action_readiness: ready
action_basis_ready_claimed: true
action_mode: schema_change
operation_mode: schema_change
actor_tier: owner
significant_action: true
evidence_sufficiency: sufficient
evidence_support_status: supported
temporal_applicability: current
replacement_basis_ref:
narrowed_scope_ref:
unresolved_risk: false
warnings_or_gaps_trimmed: false
missing_evidence_trimmed: false
intent_confirmation_required: true
intent_confirmed: true
success_criteria_present: true
basis_materials: [reviewed_support, evidence_packet]
reviewed_write: false
target_bucket:
approved: true
checked_body_hash_present: true
rollback_required: true
rollback_plan_present: true
owner_final: false
---

# Failure

Schema change is ready without owner-final.

