---
record_kind: sandbox_external_relevance_judgment_kit
status: pending_external_judgment
project_id: VAKS
created_at: 2026-06-12
truth_boundary: judgment_kit_not_completed_external_judgment
action_basis_allowed: false
---

# Phase B External Relevance Judgment Kit

## Plain Task

Pro's latest audit says the next P0 is external/manual relevance judgment for the existing blind relevance packet.

Use this template:

```text
results/phase_b_blind_relevance_external_judgment_template.csv
```

Create this filled file:

```text
results/phase_b_blind_relevance_external_judgments.csv
```

## Required Workflow

```text
Judge A fills judge_a_relevance, judge_a_basis, judge_a_id.
Judge B independently fills judge_b_relevance, judge_b_basis, judge_b_id.
The arbiter fills arbitrated_relevance, arbitration_basis, arbiter_id for every row.
If Judge A and Judge B agree, arbitration_basis may simply say agreement.
If they disagree, arbitration_basis should briefly explain why the final grade was chosen.
```

## Grade

```text
2 = relevant
1 = borderline / partially relevant
0 = not relevant
```

Judge only by the row's query, relevance_question, criteria, path, heading, bucket/status, warning, and snippet.

Do not use expected_terms. Do not look at the internal heuristic judgment file before judging.

The judge-facing template intentionally hides concrete system names. `system_slot` is an opaque label only; the system mapping is for post-judgment statistics and should not be shown to judges before grading.

## Template Summary

```text
packet rows: 720
template rows: 720
query count: 18
corpora: full, primary
system slots: system_01, system_02, system_03, system_04
mapping file: results/phase_b_blind_relevance_external_judgment_mapping.csv
status: pending_external_judgment
```

## Boundary

```text
This kit prepares external/manual relevance judgment.
It does not complete external/manual relevance judgment.
It does not validate original Yuxi runtime.
It does not approve C-lite, writeback, action basis, or core-doc strong conclusions.
```
