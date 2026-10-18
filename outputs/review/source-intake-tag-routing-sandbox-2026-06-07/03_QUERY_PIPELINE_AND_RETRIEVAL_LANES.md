---
type: sandbox_retrieval_policy
status: candidate_only
created_at: 2026-06-07
scope: query pipeline and retrieval lanes for source intake metadata
truth_boundary: candidate retrieval policy only
---

# Query Pipeline And Retrieval Lanes

## Plain Rule

```text
First choose the pool.
Then search inside the pool.
Do not search everything first and repair authority later.
```

## Default Pipeline

```text
1. Query understanding
2. Hard filter extraction
3. Authority/status/project/path-role prefilter
4. Hybrid retrieval inside allowed lane
5. Link/entity/topic-pack expansion inside allowed lane
6. Separate lane display
7. Evidence support check for action-facing use
```

## Query Understanding

Extract:

```yaml
query_intent: answer | decision | implementation | research | source_inspection | audit_history
action_facing: true | false
project_scope:
source_type_filter:
time_or_version_scope:
extracted_topics: []
extracted_entities: []
query_time_filters: []
```

## Hard Filters

Apply before lexical/vector/tag search:

```yaml
knowledge_status_allowed:
retrieval_policy_allowed:
overlay_state_allowed:
project_scope_required:
action_basis_required:
review_pressure_allowed:
path_roles_allowed:
path_roles_excluded:
```

Default exclusions for ordinary current-rule search:

```text
old sandbox
baseline copy
package copy
zip file
repo snapshot
archived overlay
feedback event
unconfirmed suggestion
```

## Lanes

### Current Mainline Lane

Use for "what is the current rule?"

```text
include:
  SOURCE_INTAKE.md
  current templates
  latest relevant handoff
  wiki/indexes

exclude by default:
  sandbox packages
  baseline copies
  zip packages
  raw snapshots
  candidate distillations
  feedback events
```

### Candidate Orientation Lane

Use for research, comparison, and idea discovery.

```text
include:
  candidate distillations
  review candidates
  raw source summaries

required label:
  candidate / orientation only / not action basis
```

### Raw Drilldown Lane

Use for source inspection and final anchor lookup.

```text
include:
  raw/articles
  raw/videos
  raw/repos
  raw/papers
  stored transcripts
  snapshots when needed for stable anchors

rule:
  raw is provenance until a source span supports a specific point.
```

### Active Project Overlay Lane

Use only for the active project.

```text
include:
  confirmed overlays for current project

exclude:
  suggested overlays
  archived overlays
  overlays for other projects
```

### Audit Evidence Lane

Use for "why did we change this?" or "how was this tested?"

```text
include:
  checks/
  sandbox protocol
  pressure-test results
  baseline / with-variant copies when needed

rule:
  audit evidence explains process.
  It is not the current mainline rule by itself.
```

## Relevance Signals

Allowed inside an already-filtered lane:

```text
topics
entities
aliases
links
content_form
source_type
BM25 / lexical
dense embedding
sparse retrieval
late-interaction rerank
hybrid RRF inside one lane
topic pack routing
```

Forbidden:

```text
RRF across raw/candidate/reviewed/overlay lanes
tag hit as reviewed status
facet count as evidence
embedding score as trust
graph centrality as support
dashboard prominence as action basis
feedback click as truth confidence
```

## Output Rule

Every result lane must display or carry:

```yaml
knowledge_status:
processing_tier:
retrieval_policy.warning_code:
action_basis_allowed:
lane:
why_included:
why_excluded_if_relevant:
```

Human-facing display can simplify this to:

```text
[current rule]
[candidate only]
[raw source]
[active project overlay]
[audit evidence]
```

The machine-facing identity still needs to exist for filtering.
