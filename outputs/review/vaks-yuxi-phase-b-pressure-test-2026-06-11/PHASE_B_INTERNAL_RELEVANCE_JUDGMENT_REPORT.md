---
record_kind: sandbox_internal_relevance_judgment_report
status: complete_internal_only
project_id: VAKS
created_at: 2026-06-11
truth_boundary: internal_judgment_not_external_human_relevance
action_basis_allowed: false
---

# Phase B Internal Relevance Judgment Report

## Result

```text
judge_id: codex_internal_heuristic_judge_v1
judgment rows: 720
grade_2_relevant: 192
grade_1_borderline: 343
grade_0_not_relevant: 185
```

## Boundary

```text
This fills the relevance judgment file with an internal heuristic/model-assisted judge.
It is separate from expected_terms, but it is not external human judgment.
It is not a weak human substitute or gold standard.
It uses query-specific PROFILES, term/path matches, and VAKS bucket/status priors.
It is only a sanity diagnostic for bias checks and external rejudgment planning.
It does not validate original Yuxi runtime or C-lite.
```
