---
type: landed_snapshot_candidate
status: sandbox_landed
created_at: 2026-06-05
project: verified-action-knowledge-system
scope: project-lens-sidecar-agent-maintenance
truth_boundary: sandbox outcome only; not reviewed knowledge; not mainline architecture; not permanent best practice
---

# Landed Snapshot Candidate: Project Lens Sidecar For Agent Maintenance

## What Landed In This Sandbox

Project Lens sidecar became easier for an agent to maintain after two small changes:

```text
1. Add `kp_ref` so each lens entry can point directly to its candidate knowledge point.
2. Split target hint status into `healthy` and `conceptual`, instead of overloading `not_checked`.
```

## Driving Event

During high-intensity retesting, `kp_id` alone forced an agent to infer or search for the candidate pattern file. Also, `not_checked` mixed two different meanings:

```text
not yet checked
conceptual workflow/module target that cannot be file-checked yet
```

## Evidence From Use

Validation after the patch:

```text
lens_entries=10
missing_kp_ref=0
missing_kp_ref_file=0
bad_stance=0
bad_target_status=0
doc_targets=3
doc_missing=0
heading_missing=0
code_anchor_field=false
```

Candidate pattern source chain:

```text
candidate_pattern_files=10
derived_source_refs=42
missing_source_refs=0
```

## Why This Is Useful

For an agent, the sidecar now supports a direct route:

```text
Project Lens entry
-> kp_ref candidate pattern
-> Derived From Sources
-> raw source card / artifact
```

That is faster and less error-prone than searching by name.

## Boundaries

This landed only as sandbox agent-maintenance behavior.

It does not mean:

```text
Project Lens is mainline architecture.
kp_ref is a formal schema field.
candidate patterns are reviewed truth.
target_hint is action basis.
```

## Recommendation

Keep `kp_ref` and `conceptual` status in the Project Lens sandbox. If the same shape stays useful across another real window, promote only the wording rule, not a heavy schema.

