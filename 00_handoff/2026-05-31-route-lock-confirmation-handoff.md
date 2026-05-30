---
type: handoff
status: current
created: 2026-05-31
project: verified-action-knowledge-system
scope:
  - route-lock
  - recovery-state
  - architecture-boundary
mainline_change: route-confirmation-only
---

# Route Lock Confirmation Handoff

## Purpose

This handoff records the current route lock so future windows do not reopen settled architecture questions.

This is a confirmation and recovery note, not a framework rewrite.

## Locked Route

The public architecture spine stays fixed:

```text
Capture -> Understand -> Review -> Connect -> Act and Learn
```

The internal loop stays fixed:

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

## Locked Items

1. Main spine does not change.

2. Internal verified-action loop does not change.

3. Intake uses light / medium / heavy.

```text
light:
  quick capture; no review; no truth creation

medium:
  reusable material; tags/workbench/candidate handling; still no truth creation

heavy:
  strong source or action-relevant material; evidence-aware review can create reviewed knowledge
```

Default rule:

```text
default light
upgrade only when triggered
```

4. Evidence discipline remains a lazy gate.

Strict checks appear for promotion, decision, action basis, strong relation, risk-sensitive answer, conflict, stale/contested claim, or explicit "can we trust this" use.

5. External plugins are not truth authority.

```text
plugin output != reviewed knowledge
retrieval != authority
dashboard != judge
draft != truth
agent memory != reviewed memory
```

6. Automatic compile is parked.

Do not turn AI-generated wiki compilation into reviewed truth or a mainline automation goal.

7. Do not create a new formal two-lane architecture.

`Karpathy-light / VAKS-strict` is allowed as a plain-language explanation only.

It is not a new module tree, folder structure, or replacement route.

## Final Wording

Use this wording when explaining the route:

```text
This is not a dual architecture.
It is one main route + graded intake + lazy evidence gates.
```

Chinese shorthand:

```text
不是双架构。
是一条主路 + 分级入口 + 懒证据闸门。
```

The simplest mental model:

```text
轻中重是门。
主脊椎是路。
证据纪律是关卡。
```

## Parked Topics

Keep these parked unless the user explicitly reopens them:

```text
automatic compile
formal Draft Wiki Lane / Reviewed Action Lane architecture
plugin registry
custom dashboard plugin
Misa write gateway
RAG / Graph runtime as core
agent OS / MCP runtime as core
```

## Recovery Note

The latest accepted mainline remains v0.3 evidence discipline.

This handoff confirms route interpretation only.

Do not modify `SCHEMA.md`, `FUSION_ARCHITECTURE_V0_2_DRAFT.md`, or `ARCHITECTURE_PRINCIPLES.md` from this note alone.

