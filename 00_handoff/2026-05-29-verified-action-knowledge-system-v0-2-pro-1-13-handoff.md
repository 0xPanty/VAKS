---
type: handoff
status: active
created: 2026-05-29
project: verified-action-knowledge-system
scope:
  - architecture
  - pro-review
  - supplements-1-13.3
  - next-window
---

# Verified Action Knowledge System v0.2 - Pro 1-13.3 Handoff

## Working Directory

```text
C:\Users\Administrator\Documents\资料库
```

## Current State

Pro supplements 1-13.3 have been reviewed and written back into the architecture files.

The public spine remains:

```text
Capture -> Understand -> Review -> Connect -> Act and Learn
```

The internal loop remains:

```text
source
-> candidate point
-> calibration / point collision
-> review
-> reviewed node / reviewed relation
-> context pack / action basis
   with coverage_map / evidence_sufficiency when action-ready or high-impact
-> action
-> use ledger / feedback
```

Main controlling principle:

```text
Strict checks are lazy gates.

Capture stays light.
Ordinary query stays simple.
Promotion gets strict.
Action basis gets auditable.
Feedback improves activation, not truth.
```

## Supplement 13 Landed

13. RKA Review Queue / Decision Superseding
   - RKA source later identified as `infinitywings/rka`.
   - Absorbed as review / action guardrails only, not as runtime architecture.
   - Review queue item types:
     - low_confidence_claim
     - contradiction
     - missing_evidence
     - synthesis_needed
     - decision_superseded
   - Queue actions are workflow resolutions, not truth changes.
   - Decision superseding keeps the old decision, links the replacement, and marks affected downstream claims / patterns / relations / context packs review_due.
   - Additional RKA-inspired points landed:
     - intent confirmation / backbrief for significant action
     - verbatim user input vs model interpretation
     - maintenance manifest / lint queue
     - stale vs valid_until distinction
     - confidence cap without full text
     - decision outcome calibration
   - Full runtime, MCP, dashboard, or automatic workflow authority were not adopted.

## Source Status

Evidence Sufficiency Gate sources are present and should be included in the review bundle:

```text
Self-RAG source record: raw/papers/2026-05-29-self-rag-source.md
CRAG source record: raw/papers/2026-05-29-crag-source.md
A2RAG source record: raw/papers/2026-05-29-a2rag-source.md
```

The RKA source identity and checked commit are recorded:

```text
https://github.com/infinitywings/rka
checked commit: 7bc2d76efba61b92db5b056220f7009763003a0d
source record: raw/repos/2026-05-29-rka-source.md
```

GraphRAG / LightRAG sources captured:

```text
GraphRAG docs: https://microsoft.github.io/graphrag/index/default_dataflow/
GraphRAG repo: https://github.com/microsoft/graphrag
source record: raw/repos/2026-05-29-graphrag-source.md

LightRAG paper: https://arxiv.org/abs/2410.05779
LightRAG repo: https://github.com/HKUDS/LightRAG
source record: raw/papers/2026-05-29-lightrag-source.md
```

## Supplement 13.3 Landed

13.3. GraphRAG / LightRAG Graph Retrieval Stratification
   - Absorbed as retrieval / activation / context-pack preparation only.
   - Low-level retrieval:
     - source
     - text unit
     - claim
     - entity
   - High-level retrieval:
     - pattern
     - theme
     - community
     - community report
   - Relation-neighborhood retrieval:
     - reviewed relation neighborhood around the query seed
     - candidate_relation_neighborhood when traversal uses candidate relations
   - TextUnit anchors are provenance, not support.
   - Community reports are briefings, not truth.
   - Graph rank is retrieval priority, not trust.
   - Auto-extracted relations are candidate material, not reviewed relations.
   - No GraphRAG / LightRAG runtime, graph extraction authority, or automatic truth update was adopted.

## Files Updated In Supplements 13-13.3

```text
AGENTS.md
README.md
ARCHITECTURE_PRINCIPLES.md
FUSION_ARCHITECTURE_V0_2_DRAFT.md
SCHEMA.md
SECOND_BRAIN_MODEL.md
SOURCE_INTAKE.md
REVIEW_QUEUE.md
templates/decision-record.md
templates/dev-context-pack.md
templates/feedback-event.md
templates/maintenance-manifest.md
templates/query-run.md
templates/review-candidate.md
wiki/indexes/knowledge-graph-index.md
raw/repos/2026-05-29-rka-source.md
raw/repos/2026-05-29-graphrag-source.md
raw/papers/2026-05-29-lightrag-source.md
00_handoff/2026-05-29-verified-action-knowledge-system-v0-2-pro-1-13-handoff.md
```

## Next Review

Give Pro the supplement 1-13.3 bundle and ask specifically:

```text
Does the review_queue_item taxonomy help without creating a parallel truth node type?
Are approve / reject / merge / override clearly workflow actions, not truth changes?
Does decision_superseded preserve audit trail and scope boundaries?
Do affected downstream claims / patterns / relations / context packs become review_due instead of being silently changed?
Are intent confirmation, backbrief, and maintenance manifest clearly lazy gates?
Does decision outcome calibration improve future recommendations without changing truth?
Does graph retrieval stratification improve context-pack preparation without creating a retrieval truth layer?
Are community reports, graph rank, and auto-extracted relations clearly barred from truth/support/confidence/reviewed relation status?
Does the main spine remain unchanged?
```

## Do Not Do By Default

```text
No automation.
No API/MCP/viewer implementation.
No dev context pack trial unless explicitly requested.
No commit/push except when explicitly requested.
No source record promotion without review.
```
