---
record_kind: sandbox_failure_case_oracle
slice_id: 2026-06-15-p0-07-action-boundary-failure-matrix-sandbox
truth_boundary: oracle_for_sandbox_verification_only
---

# Failure Case Oracle

Each failure case must exit non-zero and include the expected code.

| Case | Expected code | Rule source |
| --- | --- | --- |
| `failure-cases/missing-required-case.json` | `MATRIX_MISSING_REQUIRED_CASE` | Matrix must include all AB-01..AB-12 cases. |
| `failure-cases/missing-case-field.json` | `MATRIX_CASE_MISSING_FIELD` | Each case needs required fields including detection. |
| `failure-cases/forbidden-authority-claim.json` | `MATRIX_FORBIDDEN_AUTHORITY_CLAIM` | Matrix cannot claim mainline/reviewer/truth/action authority. |
| `failure-cases/unblocked-outcome.json` | `MATRIX_CASE_NOT_BLOCKING` | Failure cases must block, mark not ready, require review, or reject. |
| `failure-cases/duplicate-case-id.json` | `MATRIX_DUPLICATE_CASE_ID` | Case IDs must be unique. |
| `failure-cases/unknown-ab-case-id.json` | `MATRIX_UNKNOWN_CASE_ID` | Unknown `AB-*` IDs are not part of the P0 minimum scope. |
| `failure-cases/missing-guard-entry.json` | `MATRIX_CASE_MISSING_GUARD` | `blocked_by` entries need both `slice_id` and `guard`. |

This oracle is not a validator approval, reviewed knowledge, evidence support,
action basis, or mainline readiness.

