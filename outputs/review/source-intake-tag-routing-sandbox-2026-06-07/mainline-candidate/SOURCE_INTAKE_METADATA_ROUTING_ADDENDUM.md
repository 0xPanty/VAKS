---
type: source_intake_addendum_candidate
status: candidate_only
created_at: 2026-06-07
target_file: SOURCE_INTAKE.md
truth_boundary: sandbox candidate addendum only
---

# Candidate Addendum: Metadata, Tags, And Routing

## AI-readable preamble

This addendum keeps the current Source Intake Control Flow intact and adds a
small metadata/routing discipline.

It does not create a tag system, ontology, truth layer, or automatic retrieval
engine.

## Core Rule

```text
Use fields for boundaries.
Use facets for filtering.
Use entities for anchoring.
Use tags for recall.
Use candidate points for knowledge.
Use overlays for project borrowing.
Use review/action gates for authority.
```

## Metadata Layers

### Layer 1: Hard Boundary Fields

These are not tags:

```text
processing_tier
knowledge_status
retrieval_policy
promotion_gate
source_type
captured_at
raw_location / source_url
overlay_state
review_pressure
action_basis_allowed
```

### Layer 2: Small Controlled Discovery Facets

These fields can improve filtering and routing:

```text
topics
content_form
language
version_or_time_scope
```

They are not authority.

### Layer 3: Entity Anchors

Start lightweight:

```text
entities
aliases
entity_refs
```

Entity strings are enough by default. Use `entity_refs` only when canonical
disambiguation is needed.

### Layer 4: Open Recall Tags

Tags are optional recall hints.

They cannot mean:

```text
reviewed
approved
adopted
truth
safe
action basis
decision
best practice
project borrowing verdict
```

## Knowledge Point Rule

Do not put atomic knowledge points into source tags.

Use candidate points:

```yaml
candidate_points:
  - kp_ref: KP-001
    point_text:
    point_type:
    source_anchor_ref:
    review_route:
    routing_hint: []
    uncertainty:
```

## Suggestion Rule

Automatic suggestions can propose:

```text
topics
entities
content_form
language
version_or_time_scope
routing_hint
query-time filters
```

But suggested metadata should default to:

```text
temporary sidecar
review diff
query-run trace
agent trace
suggestion inbox
```

Confirmed writeback is required before it becomes source frontmatter.

## Retrieval Rule

Default query order:

```text
query understanding
-> hard filters
-> authority/status/project/path-role lane selection
-> hybrid retrieval inside lane
-> link/entity/topic-pack expansion inside lane
-> lane-separated output
-> evidence support check for action-facing use
```

Tags, topics, entities, embeddings, BM25, facets, rerankers, and graph signals
rank or route inside an allowed lane. They do not create authority.

## Topic Pack Rule

Topic retrieval packs are allowed for high-value topics.

They provide:

```text
entry point
include defaults
exclude defaults
lane routing
query expansion
```

They do not provide:

```text
truth
reviewed relation
action basis
ontology
global topic registry
```
