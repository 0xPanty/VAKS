# Main Rule Overlap Audit

Status:

```text
sandbox-only
read-only comparison against main vault
no mainline writeback
```

## Checked Main Rules

The alpha candidates were checked against the current main-vault boundaries by reading:

```text
README.md
ARCHITECTURE_PRINCIPLES.md
SCHEMA.md
SOURCE_INTAKE.md
REVIEW_QUEUE.md
FEEDBACK.md
```

Relevant existing boundaries found:

```text
Strict checks are lazy gates.
Ordinary capture and ordinary query stay light.
Evidence Packet is review input, not a truth layer.
Coverage map is an audit surface, not a truth layer.
Complete coverage_map is required only for key judgments actually used in an answer or action basis.
Ordinary query does not require a complete coverage_map.
Feedback improves activation/usefulness/scope fit, not truth confidence.
Explicit correction creates review_due.
Cluster is not truth.
Review queue actions and routing labels are not truth changes.
Retrieval, dashboards, graph rank, tests, and LLM-judge results are diagnostics, not truth.
```

## Candidate Fit

| Alpha | Overlap With Existing Rule | Conflict Found? | Interpretation |
| --- | --- | --- | --- |
| compact_evidence_card | Overlaps with lazy gates and Evidence Packet as review input. | No | This is an operation-shape candidate: small claims get a card front; promotion/challenge/memory-only cases still thicken. |
| compact_coverage_card | Overlaps with existing rule that ordinary query does not require full coverage_map. | No | This is not a new truth rule. It operationalizes compact/full coverage display. |
| support_refine_cluster | Overlaps with REVIEW_QUEUE cluster not being truth. | No | Useful but needs real-source testing because over-grouping can hide meaningful differences. |
| categorical_feedback_stub | Overlaps with FEEDBACK: positive feedback weak, negative feedback review pressure, explicit correction review_due. | No | Removes fake numeric deltas and keeps feedback outside truth changes. |

## Boundary Notes

The alpha candidates should not be written as SCHEMA fields first.

Preferred landing order, if later accepted:

```text
operation convention
template wording
review-lite guidance
queue view convention
anti-pattern note
future runtime parked note
SCHEMA only after repeated sandbox evidence
```

## Risks To Retest

```text
compact evidence card:
  risk: hides challenge/omission if gate is too weak

compact coverage card:
  risk: summary looks action-ready without full coverage

support/refine cluster:
  risk: over-groups distinct evidence problems

categorical feedback stub:
  risk: too little detail for later activation debugging
```

## Verdict

No direct conflict with the main architecture boundaries was found in this read-only comparison.

The candidates mostly turn existing principles into lighter record/view conventions:

```text
default light
condition thick
raw anchors jump-backable
no truth mutation through feedback/grouping/retrieval
```

