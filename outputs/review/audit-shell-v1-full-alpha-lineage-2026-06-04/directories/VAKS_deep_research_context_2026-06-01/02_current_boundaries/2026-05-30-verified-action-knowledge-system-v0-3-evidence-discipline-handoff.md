---
type: handoff
status: active
created: 2026-05-30
project: verified-action-knowledge-system
scope:
  - architecture
  - evidence-discipline
  - v0-3
  - next-window
---

# Verified Action Knowledge System v0.3 Evidence Discipline Handoff

## Working Directory

```text
C:\Users\Administrator\Documents\资料库
```

## Current State

The public spine is unchanged:

```text
Capture -> Understand -> Review -> Connect -> Act and Learn
```

The fixed internal loop remains:

```text
source
-> candidate point
-> calibration / point collision
-> evidence-aware review
-> reviewed node / reviewed relation
-> context pack / action basis
-> action
-> use ledger / feedback / review_due
```

v0.3 adds lazy gates around important candidates, promotions, context packs, and actions:

```text
source_anchor
evidence_packet
warrant / challenge / minimal_revision_needed
coverage_map
evidence_sufficiency
temporal_applicability
context_pack_trace
intent_confirmation
```

These gates do not run for every ordinary capture or ordinary query.

This supplement compresses `outputs/review/2026-05-29-framework-reference-research.md` and the Pro review into small review / evidence / context-pack rules.

## Adopted Alpha Principles

```text
1. Evidence Packet
2. Warrant separation
3. Challenge taxonomy
4. Minimal revision needed
5. Source anchor mini-profile
6. Evidence granularity / escalation
7. Omission check
8. Context pack trace
9. Agent memory quarantine
10. Review due triggers
```

## Boundary

```text
Evidence Packet is review input, not a truth layer.
It is not a formal logic engine.
It is not an automatic truth engine.

source is not evidence by itself
citation is not support by itself
retrieval relation is not reviewed relation
feedback is not truth update
agent memory is not reviewed memory
cache / index / graph / generated wiki are not source of truth
```

## Files Updated

```text
AGENTS.md
ARCHITECTURE_PRINCIPLES.md
FUSION_ARCHITECTURE_V0_2_DRAFT.md
SCHEMA.md
REVIEW_QUEUE.md
SOURCE_INTAKE.md
FEEDBACK.md
templates/review-candidate.md
templates/source-record.md
templates/dev-context-pack.md
templates/feedback-event.md
templates/maintenance-manifest.md
wiki/indexes/knowledge-graph-index.md
raw/articles/2026-05-30-w3c-web-annotation-source.md
raw/papers/2026-05-30-wicer-source.md
outputs/review/2026-05-30-evidence-packet-micro-trial.md
outputs/review/2026-05-30-rka-evidence-packet-source-record-trial.md
outputs/review/2026-05-30-rka-source-code-anchor-review.md
outputs/review/2026-05-30-v0-3-ten-alpha-validation.md
outputs/review/2026-05-30-v0-3-integrated-ten-alpha-trial.md
outputs/review/2026-05-30-v0-3-reference-source-depth-audit.md
00_handoff/2026-05-30-verified-action-knowledge-system-v0-3-evidence-discipline-handoff.md
```

## Next Step

One manual micro-trial has been run:

```text
outputs/review/2026-05-30-evidence-packet-micro-trial.md
```

Result:

```text
Evidence Packet is useful enough to keep as Review Queue input.
It should not become a truth layer.
The first trial validated local contract behavior, not external source truth.
```

What it proved:

```text
Evidence Packet keeps point and evidence span together.
Warrant / scope / challenge become visible.
Omission check exposes source-depth limits.
Context pack trace makes ignored sources explicit.
```

Main limitation:

```text
The trial used local excerpts and local schema rules.
It did not recheck external primary sources or repo implementations.
```

Next trial should use one external primary source or repo source record:

```text
1 source
2-3 candidate points
1 Evidence Packet
1 challenge_kind
1 minimal_revision_needed
1 context_pack_trace
```

The trial should answer:

```text
Does Evidence Packet make review clearer?
Does it stay lightweight?
Does it prevent provenance/citation/retrieval from being mistaken for support?
Does omission_check catch missing risk or scope?
Does context_pack_trace make used/ignored material explainable?
```

Second local-material trial completed:

```text
outputs/review/2026-05-30-rka-evidence-packet-source-record-trial.md
```

Result:

```text
Evidence Packet passed a repo source-record pressure test.
RKA source record is enough for conceptual adoption.
It is not enough for high-confidence code-level proof without exact code anchors.
```

What it proved:

```text
Source record with checked commit can support conceptual adoption with a confidence cap.
Source record without code snippets triggers source_hygiene and needs_full_source_read.
Review queue taxonomy remains optional metadata, not a truth node type.
Decision superseding remains audit flow, not truth mutation.
RKA runtime / MCP / dashboard stays rejected for core adoption.
```

Next possible step, only if code-level support is needed:

```text
Fetch or open the exact checked commit and capture code anchors for:
- rka/models/review_queue.py
- rka/services/decisions.py
- rka/db/migrations/014_add_staleness_and_assumptions.sql
```

RKA exact-commit source-code anchor review completed:

```text
outputs/review/2026-05-30-rka-source-code-anchor-review.md
```

Result:

```text
RKA source code strongly supports the adopted workflow ideas.
It confirms review queue as routing metadata, decision superseding as history-preserving review pressure, staleness versus validity split, outcome calibration as future recommendation tuning, and maintenance checks as structural hygiene.
It does not justify adopting RKA runtime, MCP, dashboard, SQLite truth source, or context rank as trust.
```

Small additional hardening adopted from code review:

```text
decision_outcome now has an explicit precondition:
record the recommendation and user choice, or explicit user override, before recording a final outcome.
```

Full 10-alpha validation completed:

```text
outputs/review/2026-05-30-v0-3-ten-alpha-validation.md
outputs/review/2026-05-30-v0-3-integrated-ten-alpha-trial.md
```

Validation result:

```text
All 10 alpha points are landed at architecture / schema / template level.
They were checked as lazy gates, not new modules.
The integrated trial exercised Evidence Packet, Warrant separation, Challenge taxonomy, Minimal revision needed, Source anchor, Evidence granularity, Omission check, Context pack trace, Agent memory quarantine, and Review due triggers together.
Post-Pro patch fixed schema conformance, evidence_support pressure tests, template weight, Source node confidence leakage, package-visible source record confidence leakage, Source relation example cleanup, RKA trial point_type cleanup, package self-containment, and lazy-gate wording.
```

Reference source-depth audit completed:

```text
outputs/review/2026-05-30-v0-3-reference-source-depth-audit.md
```

Result:

```text
Reference depth is sufficient for v0.3 Pro review after the refreshed package includes the listed source records.
Not every mentioned library was source-code reviewed, intentionally.
Only references that affect schema, review gates, action basis, or truth boundaries require source/code depth now.
```

Code / source depth now recorded:

```text
RKA exact commit:
infinitywings/rka@7bc2d76efba61b92db5b056220f7009763003a0d

Graphiti targeted code anchor:
getzep/graphiti@34f56e65e0fe2096132c8d16f3a1a4ac9300a5f6

New source record for source_anchor:
raw/articles/2026-05-30-w3c-web-annotation-source.md

New source record for omission_check:
raw/papers/2026-05-30-wicer-source.md
```

Boundary:

```text
RKA and Graphiti code anchors support narrow adopted mechanisms only.
They do not justify adopting either runtime.
Watch / parked references are not proof for current v0.3 truth architecture.
Any parked reference must get fresh source/code review before becoming implementation dependency.
```

## Do Not Do By Default

```text
No public README rewrite.
No formal logic engine.
No systematic review workflow.
No GraphRAG / RAG eval / observability platform.
No agent memory platform.
No MCP write tools.
No automation before micro-trial.
No commit / push unless explicitly requested.
```
