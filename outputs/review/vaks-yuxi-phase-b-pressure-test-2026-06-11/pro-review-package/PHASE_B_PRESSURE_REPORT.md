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

Phase B is worth keeping as a sandbox candidate.

Reason:

- It improves retrieval over the file-level baseline, especially in the noisy corpus.
- It keeps VAKS governance stronger than the Yuxi-native profile.
- It gives click-back, hash, adapter, and receipt coverage that baseline and Yuxi-native do not provide.

Boundary:

- This supports keeping Phase B in sandbox.
- It does not approve C-lite, Skills, MCP writes, subagents, or formal writeback.

## Corpus Stats

| Corpus | Files | Chunks | Stale Paths |
|---|---:|---:|---|
| primary | 339 | 3975 | FEEDBACK.md, SCHEMA.md, SOURCE_INTAKE.md |
| full | 4198 | 18769 | FEEDBACK.md, SCHEMA.md, SOURCE_INTAKE.md |

## Summary Metrics

| Corpus | Mode | hit@5 | hit@10 | MRR | action leakage | forbidden top1 | cross-bucket violation | warning coverage | clickback | hash | adapter | receipt | stale detection |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| full | baseline_file_lexical | 27/30 | 29/30 | 0.7272 | 1.0000 | 0.9500 | 0.9500 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| full | vaks_b_adapter_skeleton | 30/30 | 30/30 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| full | vaks_b_adapter_v1 | 30/30 | 30/30 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| full | vaks_b_adapter_v1_1 | 30/30 | 30/30 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| full | vaks_b_bucket_local | 30/30 | 30/30 | 0.8528 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| full | vaks_b_bucketless | 29/30 | 29/30 | 0.9041 | 0.7500 | 0.7500 | 0.7500 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |
| full | yuxi_native_profile | 29/30 | 29/30 | 0.9041 | 1.0000 | 0.7500 | 0.7500 | 0.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| primary | baseline_file_lexical | 27/30 | 29/30 | 0.7766 | 1.0000 | 0.9500 | 0.9500 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| primary | vaks_b_adapter_skeleton | 30/30 | 30/30 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| primary | vaks_b_adapter_v1 | 30/30 | 30/30 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| primary | vaks_b_adapter_v1_1 | 30/30 | 30/30 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| primary | vaks_b_bucket_local | 30/30 | 30/30 | 0.9233 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| primary | vaks_b_bucketless | 30/30 | 30/30 | 0.9511 | 0.5000 | 0.5000 | 0.5000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| primary | yuxi_native_profile | 30/30 | 30/30 | 0.9511 | 1.0000 | 0.5000 | 0.5000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## Key Comparisons

Primary corpus:

- baseline hit@5: 27/30
- VAKS+B bucket-local hit@5: 30/30
- VAKS+B adapter v1 hit@5: 30/30
- VAKS+B adapter v1.1 hit@5: 30/30
- VAKS+B adapter skeleton hit@5: 30/30
- Yuxi-native profile hit@5: 30/30
- VAKS+B action leakage: 0.0000
- VAKS+B adapter v1 action leakage: 0.0000
- VAKS+B adapter v1.1 action leakage: 0.0000
- VAKS+B adapter skeleton action leakage: 0.0000
- Yuxi-native action leakage: 1.0000

Full noisy corpus:

- baseline hit@5: 27/30
- VAKS+B bucket-local hit@5: 30/30
- VAKS+B adapter v1 hit@5: 30/30
- VAKS+B adapter v1.1 hit@5: 30/30
- VAKS+B adapter skeleton hit@5: 30/30
- Yuxi-native profile hit@5: 29/30
- VAKS+B action leakage: 0.0000
- VAKS+B adapter v1 action leakage: 0.0000
- VAKS+B adapter v1.1 action leakage: 0.0000
- VAKS+B adapter skeleton action leakage: 0.0000
- Yuxi-native action leakage: 1.0000

## Notes

- Original Yuxi was not run end to end because Docker is not installed locally.
- `yuxi_native_profile` is a code/doc-aligned local comparator: global hybrid retrieval + graph-like fusion + click-back, without VAKS authority governance.
- These results are sandbox diagnostics only. They do not create reviewed knowledge, production readiness, or mainline adoption.
