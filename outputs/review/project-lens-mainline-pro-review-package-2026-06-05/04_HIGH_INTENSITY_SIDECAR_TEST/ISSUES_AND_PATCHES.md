---
type: issues_and_patches
status: active
created_at: 2026-06-05
project: verified-action-knowledge-system
scope: project-lens-pressure-test-issue-log
truth_boundary: sandbox issue log only; not reviewed knowledge
---

# Issues And Patches

## Issue Log

### I01: Markdown Wide Table Does Not Scale

Status:

```text
fixed_in_candidate_sidecar
```

Finding:

```text
The original Project Lens sidecar used a wide Markdown table.
It was compact but hard to read in Obsidian and brittle for long text.
```

Patch:

```text
Changed outputs/review/project_lens_overlays/VAKS.md to one Lens Entry block per kp_id.
Each block uses a small YAML-like field set.
```

Residual risk:

```text
If the file grows beyond 50-100 entries, consider a JSONL materialized index or one file per project/lane.
Do not make JSONL the only human-facing source yet.
```

### I02: Anchor Health Was Too Coarse

Status:

```text
fixed_in_candidate_sidecar
```

Finding:

```text
The first block-form sidecar left every entry as anchor_health: pattern_id_only.
That was too vague because several target_hint values already pointed to concrete docs.
```

Patch:

```text
Checked doc:SOURCE_INTAKE.md and doc:MEMORY_TIER.md#Activation Tier.
Concrete checked doc anchors now use anchor_health: healthy.
Pure module/workflow hints now use anchor_health: conceptual instead of pretending to be file-checkable.
```

Residual risk:

```text
Future module/workflow hints need a lightweight registry or periodic anchor-health check if they become action-facing.
Do not build that registry before repeated use proves the need.
```

### I03: `kp_id` Was Not Enough For Agent Navigation

Status:

```text
fixed_in_candidate_sidecar
```

Finding:

```text
`kp_id` identified the idea but did not give the agent a direct path back to the candidate pattern file.
```

Patch:

```text
Added `kp_ref` to every Lens Entry.
```

Residual risk:

```text
If future Core KP files replace candidate pattern files, kp_ref must be updated rather than left stale.
```

### I04: `not_checked` Was Overloaded

Status:

```text
fixed_in_candidate_sidecar
```

Finding:

```text
`not_checked` mixed unchecked file anchors with conceptual workflow/module hints.
```

Patch:

```text
Added `conceptual` target status and conceptual anchor_health.
```

Residual risk:

```text
Conceptual hints are useful for routing but should not be treated as verified engineering anchors.
```

### I05: Source Routing Had A Broken Pattern Route

Status:

```text
fixed_in_source_routing
```

Finding:

```text
`agent-memory-quarantine` was referenced but no matching candidate pattern file existed.
```

Patch:

```text
Replaced it with `memory-granularity-and-quarantine`.
```

Residual risk:

```text
Future source routing tables need a route-to-pattern existence check.
```

### I06: `outcome_ref` Patch Drift

Status:

```text
mitigated
```

Finding:

```text
Repeated YAML fields can be patched into the wrong Lens Entry if the patch lacks block context.
```

Patch:

```text
Corrected misplaced refs and validated outcome_ref paths.
```

Residual risk:

```text
Future edits must patch by `### Lens Entry: <id>` block context.
```

### I07: Regex Newline Trap

Status:

```text
mitigated
```

Finding:

```text
Naive `\s*` parsing can consume a newline and misread the next field as the current field.
```

Patch:

```text
Use line-bounded parsing for Lens Entry validation.
```

Residual risk:

```text
If automation grows, use a structured parser or generated JSONL index instead of ad hoc regex.
```
