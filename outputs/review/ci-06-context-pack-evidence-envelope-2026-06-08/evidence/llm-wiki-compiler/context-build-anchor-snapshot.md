# llm-wiki-compiler Context Build Anchor Snapshot

Source:

```text
raw/repos/_snapshots/llm-wiki-compiler-main-2026-05-26.zip
llm-wiki-compiler-main/src/context/build.ts
```

Checked in this sandbox on 2026-06-08.

## Anchors

```text
src/context/build.ts:1-20
```

Observed behavior:

- `buildContextPack()` emits the full stable v1 JSON field set.
- Later features can fill placeholders without breaking consumers.

```text
src/context/build.ts:56-76
```

Observed behavior:

- Build options include prompt, budget, depth, top pages, top chunks, omit root,
  neighbors, and `includeSources`.

```text
src/context/build.ts:104-119
```

Observed behavior:

- Source windows are attached only when `includeSources` is true.
- Project warnings are appended after source window handling and before budget trimming.
- The pack is finalized through budget handling.

```text
src/context/build.ts:227-264
```

Observed behavior:

- The draft pack assembles version, prompt, budget, project, primary, neighbors,
  warnings, gaps, and suggested actions.
- Graph-neighbor reasons annotate already ranked primary entries; they do not
  promote a page into primary by graph alone.

```text
src/context/build.ts:449-505
```

Observed behavior:

- Budget finalization trims structured sections deterministically.
- It does not slice serialized JSON.

```text
src/context/build.ts:513-565
```

Observed behavior:

- Pending candidates, lint errors, and missing source windows surface as warnings.

## VAKS Extraction

This supports using context packs as read-only activation/evidence envelopes.

It does not support treating retrieval, graph neighbors, citations, or source
windows as truth or approval.

