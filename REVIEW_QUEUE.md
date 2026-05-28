---
type: implementation-note
status: active
created: 2026-05-27
updated: 2026-05-28
project: verified-action-knowledge-system
related_decisions:
  - "[[2026-05-27-traceability-first-graduated-verification]]"
related_patterns:
  - "[[review-gated-compile-queue]]"
  - "[[accumulated-source-cross-validation]]"
  - "[[claim-level-provenance-source-ranges]]"
sources:
  - "[[IMPLEMENTATION_BLUEPRINT]]"
  - "[[2026-05-27-alpha-point-collision-research]]"
verification_status: active
evidence_level: synthetic
confidence: high
validated_by:
  - "subagent adversarial review"
  - "external source comparison"
rollback_path:
  - "If point collision creates noise, keep source/candidate records and disable collision promotion until manual review rules improve."
last_verified: 2026-05-28
next_review: 2026-06-03
relations:
  - target: "[[IMPLEMENTATION_BLUEPRINT]]"
    type: refines
    strength: 5
    confidence: high
    evidence:
      - "[[REVIEW_QUEUE]]"
    rationale: "This file defines the first concrete review queue contract required by the implementation blueprint."
    created: 2026-05-27
    last_verified: 2026-05-28
  - target: "[[accumulated-source-cross-validation]]"
    type: refines
    strength: 5
    confidence: high
    evidence:
      - "[[REVIEW_QUEUE]]"
    rationale: "The queue introduces candidate points, collision signals, and point clusters as the practical mechanism for accumulated cross-validation."
    created: 2026-05-27
    last_verified: 2026-05-28
tags:
  - review-queue
  - point-collision
  - alpha
  - traceability-first
---

# REVIEW_QUEUE.md v0.1

## AI-readable preamble

This is the first review queue contract for the vault.

The queue is not a dumping ground and not a reviewed knowledge layer. It is where raw sources become reviewable candidate points, and where similar points collide before anything is promoted.

The core alpha mechanism is:

```text
provenance-first
-> candidate point
-> point collision signal
-> reviewed cluster
-> promoted claim / pattern / anti-pattern / decision
```

## 1. Why This Exists

We do not want every source to be fully verified when it enters the vault.

We also do not want AI output to become formal reviewed knowledge directly.

The review queue solves the middle:

```text
capture stays light
candidate points stay inspectable
similar points can cross-check each other
promotion stays reviewed
```

## 2. Queue Directory

Use this structure:

```text
outputs/review/
  candidates/
  collisions/
  clusters/
  archived/
```

v0.1 can create these directories lazily. The contract matters more than the folder existing before first use.

## 3. Core Records

### 3.1 Source Trace

Source trace is the minimum record needed before point extraction.

```yaml
source_id:
source_url_or_path:
raw_location:
source_type: article | paper | repo | docs | transcript | screenshot | chat | other
source_family:
upstream_sources: []
captured_at:
captured_by:
processing_mode: inbox | immediate
processing_status: raw-only | point-candidate-generated | reviewed | promoted | rejected
topics: []
```

Rules:

```text
source_family marks likely shared origin: same URL, same repo, same author, same org, same article chain, same transcript, same AI output.
upstream_sources records what this source appears to depend on or cite.
source_family and upstream_sources are hints, not final independence judgments.
```

### 3.2 Candidate Point

Candidate point is the atomic review unit.

It should be one small comparable idea, not a whole article summary.

```yaml
record_type: candidate-point
point_id:
point_text:
normalized_point:
point_type: fact | take | hypothesis | practice | warning | decision-candidate
topics: []
entities: []
scope:
  domain:
  project:
  version:
  time_range:
  conditions:
source_refs:
  - source_id:
    source_url_or_path:
    source_range:
    quote_or_excerpt:
extracted_by:
extracted_at:
uncertainty:
possible_related_points: []
review_status: pending | accepted | rejected | needs-edit
promotion_target:
```

Rules:

```text
If a point cannot be traced to a source range or excerpt, it is not ready for collision.
If a point has broad wording, narrow the scope before promotion.
If a point is an AI inference, mark it as hypothesis unless source text directly supports it.
```

### 3.3 Collision Signal

Collision signal records how two points relate.

```yaml
record_type: collision-signal
signal_id:
from_point:
to_point:
relation: supports | contradicts | refines | risk_of | derived_from | duplicates | near_miss | unrelated
similarity_basis:
  - keyword
  - entity
  - source_overlap
  - semantic_similarity
  - manual
source_independence: independent | same-origin | derived | unknown
independence_rationale:
relation_rationale:
review_status: pending | accepted | rejected | needs-edit
reviewed_by:
reviewed_at:
```

Rules:

```text
Similarity only creates a pending signal.
Only reviewed signals can increase promotion readiness.
Same-origin or derived sources do not count as independent support.
Contradictions must stay visible; do not auto-resolve them.
```

### 3.4 Point Cluster

Point cluster groups recurring candidate points.

```yaml
record_type: point-cluster
cluster_id:
canonical_point:
member_points: []
reviewed_supports: []
reviewed_contradictions: []
reviewed_refinements: []
source_families: []
independent_source_count:
primary_source_count:
status: emerging | in-review | promoted | conflicted | stale | rejected
promotion_readiness: none | watch | review | promote-candidate
promotion_target:
gaps: []
warnings: []
last_seen:
next_review:
```

Rules:

```text
A cluster is not truth.
A cluster is a dashboard for promotion review.
Clusters with contradictions can still be valuable, but they promote as conflict-aware claims or anti-patterns.
```

## 4. Minimum Workflow

### Step 1: Capture Source

Write source into `raw/` or source-specific raw folder.

Minimum requirement:

```text
source_url_or_path
raw_location
captured_at
captured_by
processing_status
```

### Step 2: Extract Candidate Points

Codex extracts 2-8 candidate points from the source.

Each point must be small enough to compare.

Good:

```text
Claude-Obsidian uses hot.md as a recent context cache for cross-session recall.
```

Too broad:

```text
Claude-Obsidian is useful.
```

### Step 3: Find Possible Collisions

For each new point, search existing points and promoted nodes.

v0.1 search order:

```text
1. exact entity / keyword search
2. topic and tag search
3. source family / source overlap search
4. optional embedding search later
```

### Step 4: Create Pending Collision Signals

Do not decide truth yet.

Create pending signals:

```text
supports
contradicts
refines
risk_of
derived_from
duplicates
near_miss
unrelated
```

### Step 5: Review Collision Signals

Review asks:

```text
Are these points actually saying the same thing?
Are their scopes compatible?
Are the sources independent?
Does one source copy the other?
Is the newer source more authoritative?
Is there a direct contradiction?
```

### Step 6: Update Cluster

Accepted signals update the point cluster.

Rejected signals stay auditable.

### Step 7: Promote

Promotion is allowed only when a cluster is reviewed.

Promotion examples:

```text
claim:
  two independent sources support a narrow factual point

pattern:
  several sources show the same reusable design

anti-pattern:
  repeated evidence shows a failure mode

decision:
  reviewed pattern + project fit + risk + rollback
```

## 5. Promotion Rules

### Claim Promotion

Minimum:

```text
at least one source-backed candidate point
source range or excerpt
no unresolved high-severity contradiction
reviewed collision signals if cross-source support is claimed
```

Strong candidate:

```text
2+ independent source families support it
or 1 primary source directly supports it
```

### Pattern Promotion

Minimum:

```text
one or more reviewed claims
one reusable design statement
applicable context
failure condition
negative evidence or explicit "not found yet"
```

### Decision Promotion

Minimum:

```text
reviewed source-backed basis
risk
preconditions
rollback
success metric
feedback path
```

## 6. What Must Not Be Automated

v0.1 forbids:

```text
auto cross-checked from similarity
auto confidence increase from repetition
counting same-origin copies as independent support
counting AI summaries as independent sources
auto contradiction resolution
auto promotion to claim / pattern / decision
vector score as evidence
silent overwrite of older claims
```

## 7. Lint Rules

First lint checks:

```text
candidate point without source_refs
candidate point without source_range or excerpt
collision signal still pending but used for promotion
support signal with source_independence: same-origin counted as independent
contradiction signal ignored during promotion
point cluster promoted with no reviewed signals
point cluster promoted while status: conflicted
decision promoted without rollback or feedback path
```

## 8. First Field Test

Use 10 real sources.

Expected output:

```text
10 source traces
20-50 candidate points
10-30 collision signals
3-8 point clusters
1 promoted claim or pattern candidate
1 visible contradiction or near_miss
```

Success condition:

```text
The queue makes it easier to see recurring ideas and conflicts than reading the source list manually.
```

Failure condition:

```text
The queue produces noisy clusters that cannot support promotion decisions.
```

If it fails, adjust point granularity and source independence rules before adding embeddings or scoring.
