# llm-wiki-compiler Claim Citation Parser Anchor Snapshot

Source:

```text
raw/repos/_snapshots/llm-wiki-compiler-main-2026-05-26.zip
llm-wiki-compiler-main/src/utils/markdown.ts
```

Checked in this sandbox on 2026-06-08.

## Anchors

```text
src/utils/markdown.ts:18-25
```

Observed behavior:

- Citation markers use `^[...]`.
- Claim-level span suffix supports `:start-end` and `#Lstart-Lend`.
- Source span line numbers are 1-indexed.

```text
src/utils/markdown.ts:117-190
```

Observed behavior:

- Parser handles paragraph citations, multi-source citations, and claim-level line ranges.
- `extractClaimCitations` returns `ClaimCitation` objects in document order.
- Line ranges must be >= 1 and end must not be before start.

```text
src/utils/markdown.ts:195-230
```

Observed behavior:

- Malformed entries include bad grammar, line 0, or end-before-start.
- `inspectProvenance` groups spans by source file and records `{start, end}` ranges.

## VAKS Extraction

Claim-level provenance can point from a claim to a specific source span.

It does not by itself prove that the span supports the claim.

