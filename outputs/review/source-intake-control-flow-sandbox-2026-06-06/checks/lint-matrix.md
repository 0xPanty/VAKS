---
type: sandbox_lint_matrix
status: candidate_only
created_at: 2026-06-06
scope: Source Intake sandbox lint expectations
truth_boundary: diagnostic only
---

# Lint Matrix

| Check | Expected | Fixture evidence |
|---|---|---|
| Light source has `knowledge_status: raw`. | PASS | `fixtures/source-card-light.md` |
| Light source cannot be action basis. | PASS | `action_basis_allowed: false` |
| Medium candidate has `knowledge_status: candidate`. | PASS | `fixtures/candidate-distillation-medium.md` |
| Medium candidate uses `routing_hint`, not project borrow conclusion. | PASS | `fixtures/candidate-distillation-medium.md` |
| Medium candidate explicitly blocks direct action-basis use. | PASS | `retrieval_policy.action_basis_allowed: false` |
| Suggested overlay is trace-only. | PASS | `fixtures/query-run-suggested-overlay-trace.md` |
| Confirmed overlay has `project_non_borrow_scope`. | PASS | `fixtures/confirmed-project-overlay.md` |
| Confirmed overlay has `project_reopen_trigger`. | PASS | `fixtures/confirmed-project-overlay.md` |
| Feedback event has `project_ref`. | PASS | `fixtures/feedback-event-misleading-orientation.md` |
| Feedback event forbids truth mutation. | PASS | `fixtures/feedback-event-misleading-orientation.md` |
| Heavy review open but blocked cannot enter answer pool. | PASS | `fixtures/heavy-review-open-blocked.md` |

## Forbidden Effects Covered

```text
candidate_used_as_rule: blocked
suggested_overlay_persisted: blocked
project_non_borrow_as_universal_ban: blocked
candidate_summary_as_evidence: blocked
feedback_truth_mutation: blocked
broken_anchor_action_use: blocked
heavy_review_open_as_answer_pool: blocked
archived_overlay_default_retrieval: blocked by protocol
action_facing_candidate_anchor: blocked by round2 fixture
confirmed_overlay_outside_active_project: blocked by protocol
```
