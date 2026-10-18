---
record_kind: sandbox_external_relevance_judge_only_instructions
status: judge_packet
project_id: VAKS
created_at: 2026-06-12
truth_boundary: judge_instructions_not_completed_judgment
action_basis_allowed: false
---

# Phase B External Relevance Judge-Only Instructions

## Task

Fill this anonymous CSV:

```text
results/phase_b_blind_relevance_external_judgment_template.csv
```

Return the filled CSV as:

```text
results/phase_b_blind_relevance_external_judgments.csv
```

## Blindness Rule

Do not ask for or inspect:

```text
system mapping
mode names
internal heuristic judgments
expected_terms
Phase B result summaries
```

`system_slot` is an opaque label only. Do not infer which system it represents.

## Grade

```text
2 = relevant
1 = borderline / partially relevant
0 = not relevant
```

Judge relevance to the row's `relevance_question`, using the row's:

```text
query
relevance_question
relevant_criteria
borderline_criteria
non_relevant_criteria
path
heading
bucket
status
warning_code
snippet
```

## Fields To Fill

If acting as Judge A:

```text
judge_a_relevance
judge_a_basis
judge_a_id
```

If acting as Judge B:

```text
judge_b_relevance
judge_b_basis
judge_b_id
```

After Judge A and Judge B are filled, the arbiter fills:

```text
arbitrated_relevance
arbitration_basis
arbiter_id
```

If both judges agree, `arbitration_basis` can say `agreement`. If they disagree, briefly explain the final grade.

## Boundary

This is relevance judgment only. It is not truth review, original Yuxi runtime validation, C-lite approval, writeback approval, or action-basis approval.
