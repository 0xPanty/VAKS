---
record_kind: sandbox_decision_rehearsal_stop_conditions
slice_id: 2026-06-15-p2-26-formal-vault-write-decision-rehearsal-sandbox
status: sandbox_pilot
sandbox_only: true
truth_boundary: sandbox_only
---

# Stop Conditions

- actual user approval collection requested
- formal vault read requested
- formal vault scan requested
- formal vault write requested
- formal vault hash or snapshot requested
- absolute vault path requested
- Obsidian sync requested
- commit or push requested
- promotion requested
- decision inferred from silence or prior PASS
- packet hash mismatch
- source bundle hash mismatch
- scope hash mismatch
- rehearsal hash mismatch
- approved synthetic scenario treated as action basis
- denied or revise scenario allows write
- extra files requested
- rollback or hash acknowledgement missing for synthetic approval

## Safe Alternative

Record the requested move as a future user decision or future sandbox item and
stop. Do not perform the operation in this slice.
