---
record_kind: sandbox_pressure_report
status: candidate
project_id: VAKS
created_at: 2026-06-11
truth_boundary: diagnostic_not_mainline_decision
action_basis_allowed: false
---

# VAKS Phase B Retrieval Pressure Report

## Plain-Language Verdict

Phase B does not yet pass the keep bar.

Reason:

- Retrieval positive: False
- Governance positive: True

Keep iterating in sandbox before any adoption.

## Corpus Stats

| Corpus | Files | Chunks | Stale Paths |
|---|---:|---:|---|
| primary | 336 | 3947 | FEEDBACK.md, SCHEMA.md, SOURCE_INTAKE.md |
| full | 4193 | 18708 | FEEDBACK.md, SCHEMA.md, SOURCE_INTAKE.md |

## Summary Metrics

| Corpus | Mode | hit@5 | hit@10 | MRR | action leakage | forbidden top1 | cross-bucket violation | warning coverage | clickback | hash | adapter | receipt | stale detection |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| full | baseline_file_lexical | 13/15 | 13/15 | 0.4944 | 1.0000 | 0.8333 | 0.8333 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| full | vaks_b_adapter_skeleton | 13/15 | 13/15 | 0.7591 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |
| full | vaks_b_adapter_v1 | 11/15 | 12/15 | 0.5924 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |
| full | vaks_b_adapter_v1_1 | 13/15 | 13/15 | 0.7591 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |
| full | vaks_b_bucket_local | 10/15 | 12/15 | 0.4165 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |
| full | vaks_b_bucketless | 8/15 | 8/15 | 0.5137 | 0.8333 | 0.8333 | 0.8333 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |
| full | yuxi_native_profile | 8/15 | 8/15 | 0.5137 | 1.0000 | 0.8333 | 0.8333 | 0.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| primary | baseline_file_lexical | 9/15 | 12/15 | 0.4633 | 1.0000 | 0.8333 | 0.8333 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| primary | vaks_b_adapter_skeleton | 12/15 | 13/15 | 0.7811 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |
| primary | vaks_b_adapter_v1 | 10/15 | 12/15 | 0.6088 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |
| primary | vaks_b_adapter_v1_1 | 12/15 | 13/15 | 0.7811 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |
| primary | vaks_b_bucket_local | 9/15 | 10/15 | 0.4724 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |
| primary | vaks_b_bucketless | 10/15 | 11/15 | 0.5808 | 0.6667 | 0.6667 | 0.6667 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |
| primary | yuxi_native_profile | 10/15 | 11/15 | 0.5808 | 1.0000 | 0.6667 | 0.6667 | 0.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## Key Comparisons

Primary corpus:

- baseline hit@5: 9/15
- VAKS+B bucket-local hit@5: 9/15
- VAKS+B adapter v1 hit@5: 10/15
- VAKS+B adapter v1.1 hit@5: 12/15
- VAKS+B adapter skeleton hit@5: 12/15
- Yuxi-native profile hit@5: 10/15
- VAKS+B action leakage: 0.0000
- VAKS+B adapter v1 action leakage: 0.0000
- VAKS+B adapter v1.1 action leakage: 0.0000
- VAKS+B adapter skeleton action leakage: 0.0000
- Yuxi-native action leakage: 1.0000

Full noisy corpus:

- baseline hit@5: 13/15
- VAKS+B bucket-local hit@5: 10/15
- VAKS+B adapter v1 hit@5: 11/15
- VAKS+B adapter v1.1 hit@5: 13/15
- VAKS+B adapter skeleton hit@5: 13/15
- Yuxi-native profile hit@5: 8/15
- VAKS+B action leakage: 0.0000
- VAKS+B adapter v1 action leakage: 0.0000
- VAKS+B adapter v1.1 action leakage: 0.0000
- VAKS+B adapter skeleton action leakage: 0.0000
- Yuxi-native action leakage: 1.0000

## Notes

- Original Yuxi was not run end to end because Docker is not installed locally.
- `yuxi_native_profile` is a code/doc-aligned local comparator: global hybrid retrieval + graph-like fusion + click-back, without VAKS authority governance.
- These results are sandbox diagnostics only. They do not create reviewed knowledge, production readiness, or mainline adoption.
