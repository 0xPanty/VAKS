---
type: project_overlay_closeout_note
status: sandbox_sample
created_at: 2026-06-06
truth_boundary: closeout drain sample only; not lifecycle schema; not action basis
source_project: MISA
---

# MISA Closeout Drain Note

## Plain Rule

At project closeout, live overlay entries do not keep floating. They are drained
into a small set of outcomes:

```text
candidate experience note
candidate boundary note
archive
delete + tombstone exception
```

This is a drain note, not a lifecycle state machine.

## Live Sample Count

```text
live_entries_checked: 8
```

## Drain Result

| Entry | Drain Result | Note |
|---|---|---|
| memory-granularity-and-quarantine | candidate experience note | concrete Misa no-effect memory boundary |
| retrieval-is-activation-not-truth | candidate boundary note | hints cannot own control authority |
| graph-and-ontology-as-candidate-context | candidate boundary note | graph carrier cannot own Misa control |
| visual-workbench-for-retrieval-diagnostics | archive | useful, but no standalone cross-project result yet |
| file-first-agent-workbench | archive | already broadly present; no new project-specific result yet |
| skills-and-prompts-as-visible-files | archive | belongs to a later skill-control pass |
| adaptive-retrieval-depth | archive | deferred because current evidence does not need it |
| search-to-analysis-before-answer | archive | action-facing trigger remains v0.2.13, not overlay |

## Candidate Experience Note

```text
candidate_notes/experience/misa-runtime-memory-quarantine-no-effect-gate.md
```

## Candidate Boundary Notes

```text
candidate_notes/boundary/misa-retrieval-hints-not-control-authority.md
candidate_notes/boundary/misa-graph-carrier-not-controller.md
```

## Delete + Tombstone Exception

The old duplicate entry from the prior seven-candidate test should not be kept
live:

```text
adaptive-retrieval-depth-duplicate-vector-priority
```

Reason:

```text
duplicate, vague, low-value, and likely to reintroduce rank-as-authority drift
```

Tombstone behavior:

```text
not in default semantic retrieval
visible only when explicitly auditing deleted overlay leftovers
```

## Carry Forward

No live entry is carried forward as an outcome. If a future Misa skill-control
project needs `skills-and-prompts-as-visible-files`, that project should create
a new overlay entry and optionally link this archive note.

## Supersede

No live overlay entry uses supersede. Supersede is reserved for candidate
experience or candidate boundary notes if a newer note later replaces an older
one.

