# CI-08 Sandbox Test Report: Claim-Level Provenance Source Ranges

Date: 2026-06-08

Sandbox:

```text
outputs/review/ci-08-claim-level-provenance-source-ranges-2026-06-08/
```

Base architecture:

```text
outputs/review/ci-06-context-pack-evidence-envelope-2026-06-08/architecture/
```

Stack tested:

```text
CI-02
+ CI-02.5
+ CI-03
+ CI-04
+ CI-05
+ CI-06
+ CI-08
```

## Plain-Language Result

CI-08 is positive.

It is not a new architecture layer. It is a small tightening rule: when a claim, decision, relation, promotion, or action-facing answer cites a source, a concrete line range helps reviewers check the exact source span.

But the line range itself is not proof. It only tells us where to look. To count as support, the record still needs the target claim, support judgment, role, warrant, and scope.

## Existing Architecture Check

The current architecture already has most of this logic:

- `SCHEMA.md` already separates provenance from support.
- `SCHEMA.md` already says URL-only citations are provenance, not evidence support.
- `templates/claim-record.md` already has `source_range`, `source_access`, and `evidence_support`.
- `REVIEW_QUEUE.md` and review-candidate shape already require source anchors and block source summaries from acting as support.
- `wiki/patterns/claim-level-provenance-source-ranges.md` already exists as an adopt-soon candidate.

CI-08 therefore does not replace the architecture. It tightens an existing rule and makes the support boundary harder to fake.

## Source Evidence Checked

Local source snapshot:

```text
raw/repos/_snapshots/llm-wiki-compiler-main-2026-05-26.zip
```

Sandbox evidence snapshots:

```text
evidence/llm-wiki-compiler/claim-citation-parser-anchor-snapshot.md
evidence/llm-wiki-compiler/citation-lint-anchor-snapshot.md
evidence/llm-wiki-compiler/citation-render-and-context-anchor-snapshot.md
```

Checked anchors:

- `src/utils/markdown.ts:18-25`
- `src/utils/markdown.ts:117-190`
- `src/utils/markdown.ts:195-230`
- `src/linter/rules.ts:348-446`
- `src/linter/rules.ts:450-536`
- `src/linter/rules.ts:556-584`
- `src/viewer/citation-rule.ts:1-16`
- `src/viewer/citation-rule.ts:88-115`
- `src/viewer/citation-rule.ts:162-190`
- `src/context/provenance.ts:67-91`
- `src/context/provenance.ts:116-149`
- `src/context/provenance.ts:170-198`
- `src/context/provenance.ts:222-246`

## Sandbox Changes

Changed only inside the sandbox architecture copy:

- `architecture/wiki/patterns/claim-level-provenance-source-ranges.md`
- `architecture/templates/claim-record.md`
- `architecture/SCHEMA.md`
- `architecture/wiki/indexes/knowledge-graph-index.md`

Added test files:

- `tests/fixtures/claim-provenance/`
- `tests/pressure-test.ps1`

## Pressure Fixtures

PASS:

- Direct source range support with exact target, support role, warrant, and scope.
- Counterexample source range routed as challenge evidence, not support evidence.

BLOCK:

- URL-only reference as support.
- Summary-only reference as support.
- `background_context` as support.
- Source range without target claim.
- Source range without warrant / scope.
- Malformed citation line range.
- Out-of-bounds citation range.
- Missing source file.
- Valid source range used to automatically set truth confidence or verification status.

## Test Result

Command:

```powershell
powershell -ExecutionPolicy Bypass -File outputs/review/ci-08-claim-level-provenance-source-ranges-2026-06-08/tests/pressure-test.ps1
```

Result:

```text
TOTAL passed=96 failed=0
```

## Compatibility

No conflict found with the existing sandbox stack:

- CI-02 review-gated compile queue remains present.
- CI-02.5 candidate lint remains present.
- CI-03 source hash registry remains present.
- CI-04 decision outcome precondition remains present.
- CI-05 scope dashboard candidate remains present.
- CI-06 context pack evidence envelope remains present.

CI-08 is compatible because it only tightens evidence location and support checks. It does not introduce runtime, dashboard, database, MCP, API, viewer dependency, Obsidian plugin dependency, or automatic promotion.

## Overdesign Judgment

Not overdesigned if kept narrow.

Acceptable scope:

- claims
- decisions
- reviewed relations
- promotion evidence
- action-facing evidence
- context pack citations when action or review use needs source windows

Too much:

- requiring line ranges for every raw capture
- requiring line ranges for ordinary light summaries
- treating source ranges as automatic support
- adding full viewer/runtime/API/MCP just to enforce this rule

## Merge Recommendation

Recommend later lightweight mainline merge.

Suggested merge shape:

- Add a short CI-08 boundary note to `SCHEMA.md`.
- Add a compact source range boundary block to `templates/claim-record.md`.
- Update the existing `wiki/patterns/claim-level-provenance-source-ranges.md`.
- Do not add runtime, dashboard, SQLite, MCP, API, or automatic source-window system now.

Do not merge as an independent architecture layer. Treat it as evidence-discipline hardening for existing provenance and review rules.

## Pollution Check

The pressure test verified:

- root `wiki/patterns/claim-level-provenance-source-ranges.md` was not sandbox-mutated
- root `templates/claim-record.md` was not sandbox-mutated
- root `SCHEMA.md` was not sandbox-mutated
- root `wiki/indexes/knowledge-graph-index.md` was not sandbox-mutated

No commit, no push, and no permanent Obsidian sync were performed.
