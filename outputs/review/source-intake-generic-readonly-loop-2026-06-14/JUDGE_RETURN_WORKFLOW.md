# Judge Return Workflow

Status: ready_not_judged

This workflow is the next step after the generic read-only loop sandbox package.
It does not complete semantic support judgment by itself. It only defines how to
collect two independent judge returns and produce an arbitration queue.

## Send

Send these files to independent judges:

- Judge A: `semantic-support-judge-a.zip`
- Judge B: `semantic-support-judge-b.zip`

Do not send either judge:

- row-to-case mapping
- expected outcomes
- author-side self-check
- the other judge's filled CSV
- arbiter columns
- the full Pro review package

## Return

Ask each judge to return only the filled CSV from their zip.

Recommended local return paths:

- `judge-return-results/returned_judge_a.csv`
- `judge-return-results/returned_judge_b.csv`

## Merge

After both filled CSVs are returned, run:

From an unpacked followup kit root:

```powershell
python .\merge_semantic_support_judgments.py `
  --judge-a .\judge-return-results\returned_judge_a.csv `
  --judge-b .\judge-return-results\returned_judge_b.csv `
  --base-template .\semantic_support_judgment_template_baseline.csv `
  --out-dir .\judge-return-results
```

From the full workspace root:

```powershell
python tools\merge_semantic_support_judgments.py `
  --judge-a outputs\review\source-intake-generic-readonly-loop-2026-06-14\judge-return-results\returned_judge_a.csv `
  --judge-b outputs\review\source-intake-generic-readonly-loop-2026-06-14\judge-return-results\returned_judge_b.csv `
  --base-template outputs\review\source-intake-generic-readonly-loop-2026-06-14\results\semantic_support_judgment_template.csv `
  --out-dir outputs\review\source-intake-generic-readonly-loop-2026-06-14\judge-return-results
```

Outputs:

- `semantic_support_judgment_merged.csv`
- `semantic_support_arbitration_queue.csv`
- `semantic_support_judgment_merge_summary.json`

The merge step hard-checks that returned `row_id` values and visible fields match
the original dispatch template. If both judges omit the same row or edit the same
visible field, the merge must remain `not_ready_missing_or_invalid_returns`.

## Boundary

Merged semantic-support judgments do not prove Source Intake P0 passed,
production runtime validation, reviewed truth promotion, or action readiness.
They only close the independent relevance/sufficiency judgment step for the
allowed read-only support rows in this sandbox package.
