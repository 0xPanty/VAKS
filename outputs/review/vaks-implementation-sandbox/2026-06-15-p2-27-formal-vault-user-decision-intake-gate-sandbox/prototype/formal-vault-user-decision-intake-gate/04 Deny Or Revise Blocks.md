---
record_kind: sandbox_deny_or_revise_blocks
slice_id: 2026-06-15-p2-27-formal-vault-user-decision-intake-gate-sandbox
status: sandbox_pilot
truth_boundary: sandbox_only
---

# Deny Or Revise Blocks

| Sample | Verdict | Expected Gate Result | Write Allowed Now |
| --- | --- | --- | --- |
| `future_approve_reference_capture` | `APPROVED_BY_USER` | `VALID_FUTURE_APPROVAL_RECORD_BUT_NOT_ACTIONABLE_IN_THIS_SLICE` | `False` |
| `future_deny_reference_capture` | `DENIED_BY_USER` | `BLOCKED_BY_FUTURE_DENIAL_RECORD` | `False` |
| `future_revision_reference_capture` | `NEEDS_REVISION` | `BLOCKED_PENDING_PACKET_REVISION` | `False` |

## Boundary

Deny and revise always block write. Approval also remains non-actionable inside
this slice.
