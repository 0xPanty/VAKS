---
record_kind: sandbox_failure_case_oracle
slice_id: 2026-06-15-p0-05-action-readiness-validator-sandbox
truth_boundary: oracle_for_sandbox_verification_only
---

# Failure Case Oracle

Each failure case must exit non-zero and include the expected code.

| Case | Expected code | Rule source |
| --- | --- | --- |
| `failure-cases/insufficient-evidence-ready.md` | `AR_INSUFFICIENT_EVIDENCE_READY` | P0-05 must block insufficient evidence but ready. |
| `failure-cases/weak-evidence-ready.md` | `AR_EVIDENCE_SUFFICIENCY_NOT_SUFFICIENT` | Ready action basis must be explicitly sufficient, not weak. |
| `failure-cases/unchecked-evidence-ready.md` | `AR_EVIDENCE_SUFFICIENCY_NOT_SUFFICIENT` | Ready action basis must not skip sufficiency. |
| `failure-cases/missing-evidence-sufficiency-ready.md` | `AR_EVIDENCE_SUFFICIENCY_NOT_SUFFICIENT` | Ready action basis must declare sufficiency. |
| `failure-cases/out-of-scope-ready.md` | `AR_OUT_OF_SCOPE_READY` | P0-05 must block out_of_scope but ready. |
| `failure-cases/stale-without-replacement-ready.md` | `AR_STALE_SUPERSEDED_WITHOUT_REPLACEMENT_READY` | Stale basis needs replacement or narrowed scope. |
| `failure-cases/superseded-without-replacement-ready.md` | `AR_STALE_SUPERSEDED_WITHOUT_REPLACEMENT_READY` | Superseded basis needs replacement or narrowed scope. |
| `failure-cases/unresolved-risk-ready.md` | `AR_UNRESOLVED_RISK_READY` | Unresolved risk cannot be action ready. |
| `failure-cases/hidden-warning-trimmed-ready.md` | `AR_HIDDEN_WARNING_OR_GAP_READY` | Hidden warning/gap/missing evidence due to trimming blocks ready. |
| `failure-cases/missing-intent-confirmation-ready.md` | `AR_MISSING_INTENT_CONFIRMATION` | Significant action requires intent confirmation. |
| `failure-cases/significant-action-intent-self-disabled-ready.md` | `AR_MISSING_INTENT_CONFIRMATION` | Significant action cannot self-disable intent confirmation. |
| `failure-cases/missing-success-criteria-ready.md` | `AR_MISSING_SUCCESS_CRITERIA` | Significant action basis needs visible success criteria. |
| `failure-cases/missing-reviewed-action-basis-ready.md` | `AR_MISSING_REVIEWED_ACTION_BASIS` | Ready action basis needs reviewed support or evidence packet reference. |
| `failure-cases/candidate-basis-ready.md` | `AR_CANDIDATE_BASIS_READY` | Candidate material is review input, not action basis. |
| `failure-cases/feedback-basis-ready.md` | `AR_FEEDBACK_BASIS_READY` | Feedback may create review pressure, not direct action basis. |
| `failure-cases/retrieval-rank-basis-ready.md` | `AR_RETRIEVAL_RANK_BASIS_READY` | Retrieval rank is not trust or readiness. |
| `failure-cases/source-summary-basis-ready.md` | `AR_SOURCE_SUMMARY_BASIS_READY` | Source summary cannot self-serve as final action support. |
| `failure-cases/context-pack-only-ready.md` | `AR_CONTEXT_PACK_ONLY_READY` | Context pack prepares attention; it is not action basis by itself. |
| `failure-cases/diagnostic-pass-basis-ready.md` | `AR_DIAGNOSTIC_BASIS_READY` | Test/lint/validator/blind review are diagnostic, not approval or basis. |
| `failure-cases/reviewed-write-missing-approval.md` | `AR_REVIEWED_WRITE_MISSING_APPROVAL` | Reviewed write needs explicit approval. |
| `failure-cases/reviewed-write-missing-checked-body-hash.md` | `AR_REVIEWED_WRITE_MISSING_CHECKED_BODY_HASH` | Reviewed write needs checked body hash. |
| `failure-cases/destructive-without-rollback-ready.md` | `AR_DESTRUCTIVE_MISSING_ROLLBACK` | Destructive operation needs rollback plan. |
| `failure-cases/action-delete-without-rollback-ready.md` | `AR_DESTRUCTIVE_MISSING_ROLLBACK` | Action-mode delete also needs rollback plan. |
| `failure-cases/read-only-actor-write-ready.md` | `AR_READ_ONLY_ACTOR_WRITE` | Read-only or suggest-only actor cannot write. |
| `failure-cases/schema-change-missing-owner-final-ready.md` | `AR_SCHEMA_CHANGE_MISSING_OWNER_FINAL` | Schema change needs owner-final. |
