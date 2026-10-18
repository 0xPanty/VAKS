---
record_kind: sandbox_source_map
slice_id: 2026-06-15-p0-04-support-boundary-validator-sandbox
status: ready_for_recheck
truth_boundary: source_map_for_sandbox_only
---

# Source Map

## Source Files Read

| Source | Used For | Boundary |
|---|---|---|
| `AGENTS.md` | Workspace router and protected path boundaries. | Local operating rule, not a new artifact source. |
| `outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md` lines 2196-2213 | P0-04 artifact target and must-block cases. | Implemented only as sandbox-local prototype, not mainline `tools/`. |
| `REVIEW_QUEUE.md` lines 270-304 | URL-only provenance is not support; background context cannot count as support; evidence support is source-span-to-target. | Rule source for validator behavior. |
| `REVIEW_QUEUE.md` lines 925-936 | Failure patterns for URL-only, background_context, memory/model-background, unsupported spans, insufficient evidence. | Rule source for failure semantics. |
| `SOURCE_INTAKE.md` lines 1440-1451 | Retrieval rank is not trust; graph rank cannot create support/action readiness; URL-only has confidence cap. | Rule source for rank/score and URL-only blocking. |
| `SOURCE_INTAKE.md` lines 1484-1518 | Claim refs are trace handles; claim note cannot self-support; independent anchors required; not-enough list. | Rule source for positive and negative fixtures. |
| `SOURCE_INTAKE.md` lines 1388-1395 | Candidate summary, graph/rank score, feedback mutation boundary examples. | Failure-case inspiration. |
| `outputs/review/vaks-implementation-sandbox/2026-06-15-p0-01-retrieval-receipt-template-sandbox/artifact/retrieval-receipt-template.md` | P0-01 authority bucket and selected-by boundary pattern. | Prior sandbox pattern only. |
| `outputs/review/vaks-implementation-sandbox/2026-06-15-p0-03-body-hash-validator-sandbox/product-acceptance-report.md` | Confirms P0-03 `PASS_PRODUCT_GRADE`. | Prior slice state only. |

## Requirement Mapping

| Requirement | Implemented In |
|---|---|
| Candidate as support blocked | `failure-cases/candidate-as-support.md` |
| URL-only as direct support blocked | `failure-cases/url-only-direct-support.md` |
| Rank/score as support or trust blocked | `failure-cases/rank-score-as-support.md` |
| Feedback as support blocked | `failure-cases/feedback-as-support.md` |
| Source summary self-support blocked | `failure-cases/source-summary-self-support.md` |
| Claim note self-support loop blocked | `failure-cases/claim-note-self-support-loop.md` |
| Legacy metadata support blocked | `failure-cases/legacy-metadata-support.md` |
| Background context counted as support blocked | `failure-cases/background-context-counted-as-support.md` |
| Valid independent raw anchor support | `fixtures/valid-direct-raw-anchor-support.md` |
| Valid inferential support with reviewer note | `fixtures/valid-inferential-support-with-reviewer-note.md` |
| Background context allowed when not support | `fixtures/valid-background-context-not-support.md` |
| Missing current independent anchor blocked | `failure-cases/missing-independent-anchor.md` |
| Inferential support without reviewer note blocked | `failure-cases/inferential-support-missing-reviewer-note.md` |
| Single expected failure oracle | `artifact/failure-case-oracle.md` |

## Out Of Scope

- No mainline `tools/validate_support_boundary.py` is created.
- No `templates/` file is created or modified.
- No evidence support, reviewed knowledge, approval, promotion, action basis,
  commit, push, or Obsidian sync is performed.
