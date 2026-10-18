---
record_kind: sandbox_preflight_blocks
slice_id: 2026-06-15-p2-28-formal-vault-execution-preflight-dry-run-sandbox
status: sandbox_pilot
truth_boundary: sandbox_only
---

# Deny Or Revise Blocks

| Sample | Verdict | Expected Result | Executed |
| --- | --- | --- | --- |
| `synthetic_approved_reference_preflight` | `APPROVED_BY_USER` | `PREFLIGHT_DRY_RUN_COMPLETE_NOT_EXECUTABLE` | `False` |
| `synthetic_denied_reference_preflight` | `DENIED_BY_USER` | `BLOCKED_BY_DENIAL_NOT_EXECUTED` | `False` |
| `synthetic_revision_reference_preflight` | `NEEDS_REVISION` | `BLOCKED_PENDING_PACKET_REVISION_NOT_EXECUTED` | `False` |
| `synthetic_dirty_state_preflight_block` | `APPROVED_BY_USER` | `BLOCKED_BY_DIRTY_STATE_ACK_MISSING_NOT_EXECUTED` | `False` |

## Boundary

Deny and revise block execution. Dirty-state acknowledgement gaps block
execution. Approved references also remain non-executable inside this slice.
