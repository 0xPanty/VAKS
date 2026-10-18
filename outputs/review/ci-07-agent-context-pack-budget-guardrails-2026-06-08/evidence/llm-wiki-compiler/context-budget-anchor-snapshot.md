# Context Budget Anchor Snapshot

Source snapshot:

```text
raw/repos/_snapshots/llm-wiki-compiler-main-2026-05-26.zip
```

Checked local extraction:

```text
%TEMP%/vaks-ci09-llm-wiki-compiler/llm-wiki-compiler-main/
```

## Anchors

`src/context/budget.ts:1-24`

- Describes token estimation and deterministic trimming.
- Documents trim order: neighbors, source windows, semantic chunks / excerpts, primary pages.
- States trimming drops whole array elements and preserves JSON validity.

`src/context/budget.ts:31-43`

- Defines allowed trimmed section names and the approximate token estimator.

`src/context/budget.ts:56-69`

- Builds a budget envelope with `truncated: false` and `trimmedSections: []` defaults.

`src/context/budget.ts:77-103`

- Trims a deep-cloned pack deterministically and returns structured `trimmedSections`.

`src/context/budget.ts:116-173`

- Implements section trimming in order: neighbors, source windows, chunks, primary.

`src/context/build.ts:449-505`

- Finalizes budget by structured trimming, recomputing estimated tokens, and setting `budget.truncated` / `budget.trimmedSections`.

## VAKS Reading

Useful borrowed rule:

```text
Budget trimming may reduce context volume, but must remain visible through budget.truncated and trimmed_sections.
```

Budget trimming is not permission to hide known warnings, gaps, evidence insufficiency, or action-risk notes.
