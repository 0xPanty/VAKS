---
record_kind: sandbox_failure_case_oracle
slice_id: 2026-06-15-p1-11-semantic-anchor-support-check-sandbox
status: implemented_pending_review
truth_boundary: sandbox_oracle_only
---

# Failure Case Oracle

Each failure case contains `expected_valid: false` and one or more
`expected_codes`. The suite only requires the listed codes; extra blocking codes
are allowed when a single bad record violates several boundaries.

| Failure case | Primary expected code |
|---|---|
| `semantic-score-as-support.json` | `SA_SEMANTIC_SCORE_AS_SUPPORT` |
| `graph-rank-as-support.json` | `SA_GRAPH_RANK_AS_SUPPORT` |
| `url-only-direct-support.json` | `SA_URL_ONLY_SUPPORT` |
| `metadata-only-support.json` | `SA_SUPPORT_REQUIRES_STABLE_ANCHOR` |
| `llm-summary-support.json` | `SA_SUMMARY_AS_SUPPORT` |
| `candidate-distillation-support.json` | `SA_CANDIDATE_AS_SUPPORT` |
| `project-overlay-support.json` | `SA_CANDIDATE_AS_SUPPORT` |
| `feedback-event-support.json` | `SA_FEEDBACK_AS_SUPPORT` |
| `runtime-artifact-anchor.json` | `SA_RUNTIME_ARTIFACT_ANCHOR` |
| `generated-receipt-support.json` | `SA_RUNTIME_ARTIFACT_AS_SUPPORT` |
| `missing-selector-support.json` | `SA_MISSING_SELECTOR` |
| `missing-source-ref-support.json` | `SA_MISSING_SOURCE_REF` |
| `unknown-anchor-kind.json` | `SA_UNKNOWN_ANCHOR_KIND` |
| `action-basis-claim.json` | `SA_ANCHOR_CLAIMS_ACTION_BASIS` |
| `reviewed-knowledge-claim.json` | `SA_ANCHOR_CLAIMS_REVIEWED_KNOWLEDGE` |
| `self-support-loop.json` | `SA_SELF_SUPPORT_LOOP` |
| `inferential-support-missing-reviewer-note.json` | `SA_INFERENTIAL_SUPPORT_MISSING_REVIEWER_NOTE` |
| `invalid-authority-bucket-support.json` | `SA_AUTHORITY_BUCKET_INVALID_FOR_SUPPORT` |
| `duplicate-anchor-id.json` | `SA_DUPLICATE_ANCHOR_ID` |
| `stable-url-missing-capture.json` | `SA_URL_ONLY_SUPPORT` |
| `support-role-invalid.json` | `SA_SUPPORT_ROLE_INVALID` |
| `missing-anchors.json` | `SA_MISSING_ANCHORS` |

Expected blocks are sandbox validation outcomes only. They do not prove the
inverse: a passing record is still only a well-shaped support candidate.
