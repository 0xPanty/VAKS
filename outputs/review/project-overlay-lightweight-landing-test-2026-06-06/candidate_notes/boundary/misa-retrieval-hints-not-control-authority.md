---
type: candidate_boundary_note
status: sandbox_sample
created_at: 2026-06-06
truth_boundary: candidate boundary only; not universal ban; not action basis
source_project: MISA
---

# Candidate Boundary: Misa Retrieval Hints Are Not Control Authority

## Scope

This note records a boundary observed in the Misa pressure sample.

It applies to Misa-like systems where diagnostic, retrieval, ranker, or digest
outputs may be close to project control surfaces.

## Boundary

Misa may use retrieval and diagnostic outputs as hints, but those hints must not
own route mutation, repair triggering, or project control authority.

## Applicability

Use this note only when:

- The project has retrieval, vector rank, digest, or diagnostic outputs.
- Those outputs are near a control surface.
- The project has not passed a separate action-facing review for the proposed
  control behavior.

## Anchors

```text
C:\Users\Administrator\Documents\New project\misa-cybernetic-evolution\scripts\lib\perception-sidecar.mjs
C:\Users\Administrator\Documents\New project\misa-cybernetic-evolution\scripts\lib\component-health.mjs
C:\Users\Administrator\Documents\New project\misa-cybernetic-evolution\CONTROL_CONTRACT.md
```

## Boundary Of This Boundary

This is not a general ban on retrieval or diagnostics. It only says they cannot
replace action-facing review when control behavior is at stake.

