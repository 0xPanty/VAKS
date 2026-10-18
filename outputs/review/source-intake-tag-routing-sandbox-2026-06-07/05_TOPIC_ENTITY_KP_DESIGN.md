---
type: sandbox_design_note
status: candidate_only
created_at: 2026-06-07
scope: topic, entity, and candidate knowledge point design
truth_boundary: sandbox design note only
---

# Topic / Entity / Candidate Point Design

## Main Design

```text
source gets discovery metadata
candidate note gets atomic knowledge points
project overlay gets project-specific borrowing
reviewed/action layer gets adoption and action basis
```

## Topics

Use `topics` as a small controlled discovery facet.

Good topics:

```text
source-intake
retrieval
rag-evaluation
agent-memory
obsidian-workbench
project-overlay
context-pack
evidence-support
```

Rules:

```text
Keep topics small.
Prefer stable nouns over one-off phrasing.
Do not encode authority or project adoption in topics.
Do not create a heavy ontology now.
```

Open question:

```text
How small should the controlled topic set be?
```

## Entities

Start with strings:

```yaml
entities:
  - Obsidian
  - Tana
  - Qdrant
aliases:
  - vector database
entity_refs: []
```

Upgrade to `entity_refs` only when:

```text
the entity appears repeatedly
aliases cause confusion
the entity needs its own note
the entity participates in reviewed relations
the entity is needed for a context pack or action basis
```

Open question:

```text
Should entities remain strings first, or move toward alias + canonical refs?
```

## Candidate Knowledge Points

Do not make reusable knowledge a source tag.

Use stable candidate points:

```yaml
candidate_points:
  - kp_ref: KP-001
    point_text: "Metadata filters should run before semantic ranking when business boundaries matter."
    point_type: pattern
    source_anchor_ref: source:section-or-range
    review_route: instance_check
    routing_hint:
      - retrieval
      - metadata-filter
    uncertainty: "Needs VAKS local pressure test before promotion."
```

Rules:

```text
`kp_ref` is local to the candidate note by default.
Candidate points are review units, not truth.
Candidate point IDs help agents quote and route a point without turning it into
a global ontology object.
Promoted knowledge still needs review.
```

Open question:

```text
What minimal candidate point ID format helps agents without making schema heavy?
```

## Topic Retrieval Pack

Use only for high-value themes.

Purpose:

```text
entry point
include / exclude defaults
lane routing
human explanation
query expansion
```

Not purpose:

```text
truth
reviewed relation
action basis
automatic ontology
global topic registry
```

## Stop Point

This sandbox recommends:

```text
small topics
string entities first
local kp_ref first
topic packs for high-value navigation only
```

It does not recommend:

```text
global controlled vocabulary buildout
full entity graph
heavy ontology
knowledge-point tag system
automatic context-pack builder
```
