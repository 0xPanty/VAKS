---
record_kind: sandbox_iteration_locked_baseline_comparison
status: candidate
project_id: VAKS
created_at: 2026-06-11
truth_boundary: diagnostic_not_mainline_decision
action_basis_allowed: false
---

# Phase B v1 vs Locked v0 Baseline

## Compared Versions

- Locked v0: the previous passing `vaks_b_bucket_local` summary saved before this iteration.
- v1: `vaks_b_adapter_v1`, adding anchor/path/exact-phrase aware ordering inside VAKS authority buckets.

## Main Pressure Set

| Corpus | Metric | locked v0 | v1 | Result |
|---|---|---:|---:|---|
| primary | hit@5 | 30/30 | 30/30 | same |
| primary | hit@10 | 30/30 | 30/30 | same |
| primary | MRR | 0.9083 | 1.0000 | improved |
| primary | action leakage | 0.0000 | 0.0000 | same |
| primary | forbidden top1 | 0.0000 | 0.0000 | same |
| primary | cross-bucket violation | 0.0000 | 0.0000 | same |
| full | hit@5 | 30/30 | 30/30 | same |
| full | hit@10 | 30/30 | 30/30 | same |
| full | MRR | 0.8528 | 1.0000 | improved |
| full | action leakage | 0.0000 | 0.0000 | same |
| full | forbidden top1 | 0.0000 | 0.0000 | same |
| full | cross-bucket violation | 0.0000 | 0.0000 | same |

## Holdout Pressure Set

The holdout set was added after v1 looked suspiciously perfect on the original
test wording. It uses paraphrased questions and separate outputs.

| Corpus | Metric | v0 | v1 | Result |
|---|---|---:|---:|---|
| primary | hit@5 | 9/15 | 10/15 | improved |
| primary | hit@10 | 10/15 | 12/15 | improved |
| primary | MRR | 0.4771 | 0.6144 | improved |
| primary | action leakage | 0.0000 | 0.0000 | same |
| primary | forbidden top1 | 0.0000 | 0.0000 | same |
| primary | cross-bucket violation | 0.0000 | 0.0000 | same |
| full | hit@5 | 9/15 | 11/15 | improved |
| full | hit@10 | 12/15 | 12/15 | same |
| full | MRR | 0.3665 | 0.5868 | improved |
| full | action leakage | 0.0000 | 0.0000 | same |
| full | forbidden top1 | 0.0000 | 0.0000 | same |
| full | cross-bucket violation | 0.0000 | 0.0000 | same |

## Regression Notes

Holdout query-level MRR had two regressions:

- `h13_resource_filter_before_search` on primary: v1 moved a weak but measurable expected hit out of top 20. This is a real weakness for Yuxi-style middleware/resource-filter questions in the primary corpus.
- `h10_old_sandbox_benchmark_truth` on full: v1 moved `IMPLEMENTATION_BLUEPRINT.md` / lint-health material above `templates/maintenance-manifest.md`. This may be a metric narrowness issue, but it should still be reviewed before mainline adoption.

## Verdict

v1 is a positive sandbox step over locked v0.

Keep v1 as the next sandbox candidate because:

- Main pressure MRR improves to 1.0000 on both corpora.
- Holdout hit@5, hit@10, and MRR improve overall.
- Boundary metrics stay at zero leakage.

Do not promote v1 to mainline yet because:

- The holdout regressions need a v1.1 regression pass.
- The implementation is still a sandbox harness, not a production adapter.
- Original Yuxi was still not run end to end locally.
