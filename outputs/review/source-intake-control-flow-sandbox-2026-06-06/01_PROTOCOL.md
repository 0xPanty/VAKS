---
type: sandbox_protocol
status: candidate_only
created_at: 2026-06-06
scope: source intake lifecycle and dimensions
truth_boundary: protocol candidate only
---

# 01 Protocol

## Short Lifecycle

```yaml
lifecycle_state:
  - source_registered
  - light_findable
  - candidate_provisional
  - heavy_review_open
  - reviewed_promoted
  - archived_cold
```

Plain language:

```text
source_registered = source exists
light_findable = source is easy to find later
candidate_provisional = candidate points exist, not authority
heavy_review_open = strict review started, not passed
reviewed_promoted = reviewed knowledge / decision / adopted pattern
archived_cold = retained history, excluded by default
```

## Four Orthogonal Dimensions

```yaml
processing_tier: light | medium | heavy
knowledge_status: raw | candidate | reviewed
overlay_state: none | suggested | confirmed | archived
review_pressure: none | review_due | blocked
```

Rules:

```text
processing_tier says how much work was done.
knowledge_status says whether it can act as knowledge.
overlay_state says whether it has a project sidecar.
review_pressure says whether something needs review or blocking.
```

Hard boundary:

```text
heavy == more processed
heavy != more true
```

## Promotion Triggers

Move `candidate_provisional` to `heavy_review_open` when any of these appear:

```text
architecture adoption
decision
action basis
risk-sensitive answer
strong relation
reviewed knowledge promotion
normative should/must/adopt/reject language
conflict resolution
negative knowledge promotion
```

## Overlay Confirmation

```text
suggested overlay:
  trace-only
  not a durable vault note
  not default retrieval

confirmed overlay:
  requires explicit confirmation or explicit project-intake write permission
  stored under outputs/review/project_overlays/<project>/...
  current project retrieval only

archived overlay:
  excluded from default retrieval
```

## Feedback Rule

```text
feedback writes events
feedback does not mutate truth
feedback can update activation / routing / review_pressure
heavy review is required before any reviewed boundary or decision changes
```
