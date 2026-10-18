---
type: full_mainline_copy_insertion_test_report
status: pass_as_full_copy_sandbox
created_at: 2026-06-05
project: verified-action-knowledge-system
scope: project-lens-full-mainline-copy-insertion
truth_boundary: sandbox test report only; not reviewed knowledge; not mainline architecture; not commit authority
---

# Full Mainline Copy Insertion Test Report

## Verdict

```yaml
verdict: pass_as_full_copy_sandbox
mainline_merge_authorized: no
commit_authorized: no
push_authorized: no
```

Human-readable:

```text
Project Lens can be inserted into complete copies of the two main architecture docs without breaking the surrounding architecture logic.
The test supports viability of a minimal mainline paragraph.
It does not by itself authorize changing the real mainline files.
```

## What Was Tested

Complete copies were made:

```text
FUSION_ARCHITECTURE_V0_2_DRAFT.md
ARCHITECTURE_PRINCIPLES.md
```

Two versions exist:

```text
baseline/
with-project-lens/
```

The baseline copies match the current root files:

```text
FUSION root vs baseline: true
ARCHITECTURE_PRINCIPLES root vs baseline: true
```

## Insertions

### FUSION_ARCHITECTURE_V0_2_DRAFT.md

Insertion locations:

```text
line 81: Project Lens in Current controlling interpretation
line 725: Project Lens Sidecar between Dev Context and Context Pack / Action Basis
```

Line delta:

```text
baseline_lines=3408
patched_lines=3455
added_lines=47
deleted_lines=0
```

### ARCHITECTURE_PRINCIPLES.md

Insertion location:

```text
line 249: 3.3.3 Project Lens is a sidecar, not project truth
```

Line delta:

```text
baseline_lines=785
patched_lines=804
added_lines=19
deleted_lines=0
```

## Boundary Checks

The inserted wording explicitly says Project Lens is:

```text
optional
project-scoped
sidecar overlay
development-time reuse context
not reviewed knowledge
not ADR
not action basis
not truth confidence
not schema
not template
not permanent project status
```

It also preserves the v0.2.13 trigger:

```text
When a lens item is used for significant promotion, decision, architecture absorption, action basis, or risk-sensitive answer, evidence is not enough; show the non-circular warrant.
```

## Mechanical Test Results

```text
root FUSION vs baseline hash_match: true
root ARCHITECTURE_PRINCIPLES vs baseline hash_match: true
Project Lens terms in patched copies: present
Project Lens terms in root mainline docs: absent
SCHEMA.md diff: none
REVIEW_QUEUE.md diff: none
templates diff: none
staged files: none
```

No formal folders were created:

```text
Core_KP: false
Lenses: false
Snapshots: false
outputs/review/Core_KP: false
outputs/review/Lenses: false
outputs/review/Snapshots: false
```

## Semantic Consistency Results

```yaml
source_card_boundary_preserved: yes
candidate_pattern_boundary_preserved: yes
project_lens_not_truth: yes
project_lens_not_adr: yes
project_lens_not_action_basis: yes
ordinary_intake_stays_light: yes
v0_2_13_trigger_preserved: yes
schema_template_expansion: no
formal_workspace_directory: no
```

## Remaining Decision

The test changes the status from:

```text
not yet tested as full mainline copy insertion
```

to:

```text
full mainline copy insertion sandbox passed
```

But the remaining decision is still explicit:

```text
Should the user approve applying a minimal Project Lens paragraph to the real mainline docs?
```

