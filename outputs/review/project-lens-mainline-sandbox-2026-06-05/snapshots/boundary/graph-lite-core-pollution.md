---
type: boundary_snapshot_candidate
status: sandbox_boundary
created_at: 2026-06-05
project: verified-action-knowledge-system
scope: graph-lite-and-core-pollution
truth_boundary: sandbox negative-knowledge candidate only; not reviewed knowledge; not mainline architecture
---

# Boundary Snapshot Candidate: Graph Lite Pollutes Core Too Early

## Trap Title

Putting navigation relations into the Core layer before they are reviewed.

## Bad Move Or Non-Fit

Adding fields such as `related_kp`, `depends_on`, or `conflicts_with` to Atomic Knowledge Core as if they were stable reviewed relations.

## Failure Context

This surfaced while testing Grok's Knowledge Graph Lite suggestion.

The suggestion is useful for navigation, but dangerous if written into Core before the relation is reviewed.

## Trigger Conditions

```text
An agent wants faster navigation between knowledge points.
Multiple Project Lens entries mention the same module/workflow.
Candidate pattern reuse count looks high.
Graph View looks persuasive in Obsidian.
```

## Why It Failed

Navigation relations are useful, but Core is supposed to remain project-clean and evidence-disciplined. If a candidate relation is written into Core too early, later agents may treat it as reviewed structure.

## Boundary Of Applicability

Applies to:

```text
Core KP fields
reviewed relation promotion
Candidate Pattern Bank cross-links
Project Lens depends/conflicts ideas
Obsidian graph links that look authoritative
```

## Similar Keywords

```text
related_kp
depends_on
conflicts_with
knowledge graph lite
graph view
relation neighborhood
candidate context
```

## Warning One-Liner

Use graph links to navigate candidates; do not let them impersonate reviewed relations.

## Safer Alternative Or Escalation

Use ordinary Markdown links or sandbox notes first. Promote relation fields only after a reviewed relation rule exists and the relation has evidence support.

## Evidence Refs

```text
outputs/review/project-lens-mainline-sandbox-2026-06-05/GROK_RECOMMENDATION_TRIAGE.md
outputs/review/project-lens-mainline-sandbox-2026-06-05/AGENT_EXPERIENCE_VALUE_REPORT.md
outputs/review/candidate_pattern_bank/graph-and-ontology-as-candidate-context.md
```
