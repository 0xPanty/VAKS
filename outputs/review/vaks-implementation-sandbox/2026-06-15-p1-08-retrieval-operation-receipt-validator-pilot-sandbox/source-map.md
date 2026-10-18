---
record_kind: sandbox_source_map
slice_id: 2026-06-15-p1-08-retrieval-operation-receipt-validator-pilot-sandbox
status: implemented_pending_review
truth_boundary: sandbox_source_map_only
---

# Source Map

## Governing User Boundary

- Approved write path:
  `outputs/review/vaks-implementation-sandbox/<date>-<slice-id>/`
- Protected paths: frozen architecture docs, `wiki/claims/`, `wiki/patterns/`,
  `wiki/decisions/`, `templates/`, `tools/`, and Obsidian vault.
- No commit, push, sync, background automation, hooks, MCP write tools, or
  dependency install.
- Current dirty tree is pre-existing baseline; final audit only checks this
  slice's writes.

## Local Project Sources Read

| Source | Used For |
|---|---|
| `AGENTS.md` / pasted project instructions | Workspace boundaries, Chinese reporting default, no automatic truth/mainline/promotion. |
| `00_handoff/2026-06-08-answer-boundary-and-three-window-execution-handoff.md` | Dirty-tree caution, frozen spine, diagnostic-not-truth boundary, sandbox/mainline split. |
| `outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md:2273-2296` | P1 target and pilot stories: receipt validators before read-only query loop. |
| `outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md:2514-2554` | Implementation order: P0-01..P0-07 then P1 retrieval/operation receipt validators. |
| `outputs/review/vaks-implementation-sandbox/2026-06-15-p0-07-action-boundary-failure-matrix-sandbox/product-acceptance-report.md` | Confirmed P0-07 `PASS_PRODUCT_GRADE` and move to P1-08. |
| `outputs/review/vaks-implementation-sandbox/2026-06-15-p0-01-retrieval-receipt-template-sandbox/artifact/retrieval-receipt-template.md` | Retrieval receipt fields, authority buckets, selected-by boundary, support boundary flags. |
| `outputs/review/vaks-implementation-sandbox/2026-06-15-p0-01-retrieval-receipt-template-sandbox/artifact/contract-notes.md` | Future validator hints: same-bucket RRF, no candidate/overlay/feedback support, no rank as support, no URL-only direct support. |
| `outputs/review/vaks-implementation-sandbox/2026-06-15-p0-02-operation-receipt-template-sandbox/artifact/operation-receipt-template.md` | Actor tier matrix, operation mode rules, basis rules, approval rules, rollback rules, non-claims. |
| `outputs/review/vaks-implementation-sandbox/2026-06-15-p0-02-operation-receipt-template-sandbox/artifact/failure-case-oracle.md` | Expected operation failure families and primary reasons. |
| `SOURCE_INTAKE.md` | Retrieval rank/support/action boundary and action-facing anchor rules. |
| `DEV_CONTEXT.md` | Retrieval receipts and context packs are not action basis by themselves. |
| `REVIEW_QUEUE.md` | Decision/action basis requires reviewed source-backed basis, risk, rollback, evidence sufficiency; automation cannot create support/confidence/promotion. |

## Borrowed P0 Contracts

### Retrieval Receipt Validator Checks

- `rrf_scope` must remain `same_authority_bucket_only`.
- Authority buckets and pack roles fail closed when unknown labels appear.
- Cross-bucket RRF/rank cannot create authority.
- `selected_by`, scores, graph rank, and retrieval rank cannot be support or
  trust.
- Candidate, source annotation, project overlay, and feedback items cannot be
  final support or action basis.
- Legacy raw metadata is excluded from support-grade retrieval receipts.
- Direct support needs an independent stable anchor; URL-only is insufficient.
- Retrieval receipts cannot claim review approval, evidence support, reviewed
  knowledge, action basis, promotion, or mainline readiness.

### Operation Receipt Validator Checks

- `read_only` and `suggest_only` actors cannot perform writes.
- Actor tiers, operation modes, and target scopes fail closed when unknown
  labels appear.
- `candidate_write` stays within candidate/sandbox scope.
- Reviewed writes require approval and checked body hash.
- Mainline, formal, schema, or protected writes require approval and checked
  body hash.
- Body hash mismatch invalidates approval for changed body.
- Schema changes and destructive deletes require owner-final authority where
  applicable.
- Delete/schema/mainline/reviewed operations require rollback when applicable.
- Significant operations require user intent confirmation.
- Candidate, feedback, retrieval receipt, retrieval rank, graph rank, source
  summary, briefing summary, and context pack material cannot be action basis.
- Operation receipts cannot claim truth, review approval, reviewed knowledge,
  action basis, promotion, or mainline readiness.

## Non-Authority Note

This source map explains why the sandbox pilot was built this way. It is not
reviewed knowledge, evidence support, reviewer approval, action basis, or a
mainline implementation decision.
