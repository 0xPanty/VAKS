---
type: sandbox_check
status: completed
created_at: 2026-06-05
scope: seven-candidate-mainline-copy-insertion
truth_boundary: test report only; not reviewed knowledge; not action basis
---

# Mainline Copy Insertion Check

## What Was Tested

The seven candidate mechanisms were inserted into sandbox copies of the two
main architecture documents:

```text
outputs/review/project-sidecar-seven-candidate-pressure-test-2026-06-05/mainline_with_seven_candidates/ARCHITECTURE_PRINCIPLES.md
outputs/review/project-sidecar-seven-candidate-pressure-test-2026-06-05/mainline_with_seven_candidates/FUSION_ARCHITECTURE_V0_2_DRAFT.md
```

The real mainline files were not edited.

## Diff Size

```text
ARCHITECTURE_PRINCIPLES.md: +131 / -0
FUSION_ARCHITECTURE_V0_2_DRAFT.md: +15 / -0
total insertion: +146 / -0
```

## Candidate Vocabulary Counts

| Term | Baseline copy | With seven candidates |
|---|---:|---:|
| `Project Lens` | 0 | 2 |
| `kp_ref` | 0 | 4 |
| `stance` | 3 | 10 |
| `borrow_scope` | 0 | 4 |
| `target_hint` | 0 | 3 |
| `outcome_ref` | 0 | 3 |
| `candidate experience` | 0 | 3 |
| `candidate boundary` | 0 | 2 |
| `tombstone` | 0 | 5 |
| `carry-forward` | 0 | 2 |
| `Default retrieval precedence` | 0 | 2 |

Baseline already has unrelated `supersede/superseded` terminology for temporal
and decision review, so that word is not a clean Project Lens pollution signal.

## Result

```text
mainline_readiness: fail_for_now
sandbox_value: high
pollution_risk: high
```

## Interpretation

The full candidate bundle is easy to write into the architecture, but doing so
turns one minimal boundary paragraph into an object model, field convention,
lifecycle protocol, retrieval policy, and manifest discipline.

The result is readable for a sandbox, but too heavy for current mainline.

Mainline should keep the already-landed generic principle:

```text
project-scoped sidecar overlays are allowed outside generic knowledge points;
they are not truth, reviewed knowledge, ADR, action basis, or confidence.
```

The seven candidate mechanisms should remain in `outputs/review`.
