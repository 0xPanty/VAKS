---
type: mainline_candidate_delta
status: candidate_only
created_at: 2026-06-07
scope: candidate additions to SOURCE_INTAKE and related templates
truth_boundary: sandbox candidate delta only
---

# Mainline Candidate Delta

## Plain Rule

```text
tags help find
fields filter
entities anchor
candidate points carry knowledge
overlays carry project borrowing
review/action gates carry authority
```

## Candidate Insert For SOURCE_INTAKE.md

### Intake Metadata Layers

Source intake metadata has four layers.

```text
Layer 1: hard boundary fields
  processing_tier
  knowledge_status
  retrieval_policy
  promotion_gate
  source_type
  captured_at
  raw_location / source_url

Layer 2: small controlled discovery facets
  topics
  content_form
  language
  version_or_time_scope

Layer 3: entity anchors
  entities
  aliases
  entity_refs when an entity needs a canonical note or reviewed link

Layer 4: open recall tags
  optional tags / informal keywords
  recall only
  never authority
```

Rules:

```text
Hard boundary fields must be formal fields, not tags.
Controlled facets are for filtering and routing, not truth.
Entity fields are anchors for aggregation and disambiguation, not reviewed
relations by themselves.
Open tags can help rediscovery, but cannot express reviewed, adopted, safe,
best practice, action basis, or decision status.
```

### Source Card Boundary

Source cards may carry confirmed discovery metadata:

```yaml
topics: []
content_form:
language:
version_or_time_scope:
entities: []
aliases: []
entity_refs: []
tags: []
```

These fields mean:

```text
findability
filtering
routing
source inspection
context-pack preparation
```

They do not mean:

```text
truth
reviewed status
adoption
action basis
project borrowing verdict
source reliability
```

### Candidate Distillation Boundary

Do not express reusable knowledge points as source tags.

Use explicit candidate points:

```yaml
candidate_points:
  - kp_ref: KP-001
    point_text:
    point_type:
    source_anchor_ref:
    review_route:
    uncertainty:
```

Candidate points remain provisional:

```text
orientation only
not reviewed knowledge
not action basis
not evidence support by themselves
```

### Project Borrowing Boundary

Project-specific borrowing does not belong in generic source-card tags or
source metadata.

Forbidden source-card tags:

```text
#for-vaks
#do-not-borrow-for-vaks
#adopt-for-vaks
#use-for-project
#project-best-practice
```

Use Project Overlay instead:

```yaml
project_id:
target_ref:
project_borrow_scope:
project_non_borrow_scope:
project_reopen_trigger:
target_hint:
```

### Suggested Metadata Boundary

Automatic suggestions default to temporary surfaces:

```text
intake UI
temporary sidecar
review diff
query-run trace
agent trace
suggestion inbox
```

They should not be written into the main source note as confirmed fields unless
a human confirms them or an explicit intake task says to write them.

### Retrieval Boundary

Default query order:

```text
1. understand query
2. extract hard filters and scope
3. filter by authority/status/project boundary
4. retrieve/rank inside allowed lane
5. expand via links/entities/topic packs only after hard filtering
6. display lanes separately
7. require raw/stable anchors for action-facing support
```

Bad:

```text
tag search across all raw/candidate/reviewed/overlay/sandbox files
-> one global relevance list
-> manual correction later
```

Good:

```text
select mode and lane
-> apply knowledge_status/retrieval_policy/project scope/path role filters
-> use topics/entities/tags/BM25/vector/rerank only inside that lane
```

## Candidate Template Deltas

### source-record.md / video-source.md

Add confirmed discovery metadata:

```yaml
topics: []
content_form:
language:
version_or_time_scope:
entities: []
aliases: []
entity_refs: []
tags: []
```

Add note:

```text
`topics`, `entities`, and `tags` are recall / filtering metadata.
They cannot express reviewed status, adoption, truth confidence, action basis,
project borrowing, or source reliability.
```

### candidate-distillation.md

Add stable candidate point format:

```yaml
candidate_points:
  - kp_ref: KP-001
    point_text:
    point_type: claim | interpretation | hypothesis | pattern | risk | preference | decision | open_question | implementation_note
    source_anchor_ref:
    review_route:
    routing_hint: []
    uncertainty:
```

### query-run.md

Add query understanding and lane fields:

```yaml
query_understanding:
  action_facing: true | false
  project_scope:
  source_type_filter:
  time_or_version_scope:
  extracted_entities: []
  extracted_topics: []
  extracted_filters: []
hard_filters:
  knowledge_status_allowed: []
  retrieval_policy_allowed: []
  overlay_scope:
  action_basis_required: true | false
  excluded_path_roles: []
retrieval_lanes:
  reviewed:
  candidate_orientation:
  raw_drilldown:
  active_project_overlay:
  audit_evidence:
diagnostic_signals:
  tag_hits:
  facet_counts:
  retrieval_scores:
  graph_centrality:
  feedback_clicks:
```

Rule:

```text
diagnostic signals cannot become support_refs, confidence, action_readiness, or
evidence_sufficiency.
```

## Candidate Merge Verdict

```text
This delta is compatible with the current Source Intake Control Flow.
It strengthens filtering and routing without changing truth-layer authority.
It should be tested before mainline writeback.
```
