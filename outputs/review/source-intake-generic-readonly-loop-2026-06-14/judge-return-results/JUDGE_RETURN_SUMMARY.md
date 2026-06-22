# Semantic Support Judge Return Summary

Status: completed with partial sufficiency.

Scope: excerpt-based semantic-support judgment for the generic read-only loop judge packet only. This is not Source Intake P0 approval, production runtime validation, reviewed truth promotion, or action readiness.

## Inputs

- Judge A return: `returned_judge_a.csv`
- Judge B return: `returned_judge_b.csv`
- Base template: `../results/semantic_support_judgment_template.csv`
- Merge output: `semantic_support_judgment_merged.csv`
- Arbitration queue: `semantic_support_arbitration_queue.csv`
- Arbiter return: `returned_arbiter.csv`
- Final adjudicated output: `semantic_support_judgment_final.csv`
- Final summary: `semantic_support_judgment_final_summary.json`

## Merge Result

- Rows: 11
- Judge A completed rows: 11
- Judge B completed rows: 11
- Initial agreement rows: 8
- Arbitration rows: 3
- Missing or invalid rows: 0
- Baseline visible-field integrity errors: 0

## Final Adjudicated Result

- Final relevance 2 count: 11
- Final sufficiency 2 count: 5
- Final sufficiency 1 count: 6
- Final sufficiency 0 count: 0

Fully sufficient rows:

- `judge-row-001`
- `judge-row-007`
- `judge-row-008`
- `judge-row-010`
- `judge-row-011`

Relevant but only partially sufficient rows:

- `judge-row-002`
- `judge-row-003`
- `judge-row-004`
- `judge-row-005`
- `judge-row-006`
- `judge-row-009`

## Interpretation

The judge dispatch and merge process completed. All allowed anchors were judged relevant to their visible query and claim. However, six rows were only partially sufficient, so the result should be reported as independent semantic-support judgment completed with partial sufficiency, not as fully supported evidence, P0 pass, or action readiness.
