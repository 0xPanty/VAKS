---
record_kind: retrieval_pilot_workspace
status: candidate
knowledge_status: candidate
project_id: VAKS
created_at: 2026-06-11
action_basis_allowed: false
truth_mutation_allowed: false
---

# VAKS + Yuxi-Like Retrieval Pilot

## Purpose

Test whether adding a Yuxi-like runtime layer helps VAKS retrieval.

This is not a Yuxi deployment. Docker is unavailable on this machine, so this pilot simulates the relevant Yuxi-style retrieval logic locally:

```text
document parsing
chunk anchors
metadata extraction
lexical + vector-like retrieval
RRF fusion
light graph/link expansion
boundary labels as reminders
```

## Test Question

Does a Yuxi-like agent retrieval layer improve VAKS retrieval without needing hard constraints first?

## Compared Modes

```text
T0 baseline:
  file-level lexical retrieval.

T1 yuxi_like_no_labels:
  chunk-level lexical + vector-like retrieval + RRF + graph/link boost.
  No VAKS hard constraints.

T2 yuxi_like_boundary_labels:
  same retrieval as T1, but each result carries VAKS labels:
  knowledge_status, authority_bucket, action_basis_allowed, warning.
```

## Boundary

This sandbox may produce diagnostics and candidate design evidence only.

It does not create reviewed knowledge, action basis, mainline architecture decisions, or production dependencies.

