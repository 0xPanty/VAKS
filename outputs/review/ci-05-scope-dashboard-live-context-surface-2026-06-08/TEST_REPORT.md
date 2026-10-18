# CI-05 Sandbox Test Report: Scope Dashboard Live Context Surface

Date: 2026-06-08

Scope:

```text
CI-05 is a workbench / dev-context candidate surface.
It is not a truth layer, evidence support layer, reviewed relation, action basis, permanent activation tier, or Obsidian plugin authority.
```

## Sandbox

Sandbox root:

```text
outputs/review/ci-05-scope-dashboard-live-context-surface-2026-06-08/
```

Base architecture copied from:

```text
outputs/review/ci-04-decision-outcome-precondition-before-calibration-2026-06-08/architecture/
```

This sandbox tests CI-05 on top of CI-02, CI-02.5, CI-03, and CI-04.

No permanent Obsidian sync was performed.

## Why This Needed Extra Evidence

CI-05 was not in the same state as CI-01 through CI-04.

Previous state:

```text
support: weak
sufficiency: insufficient
recommendation: needs_more_evidence
```

Missing evidence from the promotion packet:

```text
Reopen original Dusk template entries or retain a local template snapshot.
Run one VAKS dev-context example showing dashboard -> briefing -> dev context pack selection.
Record failure cases: dashboard stale, plugin output treated as authority, task state polluting truth.
```

## Evidence Added

Reopened local Dusk material from:

```text
%TEMP%/codex-dusk-obsidian-vault/
```

Retained sandbox evidence snapshots:

```text
evidence/dusk/template-area-anchor-snapshot.md
evidence/dusk/onboarding-part-3-anchor-snapshot.md
```

Confirmed anchors:

```text
template_area.md:13-38
template_area.md:40-66
Vault Onboarding Part 3 - Main Features.md:72-83
```

Observed support:

- The Area Family template gathers components, connected projects, documentation/workstation notes, meetings, ongoing tasks, and completed tasks.
- The onboarding text says an `area_family` note can show connected components, projects, documentation notes, workstation notes, meetings, and tasks.
- The onboarding text also says Area Family can serve as a MOC for the topic.

## Sandbox Trial

Trial flow:

```text
scope dashboard
-> compact briefing
-> temporary dev context pack selection
```

Added fixtures:

```text
tests/fixtures/scope-dashboard/pass-scope-dashboard.md
tests/fixtures/scope-dashboard/pass-compact-briefing.md
tests/fixtures/scope-dashboard/pass-dev-context-pack-selection.md
tests/fixtures/scope-dashboard/block-dashboard-as-truth.md
tests/fixtures/scope-dashboard/block-plugin-output-authority.md
tests/fixtures/scope-dashboard/block-auto-context-pack.md
tests/fixtures/scope-dashboard/block-action-basis-ready.md
tests/fixtures/scope-dashboard/block-reviewed-relation.md
tests/fixtures/scope-dashboard/block-permanent-activation.md
```

Allowed:

```text
surface Core / Support / Risk / Task / Cold candidates
create a compact briefing
select a temporary dev context pack with rationale
show stale/risky candidates
```

Blocked:

```text
dashboard as truth
plugin output as authority
automatic dev context pack selection
dashboard as action basis
dashboard-created reviewed relation
permanent activation-tier mutation from dashboard appearance
```

## Pressure Test

Command:

```powershell
& "outputs\review\ci-05-scope-dashboard-live-context-surface-2026-06-08\tests\pressure-test.ps1"
```

Result:

```text
RESULT pass=90 fail=0
```

Test dimensions:

- Dusk anchor snapshots exist and contain the required anchor claims.
- CI-05 pattern references the new snapshots and the local trial.
- `DEV_CONTEXT.md` sandbox copy contains the scope dashboard trial boundary.
- Knowledge graph index sandbox copy records the CI-05 boundary.
- PASS fixtures complete dashboard -> briefing -> dev context pack selection.
- BLOCK fixtures catch truth, plugin authority, auto-selection, action-basis, reviewed-relation, and permanent activation misuse.
- Compatibility checks confirm CI-02, CI-02.5, CI-03, and CI-04 still exist in the same sandbox.
- Root pollution checks confirm formal root files were not changed by CI-05 sandbox-only wording.

## Result

Positive, but lower confidence than CI-01 through CI-04.

CI-05 is useful as a workbench / dev-context helper. It reduces scattered searching and helps an agent or human choose a temporary context pack.

It does not conflict with the existing architecture if kept outside the truth core.

It becomes overdesigned if treated as:

```text
truth authority
review authority
automatic context-pack builder
action-basis generator
permanent activation-tier engine
required Obsidian plugin runtime
```

## Recommendation

Keep CI-05 as a sandbox-positive candidate.

Do not promote it at the same level as CI-01 through CI-04 yet.

If merged later, merge only a lightweight boundary:

```text
scope dashboard = candidate context surface
briefing = explanation of why candidates may matter
dev context pack = explicit selected temporary working context
review gate / evidence sufficiency = still required for truth and action basis
```

Do not merge:

```text
tests/fixtures/
tests/pressure-test.ps1
Obsidian plugin dependencies
Dataview / Tasks / Bases as authority
automatic pack generation
dashboard-driven truth or relation changes
```

## Final Judgment

```text
positive: yes
overdesigned: no, if kept as a workbench candidate surface
conflict_with_existing_architecture: no
promotion_ready_like_CI01_to_CI04: no
recommend_keep_candidate: yes
recommend_mainline_merge_later: maybe, lightweight only
```

