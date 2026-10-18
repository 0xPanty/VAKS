---
record_kind: sandbox_user_decision_intake_gate_stop_conditions
slice_id: 2026-06-15-p2-27-formal-vault-user-decision-intake-gate-sandbox
status: sandbox_pilot
truth_boundary: sandbox_only
---

# Stop Conditions

- actual user approval collection requested
- actual user decision collection requested
- real user text storage requested
- formal vault read requested
- formal vault scan requested
- formal vault write requested
- formal vault hash or snapshot requested
- absolute vault path requested
- Obsidian sync requested
- commit or push requested
- promotion requested
- decision inferred from silence or prior PASS
- future user exact text reference missing
- required confirmation phrase missing
- packet hash mismatch
- source bundle hash mismatch
- scope hash mismatch
- rehearsal hash mismatch
- intake gate hash mismatch
- approved record treated as action basis
- denied or revise record allows write
- extra files requested
- rollback, hash, or dirty-state acknowledgement missing for approval

## Safe Alternative

Record the requested move as a future user-decision intake issue or future
sandbox item and stop. Do not perform the operation in this slice.
