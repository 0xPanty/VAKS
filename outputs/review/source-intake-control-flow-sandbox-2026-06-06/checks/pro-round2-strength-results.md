---
type: sandbox_strength_test_results
status: candidate_only
created_at: 2026-06-06
scope: Pro round-2 source intake control flow strength test
truth_boundary: diagnostic only; not reviewed knowledge; not mainline policy; not action basis
---

# Pro Round-2 Strength Test Results

## Summary

Pro round-2 recommendations were added to the Source Intake Control Flow
sandbox as a harder runtime-boundary test.

First static round-2 run:

```text
15/16 passed
```

The failed check was useful. The feedback fixture still contained stale
truth-mutation field names as explicit forbidden fields. That was readable as a
human warning, but a machine filter could still match those fields and route the
event incorrectly.

Patch applied:

```text
removed truth_confidence_delta / auto_mutate_reviewed_note from feedback fixture data fields
added forbidden_truth_mutation_fields_absent: true
kept reviewed/source mutation as explicit false booleans
```

Final static round-2 rerun:

```text
16/16 passed
```

## Comparison With First Sandbox Pass

The first sandbox pressure test ended at 11/11 and validated the basic split:

```text
candidate is not action basis
suggested overlay is not persistent overlay
confirmed overlay is project-scoped
feedback does not mutate truth
RRF does not cross authority buckets
```

Round 2 adds harder failure cases that the first pass did not fully cover:

```text
final action-facing support cannot anchor to candidate / overlay artifacts
archived overlays are excluded from default retrieval
changed or broken source anchors enter blocked pressure
confirmed overlays are active-project-only
forbidden field-name leakage in fixture data is detectable
```

Result:

```text
effect improved: yes
reason: the stricter matrix caught one real fixture weakness that the 11/11 pass missed
```

## Final Checks

| ID | Check | Status |
|---|---|---|
| ST-01 | Medium candidate is excluded from action/review mode. | PASS |
| ST-02 | Suggested overlay remains trace-only and non-persistent. | PASS |
| ST-03 | Project non-borrow scope stays project-scoped and reopenable. | PASS |
| ST-04 | Candidate summary cannot outrank raw as final evidence. | PASS |
| ST-05 | Feedback event has no truth-mutation field leakage. | PASS |
| ST-06 | Changed/broken source anchor is blocked for action-facing use. | PASS |
| ST-07 | Heavy review open/blocked stays out of default answer pool. | PASS |
| ST-08 | Archived overlay is excluded from default retrieval. | PASS |
| ST-09 | Candidate distillation fails as final support anchor. | PASS |
| ST-10 | RRF is restricted to one allowed authority bucket at a time. | PASS |
| ST-11 | Confirmed overlay is active-project-only. | PASS |
| ST-12 | Source card does not carry adopt/reject verdict or truth score. | PASS |
| ST-13 | Feedback requires project/context scope before negative reuse. | PASS |
| ST-14 | Project overlay is not ADR, decision, review verdict, or universal ban. | PASS |
| ST-15 | Valid action-facing support uses raw/stable selector-grade anchor. | PASS |
| ST-16 | Field contract uses project-scoped borrow field names. | PASS |

## Interpretation

The Pro additions improve the sandbox because they harden the exact places where
truth pollution usually leaks in:

```text
pretty candidate summary -> blocked as final evidence
semantic match -> suggestion only, not confirmed overlay
project warning -> local boundary, not universal ban
feedback -> routing pressure, not truth update
retrieval rank -> relevance only, not authority
```

The control flow is still intentionally light. It does not add a new ontology or
workflow platform. It makes the existing intake flow more executable by turning
warnings into filterable fields and mode-based retrieval rules.

## Boundary

```text
This is a sandbox diagnostic.
It does not promote any source, candidate, overlay, or feedback event.
It does not create reviewed knowledge, a decision, a pattern, or action basis.
It does not change the truth layer.
```
