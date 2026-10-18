# llm-wiki-compiler Context Types Anchor Snapshot

Source:

```text
raw/repos/_snapshots/llm-wiki-compiler-main-2026-05-26.zip
llm-wiki-compiler-main/src/context/types.ts
```

Checked in this sandbox on 2026-06-08.

## Anchors

```text
src/context/types.ts:1-11
```

Observed behavior:

- The context pack is a stable v1 JSON contract.
- Top-level fields remain present from Slice 1 onward.
- Empty list fields are empty arrays.
- Top-level keys must not be added or removed without bumping `version`.

```text
src/context/types.ts:49-55
```

Observed behavior:

- The pack includes a `budget` block with requested tokens, estimated tokens,
  truncation state, and trimmed section names.

```text
src/context/types.ts:93-99
```

Observed behavior:

- Source windows are a separate structure and are emitted only when
  `--include-sources` is set.

```text
src/context/types.ts:150-161
```

Observed behavior:

- The top-level v1 envelope contains `version`, `prompt`, `budget`, `project`,
  `primary`, `neighbors`, `warnings`, `gaps`, and `suggestedActions`.

## VAKS Extraction

This supports a narrow rule:

```text
A context pack should be a stable read-only evidence/context envelope with
warnings and gaps visible.
```

It does not support:

```text
truth confidence mutation
evidence support by retrieval alone
reviewed relation creation
action basis readiness by context pack alone
wiki writeback
raw source snippets by default
```

