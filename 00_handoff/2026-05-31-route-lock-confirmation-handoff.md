---
type: handoff
status: current
created: 2026-05-31
updated: 2026-06-01
project: verified-action-knowledge-system
scope:
  - route-lock
  - recovery-state
  - architecture-boundary
  - alpha-minimal-writeback
mainline_change: review-boundary-tightening
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

The latest accepted mainline is v0.3 evidence discipline plus the minimal review-boundary tightening in commit `1eed9e2`.

This handoff confirms route interpretation only.

Do not modify `SCHEMA.md`, `FUSION_ARCHITECTURE_V0_2_DRAFT.md`, or `ARCHITECTURE_PRINCIPLES.md` from this note alone.

## 2026-05-31 Minimal Alpha Writeback

Commit:

```text
1eed9e2 Tighten review and maintenance boundaries
```

Mainline files changed:

```text
REVIEW_QUEUE.md
templates/maintenance-manifest.md
```

What landed:

```text
Approval integrity:
  LLM-assisted labels, prefilled review notes, high agreement, majority vote,
  or human "looks good" approval are review input / review pressure only.
  They do not create evidence review, truth confidence, reviewed relations,
  or automatic promotion.

Known omission check:
  Context-pack, action-basis, risk-sensitive, or explicit sufficiency reviews
  should expose known support, known counterevidence, known gaps, and known
  conflicts. This is review input, not action readiness.

Maintenance report discipline:
  Test, benchmark, fixture, and LLM-judge results are lint / diagnostic input.
  They do not create truth confidence, benchmark authority, runtime readiness,
  mainline readiness, or a new eval/test template family.
```

What stayed untouched:

```text
SCHEMA.md
README.md public five-layer spine
ARCHITECTURE_PRINCIPLES.md
runtime / API / MCP / dashboard
eval platform
agent toolchain
```

Post-writeback documentation sync:

```text
README.md, AGENTS.md, and wiki/indexes/knowledge-graph-index.md were later
updated to mention the accepted boundary tightening for recovery/discovery.
This did not change the public five-layer spine, schema, runtime, eval platform,
or agent toolchain.
```

Sandbox evidence:

```text
triage-compression-2026-05-31/mainline-placement-review/
  MAINLINE_PLACEMENT_REVIEW.md
  PLACEMENT_SCORE_MATRIX.md
  placement_test_report.md
  placement_results.json

triage-compression-2026-05-31/minimal-review-pressure-tests/
  report.md
  results.json
```

Post-writeback checks:

```text
placement test: 160 combinations, recommendation unchanged
pressure tests: 59 passed / 0 failed
git diff --check: passed, with Windows CRLF warnings only
```

## 2026-06-01 Reverse-Audit 2+1 Closeout

Final narrow writeback:

```text
REVIEW_QUEUE.md:
  prior chat memory / agent memory / model background cannot count as current
  source support unless tied to a current source span.

REVIEW_QUEUE.md:
  dynamic data evidence used for promotion or ready action basis needs
  query/filter/subset/as-of/result-set identity.

wiki/anti-patterns/transformed-evidence-as-original-source.md:
  OCR / translation / bbox / layout / table-derived evidence must not masquerade
  as original source support without a recoverable original anchor.
```

Explicitly not landed:

```text
oracle type taxonomy:
  parked / cut because AGENTS.md and templates/maintenance-manifest.md already
  say test, benchmark, fixture, and LLM-judge results are diagnostic lint only.
```

Untouched:

```text
SCHEMA.md
README.md public spine
runtime / API / MCP / dashboard
eval platform
agent toolchain
```
