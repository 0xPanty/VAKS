---
record_kind: sandbox_enterprise_readiness_report
status: complete
created_at: 2026-06-14
scope: source-annotation-scale-enterprise-stress
truth_boundary: sandbox_recommendation_not_main_architecture
---

# Enterprise Readiness Report

## Plain-Language Verdict

The design is now enterprise-ready as a sandbox-proven landing plan.

More precisely:

```text
L3 stress validated
L4 pilot-ready
not yet L5 production-operated
```

It can be directly piloted in a real Obsidian vault with the gates below. It
should not be called fully production-operated until real users run it, repair
real broken anchors, and confirm the Bases workflow is comfortable under daily
use.

## What Changed In This Round

The earlier product model was correct but not enough for enterprise use.

High-pressure testing found and fixed four issues:

| Issue | Why it matters | Fix |
|---|---|---|
| archived + bad-anchor lifecycle conflict | one record could look archived and repair-needed at the same time | archived lifecycle now wins |
| 5,000-file validation was too slow | enterprise checks need to run regularly | C YAML loader and lazy exact matching |
| default inbox was too large | 4,691 rows is not a workbench, it is a pile | split working inbox from locator pool |
| support_checked overrode ambiguous anchor | bad anchors must not become current support-audit items | anchor repair beats support audit |

## Quantitative Results

### 5,000-Annotation Enterprise Gate

Persistent report:

```text
results/enterprise-stress-report-5000.md
```

Result:

```text
passed: true
runtime: 3.848s
records/sec: 1299.33
errors: 0
mutation caught: 29 / 29
bad context packs caught: 5 / 5
AI ready contamination: 0
repair missing: 0
stale missing: 0
working inbox: 153
locator pool: 4,538
context pack: 60 items / 72,583 bytes
context sources: 24
max items per source: 5
source digest backlog: 9
digest backlog p95 age: 14 days
```

### 10,000-Annotation Stretch Gate

Persistent report:

```text
results/enterprise-stress-report-10000.md
```

Result:

```text
passed: true
runtime: 8.364s
records/sec: 1195.61
errors: 0
mutation caught: 29 / 29
bad context packs caught: 5 / 5
AI ready contamination: 0
repair missing: 0
stale missing: 0
working inbox: 303
locator pool: 9,088
repair queue: 329
stale queue: 130
scale debt: 7,478
context pack: 60 items / 72,703 bytes
context sources: 24
max items per source: 5
source digest backlog: 9
digest backlog p95 age: 14 days
```

## Enterprise Product Shape

The enterprise design is not:

```text
one giant annotation inbox
```

It is:

```text
Working inbox
Locator pool
Source drilldown
Project lens
Repair queue
Stale queue
Scale-debt dashboard
Support audit
AI review-input ready / blocked
Cold archive
```

## Hard Invariants

These are now tested:

1. `source_annotation` cannot be support.
2. `source_annotation` cannot be action basis.
3. `source_annotation` cannot mutate truth.
4. `project_borrow_scope` and `project_non_borrow_scope` are forbidden.
5. `support_checked: true` requires `evidence_packet_ref`.
6. `support_checked` cannot be current on broken, ambiguous, source_changed, or stale anchors.
7. bad anchors cannot enter AI export ready.
8. stale anchors cannot enter AI export ready.
9. archived annotations cannot enter normal retrieval.
10. duplicate IDs fail.
11. malformed selectors fail.
12. bad context packs fail if they cite annotations as support.

## Why This Is Now Enterprise-Level

It has:

```text
large file-backed corpus
mutation suite
bad context-pack suite
performance gate
operator-load gate
repair queue accuracy
stale queue accuracy
AI contamination checks
project pollution checks
scale-debt visibility
source-health reporting
source digest backlog SLA
source-diverse AI context packing
```

The most important enterprise improvement is the workbench split:

```text
working inbox = human daily queue
locator pool = large stable machine-queryable pool
source health = source-level operations dashboard
```

That is what prevents the system from becoming another giant tag pile.

## Remaining Real-World Risks

These cannot be fully proven in synthetic sandbox data:

1. Real Obsidian Bases UI comfort.
2. Real OCR / ASR / PDF anchor drift.
3. Human willingness to repair stale anchors.
4. Whether project teams agree on role labels.
5. Backup and migration behavior under thousands of tiny Markdown files.
6. Whether source digest creation keeps up with scale debt.

## Recommendation

Adopt as a real-vault pilot, not as a hidden automatic migration.

Pilot gate:

```text
100 real annotations
then 500
then 2,000
then 10,000 only after repair/source-health workflow is comfortable
```

Production gate:

```text
same validator green
real Bases views usable
repair backlog visible
source digest process established
AI export reviewed with real prompts
backup/sync behavior verified
```

## Final Status

This sandbox has achieved enterprise stress validation for the design.

The next step is not more abstract design. The next step is a controlled real
vault pilot using this landing package.
