---
bundle: VAKS_deep_research_context_2026-06-01
purpose: external-research-brief
status: handoff
main_vault_write: false
schema_change_requested: false
final_decision_requested: false
---

# Read First: VAKS Deep Research Context

## 2026-06-01 Current Use Note

This file began as the external Deep Research intake brief for the first audit-noise investigation. The package now also contains downstream work from that research:

```text
09_external_research_intake/
10_alpha_noise_test/
11_audit_shell_v1_followup/
12_audit_shell_v1_pilot/
13_pro_review_feedback/
14_audit_shell_v1_adversarial_96/
```

For a new Codex/Pro window, read this file for the original research objective, but use this newer recovery file for the current state and exact next step:

```text
00_READ_FIRST/NEXT_WINDOW_RECOVERY_FULL_GRAIN.md
```

Current latest state:

```text
audit shell v1 passed a 96-case adversarial fixture patch
main vault remains unchanged by audit-shell work
SCHEMA remains untouched
the next decision is Pro review, then possible 480 real-data paired pilot
```

## What This Bundle Is

This bundle is context for an external Deep Research pass.

The goal is not to redesign VAKS.

The goal is to research whether existing papers, libraries, standards, or product patterns can help with four pain points found in the first real VAKS end-to-end trial.

## VAKS In One Paragraph

VAKS means Verified Action Knowledge System.

Public story:

```text
Capture -> Understand -> Review -> Connect -> Act and Learn
```

Internal loop:

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

Core boundary:

```text
provenance is not support
support is not truth
reviewed knowledge is not automatically action-ready
feedback changes activation/scope-fit, not truth
strict checks are lazy gates
```

## Current Status

The first real manual E2E trial was run in sandbox using four real papers:

```text
ALCE
Attributed QA
GopherCite
FRONT
```

The full spine ran:

```text
raw source
-> candidate
-> manual review
-> wiki claim
-> context pack
-> feedback
```

The architecture did not collapse. The pain is operational friction.

## Current Pain Points To Research

Research only these four pain points:

1. Source independence is unclear.

```text
Multiple sources may support the same point, but they may share origin,
cite the same upstream work, belong to the same research family, or copy each other.
We do not want source count to masquerade as independent support.
```

2. `processing_level` vs `source_access` is easy to confuse.

```text
A source may be important enough for heavy processing,
while the actual evidence access may be abstract_only or snippet_only.
The trial showed these concepts need clearer separation.
```

3. `coverage_map` is too heavy.

```text
Coverage maps are valuable for action basis and high-risk answers,
but full coverage rows are too much for every ordinary design answer.
We need progressive disclosure or minimal coverage patterns.
```

4. No runtime means activation change is manually recorded.

```text
Feedback should change activation and scope-fit, not truth.
But without runtime, activation change is only a before/after query-run note.
We need lightweight, auditable activation logging ideas for future runtime.
```

## What To Avoid

Do not recommend:

```text
new truth core
schema rewrite
full graph database migration
runtime platform as immediate fix
LLM judge as truth
benchmark pass as truth
retrieval score as confidence
source count as independence
automatic promotion
automatic truth update from feedback
```

## Desired Research Output

For each of the four pain points, find candidate mechanisms from primary sources:

```text
papers
official docs
standards
open-source repos
well-documented product patterns
```

For each candidate, provide:

```text
1. name / link
2. which pain point it addresses
3. key mechanism
4. smallest design VAKS could borrow
5. what VAKS should not absorb
6. whether it requires schema change: yes/no, prefer no
7. possible landing place:
   - operation convention
   - review-lite
   - anti-pattern
   - future runtime
   - parked
8. risk
```

End with a table:

```text
pain point | external reference | borrowable mechanism | adoption degree | schema change? | suitable now?
```

Do not make final architecture decisions. Give researched candidates and evidence.

## Reading Order

1. `08_research_prompt/DEEP_RESEARCH_PROMPT.md`
2. `06_e2e_trial/PAIN_REPORT.md`
3. `06_e2e_trial/lightweight-variant/LIGHTWEIGHT_PATH_COMPARISON.md`
4. `01_main_architecture/AGENTS.md`
5. `02_current_boundaries/2026-05-31-route-lock-confirmation-handoff.md`
6. `01_main_architecture/REVIEW_QUEUE.md`
7. `01_main_architecture/SOURCE_INTAKE.md`
8. `01_main_architecture/SCHEMA.md`
9. `01_main_architecture/FEEDBACK.md`
10. `04_indexes/knowledge-graph-index.md`

Use the rest as needed.
