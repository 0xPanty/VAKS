---
record_kind: sandbox_blind_relevance_judgment_instructions
status: candidate
project_id: VAKS
created_at: 2026-06-11
truth_boundary: instructions_not_completed_judgment
action_basis_allowed: false
---

# Phase B Blind Relevance Judgment Instructions

## Plain Task

Fill the judgment file from the packet below:

```text
results/phase_b_blind_relevance_judgment_packet.csv
```

Create:

```text
results/phase_b_blind_relevance_judgments.csv
```

Keep every row and fill only:

```text
judged_relevance
judgment_basis
judge_id
```

## Grade

```text
2 = relevant
1 = borderline / partially relevant
0 = not relevant
```

Use the row's `relevance_question`, `relevant_criteria`, `borderline_criteria`, and `non_relevant_criteria`.

Do not use `expected_terms`; this evaluation is meant to be separate from the old expected-terms proxy.

## Boundary

```text
This is relevance judgment, not truth review.
This does not validate original Yuxi runtime.
This does not approve C-lite, writeback, action basis, or core-doc strong conclusions.
```

