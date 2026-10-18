---
record_kind: sandbox_failure_case_oracle
slice_id: 2026-06-15-p1-10-runtime-artifact-exclusion-test-sandbox
status: implemented_pending_review
truth_boundary: validator_fixture_guidance_only
---

# Failure Case Oracle

| Failure case | Expected primary code |
|---|---|
| `runtime-filter-disabled.json` | `RA_RUNTIME_FILTER_DISABLED` |
| `pycache-selected.json` | `RA_RUNTIME_ARTIFACT_SELECTED` |
| `suite-output-as-support.json` | `RA_RUNTIME_ARTIFACT_AS_SUPPORT` |
| `suite-output-pack-role-evidence-support.json` | `RA_RUNTIME_ARTIFACT_AS_SUPPORT` |
| `generated-receipt-action-basis.json` | `RA_RUNTIME_ARTIFACT_ACTION_BASIS` |
| `generated-receipt-pack-role-action-basis.json` | `RA_RUNTIME_ARTIFACT_ACTION_BASIS` |
| `runtime-bad-exclusion-reason.json` | `RA_RUNTIME_ARTIFACT_BAD_EXCLUSION_REASON` |
| `runtime-not-excluded.json` | `RA_RUNTIME_ARTIFACT_NOT_EXCLUDED` |
| `runtime-mislabeled-false.json` | `RA_RUNTIME_ARTIFACT_MISLABELED` |
| `runtime-path-underscore-mislabeled-selected.json` | `RA_RUNTIME_ARTIFACT_MISLABELED` + `RA_RUNTIME_ARTIFACT_SELECTED` |
| `runtime-path-space-mislabeled-selected.json` | `RA_RUNTIME_ARTIFACT_MISLABELED` + `RA_RUNTIME_ARTIFACT_SELECTED` |
| `unknown-artifact-kind.json` | `RA_UNKNOWN_ARTIFACT_KIND` |
| `runtime-reviewed-authority-bucket.json` | `RA_RUNTIME_ARTIFACT_AUTHORITY_BUCKET` |
| `runtime-raw-authority-bucket.json` | `RA_RUNTIME_ARTIFACT_AUTHORITY_BUCKET` |
| `runtime-support-authority-bucket.json` | `RA_RUNTIME_ARTIFACT_AUTHORITY_BUCKET` |
| `runtime-action-authority-bucket.json` | `RA_RUNTIME_ARTIFACT_AUTHORITY_BUCKET` |
| `runtime-claims-authority.json` | `RA_RUNTIME_ARTIFACT_CLAIMS_AUTHORITY` |
| `duplicate-item-id.json` | `RA_DUPLICATE_ITEM_ID` |
| `derived-index-selected.json` | `RA_RUNTIME_ARTIFACT_SELECTED` |
| `missing-items.json` | `RA_MISSING_ITEMS` |

The suite runner allows extra issue codes when a manifest violates more than
one boundary, but every expected code must be present.

This oracle is fixture guidance only. It is not reviewed knowledge, evidence
support, reviewer approval, action basis, or mainline readiness.
