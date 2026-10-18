---
record_kind: sandbox_stop_conditions
slice_id: 2026-06-15-p2-24-formal-vault-write-plan-dry-run-sandbox
status: sandbox_pilot
sandbox_only: true
truth_boundary: sandbox_only
---

# Stop Conditions

- formal vault read requested
- formal vault write requested
- absolute vault path requested
- Obsidian sync requested
- real .base requested
- commit or push requested
- promotion requested
- dependency install requested
- background service requested
- MCP write tool requested
- approval prompt missing or default not deny
- rollback manifest missing
- hash-before or hash-after missing

## Safe Alternative

Record the requested move as a future approval item and stop. Do not perform the
operation in this slice.
