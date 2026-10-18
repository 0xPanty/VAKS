---
record_kind: sandbox_final_report
status: complete
created_at: 2026-06-14
scope: source-annotation-scale-product-sandbox
truth_boundary: sandbox_recommendation_not_main_architecture
---

# Source Annotation Scale Sandbox Final Report

## Verdict

The source annotation design is worth keeping.

It is stronger than the simple inline-footnote idea because it keeps the same
comfortable capture entrance while adding VAKS-grade safeguards:

```text
footnote comfort
+ source-span sidecar
+ repairable selectors
+ project lens
+ scale-debt queue
+ AI context export boundary
+ support/action denial tests
```

The design is not "final final" as a user experience. It is now a product-grade
sandbox candidate. The remaining proof should come from real Obsidian use.

## What To Do When Annotations Grow

Do not build a larger tag pile.

Use this structure:

```text
Capture -> Triage -> Use -> Repair
```

### Capture

The user marks useful original text. The system writes a sidecar record.

Human-facing fields stay small:

```text
source
span
short note
role
optional Project Overlay link
```

### Triage

Bases provides workbench views:

```text
Annotation inbox
Source drilldown
Project lens
Routing queue
Needs anchor repair
Stale anchors
Scale debt
Support checked audit
AI export ready
AI export blocked
Cold archive
```

### Use

AI export never sends a naked note. It sends:

```text
annotation record
resolved source span
role
short note
warning: annotation_not_support
action_basis_allowed: false
```

### Repair

Bad anchors are first-class work items:

```text
ambiguous -> repair
broken -> repair
source_changed -> repair / review pressure
stale -> refresh before AI export
```

## Why This Solves The User Experience Problem

### Bases Summary Can Stay Readable

Default table shows only the fields a human needs:

```text
source
role
note
anchor status
pressure
route refs
path
```

Long quote selectors, hashes, timestamps, and packet details are hidden in
repair/audit views.

### Project Filtering Does Not Get Mixed Up

Project filtering uses:

```text
project_overlay_refs
```

The table may display a project name, but the annotation itself does not create:

```text
project_borrow_scope
project_non_borrow_scope
project verdict
```

Project decisions still live in Project Overlay.

### Broken Anchors Can Be Fixed

Each annotation keeps:

```text
source_snapshot_ref
source_hash
selector_exact
selector_prefix
selector_suffix
position / line / timestamp / page fields
anchor_status
anchor_checked_at
anchor_match_count
```

That lets the system separate:

```text
exact_verified
fuzzy_recovered
ambiguous
broken
source_changed
stale
```

### AI Gets The Right Context

The AI context pack includes the original source excerpt. It also explicitly says
that the annotation is only review input.

The support gate remains:

```text
Evidence Packet / evidence_support
```

not:

```text
source_annotation
```

## Sandbox Implementation

Created:

```text
product-model-v0.md
workbench-prototype.base
scripts/generate_sandbox_fixtures.py
scripts/validate_annotation_sandbox.py
samples/
results/
```

Generated fixtures:

```text
35 good annotations
7 bad mutation annotations
1 bad context pack
4 sample source artifacts
```

Validation result:

```text
passed: true
good-corpus errors: 0
mutation annotations caught: 7 / 7
bad context pack caught: true
```

Current view counts:

```text
AI export ready: 30
Needs anchor repair: 3
Stale anchors: 1
Scale debt: 29
Project lens: 14
Routing queue: 12
Support checked audit: 1
Cold archive: 1
```

Warnings surfaced:

```text
one dense source needs a source digest route
three selector duplicate pressure groups need consolidation
```

These warnings are expected and healthy. They are the product showing
maintenance debt instead of hiding it.

## Required Mainline Adoption Gates

Before moving from sandbox into the main framework, keep these gates:

1. `source_annotation` cannot be packed as support.
2. `action_basis_allowed` must remain false.
3. `truth_mutation_allowed` must remain false.
4. `support_checked: true` requires `evidence_packet_ref`.
5. bad anchors cannot enter AI export ready.
6. stale anchors cannot enter AI export ready.
7. project references cannot create project borrow verdicts.
8. dense sources must route to source digest / consolidation.
9. duplicate IDs fail.
10. duplicate selector pressure is visible.

## Recommendation

Adopt the product shape, not every sandbox field immediately.

The next real step should be:

```text
Use this workbench on a small real source batch.
Keep the sidecar canonical.
Keep inline footnote as optional capture handle.
Let Bases show inbox, project lens, repair, stale, scale debt, and AI export ready.
Only then decide which extra fields deserve main schema adoption.
```

This keeps the system both comfortable and strict.

## Enterprise Stress Extension

After the first product-level sandbox, an enterprise stress extension was run.

Persistent reports:

```text
results/enterprise-stress-report-5000.md
results/enterprise-stress-report-10000.md
enterprise-readiness-report.md
enterprise-landing-runbook.md
```

Final enterprise result:

```text
5,000 annotations: passed, 3.848s, 0 errors
10,000 annotations: passed, 8.364s, 0 errors
mutation suite: 29 / 29 caught
bad context packs: 5 / 5 caught
AI ready contamination: 0
context pack source cap: max 5 items per source
source digest backlog p95 age: 14 days
```

Key enterprise refinement:

```text
working inbox != locator pool
```

Stable annotations can scale into the locator pool without flooding the daily
human inbox.

Final product-level status:

```text
product-grade pilot design: yes
long-run architecture risk controlled: yes
fully production-operated proof: not yet
```
