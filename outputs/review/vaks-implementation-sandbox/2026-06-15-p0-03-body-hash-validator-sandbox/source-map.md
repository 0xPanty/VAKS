---
record_kind: sandbox_source_map
slice_id: 2026-06-15-p0-03-body-hash-validator-sandbox
status: draft
truth_boundary: source_map_for_sandbox_only
---

# Source Map

## Source Files Read

| Source | Used For | Boundary |
|---|---|---|
| `AGENTS.md` | Workspace router and protected path boundaries. | Local operating rule, not a new artifact source. |
| `outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md` lines 2181-2194 | P0-03 artifact target and must-block cases. | Implemented only as sandbox-local prototype, not mainline `tools/`. |
| `REVIEW_QUEUE.md` lines 341-352 | Canonical body hash rule and approval drift rule. | Rule source for validator behavior. |
| `templates/review-candidate.md` lines 41-44 | Canonical template shape: `review_object_state`, `candidate_body_location: "# Candidate Body"`, `body_hash`, body hash algorithm. | Read-only source; this slice does not edit `templates/`. |
| `outputs/review/vaks-implementation-sandbox/2026-06-15-p0-02-operation-receipt-template-sandbox/product-acceptance-report.md` | Confirms P0-02 `PASS_PRODUCT_GRADE` and points P0-03 as next body hash validator sandbox. | Prior slice state only. |

## Requirement Mapping

| Requirement | Implemented In |
|---|---|
| Canonical body hash rule | `artifact/body_hash_validator_sandbox.py`, `artifact/validator-contract.md` |
| Body hash mismatch blocked | `failure-cases/body-hash-mismatch.md` |
| Checked body hash mismatch blocked | `failure-cases/checked-body-hash-mismatch.md` |
| Fixed/approved missing body hash blocked | `failure-cases/fixed-approved-missing-body-hash.md` |
| Writeback-ready changed body blocked | `failure-cases/writeback-ready-body-changed.md` |
| Template-shaped `review_object_state` support | `fixtures/valid-template-section-candidate.md`, `failure-cases/template-fixed-missing-body-hash.md` |
| Same-file section locator support | `fixtures/valid-template-section-candidate.md` |
| CRLF normalization support | `fixtures/valid-crlf-normalization.md`, verification CRLF literal check |
| Positive fixture pass | `fixtures/valid-approved-candidate.md`, `fixtures/valid-draft-no-hash.md`, `fixtures/valid-heading-normalization.md`, `fixtures/valid-template-section-candidate.md`, `fixtures/valid-crlf-normalization.md` |
| Single expected failure oracle | `artifact/failure-case-oracle.md` |
| Validator boundary | `artifact/contract-notes.md`, `verification.md`, reports |

## Out Of Scope

- No mainline `tools/validate_review_candidate_body_hash.py` is created.
- No `templates/` file is created or modified.
- No approval, promotion, reviewed write, commit, push, or Obsidian sync is
  performed.
