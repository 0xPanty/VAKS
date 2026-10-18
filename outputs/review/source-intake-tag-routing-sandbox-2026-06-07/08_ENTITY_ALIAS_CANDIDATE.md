---
type: entity_alias_candidate
status: candidate_only
created_at: 2026-06-07
scope: lightweight entity and alias candidate design
truth_boundary: candidate registry only; entity routing, not reviewed graph
---

# Entity / Alias Candidate

## Boundary

Entities are anchors for retrieval and disambiguation.

They are not reviewed relations by themselves.

## Initial Entity Set From The Pro Report

| canonical | aliases | kind | note |
|---|---|---|---|
| `Obsidian` | `Obsidian Bases`, `Bases` | product | PKM/vault surface and property views |
| `Notion` | `Notion database` | product | database/page/property reference |
| `Tana` | `supertag`, `super tag` | product | node/reference/field inspiration |
| `Capacities` | `objects`, `collections` | product | object type vs tag distinction |
| `Qdrant` | `vector filter`, `metadata filter` | retrieval system | metadata filtering reference |
| `Pinecone` | `Pinecone metadata filter` | retrieval system | metadata filtering reference |
| `LlamaIndex` | `router`, `metadata filter` | RAG framework | query routing/filter reference |
| `Haystack` | `query metadata extraction` | RAG framework | filter extraction reference |
| `Azure AI Search` | `Azure Search` | search system | hybrid/facet reference |
| `Weaviate` | `hybrid search` | vector database | hybrid retrieval reference |
| `Vespa` | `hybrid retrieval` | search system | ranking/reference |
| `GraphRAG` | `Microsoft GraphRAG` | research/system | graph retrieval stratification |
| `LightRAG` | `Light RAG` | research/system | graph retrieval reference |
| `HippoRAG` | `hippocampal indexing` | research/system | association activation reference |
| `Graphiti` | `Zep Graphiti` | agent memory graph | temporal/entity graph reference |
| `Zep` | `Zep memory` | agent memory | user graph and memory reference |
| `TruLens` | `RAG triad` | evaluation | context relevance / groundedness / answer relevance |
| `LangSmith` | `RAG eval` | evaluation | retrieval vs generation quality |
| `RAGAs` | `Ragas` | evaluation | faithfulness/context relevance |
| `ARES` | `ARES RAG evaluation` | evaluation | RAG evaluation reference |

## Rules

```text
Start with strings in `entities`.
Use `aliases` for common spelling or product-name variants.
Use `entity_refs` only after repeated ambiguity or reviewed relation need.
Do not auto-create a full entity graph.
```

## Upgrade Trigger

```text
entity appears across 3+ important sources
aliases are causing missed retrieval
entity is used in an action-facing context pack
entity participates in a reviewed relation
user asks for an entity page or MOC
```
