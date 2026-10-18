---
record_kind: sandbox_completion_audit
status: candidate
project_id: VAKS
created_at: 2026-06-11
truth_boundary: completion_audit_not_mainline_adoption
action_basis_allowed: false
---

# Phase B Sandbox Completion Audit

## User Request

Do Phase B in a sandbox, pressure test it quantitatively, compare:

- before vs after adding Phase B
- VAKS+B vs original Yuxi shape
- multiple dimensions under pressure

Only keep it if there is a clear positive result.

## Completion Check

| Requirement | Status | Evidence |
|---|---|---|
| Run in sandbox | passed | All new artifacts are under `outputs/review/vaks-yuxi-phase-b-pressure-test-2026-06-11/`. Core VAKS docs were not modified in this run. |
| Test Phase B only | passed | The kept candidate is `vaks_b_bucket_local`: parser/chunk/index-style retrieval, bucket-local authority ordering, click-back, adapter labels, hashes, receipts, and stale warnings. |
| Baseline vs added | passed | `baseline_file_lexical` vs `vaks_b_bucket_local` in `results/phase_b_summary.csv`. |
| Added vs Yuxi shape | passed with limitation | `vaks_b_bucket_local` vs `yuxi_native_profile` in `results/phase_b_summary.csv`; see `external/YUXI_LOCAL_REPO_EVIDENCE.md` for original Yuxi code evidence and Docker limitation. |
| Multi-dimensional metrics | passed | hit@5, hit@10, MRR, action leakage, forbidden top1, cross-bucket violation, warning coverage, click-back, hash coverage, adapter coverage, receipt coverage, stale detection. |
| Pressure corpus | passed | 30 queries across primary and full noisy corpora; 4 modes; 240 per-query metric rows; 2400 top-result rows. |
| Clear positive result | passed | Full noisy hit@5 improved from 27/30 to 30/30 while action leakage dropped from 1.0000 to 0.0000. |
| Boundary preserved | passed | Report and keep decision are candidate/sandbox only with `action_basis_allowed: false`; no C-lite, Skills, MCP writes, subagents, formal writeback, or production adoption approved. |

## Original Yuxi Limitation

Original Yuxi was not run end to end because Docker is not installed on this
machine. To avoid pretending otherwise, this run used a code/doc-aligned
`yuxi_native_profile` comparator based on inspected Yuxi retrieval/runtime
files.

This means the result supports a Phase B VAKS design decision, not a benchmark
claim against a live production Yuxi deployment.

## Verdict

The objective is complete for sandbox evaluation.

Keep:

```text
Yuxi-like parser/chunk/hybrid retrieval/click-back ideas
+ VAKS authority-bucket ordering before final ranking
+ VAKS adapter labels, hashes, receipts, and warnings
```

Do not keep:

```text
Yuxi-like global retrieval without VAKS bucket-local ordering
```

Do not promote yet:

```text
C-lite
Skills
MCP writes
subagents
formal writeback
mainline adoption
production readiness
```
