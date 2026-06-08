---
type: pattern
status: draft
created: 2026-05-27
updated: 2026-05-27
source_libraries:
  - willynikes2/knowledge-base-server
related_concepts:
  - "[[source-hash-registry-and-idempotent-ingest]]"
  - "[[MEMORY_TIER]]"
  - "[[SCHEMA]]"
related_projects:
  - verified-action-knowledge-system
adoption_status: watch
verification_status: single-source
evidence_level: secondary
evidence_count: 1
confidence: medium
negative_evidence:
  - "A retrieval cache can hide drift if treated as the authoritative record."
extension_points:
  - SQLite
  - FTS
  - embeddings
  - ingest
last_verified: 2026-05-27
next_review: 2026-06-03
epistemic_type: take
gaps:
  - "Should wait until Markdown schema stabilizes."
evidence_timeline:
  - date: 2026-05-27
    source: "[[2026-05-27-knowledge-base-server-source]]"
    observation: "The repo indexes vault markdown into SQLite with content hashes and skip-unchanged logic."
    effect: supports
    confidence: medium
relations:
  - target: "[[source-hash-registry-and-idempotent-ingest]]"
    type: supports
    strength: 4
    confidence: medium
    evidence:
      - "[[2026-05-27-knowledge-base-server-source]]"
    rationale: "Content hashes and idempotent indexing are practical implementation mechanics for derived indexes."
    created: 2026-05-27
    last_verified: 2026-05-27
tags:
  - pattern
  - sqlite
  - fts
  - derived-index
  - memory-tier
---

# Incremental Vault Index Retrieval Cache

## AI-readable preamble

Index the Markdown vault into a rebuildable machine cache for fast retrieval.

The cache can speed up activation and query. It cannot own truth.

## One-line definition

Use content hashes to incrementally sync vault notes into a derived retrieval database.

## Problem solved

Large vaults need fast lookup:

```text
scan everything is slow
full-text search over files is limited
agent context selection needs metadata and summaries
semantic search needs chunk/vector state
```

A rebuildable cache solves speed without moving source of truth away from Markdown.

## Source evidence

`willynikes2/knowledge-base-server` implements:

```text
src/db.js:
  documents, documents_fts, vault_files, embeddings

src/vault/indexer.js:
  scanVault
  content hash
  skip unchanged files
  upsert vault metadata
  delete stale index rows

src/vault/parser.js:
  frontmatter and folder-derived note type parsing
```

## Applicable scenarios

- Future hot/warm/cold dashboards.
- Query-run search cache.
- Context briefing candidates.
- Point collision candidate retrieval.
- Source hash registry.
- Local-only FTS before API/MCP.

## Not applicable

- Replacing Markdown/YAML as source of truth.
- Storing only DB state for verified records.
- Letting search rank become confidence.
- Mutating truth through cache rebuild.

## Minimum implementation

Derived cache fields:

```yaml
path:
content_hash:
record_type:
memory_tier:
activation_status:
scope_key:
verification_status:
summary:
key_topics:
source_refs:
updated_at:
indexed_at:
```

Rules:

```text
Markdown is authoritative.
Cache is rebuildable.
Cache rows can be deleted and recreated.
Cache may store summaries and search vectors.
Cache may not be the only owner of review decisions.
```

## Fusion suggestion

This is a future implementation pattern, not the first step.

Recommended order:

```text
stabilize schema
run real query-run / feedback-event trial
define context briefing output
then add SQLite/FTS cache
```

## Boundary

Fast lookup is not trust.
