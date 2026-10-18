---
type: boundary_snapshot_candidate
status: sandbox_boundary
created_at: 2026-06-05
project: verified-action-knowledge-system
scope: retrieval-activation-vs-evidence-support
truth_boundary: sandbox negative-knowledge candidate only; not reviewed knowledge; not mainline architecture
---

# Boundary Snapshot Candidate: Retrieval Score Is Not Support

## Trap Title

Retrieval score treated as evidence support.

## Bad Move Or Non-Fit

Using retrieval hit, rerank position, GraphRAG community summary, dashboard pass, or feedback heat as truth confidence or action readiness.

## Failure Context

This can appear in:

```text
context-pack preparation
RAG / GraphRAG diagnostics
source routing
candidate pattern reuse
Project Lens stance assignment
```

## Trigger Conditions

```text
A result is called "supported" because it was retrieved or ranked highly.
A dashboard or RAG evaluation score is cited as action readiness.
A community summary or graph hit is treated as a reviewed relation.
A Project Lens stance is treated as proof that VAKS should act.
```

## Why It Failed

Retrieval can bring material into view, but it does not:

```text
check whether evidence supports a specific claim
test scope and assumptions
surface known challenges / gaps
provide a non-circular warrant
create reviewed relations
```

## Boundary Of Applicability

Applies whenever VAKS output is used for:

```text
reviewed knowledge
strong relation promotion
architecture absorption
action basis
risk-sensitive answer
```

## Similar Keywords

```text
retrieval score
rerank
RAGAS
GraphRAG summary
community report
dashboard pass
hit count
feedback heat
```

## Warning One-Liner

Retrieval can bring material into view; it cannot make the material true.

## Safer Alternative Or Escalation

Treat retrieval/rerank/dashboard signals as activation or diagnosis only. If the result becomes action-facing, run the v0.2.13 warrant gate.

## Evidence Refs

```text
outputs/review/project_lens_overlays/VAKS.md
outputs/review/candidate_pattern_bank/retrieval-is-activation-not-truth.md
outputs/review/2026-06-05-v0-2-13-usage-guide.md
outputs/review/project-lens-mainline-sandbox-2026-06-05/REAL_CASE_TRIALS.md
```

