---
type: topic_registry_candidate
status: candidate_only
created_at: 2026-06-07
scope: small topic registry candidate for source intake routing
truth_boundary: candidate registry only; navigation/filtering, not truth
---

# Topic Registry Candidate

## Boundary

This is not a global ontology.

It is a small candidate list for reducing spelling drift and improving
retrieval filters.

## Initial Topic Set

| topic | use when | avoid using for |
|---|---|---|
| `source-intake` | capture, provenance, processing tiers, source cards | reviewed truth or adoption |
| `metadata-routing` | fields, facets, filters, tag policy | authority status |
| `retrieval` | query, search, BM25/vector/hybrid, lane routing | evidence support |
| `context-pack` | assembling task/question context | automatic truth |
| `candidate-distillation` | provisional source comprehension and KP extraction | reviewed pattern |
| `project-overlay` | project-scoped sidecar and borrow/non-borrow boundaries | generic source metadata |
| `evidence-support` | source spans, support checks, anchor rules | citation-only provenance |
| `rag-evaluation` | groundedness, faithfulness, retrieval quality diagnostics | truth confidence by score |
| `agent-memory` | memory systems, activation, namespace/context | reviewed relation |
| `obsidian-workbench` | Obsidian views, Bases, MOC, navigation | formal schema |
| `entity-routing` | entities, aliases, refs, disambiguation | entity graph truth |
| `feedback-cache` | append-only feedback and review pressure | truth mutation |

## Rules

```text
Prefer one or two topics per source card.
Use topics for retrieval slicing, not authority.
Add a new topic only if repeated real materials need it.
Do not encode project adoption, truth, action basis, or review status as a topic.
```

## Review Questions

```text
1. Which topics are too broad?
2. Which topics duplicate existing tags?
3. Which topics are needed for real source-intake retrieval packs?
```
