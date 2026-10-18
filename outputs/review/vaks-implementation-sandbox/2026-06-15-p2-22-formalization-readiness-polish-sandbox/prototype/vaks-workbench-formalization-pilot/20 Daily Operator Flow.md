---
record_kind: sandbox_daily_operator_flow
status: sandbox_pilot
truth_boundary: sandbox_only
---

# Daily Operator Flow

## Operator Moves

- Capture: place a new thought or source candidate into the correct future lane.
- Triage: decide whether it needs review, receipt inspection, or boundary check.
- Inspect: open the relevant validator, receipt, reviewer report, boundary audit,
  or Product Acceptance report.
- Decide next safe step: choose a future sandbox action, not a mainline action.

## Pilot Journeys

- `new_user_first_run`: A new operator can understand the workbench without reading architecture first. Steps: Open Pilot Home -> Run First Run Script -> Confirm Boundary FAQ. Stop: Stop if any step asks for sync, commit, push, install, or formal vault write.
- `daily_triage`: An operator can decide where a new candidate belongs. Steps: Open Daily Operator Flow -> Choose capture or review radar -> Inspect next safe step. Stop: Stop if routing is presented as reviewed knowledge.
- `receipt_lookup`: An operator can find the verification trail for a slice. Steps: Open Receipt Inspector -> Select P2-21 source links -> Open relevant receipt or report. Stop: Stop if a receipt is described as source support.
- `formalization_route_choice`: A product owner can compare formalization routes without accidental merge. Steps: Open Decision Matrix -> Compare four routes -> Select a recommended next sandbox route. Stop: Stop if the matrix authorizes Obsidian sync or mainline promotion.
- `acceptance_review`: A reviewer can tell whether the pilot pack is ready for the next slice. Steps: Open Acceptance Gates -> Run validator -> Read Reviewer, Boundary, Product reports. Stop: Stop if validator output is treated as reviewer approval.

## Boundary

Triage is not review approval. A route is not evidence support. A next safe step
is not action basis.
