---
record_kind: sandbox_failure_case_oracle
slice_id: 2026-06-15-p0-06-feedback-validator-sandbox
truth_boundary: oracle_for_sandbox_verification_only
---

# Failure Case Oracle

Each failure case must exit non-zero and include the expected code.

| Case | Expected code | Rule source |
| --- | --- | --- |
| `failure-cases/truth-confidence-delta.md` | `FB_TRUTH_CONFIDENCE_MUTATION` | Feedback cannot modify truth confidence. |
| `failure-cases/truth-confidence-effect.md` | `FB_FORBIDDEN_DIRECT_EFFECT` | Feedback cannot list truth confidence as a direct effect. |
| `failure-cases/affects-truth-confidence.md` | `FB_FORBIDDEN_DIRECT_EFFECT` | Canonical `affects` cannot list truth confidence. |
| `failure-cases/affects-verification-status.md` | `FB_FORBIDDEN_DIRECT_EFFECT` | Canonical `affects` cannot list verification status. |
| `failure-cases/affects-source-reliability.md` | `FB_FORBIDDEN_DIRECT_EFFECT` | Canonical `affects` cannot list source reliability. |
| `failure-cases/verification-status-mutation.md` | `FB_VERIFICATION_STATUS_MUTATION` | Feedback cannot modify verification status. |
| `failure-cases/source-reliability-delta.md` | `FB_SOURCE_RELIABILITY_MUTATION` | Feedback cannot modify source reliability. |
| `failure-cases/source-reliability-mutation-allowed.md` | `FB_SOURCE_RELIABILITY_MUTATION` | Source reliability mutation is not allowed on feedback events. |
| `failure-cases/source-reliability-mutation-allowed-text.md` | `FB_SOURCE_RELIABILITY_MUTATION` | Text values for dangerous authority fields fail closed. |
| `failure-cases/reviewed-note-mutation.md` | `FB_REVIEWED_NOTE_MUTATION` | Feedback cannot mutate reviewed notes. |
| `failure-cases/reviewed-note-mutation-text.md` | `FB_REVIEWED_NOTE_MUTATION` | Text mutation intent also blocks, not only boolean true. |
| `failure-cases/mutates-reviewed-note-text.md` | `FB_REVIEWED_NOTE_MUTATION` | Text in `mutates_reviewed_note` also blocks. |
| `failure-cases/reviewed-relation-mutation.md` | `FB_REVIEWED_RELATION_MUTATION` | Feedback cannot mutate reviewed relations. |
| `failure-cases/reviewed-relation-mutation-text.md` | `FB_REVIEWED_RELATION_MUTATION` | Text relation mutation intent also blocks. |
| `failure-cases/mutates-reviewed-relation-text.md` | `FB_REVIEWED_RELATION_MUTATION` | Text in `mutates_reviewed_relation` also blocks. |
| `failure-cases/reviewed-relation-strength-delta.md` | `FB_REVIEWED_RELATION_MUTATION` | Feedback cannot directly change reviewed relation strength. |
| `failure-cases/reviewed-relation-strength-text.md` | `FB_REVIEWED_RELATION_MUTATION` | Text reviewed relation strength also blocks. |
| `failure-cases/explicit-correction-without-review-due.md` | `FB_EXPLICIT_CORRECTION_WITHOUT_REVIEW_DUE` | Explicit correction must create or reference review_due. |
| `failure-cases/negative-without-review-pressure.md` | `FB_NEGATIVE_WITHOUT_REVIEW_PRESSURE` | Negative feedback creates review pressure first. |
| `failure-cases/action-basis-allowed.md` | `FB_ACTION_BASIS_ALLOWED` | Feedback records cannot become action basis. |
| `failure-cases/action-basis-allowed-text.md` | `FB_ACTION_BASIS_ALLOWED` | Text in `action_basis_allowed` also blocks. |
| `failure-cases/wrong-warning-code.md` | `FB_MISSING_FEEDBACK_NOT_TRUTH_WARNING` | Feedback warning must remain feedback_not_truth. |
| `failure-cases/global-negative-knowledge.md` | `FB_GLOBAL_NEGATIVE_KNOWLEDGE_FROM_LOCAL_FEEDBACK` | Feedback events cannot create global negative knowledge. |
| `failure-cases/global-negative-knowledge-review-completed.md` | `FB_GLOBAL_NEGATIVE_KNOWLEDGE_FROM_LOCAL_FEEDBACK` | `review_completed` does not make global negative knowledge a feedback-event field. |
| `failure-cases/global-negative-knowledge-text.md` | `FB_GLOBAL_NEGATIVE_KNOWLEDGE_FROM_LOCAL_FEEDBACK` | Text in `global_negative_knowledge` also blocks. |
| `failure-cases/missing-scope-binding.md` | `FB_MISSING_SCOPE_BINDING` | Feedback must bind to project_ref or observed_in_context. |
| `failure-cases/promotion-from-feedback.md` | `FB_PROMOTION_FROM_FEEDBACK` | Feedback cannot create reviewed relation or promote knowledge. |
| `failure-cases/promotion-from-feedback-text.md` | `FB_PROMOTION_FROM_FEEDBACK` | Text in promotion authority fields also blocks. |
| `failure-cases/promotes-reviewed-knowledge-text.md` | `FB_PROMOTION_FROM_FEEDBACK` | Feedback cannot promote reviewed knowledge directly. |
| `failure-cases/unknown-effect.md` | `FB_UNKNOWN_EFFECT` | Unknown effects must not silently pass. |
| `failure-cases/incomplete-never-affects.md` | `FB_INCOMPLETE_NEVER_AFFECTS_DIRECTLY` | Boundary marker must include truth, verification, and source reliability. |
