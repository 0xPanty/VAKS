# Source Writer and Session Anchor Snapshot

Source snapshot:

```text
raw/repos/_snapshots/llm-wiki-compiler-main-2026-05-26.zip
```

## Anchors

`src/utils/source-writer.ts:1-15`

- Shared writer protects every ingest path with empty-slug guard and basename collision suffix.

`src/utils/source-writer.ts:26-34`

- Computes a stable short SHA-256 hash from source identity for collision suffix.

`src/utils/source-writer.ts:36-62`

- If the destination exists and frontmatter `source` matches, re-ingest overwrites in place.
- If the same basename belongs to a different source, it uses a hash suffix instead of silent overwrite.

`src/utils/source-writer.ts:64-95`

- `saveSource` rejects empty slugs, creates the `sources/` directory, resolves collision-free filename, and writes the document.

`src/adapters/types.ts:19-33`

- Session adapters normalize provider exports into `NormalizedSession`.

`src/adapters/types.ts:35-52`

- Session adapter contract is stateless, detects whether it recognizes a file, and parses into a normalized session.

`src/commands/ingest-session.ts:27-40`

- Session frontmatter records title, source path, adapter, ingest time, optional session time bounds, and participant identity.

`src/commands/ingest-session.ts:42-54`

- Session ingest uses the shared source writer, so empty-slug and collision protections apply.

`src/commands/ingest-session.ts:95-133`

- Directory session ingest skips bad files but fails if zero sessions import successfully.

## VAKS Reading

Useful borrowed checks:

- no empty source output
- no empty title/slug write
- no silent overwrite on same title but different source
- adapter identity kept as provenance
- zero-success batch import is a failure

These are source hygiene and ingest safety checks. They do not create reviewed knowledge.
