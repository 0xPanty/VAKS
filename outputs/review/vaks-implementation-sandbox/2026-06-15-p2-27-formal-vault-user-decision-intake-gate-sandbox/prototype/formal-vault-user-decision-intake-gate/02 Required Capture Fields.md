---
record_kind: sandbox_required_capture_fields
slice_id: 2026-06-15-p2-27-formal-vault-user-decision-intake-gate-sandbox
status: sandbox_pilot
truth_boundary: sandbox_only
---

# Required Capture Fields

- `decision_id`
- `decision_verdict`
- `future_user_exact_text_reference`
- `user_turn_id`
- `timestamp_utc`
- `packet_hash`
- `source_bundle_hash`
- `scope_hash`
- `rehearsal_hash`
- `intake_gate_hash`
- `operator_or_agent_id`
- `scope_ids`
- `explicit_exclusions_ack`
- `rollback_ack`
- `hash_ack`
- `dirty_state_ack`
- `extra_files_requested`

## Storage Rule

This slice stores no real user text. A future decision record must point to the
future user turn or exact-text reference according to the future approved
execution protocol.

## Boundary

Future user exact text reference is required, but real user text is not captured
or stored in this sandbox.
