---
type: high_intensity_gauntlet
status: pass_after_patches
created_at: 2026-06-05
project: verified-action-knowledge-system
scope: project-lens-full-agent-maintenance-pressure
truth_boundary: sandbox gauntlet only; not reviewed knowledge; not mainline architecture; not commit authority
---

# Project Lens High-Intensity Gauntlet

## Goal

Run Project Lens hard enough that it is tested as a working maintenance surface, not just a nice idea.

## Final Verdict

```yaml
overall: pass_after_patches
agent_maintenance_value: high
blocking_issue_remaining: none_found_in_current_sandbox
safe_as_candidate_sidecar: yes
safe_to_commit_without_scoped_review: no
mainline_merge_without_user_approval: no
```

Human-readable:

```text
Project Lens now feels operationally usable for me as the maintenance agent.
The hard run found real issues and fixed them.
The remaining risk is not conceptual confusion; it is commit scope and future governance.
```

## Test Matrix

| ID | Test | Result | Notes |
|---|---|---|---|
| H01 | Lens entry integrity | pass after patch | Added `kp_ref`; all 10 refs resolve. |
| H02 | Target hint semantics | pass after patch | Added `conceptual` so workflow/module hints are not misread as unchecked file anchors. |
| H03 | Candidate source refs | pass | 42 `Derived From Sources` refs resolve. |
| H04 | Source routing source paths | pass | 25 raw source paths resolve. |
| H05 | Source routing pattern routes | pass after patch | Fixed missing `agent-memory-quarantine` route. |
| H06 | Pattern-to-Lens coverage | pass | 10 candidate patterns, 10 Lens entries, no mismatch. |
| H07 | Outcome snapshot creation | pass | 1 landed candidate, 3 boundary candidates. |
| H08 | Outcome ref resolution | pass after correction | 2 Lens outcome refs resolve; mispatch risk documented. |
| H09 | Boundary snapshot section completeness | pass | 3/3 boundary snapshots include required triggerable sections. |
| H10 | Mainline pollution check | pass | No Project Lens / Grok / Core-Lens-Snapshot terms in mainline docs/templates. |
| H11 | Schema/template diff check | pass | No diff in `SCHEMA.md`, `REVIEW_QUEUE.md`, or `templates`. |
| H12 | Git staging check | pass | No staged files. |
| H13 | Obsidian sandbox sync | pass | 21/21 files match repo hashes after high-intensity sync. |

## Issues Found And Fixed

### I03. `kp_id` Was Not Enough For Agent Navigation

Problem:

```text
`kp_id` identifies the idea, but not the file.
```

Patch:

```text
Add `kp_ref` to every Lens Entry.
```

Effect:

```text
Lens -> candidate pattern -> raw sources is now direct.
```

### I04. `not_checked` Was Too Muddy

Problem:

```text
workflow/module hints were labeled not_checked even though they are conceptual by nature.
```

Patch:

```text
Add `conceptual` target status and conceptual anchor_health.
```

Effect:

```text
Agents can distinguish unresolved file anchors from intentional concept anchors.
```

### I05. Broken Pattern Route

Problem:

```text
Source routing referenced `agent-memory-quarantine`, which had no pattern file.
```

Patch:

```text
Replace with `memory-granularity-and-quarantine`.
```

Effect:

```text
Source routing -> Candidate Pattern Bank now closes cleanly.
```

### I06. `outcome_ref` Patch Drift

Problem:

```text
Repeated YAML fields make naive patching easy to misplace.
```

Patch:

```text
Correct misplaced refs and validate outcome_ref resolution.
```

Operating rule:

```text
Patch Project Lens entries only with `### Lens Entry: <id>` block context.
```

### I07. Regex Newline Trap

Problem:

```text
`outcome_ref:\s*(.*)` misread blank outcome_ref as the next line.
```

Patch:

```text
Use line-bounded parsing.
```

## What I Would Keep

```text
Project Lens name
sidecar overlay storage
block-form Lens Entry
kp_ref
structured target_hint
conceptual target status
outcome_ref to candidate snapshots
derived ledger as view only
```

## What I Would Still Not Add

```text
formal Core_KP / Lenses / Snapshots folders
Knowledge Graph Lite fields in Core
Warrant Gate pipeline templates
governance/owner/annual-review automation
Git Notes or DB as primary source
agent auto-confirmed landed/avoid
```

## My Current Architecture Feeling

```text
The flow is now smooth:
external source -> route -> candidate pattern -> Project Lens -> snapshot / gate.
```

The most important thing is that each layer has one job:

```text
Source routing says where a source may route.
Candidate Pattern says what recurring mechanism may be reusable.
Project Lens says how VAKS currently views it.
Snapshot says what happened after actual sandbox/project use.
v0.2.13 warrant gate says whether an action-facing claim is justified.
```

## Remaining Non-Blocking Risks

```text
The repo worktree is extremely dirty, so future commit must be scoped.
Derived views can go stale if the sidecar changes.
Markdown/YAML blocks are readable, but automation must be line-bounded and block-aware.
```

These are operational risks, not blockers for the Project Lens concept.
