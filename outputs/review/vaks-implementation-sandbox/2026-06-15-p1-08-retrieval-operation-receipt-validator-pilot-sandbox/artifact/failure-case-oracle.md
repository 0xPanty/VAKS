---
record_kind: sandbox_failure_case_oracle
slice_id: 2026-06-15-p1-08-retrieval-operation-receipt-validator-pilot-sandbox
status: implemented_pending_review
truth_boundary: validator_fixture_guidance_only
---

# Failure Case Oracle

## Retrieval Cases

| Failure case | Expected primary code |
|---|---|
| `retrieval-unknown-authority-bucket.md` | `RV_UNKNOWN_AUTHORITY_BUCKET` |
| `retrieval-unknown-pack-role.md` | `RV_UNKNOWN_PACK_ROLE` |
| `retrieval-cross-bucket-rrf.md` | `RV_CROSS_BUCKET_RRF` |
| `retrieval-selected-by-as-support.md` | `RV_SELECTED_BY_AS_SUPPORT` |
| `retrieval-candidate-as-support.md` | `RV_CANDIDATE_OVERLAY_FEEDBACK_AS_SUPPORT` |
| `retrieval-feedback-action-basis.md` | `RV_CANDIDATE_OVERLAY_FEEDBACK_AS_SUPPORT` |
| `retrieval-legacy-raw-metadata-used.md` | `RV_LEGACY_RAW_METADATA_USED` |
| `retrieval-graph-rank-as-trust.md` | `RV_GRAPH_RANK_AS_TRUST` |
| `retrieval-url-only-direct-support.md` | `RV_URL_ONLY_DIRECT_SUPPORT` |
| `retrieval-url-only-supported-with-none-role.md` | `RV_URL_ONLY_DIRECT_SUPPORT` |
| `retrieval-missing-independent-anchor.md` | `RV_MISSING_INDEPENDENT_SUPPORT_ANCHOR` |
| `retrieval-receipt-claims-authority.md` | `RV_RECEIPT_CLAIMS_AUTHORITY` |
| `retrieval-boundary-flag-false.md` | `RV_SUPPORT_BOUNDARY_FLAG_FALSE` |

## Operation Cases

| Failure case | Expected primary code |
|---|---|
| `operation-unknown-actor-tier-write.md` | `OV_UNKNOWN_ACTOR_TIER` |
| `operation-unknown-operation-mode.md` | `OV_UNKNOWN_OPERATION_MODE` |
| `operation-read-only-actor-write.md` | `OV_ACTOR_TIER_CANNOT_WRITE` |
| `operation-suggest-only-actor-write.md` | `OV_ACTOR_TIER_CANNOT_WRITE` |
| `operation-reviewed-write-missing-approval-hash.md` | `OV_REVIEWED_WRITE_MISSING_APPROVAL_OR_HASH` |
| `operation-mainline-write-missing-approval-hash.md` | `OV_REVIEWED_WRITE_MISSING_APPROVAL_OR_HASH` |
| `operation-checked-body-hash-mismatch.md` | `OV_CHECKED_BODY_HASH_MISMATCH` |
| `operation-schema-change-without-owner-final.md` | `OV_SCHEMA_CHANGE_MISSING_OWNER_FINAL` |
| `operation-delete-without-rollback.md` | `OV_ROLLBACK_REQUIRED` |
| `operation-missing-intent-confirmation.md` | `OV_MISSING_INTENT_CONFIRMATION` |
| `operation-candidate-as-action-basis.md` | `OV_INVALID_ACTION_BASIS` |
| `operation-candidate-write-out-of-scope.md` | `OV_CANDIDATE_WRITE_OUT_OF_SCOPE` |
| `operation-receipt-claims-authority.md` | `OV_RECEIPT_CLAIMS_AUTHORITY` |
| `operation-boundary-flag-false.md` | `OV_OPERATION_BOUNDARY_FLAG_FALSE` |

## Use

The suite runner reads `expected_valid` and `expected_codes` from each file's
frontmatter. Extra issue codes are allowed when a bad record violates more than
one boundary, but each listed expected code must be present.

This oracle is fixture guidance only. It is not reviewed knowledge, evidence
support, reviewer approval, action basis, or mainline readiness.
