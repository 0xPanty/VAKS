---
record_kind: sandbox_decision_scenario_matrix
slice_id: 2026-06-15-p2-26-formal-vault-write-decision-rehearsal-sandbox
status: sandbox_pilot
sandbox_only: true
truth_boundary: sandbox_only
---

# Scenario Matrix

| Scenario | Verdict | Expected Result | Write Allowed Now | Next Gate |
| --- | --- | --- | --- | --- |
| `synthetic_approve_exact_packet` | `APPROVED_BY_USER` | `SIMULATED_APPROVAL_VALID_BUT_NOT_ACTIONABLE` | `False` | `future_separately_approved_write_slice_required` |
| `synthetic_deny_write` | `DENIED_BY_USER` | `BLOCKED_BY_SYNTHETIC_DENIAL` | `False` | `stop_and_record_denial_only` |
| `synthetic_needs_revision` | `NEEDS_REVISION` | `BLOCKED_PENDING_PACKET_REVISION` | `False` | `revise_packet_in_future_sandbox_only` |

## Hashes

- rehearsal_hash: `cfa4c69de3df0dde571a1a4912a17bcfbf75dac3a901f112a1b1b98d84bed72c`

## Boundary

All decisions here are synthetic. The approval scenario is valid only as a
rehearsal and remains not actionable.

## Next

- [[02 Synthetic Approval Rehearsal]]
- [[07 Stop Conditions]]
