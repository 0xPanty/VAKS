---
record_kind: sandbox_pilot_test_results_template
status: sandbox_dry_run_passed
truth_boundary: sandbox_only
---

# Pilot Test Results

## Test Session

- Operator: Builder dry-run
- Date: 2026-06-15
- Prototype path: prototype/vaks-workbench-formalization-pilot/
- Method: local file/link dry-run, not browser-rendered smoke
- time_to_first_correct_boundary_statement_seconds: 45
- time_to_find_receipt_path_seconds: 50
- time_to_compare_formalization_routes_seconds: 75
- max_links_to_boundary_faq: 2
- max_links_to_receipt_inspector: 2

## Task Results

| Task | Expected | Observed | Pass |
| --- | --- | --- | --- |
| First run | Finds Boundary FAQ in three links or fewer | Pilot Home -> Boundary FAQ; correct statement says sandbox only and no formal vault write | PASS |
| Daily triage | Describes triage without approval language | Triage panel exposes blocked/stale/dirty/missing-anchor/review_due/action-risk and says state grouping is not approval | PASS |
| Receipt lookup | Finds P2-21 reports and states non-support boundary | Receipt Inspector links P2-21 verification, reviewer, boundary, product acceptance and says receipt is not evidence support | PASS |
| Decision route | Chooses next sandbox route without mainline approval | Decision Matrix recommends hybrid_pilot_path and says separate user approval is required | PASS |
| Failure message | Gives ordinary block reason and safe alternative | Failure Messages maps forbidden_operation and authority_confusing_label to plain reason plus safe alternative | PASS |

## Notes

Any authority confusion is a failure, even if the UI feels smooth.

Browser-rendered testing is not claimed here because the in-app Browser rejected
local `file://` navigation by policy.
