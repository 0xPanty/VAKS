# Obsidian Disposable Vault Absorption Pilot Report

Passed: `true`

## Summary

- Guards tested: 7
- Positive cases: 7 / 7
- Failure cases caught: 6 / 6
- Positive oracle cases: 7
- Failure oracle cases: 6
- Fixture oracle used: True
- Failure oracle used: True
- Disposable vault deleted: True
- Runtime samples retained: False
- Formal Obsidian vault touched: False
- Mainline files touched: False
- Tools promoted: False

## Interpretation

The seven candidates can be exercised as sandbox-only lazy gates against Obsidian-style Markdown and JSON records.
This proves absorption readiness, not mainline absorption.

## Case Results

| Case | Guard | Runtime sample deleted after run | Result | Codes |
| --- | --- | --- | --- | --- |
| `body_hash_valid` | `p0-03` | yes | `True` | `` |
| `body_hash_tampered` | `p0-03` | yes | `False` | `body_hash_mismatch` |
| `support_boundary_valid` | `p0-04` | yes | `True` | `` |
| `candidate_claimed_as_support` | `p0-04` | yes | `False` | `candidate_as_support` |
| `action_readiness_valid` | `p0-05` | yes | `pass` | `` |
| `destructive_action_without_rollback` | `p0-05` | yes | `fail` | `AR_DESTRUCTIVE_MISSING_ROLLBACK` |
| `feedback_valid` | `p0-06` | yes | `pass` | `` |
| `feedback_truth_confidence_mutation` | `p0-06` | yes | `fail` | `FB_FORBIDDEN_DIRECT_EFFECT, FB_TRUTH_CONFIDENCE_MUTATION` |
| `failure_matrix_valid` | `p0-07` | yes | `pass` | `` |
| `receipt_valid` | `p1-08` | yes | `True` | `` |
| `retrieval_candidate_as_support` | `p1-08` | yes | `False` | `RV_CANDIDATE_OVERLAY_FEEDBACK_AS_SUPPORT` |
| `runtime_artifact_exclusion_valid` | `p1-10` | yes | `True` | `` |
| `runtime_pycache_selected` | `p1-10` | yes | `False` | `RA_RUNTIME_ARTIFACT_SELECTED` |

## Boundary

This report is sandbox evidence only. It is not a mainline merge, not reviewed knowledge, not evidence support, not action basis, not Opus approval, not user approval, not commit, not push, and not sync.
