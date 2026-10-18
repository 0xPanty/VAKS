# CI-07 Sandbox Test Report: Agent Context Pack Budget Guardrails

Date: 2026-06-08

Sandbox:

```text
outputs/review/ci-07-agent-context-pack-budget-guardrails-2026-06-08/
```

Base architecture:

```text
outputs/review/ci-09-source-adapter-ingest-contract-2026-06-08/architecture/
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
+ CI-09
+ CI-07
```

## Plain-Language Result

CI-07 is positive as a small context-pack safety hardening.

The original architecture already says context packs must include budget, warnings, gaps, evidence sufficiency, and source-window safety. CI-07 should not add a new layer.

The useful tightening is:

```text
Budget trimming can shrink context.
It cannot hide warnings, gaps, missing evidence, retrieval fallback, source-window loss, or action risk.
If key support was trimmed, the pack cannot remain action-ready.
```

## Existing Architecture Check

Already covered:

- `SCHEMA.md` already defines context pack as a calling layer, not reviewed knowledge.
- `SCHEMA.md` already includes budget, warnings, gaps, source windows, and evidence sufficiency.
- `IMPLEMENTATION_BLUEPRINT.md` already includes minimum context pack shape, budget, warnings, gaps, coverage, and evidence sufficiency.
- `ARCHITECTURE_PRINCIPLES.md` already says good context packs include gaps, warnings, budget, and truncation notes.
- CI-06 sandbox already tested read-only envelope, warnings/gaps, source windows opt-in, and action-basis blocking.

Gap:

- The architecture did not yet explicitly say that budget trimming must preserve warnings/gaps and block action-ready if key support was removed.

## Source Evidence Checked

Local source snapshot:

```text
raw/repos/_snapshots/llm-wiki-compiler-main-2026-05-26.zip
```

Sandbox evidence snapshots:

```text
evidence/llm-wiki-compiler/context-budget-anchor-snapshot.md
evidence/llm-wiki-compiler/source-window-budget-anchor-snapshot.md
evidence/llm-wiki-compiler/retrieval-warning-anchor-snapshot.md
```

Checked anchors:

- `src/context/budget.ts:1-24`
- `src/context/budget.ts:31-43`
- `src/context/budget.ts:56-69`
- `src/context/budget.ts:77-103`
- `src/context/budget.ts:116-173`
- `src/context/build.ts:449-505`
- `src/context/provenance.ts:101-137`
- `src/context/provenance.ts:139-149`
- `src/context/provenance.ts:152-198`
- `src/context/provenance.ts:222-246`
- `src/context/build.ts:513-565`
- `src/context/retrieval.ts:38-70`
- `src/context/retrieval.ts:72-108`
- `src/context/retrieval.ts:115-147`
- `src/context/retrieval.ts:149-175`
- `src/context/types.ts:44-55`
- `src/context/types.ts:150-161`

## Sandbox Changes

Changed only inside sandbox architecture:

- `architecture/wiki/patterns/agent-context-pack-budget-guardrails.md`
- `architecture/SCHEMA.md`
- `architecture/templates/dev-context-pack.md`
- `architecture/wiki/indexes/knowledge-graph-index.md`

Added:

- `tests/fixtures/context-budget/`
- `tests/pressure-test.ps1`

## Pressure Fixtures

PASS:

- Trimmed pack still exposes warnings/gaps and is not ready.
- Semantic retrieval fallback exposes stable warning.
- Source windows are opt-in and bounded.

BLOCK:

- Budget trimming hides known gaps.
- Key support is trimmed but action readiness remains ready.
- Source windows are on by default.
- Source window escapes source path.
- Semantic fallback is silent.
- Warnings are treated as trimmable section.
- Serialized JSON is sliced instead of structured trimming.

## Test Result

Command:

```powershell
powershell -ExecutionPolicy Bypass -File outputs/review/ci-07-agent-context-pack-budget-guardrails-2026-06-08/tests/pressure-test.ps1
```

Result:

```text
TOTAL passed=97 failed=0
```

## Compatibility

No conflict found with the stacked sandbox:

- CI-02 review-gated compile queue remains present.
- CI-02.5 candidate lint remains present.
- CI-03 source hash registry remains present.
- CI-04 decision outcome precondition remains present.
- CI-05 scope dashboard remains present.
- CI-06 context pack evidence envelope remains present.
- CI-08 source range boundary remains present.
- CI-09 source adapter contract remains present.

CI-07 is compatible because it refines CI-06 rather than replacing it.

## Overdesign Judgment

Not overdesigned if kept as a guardrail.

Acceptable:

- Record budget requested/estimated/truncated/trimmed sections.
- Preserve warnings and gaps.
- Keep source windows opt-in and path-confined.
- Block action-ready when key support was trimmed.

Overdesigned:

- Building API/MCP/runtime now.
- Adding a tokenizer dependency before implementation needs it.
- Treating budget estimates as evidence quality.
- Using trimming to avoid evidence sufficiency or review.

## Merge Recommendation

Recommend later lightweight merge, mostly as wording on top of CI-06.

Merge shape:

- Add a short CI-07 rule to `SCHEMA.md`.
- Add a compact Budget Guardrails block to `templates/dev-context-pack.md`.
- Update existing `wiki/patterns/agent-context-pack-budget-guardrails.md`.

Do not add runtime, API/MCP, tokenizer, or automatic context-pack builder now.

## Pollution Check

The pressure test verified:

- root `wiki/patterns/agent-context-pack-budget-guardrails.md` was not sandbox-mutated
- root `SCHEMA.md` was not sandbox-mutated
- root `templates/dev-context-pack.md` was not sandbox-mutated
- root `wiki/indexes/knowledge-graph-index.md` was not sandbox-mutated

No commit, no push, and no permanent Obsidian sync were performed.
