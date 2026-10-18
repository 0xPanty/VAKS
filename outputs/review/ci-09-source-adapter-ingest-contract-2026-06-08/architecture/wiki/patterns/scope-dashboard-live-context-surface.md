---
type: pattern
status: sandbox-candidate
created: 2026-05-27
updated: 2026-06-08
source_libraries:
  - DuskWasHere/dusk-obsidian-vault
related_concepts:
  - "[[DEV_CONTEXT]]"
  - "[[MEMORY_TIER]]"
  - "[[property-driven-context-workbench]]"
  - "[[hierarchical-index-context-routing]]"
related_projects:
  - verified-action-knowledge-system
adoption_status: adapt
verification_status: sandbox-trial
evidence_level: primary
evidence_count: 1
confidence: medium
negative_evidence:
  - "The source implementation depends on Obsidian plugins and a legacy all-in-one vault package."
extension_points:
  - dev-context
  - context-dashboard
  - memory-tier
  - closeout
last_verified: 2026-05-27
next_review: 2026-06-03
epistemic_type: take
gaps:
  - "Still single-source Dusk evidence; promote only if accepted as workbench candidate, not truth core."
evidence_timeline:
  - date: 2026-05-27
    source: "[[2026-05-27-dusk-obsidian-vault-source]]"
    observation: "The Area Family template gathers components, connected projects, documentation, workstation notes, meetings, ongoing tasks, and completed tasks."
    effect: supports
    confidence: medium
relations:
  - target: "[[DEV_CONTEXT]]"
    type: refines
    strength: 4
    confidence: medium
    evidence:
      - "[[2026-05-27-dusk-obsidian-vault-source]]"
    rationale: "A dev context builder can use scope dashboards as candidate surfaces before selecting Core, Support, Risk, and Cold References."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[property-driven-context-workbench]]"
    type: supports
    strength: 4
    confidence: medium
    evidence:
      - "[[2026-05-27-dusk-obsidian-vault-source]]"
    rationale: "The pattern uses metadata, links, tags, and queries to surface context without moving files."
    created: 2026-05-27
    last_verified: 2026-05-27
tags:
  - pattern
  - dev-context
  - dashboard
  - memory-tier
  - workbench
---

# Scope Dashboard Live Context Surface

## AI-readable preamble

Use a project/area/scope page as a live surface that gathers relevant materials before building a temporary dev context pack.

The dashboard suggests context.

It does not decide truth.

## One-line definition

A scope dashboard gathers related notes, projects, meetings, tasks, and references into one view so an agent can select Core / Support / Risk / Cold References more efficiently.

## Problem solved

Without a scope surface, an agent often has to:

```text
search globally
open many files
infer scope from scattered notes
miss live tasks or meetings
mix old archive material with active work
```

A dashboard gives the agent a current working table.

## Source evidence

In `DuskWasHere/dusk-obsidian-vault`, `template_area.md` implements an Area Family dashboard.

It pulls:

```text
Components:
  area notes from the current area folder.

Projects:
  project notes whose connections contain the current area file.

Other:
  documentation and workstation notes connected to the current area file.

Scheduled Meetings:
  meeting notes tagged with the area.

Ongoing Task:
  unfinished tasks tagged with the area.

Completed Tasks:
  finished tasks tagged with the area.
```

The onboarding doc also says an Area Family note can act as the MOC for that topic and show connected components, projects, documentation, workstation notes, meetings, and tasks.

This sandbox reopened the local Dusk template and zip entry and retained narrow anchor snapshots:

```text
outputs/review/ci-05-scope-dashboard-live-context-surface-2026-06-08/evidence/dusk/template-area-anchor-snapshot.md
outputs/review/ci-05-scope-dashboard-live-context-surface-2026-06-08/evidence/dusk/onboarding-part-3-anchor-snapshot.md
```

It also runs one local VAKS trial:

```text
scope dashboard -> compact briefing -> selected dev context pack
```

## Applicable scenarios

- Creating a dev context pack for a project.
- Re-entering a project after a break.
- Checking active tasks and related sources before implementation.
- Reviewing what should cool down after a work phase.
- Building Obsidian Bases / Dataview / generated Markdown workbench views.

## Not applicable

- Verifying a claim.
- Promoting a pattern.
- Deciding confidence.
- Replacing source provenance.
- Replacing the dev context pack.
- Making plugin output authoritative.
- Creating action basis readiness.
- Creating reviewed relations.
- Changing activation tier permanently.

## Minimum implementation

A scope dashboard should expose:

```yaml
scope_id:
scope_name:
scope_type: project | area | domain | workflow
core_candidates: []
support_candidates: []
risk_candidates: []
task_candidates: []
meeting_or_event_candidates: []
cold_reference_candidates: []
last_refreshed:
not_truth_layer: true
not_evidence_support: true
not_action_basis: true
selection_status: candidate_only
```

For Markdown-only v0.1:

```markdown
# Scope Dashboard: <name>

## AI-readable preamble

This page suggests context for <scope>. It is not evidence and not truth.

## Candidate Core

## Candidate Support

## Candidate Risk

## Active Tasks / Follow-ups

## Cold References

## Closeout Notes
```

## Fusion suggestion

Use with the existing flow:

```text
project/domain index
-> scope dashboard
-> compact briefing
-> dev context pack
-> implementation
-> closeout / cooling
```

Role split:

```text
Index:
  tells where to start.

Scope dashboard:
  shows what is live in this scope.

Briefing:
  explains why candidates may matter.

Dev context pack:
  locks selected Core / Support / Risk / Cold References for work.

Review gate:
  decides truth and durable adoption.
```

## Boundary

The dashboard is a workbench surface.

It is not the source of truth.

It should make the next read easier, not silently change verification or memory tier.

It may suggest Core / Support / Risk / Cold candidates, but a dev context pack
must record which items were selected and why. Unselected dashboard items do not
enter the pack just because they appeared on the dashboard.
