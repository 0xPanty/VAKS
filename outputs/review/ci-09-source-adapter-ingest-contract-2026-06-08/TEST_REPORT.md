# CI-09 Sandbox Test Report: Source Adapter Ingest Contract

Date: 2026-06-08

Sandbox:

```text
outputs/review/ci-09-source-adapter-ingest-contract-2026-06-08/
```

Base architecture:

```text
outputs/review/ci-08-claim-level-provenance-source-ranges-2026-06-08/architecture/
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
```

## Plain-Language Result

CI-09 is positive only as a small source-ingest hardening.

The original architecture already has most of the source identity and provenance logic. CI-09 should not add a new architecture layer and should not force every old source card to get a heavy adapter schema.

What it adds in the sandbox is narrow:

```text
adapter output = raw source / candidate input / lint warning / review pressure
adapter output != reviewed truth / approval / action basis
```

## Existing Architecture Check

Already covered:

- `SOURCE_INTAKE.md` defines source identity and provenance.
- `templates/source-record.md` keeps source records as raw provenance and findability.
- Video intake already has project-local source-card and retained artifact routing.
- `IMPLEMENTATION_BLUEPRINT.md` already lists source adapters as extension points.
- Review, promotion, and context-pack use already live outside Source node main fields.

Gap:

- The architecture did not yet have a compact, explicit adapter-created source block that says which fields are stable enough and which effects are forbidden.

So CI-09 is not replacing the architecture. It is a light boundary clarification for future adapter-created source records.

## Source Evidence Checked

Local source snapshot:

```text
raw/repos/_snapshots/llm-wiki-compiler-main-2026-05-26.zip
```

Sandbox evidence snapshots:

```text
evidence/llm-wiki-compiler/source-adapter-core-anchor-snapshot.md
evidence/llm-wiki-compiler/source-adapter-types-anchor-snapshot.md
evidence/llm-wiki-compiler/source-writer-session-anchor-snapshot.md
```

Checked anchors:

- `src/ingest/shared.ts:11-15`
- `src/ingest/shared.ts:140-176`
- `src/commands/ingest.ts:190-205`
- `src/commands/ingest.ts:207-229`
- `src/commands/ingest.ts:231-275`
- `src/ingest/web.ts:14-63`
- `src/ingest/pdf.ts:18-57`
- `src/ingest/file.ts:12-40`
- `src/ingest/image.ts:82-114`
- `src/ingest/transcript.ts:58-73`
- `src/ingest/transcript.ts:141-156`
- `src/utils/source-writer.ts:1-95`
- `src/adapters/types.ts:19-52`
- `src/commands/ingest-session.ts:27-54`
- `src/commands/ingest-session.ts:95-133`

## Sandbox Changes

Changed only inside sandbox architecture:

- `architecture/wiki/patterns/source-adapter-ingest-contract.md`
- `architecture/SOURCE_INTAKE.md`
- `architecture/templates/source-record.md`
- `architecture/wiki/indexes/knowledge-graph-index.md`

Added:

- `tests/fixtures/source-adapter/`
- `tests/pressure-test.ps1`

## Pressure Fixtures

PASS:

- Web adapter creates raw source record.
- Partial PDF adapter creates raw source record with truncation and gaps.
- Session adapter creates raw source record with adapter identity and timing.

BLOCK:

- Adapter output creates reviewed claim.
- Adapter output upgrades truth confidence or verification status.
- Adapter output creates reviewed relation.
- Adapter output becomes action basis.
- Empty extracted content reports success.
- Same-title/different-source silently overwrites.
- Batch session import with zero successes reports ok.
- Light source capture is forced through a heavy universal schema.

## Test Result

Command:

```powershell
powershell -ExecutionPolicy Bypass -File outputs/review/ci-09-source-adapter-ingest-contract-2026-06-08/tests/pressure-test.ps1
```

Result:

```text
TOTAL passed=92 failed=0
```

## Compatibility

No conflict found with the current sandbox stack:

- CI-02 review-gated compile queue remains present.
- CI-02.5 candidate lint remains present.
- CI-03 source hash registry remains present.
- CI-04 decision outcome precondition remains present.
- CI-05 scope dashboard remains present.
- CI-06 context pack envelope remains present.
- CI-08 source range boundary remains present.

CI-09 is compatible because it sits before review and only normalizes source capture.

## Overdesign Judgment

Not overdesigned if kept light.

Acceptable:

- Add optional adapter block for adapter-created source records.
- Record adapter name, source type, input identity, output path, capture time, status, truncation, gaps, and warnings.
- Keep manual/light source cards allowed to omit the block.

Overdesigned:

- Bulk rewriting old source cards just to add adapter fields.
- Requiring full PROV ontology for light sources.
- Freezing every source type into one heavy schema now.
- Treating adapter output as reviewed knowledge, source support, or action basis.
- Starting automatic ingest/runtime/API/MCP because this contract exists.

## Merge Recommendation

Recommend later lightweight merge, but lower priority than CI-02/03/04/06/08.

Merge shape:

- Update existing `wiki/patterns/source-adapter-ingest-contract.md`.
- Add optional adapter block to `templates/source-record.md`.
- Add a short `SOURCE_INTAKE.md` boundary note.

Do not bulk modify old source records. Do not add automatic ingest scripts yet.

## Pollution Check

The pressure test verified:

- root `wiki/patterns/source-adapter-ingest-contract.md` was not sandbox-mutated
- root `SOURCE_INTAKE.md` was not sandbox-mutated
- root `templates/source-record.md` was not sandbox-mutated
- root `wiki/indexes/knowledge-graph-index.md` was not sandbox-mutated

No commit, no push, and no permanent Obsidian sync were performed.
