---
slice_id: 2026-06-19-p2-85-exact-approval-classifier-hardening-sandbox
status: source_map_defined
---

# Source Map

## Inputs

- `outputs/review/vaks-implementation-sandbox/2026-06-19-p2-75-old-file-status-normalization-approval-request-sandbox/artifact/old_file_status_normalization_approval_request.json`
- `outputs/review/vaks-implementation-sandbox/2026-06-19-p2-77-old-file-status-normalization-executor-readiness-gate-sandbox/artifact/old_file_status_normalization_executor_readiness_gate.json`
- `outputs/review/vaks-implementation-sandbox/2026-06-19-p2-83-post-rehearsal-goal-state-cockpit-sandbox/artifact/post_rehearsal_goal_state_cockpit.json`
- `outputs/review/vaks-implementation-sandbox/2026-06-19-p2-84-post-rehearsal-cockpit-mutation-hardening-sandbox/artifact/post_rehearsal_cockpit_mutation_hardening.json`

## Output Contract

p2-85 is an approval-classifier hardening artifact only. It can classify fixture text in this sandbox, but it does not collect approval, authorize writes, normalize old files, promote knowledge, create action basis, or merge anything.

## Reuse Value

Future agents can use this slice to decide whether a future user message is exactly the p2-75 approval phrase before starting a separate executor slice with fresh hash checks and stop-before-write behavior.
