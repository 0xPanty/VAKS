---
record_kind: feedback_event
status: fixture_candidate_only
truth_boundary: feedback fixture only; no truth mutation
target_ref: outputs/review/source-intake-control-flow-sandbox-2026-06-06/fixtures/candidate-distillation-medium.md
event_kind: misleading_orientation
observed_in_context: "sandbox project_exploration trial"
event_time: 2026-06-06
review_pressure_effect: review_due
project_ref: VAKS
query_run_ref: sandbox-query-run-001
write_policy: append_only
forbidden_truth_mutation_fields_absent: true
reviewed_note_mutation_allowed: false
source_reliability_mutation_allowed: false
---

# Feedback Event Fixture

This event says the candidate was misleading in one local sandbox context.

Allowed effect:

```text
downrank in similar VAKS project_exploration context
create review_due if repeated
```

Forbidden effect:

```text
mark source false
change reviewed knowledge
create universal ban
```
