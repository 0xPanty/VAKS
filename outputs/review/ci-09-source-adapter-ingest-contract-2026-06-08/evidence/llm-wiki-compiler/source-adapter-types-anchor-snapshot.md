# Source Adapter Types Anchor Snapshot

Source snapshot:

```text
raw/repos/_snapshots/llm-wiki-compiler-main-2026-05-26.zip
```

## Anchors

`src/ingest/web.ts:14-17`

- Web ingest result shape is title/content.

`src/ingest/web.ts:20-26`

- Web fetch fails on bad HTTP response.

`src/ingest/web.ts:28-42`

- Readability extraction fails if readable content cannot be parsed.

`src/ingest/web.ts:56-63`

- Web URL returns extracted title and markdown content.

`src/ingest/pdf.ts:18-27`

- PDF title uses metadata when available, otherwise filename.

`src/ingest/pdf.ts:39-57`

- PDF adapter returns title/content and destroys parser after extraction.

`src/ingest/file.ts:12-18`

- Generic file adapter explicitly supports only `.md` and `.txt`.

`src/ingest/file.ts:26-40`

- Unsupported file types are rejected; markdown or fenced text is returned as title/content.

`src/ingest/image.ts:82-114`

- Image adapter requires a vision-capable provider and returns title/content.

`src/ingest/transcript.ts:58-73`

- YouTube transcript adapter fails when no transcript exists and returns title/content when available.

`src/ingest/transcript.ts:141-156`

- Transcript adapter supports YouTube, `.vtt`, `.srt`, and `.txt`; unsupported transcript types are rejected.

## VAKS Reading

Different source types can share a tiny normalized output while still preserving source-type-specific failure rules.

For VAKS, this supports a flexible adapter contract, not a heavy universal source schema.
