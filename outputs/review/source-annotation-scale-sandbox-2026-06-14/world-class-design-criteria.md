---
record_kind: sandbox_world_class_criteria
status: active
created_at: 2026-06-14
scope: source-annotation-world-class-product-pass
truth_boundary: sandbox_only_not_main_architecture
---

# World-Class Design Criteria

## Bar

World-class here does not mean heavy or feature-rich.

It means:

```text
the obvious path is fast
the dangerous path is blocked
the large-scale path stays calm
the repair path is visible
the AI path is bounded
```

## Product Principles

### 1. Capture Should Feel Like Reading

The capture action should be:

```text
mark span
optionally add tiny note
continue reading
```

Everything else is defaulted or deferred.

### 2. The Inbox Is For Work, Not Storage

The daily inbox should not contain every stable annotation.

```text
new / untriaged -> working inbox
stable / triaged -> locator pool
bad -> repair queue
old -> stale queue
dense -> scale debt
```

### 3. Anchors Are Operational Objects

Anchors have health:

```text
exact_verified
fuzzy_recovered
ambiguous
broken
source_changed
stale
```

They are not just pretty links.

### 4. Role Is Not Verdict

`possible_support` is not support.

`counterexample` is not disproof.

`project_overlay_refs` is not project adoption.

### 5. AI Export Must Be Bounded

The AI gets:

```text
source span
annotation note
boundary warning
route refs
```

It does not get permission to treat the annotation as proof.

### 6. Source Health Is The Real Dashboard

At scale, the best view is source-level:

```text
source
active locators
repair count
stale count
scale debt
digest route
AI-ready count
```

This is how operators avoid drowning in small records.

## Metrics

| Metric | World-class target |
|---|---|
| Human capture fields | <= 5 default-facing fields |
| Working inbox p95 | <= daily triage capacity x 2 |
| Repair backlog p95 | <= weekly repair capacity |
| Stale backlog p95 | <= weekly refresh capacity |
| AI export contamination | 0 |
| Support/action contamination | 0 |
| Bad-anchor queue recall | 100% |
| Stale queue recall | 100% |
| Default context pack size | <= 250 KB |
| Context source diversity | max 5 items per source by default |
| Large corpus validation | 10,000 files under 60s |
| Long-run simulation | 180 days without unbounded inbox growth |
| Dense source operation | source-level digest backlog, not row-level panic |
| Digest backlog p95 age | <= 14 days |

## What To Avoid

Do not add:

```text
automatic truth promotion
automatic support_checked
global trust scores
graph rank as authority
annotation popularity scores
large formal ontology
mandatory dashboards before capture works
```
