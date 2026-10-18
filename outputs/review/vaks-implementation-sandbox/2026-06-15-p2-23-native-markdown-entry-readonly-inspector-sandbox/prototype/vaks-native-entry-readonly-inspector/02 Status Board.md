---
record_kind: sandbox_native_status_board
slice_id: 2026-06-15-p2-23-native-markdown-entry-readonly-inspector-sandbox
status: sandbox_pilot
sandbox_only: true
truth_boundary: sandbox_only
entry_role: status
---

# Status Board

## State Groups

| Group | Meaning | Safe Next Step |
| --- | --- | --- |
| blocked | a required gate is missing or failed | open [[04 Boundary Stop]] |
| dirty | unrelated pre-existing tree changes exist | scope audit to this slice |
| stale | source or report may be older than latest artifact | rerun sandbox validator |
| missing-anchor | link or receipt target is unresolved | repair sandbox link only |
| review_due | Reviewer, Boundary, or Product Acceptance is pending | run read-only review |
| action-risk | wording could be mistaken for action basis | rewrite boundary copy |

## Boundary

Status grouping is not approval, not truth confidence, not evidence support, and
not action basis.

## Next

- [[03 Receipt Index]]
- [[04 Boundary Stop]]
- [[06 Next Safe Step]]
