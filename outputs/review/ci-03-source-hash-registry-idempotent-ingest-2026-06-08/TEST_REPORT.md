# CI-03 Sandbox Test Report: Source Hash Registry And Idempotent Ingest

Date: 2026-06-08

Scope:

```text
CI-03 is source lifecycle hygiene.
It is not a truth layer, evidence support layer, approval layer, reviewed relation layer, action basis, Obsidian sync rule, or automatic wiki writeback rule.
```

## Sandbox

Sandbox root:

```text
outputs/review/ci-03-source-hash-registry-idempotent-ingest-2026-06-08/
```

Base architecture copied from:

```text
outputs/review/ci-02-5-candidate-lint-before-approval-2026-06-08/architecture/
```

This means the sandbox tests CI-03 on top of the current CI-02 and CI-02.5 candidate-lint sandbox state.

No permanent Obsidian sync was performed.

## Source Evidence

Promotion packet:

```text
outputs/review/promotion-funnel-pilot-2026-06-08/PROMOTION_EVIDENCE_PACKETS.md
```

Primary source anchors:

```text
raw/repos/_snapshots/openkb-main-2026-05-27.zip
OpenKB-main/openkb/state.py:8-25
OpenKB-main/openkb/state.py:39-42
OpenKB-main/openkb/state.py:80-87
OpenKB-main/openkb/converter.py:36-61
OpenKB-main/openkb/cli.py:348-361
raw/repos/2026-05-27-openkb-source.md
```

Verified source behavior:

- `state.py` defines a persistent SHA-256 hash registry.
- `state.py` exposes known-hash lookup and persistent add.
- `state.py` computes file SHA-256.
- `converter.py` computes the file hash before conversion and skips known files.
- `cli.py` registers the hash only after successful compilation.

## Sandbox Changes

Updated only inside the CI-03 sandbox:

```text
architecture/wiki/patterns/source-hash-registry-and-idempotent-ingest.md
architecture/SOURCE_INTAKE.md
architecture/wiki/indexes/knowledge-graph-index.md
```

Added test fixtures:

```text
tests/fixtures/source-records/new-source.md
tests/fixtures/source-records/repeat-same-origin-same-hash.md
tests/fixtures/source-records/same-hash-different-origin.md
tests/fixtures/source-records/same-origin-changed-hash.md
tests/fixtures/source-records/deleted-source-still-referenced.md
tests/fixtures/source-records/compile-failure-no-registry-commit.md
tests/fixtures/source-records/block-hash-as-truth.md
tests/fixtures/derived-registry/source-registry.expected.json
tests/pressure-test.ps1
```

## Rule Added In Sandbox

Plain version:

```text
Hash tells us whether bytes changed.
It does not tell us whether the source is true.
It does not tell us whether a claim is supported.
It does not let generated content skip review.
```

Operational rule:

| Case | Decision | Required behavior |
|---|---|---|
| Same origin + same hash | `idempotent_skip` | Skip duplicate compile. |
| Different origin + same hash | `preserve_new_origin` | Keep the new provenance. |
| Same origin + changed hash | `replacement_candidate` | Route to replacement/recompile candidate. |
| Missing raw source but downstream references exist | `orphan_review_due` | Preserve trace and mark review_due. |
| Compile failed | `no_registry_commit` | Do not mark the source as processed. |
| Hash proposed as truth/evidence/approval | `BLOCK_EXPECTED` | Block the shortcut. |

Registry rule:

```text
Markdown source record is primary.
JSON/source-registry state is derived and rebuildable.
If they conflict, rebuild the registry from source records.
```

## Pressure Test

Command used:

```powershell
& "outputs\review\ci-03-source-hash-registry-idempotent-ingest-2026-06-08\tests\pressure-test.ps1"
```

Result:

```text
RESULT pass=81 fail=0
```

Test dimensions:

- CI-03 pattern file contains required boundaries.
- `SOURCE_INTAKE.md` sandbox copy contains source identity rules.
- CI-02 review-gated compile queue still exists in the same sandbox.
- CI-02.5 candidate lint still exists in the same sandbox.
- All source lifecycle fixtures have expected decisions.
- Same-hash/different-origin fixture preserves provenance.
- Changed-hash fixture routes to replacement/recompile candidate.
- Deleted-source fixture preserves downstream evidence and marks review_due.
- Compile-failure fixture blocks premature registry commit.
- Hash-as-truth fixture is blocked as expected.
- Derived registry fixture keeps multiple origins for the same hash.
- OpenKB code anchors are present and match the claimed behavior.
- Formal root `SOURCE_INTAKE.md` was not polluted with the new sandbox field.
- Formal root CI-03 pattern was not polluted with the new orphan decision table.
- Changed sandbox docs do not allow hash-as-approval, hash-as-truth, or hash-as-action-basis.

Execution note:

```text
Running through Windows PowerShell 5.1 with powershell.exe misread the UTF-8 Chinese script.
Running directly in the current PowerShell shell parsed and executed correctly.
```

## Root Pollution Check

Current root search found no CI-03 sandbox-only fields in formal root files:

```text
SOURCE_INTAKE.md
wiki/patterns/source-hash-registry-and-idempotent-ingest.md
```

`git diff --check`:

```text
Only CRLF normalization warnings for already modified CI-02 root files.
No whitespace error was reported.
```

Current git state still has only the earlier formal CI-02 root changes plus sandbox/untracked files.

## Result

Positive, with a narrow scope.

CI-03 is suitable as a small source-intake hygiene pattern if merged carefully. It helps prevent duplicate compile, silent overwrite, provenance loss, and silent evidence-chain deletion.

It must stay downstream of source capture and upstream of review. It must not become a truth signal.

## Recommended Mainline Merge Shape

If approved later, merge only:

```text
wiki/patterns/source-hash-registry-and-idempotent-ingest.md
SOURCE_INTAKE.md
wiki/indexes/knowledge-graph-index.md
```

Recommended mainline content:

- Keep Markdown source record as primary.
- Add source identity / content hash fields to source intake guidance.
- Add the five routing decisions: `idempotent_skip`, `preserve_new_origin`, `replacement_candidate`, `orphan_review_due`, `no_registry_commit`.
- Record OpenKB anchors from the local source snapshot.
- Explicitly reject hash-as-truth, hash-as-evidence-support, hash-as-approval, hash-as-action-basis, and hash-bypassing-review.

Do not merge yet:

```text
tests/fixtures/
tests/pressure-test.ps1
outputs/state/source-registry.json
runtime scripts
Obsidian sync changes
automatic compile or watcher behavior
```

## Opus Review Questions

1. Does the sandbox keep CI-03 as source lifecycle hygiene instead of a truth or evidence layer?
2. Are the same-hash/different-origin and deleted-source cases strict enough?
3. Should `orphan_review_due` live in source records only, or also surface in a maintenance manifest later?
4. Is the derived-registry rule strong enough to avoid drift from Markdown source records?

