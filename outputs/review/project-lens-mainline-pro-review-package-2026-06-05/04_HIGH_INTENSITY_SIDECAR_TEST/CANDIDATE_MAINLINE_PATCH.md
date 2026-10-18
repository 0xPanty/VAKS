---
type: candidate_mainline_patch
status: sandbox_only
created_at: 2026-06-05
project: verified-action-knowledge-system
scope: project-lens-mainline-candidate-wording
truth_boundary: sandbox candidate wording only; not applied to mainline; not reviewed knowledge
---

# Candidate Mainline Patch: Project Lens

## Important

This is a simulated patch only.

It has not been applied to:

```text
FUSION_ARCHITECTURE_V0_2_DRAFT.md
ARCHITECTURE_PRINCIPLES.md
SCHEMA.md
REVIEW_QUEUE.md
templates/
```

## Candidate Placement

If Project Lens ever graduates, it should be a small paragraph near the existing activation / context-pack / action-facing review boundary, not a new schema or template family.

## Candidate Wording

```text
Project Lens is an optional, project-scoped sidecar overlay for development-time reuse.
It may attach a temporary project stance to a generic knowledge point without modifying that point.
It records possible borrow scope, non-borrow scope when needed, target hints, and a one-line reason.
It is not reviewed knowledge, ADR, action basis, truth confidence, or permanent project status.
Landed or failed outcomes are recorded separately through landed_snapshot or boundary_snapshot only after real project evidence or review.
When a lens item is used for significant promotion, decision, architecture absorption, or action basis, it must pass the late-stage action-facing review requirement:
evidence is not enough; show the non-circular warrant.
```

## Candidate Guardrail

```text
Do not write Project Lens fields into generic knowledge point YAML or body.
Do not treat stance, reuse count, project count, dashboard output, retrieval score, GraphRAG summary, AI summary, or source count as support strength.
Do not let Source Card project routes become adopt/reject decisions.
Do not let Project Lens become a lightweight ADR.
```

## Candidate Non-Goals

```text
No new schema now.
No new template now.
No formal development workspace directory now.
No database source of truth now.
No automatic AI adoption / rejection / landed / boundary confirmation.
No all-intake-heavy workflow.
```

## Open Question Before Mainline

```text
Should the user explicitly approve this candidate wording as a mainline architecture rule?
Can block-form sidecars stay readable and parseable at 50+ entries?
Can module/workflow conceptual targets remain useful without a registry?
Can any future commit be scoped safely in the currently very dirty worktree?
```

## High-Intensity Sandbox Update

```text
Current candidate sidecar passed high-intensity testing after patches.
No blocking issue remains in the sandbox concept.
Mainline merge is not automatic; it remains a user decision.
```
