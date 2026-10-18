---
record_kind: sandbox_enterprise_landing_runbook
status: complete
created_at: 2026-06-14
scope: source-annotation-scale-enterprise-stress
truth_boundary: sandbox_runbook_not_main_architecture
---

# Enterprise Landing Runbook

## Core Rule

Use annotations as source locators, not knowledge verdicts.

```text
mark useful original text
keep sidecar as canonical record
route into candidate / overlay / evidence packet only when needed
never let annotation itself become support
```

## Required Views

Pilot default should stay under five daily views:

| View | Purpose |
|---|---|
| Working inbox | new / untriaged annotations only |
| Needs anchor repair | broken, ambiguous, source_changed |
| Source drilldown | inspect all annotations for one source in source order |
| AI review-input ready / blocked | safe review-input export and unsafe blockers |
| Source health | source-level repair, stale, scale debt, digest state |

Extended operation can add these views after the pilot proves the core flow:

| View | Purpose |
|---|---|
| Locator pool | stable bulk locators; queryable, not daily inbox |
| Project lens | show annotations linked to one Project Overlay |
| Stale anchors | old anchors requiring refresh |
| Scale debt | dense sources and repeated selectors requiring digest/consolidation |
| Support checked audit | support_checked items and evidence_packet_ref |
| Cold archive | closed, duplicate, obsolete, or intentionally ignored |

## Machine Fields vs Capture Fields

The record has many machine fields. The user should not see or fill them during
capture.

Human capture fields:

```text
source span
short note
role
optional project link
optional route hint
```

Minimum enterprise machine record:

```yaml
record_kind: source_annotation
annotation_id:
source_ref:
working_copy_ref:
source_snapshot_ref:
source_hash:
selector_type:
selector_exact:
selector_prefix:
selector_suffix:
selector_position_start:
selector_position_end:
selector_timestamp_start:
selector_timestamp_end:
selector_line_start:
selector_line_end:
selector_page:
selector_rect:
content_hash:
anchor_status:
anchor_checked_at:
anchor_check_method:
anchor_match_count:
anchor_stale:
lifecycle_state:
annotation_role:
body_note:
candidate_refs: []
project_overlay_refs: []
support_checked: false
evidence_support_status: not_checked
evidence_packet_ref:
source_digest_required: false
blocked_reason:
next_action:
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: review_input_only
  action_basis_allowed: false
  warning_code: annotation_not_support
action_basis_allowed: false
truth_mutation_allowed: false
```

## Lifecycle Priority

Priority order:

```text
archived
bad anchor repair
stale refresh
support audit
project / candidate route
ordinary triage
locator pool
```

Hard rule:

```text
anchor repair beats support audit
```

## Daily Workflow

1. Capture useful source span.
2. New item enters Working inbox.
3. If anchor is bad, move to repair queue.
4. If anchor is stale, refresh before AI/export/review use.
5. If source is dense, create source digest or consolidate duplicates.
6. If project-specific, link Project Overlay.
7. If it might support a claim, create or link Evidence Packet.
8. If stable and triaged, it moves to Locator pool.
9. AI export pulls from Locator pool / source drilldown with warning boundaries.

## AI Export Contract

Every exported annotation item must include:

```yaml
record_kind: source_annotation
pack_role: review_input
warning_code: annotation_not_support
action_basis_allowed: false
```

Every resolved source span must include:

```yaml
may_count_as_support: false
support_check_required: true
```

Blocked from AI-ready:

```text
broken
ambiguous
source_changed
stale
archived
missing selector
missing warning
support_checked without evidence packet
truth/action/project verdict fields
```

Default export selection must also enforce:

```text
query-aware selection
source diversity
max items per source
prefer exact_verified over fuzzy_recovered
fuzzy_recovered is caution-only
```

## Operational Gates

Run validation before adoption and after schema/view changes.

Minimum gate:

```powershell
python outputs\review\source-annotation-scale-sandbox-2026-06-14\scripts\enterprise_stress_suite.py --count 5000 --sources 120 --spans 120 --runtime-gate-seconds 30 --max-inbox-items 250
```

Stretch gate:

```powershell
python outputs\review\source-annotation-scale-sandbox-2026-06-14\scripts\enterprise_stress_suite.py --count 10000 --sources 240 --spans 140 --runtime-gate-seconds 60 --max-inbox-items 500
```

## Source Digest SLA

Every dense source must appear in Source Health with:

```yaml
digest_ref:
last_digest_at:
next_digest_due:
debt_queue: source_digest_backlog
debt_owner_or_queue:
next_action: create_or_refresh_source_digest
digest_backlog_age_days:
```

Pilot target:

```text
p95 digest_backlog_age_days <= 14
no dense source without next_action
```

## Pilot Rollout

### Batch 1

```text
100 real annotations
```

Goal:

```text
capture comfort
view readability
no raw reading pollution
```

### Batch 2

```text
500 real annotations
```

Goal:

```text
repair queue accuracy
project lens comfort
source drilldown comfort
```

### Batch 3

```text
2,000 real annotations
```

Goal:

```text
scale-debt process
source digest process
AI export quality
```

### Batch 4

```text
10,000 real annotations
```

Goal:

```text
sync/backup performance
operator load
validator runtime
repair backlog sustainability
```

## Stop Conditions

Stop rollout if:

```text
source_annotation appears as support
action_basis_allowed becomes true
project borrow verdict appears in annotation
working inbox becomes a giant pool
repair backlog is hidden
stale anchors enter AI export
source digest cannot keep up with dense sources
```

## Enterprise Decision

Direct landing path:

```text
adopt sidecar + workbench + validator together
```

Do not adopt only the inline-footnote capture handle. The capture handle is
comfortable, but the enterprise value comes from the sidecar, views, and gates.
