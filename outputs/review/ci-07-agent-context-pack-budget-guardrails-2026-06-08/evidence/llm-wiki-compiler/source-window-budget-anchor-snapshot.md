# Source Window Budget Anchor Snapshot

Source snapshot:

```text
raw/repos/_snapshots/llm-wiki-compiler-main-2026-05-26.zip
```

## Anchors

`src/context/provenance.ts:101-137`

- Uses a shared per-pack source window budget.
- Returns no windows when the budget is exhausted.

`src/context/provenance.ts:139-149`

- Returns null when a source window read is rejected by path guard.

`src/context/provenance.ts:152-168`

- Resolves canonical `sources/` root.

`src/context/provenance.ts:170-198`

- Rejects absolute paths, parent traversal, and realpath escapes outside `sources/`.

`src/context/provenance.ts:222-246`

- Reads 1-indexed inclusive line windows and clamps to maximum lines per window.

`src/context/build.ts:513-565`

- Appends project warnings before budget trimming.
- Adds `source-window-unavailable` when include-sources was requested but citation spans could not materialize.
- Avoids spurious source-window warnings caused only by later budget trimming.

## VAKS Reading

Useful borrowed rules:

- Source windows are bounded.
- Source windows are path-confined.
- Missing or unsafe windows produce warning pressure.
- Budget-related source-window trimming must remain visible through `budget.trimmed_sections`.
