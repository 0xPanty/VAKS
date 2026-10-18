---
record_kind: sandbox_execution_preflight_stop_conditions
slice_id: 2026-06-15-p2-28-formal-vault-execution-preflight-dry-run-sandbox
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
- formal vault state inspection requested
- formal vault hash or snapshot requested
- absolute vault path requested
- Obsidian sync requested
- commit or push requested
- promotion requested
- execution requested
- decision inferred from silence or prior PASS
- intake gate hash mismatch
- packet hash mismatch
- source bundle hash mismatch
- scope hash mismatch
- preflight hash mismatch
- target manifest mismatch
- extra targets requested
- target path is absolute or parent traversal
- approved reference treated as executable
- denied or revise reference allows execution
- dirty-state acknowledgement missing
- snapshot, rollback, or hash plan missing

## Safe Alternative

Record the requested move as a future sandbox item and stop. Do not perform the
operation in this slice.
