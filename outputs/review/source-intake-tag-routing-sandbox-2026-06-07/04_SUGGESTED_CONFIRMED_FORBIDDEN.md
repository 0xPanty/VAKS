---
type: sandbox_suggestion_policy
status: candidate_only
created_at: 2026-06-07
scope: suggested, confirmed, and forbidden metadata
truth_boundary: sandbox suggestion policy only
---

# Suggested / Confirmed / Forbidden

## Default

Automatic metadata suggestions should default to temporary surfaces:

```text
intake UI
temporary sidecar
review diff
query-run trace
agent trace
suggestion inbox
```

Do not persist them into a main source note as confirmed fields unless the user
confirms them or the task explicitly authorizes intake writeback.

## Safe To Suggest

```yaml
suggested_topics: []
suggested_entities: []
suggested_content_form:
suggested_language:
suggested_version_or_time_scope:
suggested_routing_hint: []
suggested_query_time_filters: []
```

Allowed use:

```text
candidate recall
intake review
query-time filtering
context-pack preparation
future confirmation
```

Forbidden use:

```text
reviewed status
action basis
source reliability
truth confidence
project adoption
borrow / non-borrow conclusion
```

## Must Be Confirmed

```text
processing_tier
knowledge_status
retrieval_policy
promotion_gate
project_overlay_ref
candidate point keep / drop
project_borrow_scope
project_non_borrow_scope
risk / anti-pattern wording
reviewed / adopted / avoid wording
action_basis_allowed
decision / action readiness
```

Reason:

```text
These fields can affect review queue, authority lane, project absorption,
retrieval visibility, or action basis.
```

## Forbidden In Ordinary Tags

```text
#reviewed
#approved
#adopted
#use-this
#best-practice
#truth
#safe
#action-basis
#decision
#verified
#high-confidence
#for-vaks
#do-not-borrow-for-vaks
#adopt-for-vaks
```

Also forbidden:

```text
retrieval score means credible
many tag hits means true
facet count means support
dashboard prominence means action-ready
graph rank means reviewed relation
feedback click means truth confidence
```

## Allowed Tags

Open tags may remain as weak recall markers:

```text
rag
obsidian
agent-memory
source-intake
metadata
retrieval
pkm
```

Rule:

```text
Tags can help find material.
Tags cannot establish status.
```

## Lint Trigger

Any authority-like tag in a source, candidate, overlay, query-run, or feedback
file should create lint pressure:

```yaml
lint_kind: forbidden_authority_tag
review_pressure_effect: review_due
suggested_action: move status to formal field or remove the tag
```
