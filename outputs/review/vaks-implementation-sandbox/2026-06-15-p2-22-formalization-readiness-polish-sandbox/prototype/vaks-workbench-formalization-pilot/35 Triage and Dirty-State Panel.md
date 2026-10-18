---
record_kind: sandbox_triage_dirty_state_panel
status: sandbox_pilot
truth_boundary: sandbox_only
---

# Triage and Dirty-State Panel

## Groups

| Group | Meaning | Safe Operator Move |
| --- | --- | --- |
| blocked | Product or boundary gate is missing or failed | stop and inspect blocker |
| stale | status may be older than the latest artifact | refresh sandbox verification only |
| dirty | current tree has unrelated pre-existing changes | scope audit to this slice |
| missing-anchor | source/report link is missing or unresolved | repair sandbox link before review |
| review_due | reviewer, boundary, or Product Acceptance still pending | run the relevant read-only review |
| action-risk | wording could be mistaken for action basis | rewrite boundary copy and rerun validator |

## Drilldown Rule

Each group must point to a receipt, report, or safe next step. The group itself
does not approve anything.

## Boundary

State grouping is not approval. Dirty-state visibility is not blame, evidence
support, reviewed knowledge, action basis, sync approval, commit approval, push
approval, or promotion approval.
