---
record_kind: sandbox_approval_packet_stop_conditions
slice_id: 2026-06-15-p2-25-formal-vault-write-approval-packet-sandbox
status: sandbox_pilot
sandbox_only: true
truth_boundary: sandbox_only
---

# Stop Conditions

- formal vault read requested
- formal vault scan requested
- formal vault write requested before future approval
- absolute vault path requested
- Obsidian sync requested
- commit or push requested
- promotion requested
- approval collection requested in this slice
- approval inferred from silence or prior PASS
- missing exact future confirmation phrase
- packet hash missing
- source bundle hash missing
- scope hash missing
- source hash mismatch
- scope mismatch
- rollback or hash gate removed

## Ambiguity Blockers

- future user response missing exact confirmation phrase
- future response does not cite packet hash
- future response does not cite source bundle hash
- future response does not cite scope hash
- future response asks for extra files
- future response asks for sync, commit, push, or promotion
- source hash mismatch
- scope hash mismatch
- dirty tree or unexpected formal vault file state

## Safe Alternative

Record the request as a future user decision item and stop. Do not perform the
operation in this slice.
