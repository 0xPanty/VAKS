# Source Adapter Core Anchor Snapshot

Source snapshot:

```text
raw/repos/_snapshots/llm-wiki-compiler-main-2026-05-26.zip
```

Checked local extraction:

```text
%TEMP%/vaks-ci09-llm-wiki-compiler/llm-wiki-compiler-main/
```

## Anchors

`src/ingest/shared.ts:11-15`

- Defines the common `IngestedSource` shape returned by ingest modules.
- Shape is intentionally small: `title` and `content`.

`src/ingest/shared.ts:140-156`

- Enforces max source character limit.
- Returns `content`, `truncated`, and `originalChars`.

`src/ingest/shared.ts:158-176`

- Rejects empty extracted content.
- Warns for trivially short content.

`src/commands/ingest.ts:190-205`

- Detects source type: PDF, image, transcript, file, YouTube transcript, or web.

`src/commands/ingest.ts:207-229`

- Builds source frontmatter with `title`, `source`, `ingestedAt`, optional `sourceType`, and truncation metadata.

`src/commands/ingest.ts:231-248`

- Dispatches source content extraction to the relevant ingest module.

`src/commands/ingest.ts:250-275`

- Programmatic ingest returns structured result: saved filename, char count, truncation flag, source identity, and detected source type.

## VAKS Reading

The useful borrowed idea is a small adapter boundary:

```text
input source -> normalized source record / source candidate
```

This does not justify automatic promotion, truth confidence, reviewed relations, or action basis.
