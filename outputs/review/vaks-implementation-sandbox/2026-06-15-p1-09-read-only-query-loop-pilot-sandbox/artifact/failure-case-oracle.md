---
record_kind: sandbox_failure_case_oracle
slice_id: 2026-06-15-p1-09-read-only-query-loop-pilot-sandbox
status: implemented_pending_review
truth_boundary: validator_fixture_guidance_only
---

# Failure Case Oracle

| Failure case | Expected primary code |
|---|---|
| `ordinary-query-overstrict-full-audit.md` | `QL_ORDINARY_QUERY_OVERSTRICT` |
| `action-adjacent-missing-support-check.md` | `QL_ACTION_ADJACENT_MISSING_GATE` |
| `action-adjacent-claims-action-basis.md` | `QL_READ_ONLY_ACTION_BASIS_CLAIM` |
| `candidate-used-as-support.md` | `QL_CANDIDATE_USED_AS_SUPPORT` |
| `candidate-warning-missing.md` | `QL_CANDIDATE_WARNING_MISSING` |
| `stale-decision-ready-action.md` | `QL_STALE_DECISION_READY_ACTION` |
| `stale-warning-missing.md` | `QL_STALE_WARNING_MISSING` |
| `feedback-mutates-truth.md` | `QL_FEEDBACK_MUTATES_TRUTH` |
| `feedback-review-due-missing.md` | `QL_FEEDBACK_REVIEW_DUE_MISSING` |
| `agent-propose-write-missing-operation-receipt.md` | `QL_OPERATION_RECEIPT_REQUIRED` |
| `operation-receipt-required-missing-generic.md` | `QL_OPERATION_RECEIPT_REQUIRED` |
| `agent-propose-write-performs-reviewed-write.md` | `QL_AGENT_PROPOSE_WRITE_PERFORMED_WRITE` |
| `forbidden-side-effect-commit.md` | `QL_FORBIDDEN_SIDE_EFFECT` |
| `invalid-retrieval-receipt-cross-bucket.md` | `QL_RETRIEVAL_RECEIPT_INVALID` + `RV_CROSS_BUCKET_RRF` |
| `invalid-operation-receipt-unknown-actor.md` | `QL_OPERATION_RECEIPT_INVALID` + `OV_UNKNOWN_ACTOR_TIER` |
| `operation-receipt-claims-approval.md` | `QL_OPERATION_RECEIPT_INVALID` + `OV_RECEIPT_CLAIMS_AUTHORITY` |

The suite runner allows extra issue codes when a scenario violates more than
one boundary, but every expected code must be present.

This oracle is fixture guidance only. It is not reviewed knowledge, evidence
support, reviewer approval, action basis, or mainline readiness.
