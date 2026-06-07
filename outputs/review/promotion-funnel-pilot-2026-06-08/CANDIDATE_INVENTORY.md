# Candidate Inventory

## Scope

This inventory lists candidates that look close enough to review that a future
promotion decision would be plausible.

It does not promote them.

## Candidate Table

| ID | Candidate | Source location | Promotion target | Why close to review-ready | Anchor state | Initial routing |
|---|---|---|---|---|---|---|
| CI-01 | Self-contained review candidate record | `wiki/patterns/self-contained-review-candidate-record.md` | pattern | Existing pattern-candidate, primary-source status, concrete source-code behavior | Direct local zip anchors in `llm-wiki-compiler-main/src/compiler/candidates.ts` and `src/commands/review-approve.ts` | selected for packet |
| CI-02 | Review-gated compile queue | `wiki/patterns/review-gated-compile-queue.md` | pattern | Existing pattern-candidate, clear failure mode, directly supports current funnel | Direct local zip anchors in `candidates.ts` and `review-approve.ts` | selected for packet |
| CI-03 | Source hash registry and idempotent ingest | `wiki/patterns/source-hash-registry-and-idempotent-ingest.md` | pattern | Existing adopted pattern, source record and OpenKB source snapshot support the mechanism | Direct local zip anchors in OpenKB `state.py`, `converter.py`, and `cli.py` | selected for packet |
| CI-04 | Decision outcome precondition before calibration | `outputs/review/2026-05-30-rka-source-code-anchor-review.md`; `raw/repos/2026-05-29-rka-source.md` | pattern | Exact-commit code review found a small rule already aligned with VAKS Use Ledger | Exact commit GitHub code anchors for RKA `decision_option.py`, `decision_options.py`, and `api/routes/decisions.py` | selected for packet |
| CI-05 | Scope dashboard live context surface | `wiki/patterns/scope-dashboard-live-context-surface.md` | pattern | Existing draft pattern with source/template anchors and explicit boundaries | Dusk source record has template anchors, but evidence is single-source and plugin-heavy | selected for packet |
| CI-06 | Context pack evidence envelope | `wiki/patterns/context-pack-evidence-envelope.md` | pattern | Existing pattern-candidate, direct context pack code in llm-wiki-compiler | Direct local zip anchors in `src/context/types.ts` and `src/context/build.ts` | close; not selected to avoid overloading one source family |
| CI-07 | Agent context pack budget guardrails | `wiki/patterns/agent-context-pack-budget-guardrails.md` | pattern | Existing pattern-candidate, source evidence includes budget/warnings/source-window safety | Needs targeted line anchors for `budget.ts` and `provenance.ts` before promotion | review-ready after anchor pass |
| CI-08 | Claim-level provenance source ranges | `wiki/patterns/claim-level-provenance-source-ranges.md` | pattern | Strong fit with current evidence discipline and candidate -> review funnel | Needs targeted local line anchors in linter citation parsing before promotion | review-ready after anchor pass |
| CI-09 | Source adapter ingest contract | `wiki/patterns/source-adapter-ingest-contract.md` | pattern | Existing pattern-candidate, aligns with video/source intake expansion | Current note cites source support, but this pilot did not inspect adapter line anchors | needs anchor pass |
| CI-10 | Static wiki health lint before auto rewrite | `wiki/patterns/static-wiki-health-lint-before-auto-rewrite.md` | pattern | Existing pattern-candidate; strong boundary against auto-rewrite | Needs exact linter rule anchors and local lint scope decision | needs anchor pass |
| CI-11 | Retrieval is activation, not truth | `outputs/review/candidate_pattern_bank/retrieval-is-activation-not-truth.md` | pattern | Good cross-source candidate route; strongly aligned with VAKS boundary | Candidate bank derives from multiple source cards, but this pilot did not inspect the underlying video/repo/paper anchors | keep_candidate |
| CI-12 | Search to analysis before answer | `outputs/review/candidate_pattern_bank/search-to-analysis-before-answer.md` | pattern | Useful for answer preparation and context envelope discipline | Mostly source-routing/video-derived; needs raw transcript/source anchor review | keep_candidate |
| CI-13 | Source structure first for RAG | `outputs/review/candidate_pattern_bank/source-structure-first-rag.md` | pattern | Good fit for source intake and context-pack preparation | Multiple source refs, but support is still routed through candidate pattern bank | keep_candidate |
| CI-14 | Verified vault API for agent brain | `wiki/patterns/verified-vault-api-for-agent-brain.md` | pattern or decision | Clear medium-term system direction, existing candidate pattern | Needs current implementation target, API boundary, and independent anchors before decision use | needs_more_evidence |
| CI-15 | PKM -> second brain -> personal AI companion | `outputs/review/2026-06-07-aal-ruller-pkm-second-brain-ai-companian-candidate-distillation.md`; `raw/papers/2026-06-07-aal-ruller-pkm-second-brain-ai-companian-source.md` | claim or pattern | High-value framing candidate for activation / companion story | Public metadata and abstract only; ACM PDF access was 403; full-text architecture claims not anchored | not_ready |

## Selection Rationale

The 5 selected packets cover both sides of the funnel:

- source-code-backed candidates that may be promotion-ready;
- a useful but still weak single-source dashboard candidate.

This avoids turning the pilot into a rubber stamp.

## Not Selected This Round

The candidate pattern bank items are promising but not promotion-ready in this
pilot, because their immediate files are routing/candidate records. A promotion
review must go back to the underlying raw source cards, transcript segments,
paper sections, repo files, or stable artifacts.
