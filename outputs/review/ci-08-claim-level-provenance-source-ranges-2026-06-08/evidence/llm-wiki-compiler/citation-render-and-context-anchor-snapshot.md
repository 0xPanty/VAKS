# llm-wiki-compiler Citation Render And Context Anchor Snapshot

Sources:

```text
raw/repos/_snapshots/llm-wiki-compiler-main-2026-05-26.zip
llm-wiki-compiler-main/src/viewer/citation-rule.ts
llm-wiki-compiler-main/src/context/provenance.ts
```

Checked in this sandbox on 2026-06-08.

## Anchors

```text
src/viewer/citation-rule.ts:1-16
```

Observed behavior:

- Citation chips render one chip per parsed span.
- Span suffixes support `:42-58` and `#L42-L58`.
- Chips carry source filename, optional line range, and resolvability.

```text
src/viewer/citation-rule.ts:88-115
src/viewer/citation-rule.ts:162-190
```

Observed behavior:

- Each parsed span becomes render metadata.
- Rendered chips include `data-line-start`, `data-line-end`, and visible line-range labels when available.

```text
src/context/provenance.ts:1-21
src/context/provenance.ts:67-91
```

Observed behavior:

- Context packs flatten `ClaimCitation[]` into `primary[].citations[]`.
- One source span becomes one flat citation with `file`, `start`, and `end` when lines are present.

```text
src/context/provenance.ts:116-149
src/context/provenance.ts:170-198
src/context/provenance.ts:222-246
```

Observed behavior:

- Source windows only materialize claim-level spans with line ranges.
- Source windows are path-confined under `sources/`.
- Read windows are clamped to a maximum line count.

## VAKS Extraction

Source ranges should flow from candidate/review records into viewer/context-pack
surfaces, but they remain provenance until evidence support is checked.

