---
record_kind: sandbox_source_map
slice_id: 2026-06-15-p1-11-semantic-anchor-support-check-sandbox
status: implemented_pending_review
truth_boundary: sandbox_trace_only
---

# Source Map

## Project Rules Used

| Source | Rule used |
|---|---|
| `outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md` lines 2273-2288 | P1 target and required artifact list include runtime artifact exclusion test and semantic anchor support check. |
| `SOURCE_INTAKE.md` line 1395 | Graph/rank score becoming support is an explicit failure mode. |
| `SOURCE_INTAKE.md` lines 1397-1428 | Action-facing anchors must return to raw source material or stable representation; candidate distillation, project overlay, briefing summary, retrieval score, graph relation, LLM evaluator output, and feedback event are forbidden as final support anchors. |
| `SOURCE_INTAKE.md` lines 1430-1461 | Retrieval rank is not trust; graph traversal and similarity cannot create support, confidence, reviewed relations, or action readiness. |
| `DEV_CONTEXT.md` lines 302-310 | Retrieval receipts help assemble context-pack candidates but do not create action basis, evidence support, truth confidence, or reviewed relations. |
| `REVIEW_QUEUE.md` lines 762-827 | Promotion/action rules require source ranges/excerpts and forbid auto support from similarity, vector score, graph traversal, and association score. |
| P1-10 `product-acceptance-report.md` | P1-10 PASS permits moving to P1-11 and explicitly says P1-11 can reuse runtime kind/path registry and negative fixtures to reject semantic anchors pointing to runtime artifacts. |
| P1-10 `artifact/runtime_artifact_exclusion_test.py` | Runtime artifact detection for generated receipts, suite outputs, caches, bytecode, logs, derived indexes, and path variants. |
| P0-04 support boundary validator | Prior sandbox blocked candidate-as-support, URL-only direct support, rank/score as support, feedback-as-support, self-support loops, missing independent anchor, and inferential support without reviewer note. |

## Artifact Mapping

| Rule | Artifact coverage |
|---|---|
| Semantic/vector hit may orient but cannot support | `fixtures/valid-semantic-orientation-no-support.json`, `failure-cases/semantic-score-as-support.json` |
| Graph rank/relation cannot support | `failure-cases/graph-rank-as-support.json` |
| Support needs stable raw/source anchor | `fixtures/valid-raw-excerpt-direct-support.json`, `fixtures/valid-code-line-anchor-support.json`, `fixtures/valid-transcript-segment-inferential-support.json`, `failure-cases/missing-selector-support.json`, `failure-cases/missing-source-ref-support.json` |
| URL-only is not final support | `failure-cases/url-only-direct-support.json`, `failure-cases/stable-url-missing-capture.json` |
| Candidate/project overlay cannot support | `failure-cases/candidate-distillation-support.json`, `failure-cases/project-overlay-support.json` |
| Feedback cannot support | `failure-cases/feedback-event-support.json` |
| Summary/community report cannot replace source anchor | `failure-cases/llm-summary-support.json` |
| Runtime artifacts cannot be anchors/support | `failure-cases/runtime-artifact-anchor.json`, `failure-cases/generated-receipt-support.json` |
| Anchor check cannot create reviewed knowledge/action basis | `failure-cases/reviewed-knowledge-claim.json`, `failure-cases/action-basis-claim.json` |
| Self-support loop blocked | `failure-cases/self-support-loop.json` |

## Boundaries

- No mainline `tools/` validator is created.
- No schema/template/wiki file is changed.
- No support claim is approved by this sandbox.
- No reviewed knowledge, reviewed relation, action basis, promotion, commit,
  push, or Obsidian sync is created.
