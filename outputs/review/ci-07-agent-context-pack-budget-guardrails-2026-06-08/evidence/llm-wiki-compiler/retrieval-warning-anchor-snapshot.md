# Retrieval Warning Anchor Snapshot

Source snapshot:

```text
raw/repos/_snapshots/llm-wiki-compiler-main-2026-05-26.zip
```

## Anchors

`src/context/retrieval.ts:38-70`

- Defines stable semantic retrieval warning codes.
- Defines retrieval outcome as either hits or warning.

`src/context/retrieval.ts:72-108`

- Performs best-effort semantic retrieval.
- Missing store, provider/config failures, and empty results return stable warnings instead of silent success.

`src/context/retrieval.ts:115-147`

- Treats missing, malformed, empty, or unusable embedding stores as unavailable.

`src/context/retrieval.ts:149-175`

- Detects stale embedding model and classifies provider failures without leaking raw stack/provider text.

`src/context/types.ts:44-55`

- Budget envelope includes requested tokens, estimated tokens, truncated flag, and trimmed sections.

`src/context/types.ts:150-161`

- Top-level context pack includes budget, warnings, gaps, and suggested actions.

## VAKS Reading

Useful borrowed rule:

```text
Retrieval failures must become stable warnings, not invisible absence.
```

Warnings/gaps are part of the pack contract. Budget pressure and retrieval fallback cannot erase them while still presenting the pack as action-ready.
