# Promotion Funnel Pilot - 2026-06-08

## Boundary

This sandbox tests the candidate -> review -> promotion funnel.

It does not promote anything into `wiki/claims/`, `wiki/patterns/`, or
`wiki/decisions/`.

It does not change `SCHEMA.md`, `ARCHITECTURE_PRINCIPLES.md`, or
`FUSION_ARCHITECTURE_V0_2_DRAFT.md`.

It does not sync Obsidian and does not push.

## Inputs Read

Startup alignment:

- `AGENTS.md`
- `README.md`
- `SCHEMA.md`
- `FUSION_ARCHITECTURE_V0_2_DRAFT.md`
- `REVIEW_QUEUE.md`
- `REFERENCE_REVIEW_PROTOCOL.md`
- `SOURCE_INTAKE.md`
- `wiki/indexes/knowledge-graph-index.md`

Candidate sources inspected:

- `outputs/review/`
- `wiki/claims/`
- `wiki/patterns/`
- relevant `raw/repos/` and `raw/papers/` source records
- local source snapshots:
  - `raw/repos/_snapshots/llm-wiki-compiler-main-2026-05-26.zip`
  - `raw/repos/_snapshots/openkb-main-2026-05-27.zip`

External exact-commit code anchors checked for RKA:

- `infinitywings/rka@7bc2d76efba61b92db5b056220f7009763003a0d`

## Startup Git State

`git log --oneline -5` showed:

```text
ea7339b tools: add video intake source-card helpers
4fe57a8 docs: add independent answer support boundaries
0cea747 docs: merge source intake control flow guardrails
e19a3c6 docs: land v0.2.13 action gate and sidecar boundary
6547786 Graduate audit shell operator convention
```

`git status --short` was not clean at startup:

```text
?? outputs/review/2026-06-07-aal-ruller-pkm-second-brain-ai-companian-candidate-distillation.md
?? raw/papers/2026-06-07-aal-ruller-pkm-second-brain-ai-companian-source.md
```

Those two files were treated as pre-existing untracked files and were read only.

## Outputs

- `CANDIDATE_INVENTORY.md`: 15 candidate or near-candidate items.
- `PROMOTION_EVIDENCE_PACKETS.md`: 5 focused Evidence Packet reviews.
- `PROMOTION_RECOMMENDATIONS.md`: promotion recommendations, gaps, and user decision questions.
- `ARCHITECTURE_CONFLICT_MATRIX.md`: one-by-one architecture coverage and conflict check for the 15 candidates.
- `PROJECT_TAG_PRIORITY_CROSSWALK.md`: project tag, Project Lens, and P1/P2/P3 borrowing-priority crosswalk.
- `COMBINED_RESCREEN_FOR_REVIEW.md`: combined 22-item rescreen table for one-by-one follow-up review.

## Summary Judgment

Pilot result:

- `promote_ready`: 4 narrow pattern-level candidates.
- `needs_more_evidence`: 1 pattern candidate.
- `keep_candidate / not_ready`: several inventory items, especially candidate-pattern-bank and abstract-only paper material.

The strongest promotion candidates are implementation-pattern candidates with direct source/code anchors:

- self-contained review candidate record
- review-gated compile queue
- source hash registry and idempotent ingest
- decision outcome precondition before calibration

The clearest gap case is:

- scope dashboard live context surface: useful, but still single-source and needs one local dev-context trial before reviewed promotion.

## Non-Promotion Reminder

`supported` here means the anchor supports the target under the stated scope.

It does not mean truth, action readiness, decision approval, Obsidian sync, or automatic wiki writeback.
