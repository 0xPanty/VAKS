---
type: next_window_memory_alignment
status: candidate
created_at: 2026-06-05
scope: v0.2.13-structured-action-basis-envelope
project: verified-action-knowledge-system
formalization_status: candidate-only
truth_boundary: not reviewed knowledge, not architecture decision, not action basis
write_scope: outputs/review only
---

# v0.2.13 Next Window Memory Alignment

## Current Candidate Version

The current external-source borrowing / assurance-case borrowing workflow is:

```text
VAKS v0.2.13 candidate
```

This is not a mainline architecture promotion.

Mainline remains:

```text
Fusion Architecture v0.2 Draft
```

v0.2.13 is an `outputs/review` candidate-only upgrade over v0.2.12.

## What Changed From v0.2.12

v0.2.12 core stayed:

```text
Raw Source
-> Source Routing Overlay
-> Candidate Pattern Bank
-> Project Borrowing Ledger
-> Evidence-Aware Review / EtD-lite
-> Decision / Action Basis
```

v0.2.13 adds one lazy internal envelope at the final action/review end:

```text
Decision / Action Basis
-> Structured Action-Basis Envelope, only when triggered
```

The added rule is:

```text
Evidence is not enough; show the warrant.
```

For promotion, significant decision, action-basis use, risk-sensitive answer, strong reviewed relation, or an explicit "is this enough?" question, expose:

```text
claim
evidence anchors
argument / warrant
context / scope / assumptions
challenges / known gaps
residual risk / review status
```

## What Did Not Change

Do not reinterpret v0.2.13 as a new truth layer.

Still true:

```text
URL/source = provenance
raw text = source text
AI summary = candidate comprehension
candidate point = review unit
retrieval/context pack = activation/context preparation
feedback = usefulness/scope-fit pressure, not truth mutation
promotion/action basis = evidence-aware review only
tool/vendor/diagram/source-count/confidence-label = not truth confidence
```

GSN / SACM / CAE are references for organization, not systems to adopt.

```text
Borrow the envelope.
Reject the system conversion.
Keep diagrams optional.
Keep tools discovery-only.
```

## Files To Read First

For a next window, read in this order:

1. `AGENTS.md`
2. `git status --short --branch --untracked-files=all`
3. `outputs/review/2026-06-05-v0-2-13-structured-action-basis-envelope-candidate-patch.md`
4. `outputs/review/2026-06-05-v0-2-13-structured-action-basis-envelope-test.md`
5. `outputs/review/2026-06-05-v0-2-12-gsn-assurance-case-cluster-deep-read.md`
6. `outputs/review/2026-06-05-v0-2-12-next-window-memory-alignment.md`
7. `outputs/review/2026-06-05-cross-project-borrowing-v0-2-12-delta-test.md`

Do not proactively inventory all old intake files.

## Current Disposition

| Item | Disposition |
| --- | --- |
| v0.2.13 candidate patch | accepted for further candidate-only testing |
| structured action-basis envelope | useful, lazy-gated |
| candidate pattern file | not created yet |
| mainline patch | not written |
| Pro review | recommended before promotion |
| real VAKS action-basis example | still needed |
| commit / push | not done |

## Next Best Test

Use one real VAKS decision/action-basis example and force it through the envelope.

Pass condition:

```text
The envelope makes claim/evidence/warrant/scope/challenge clearer
without making ordinary intake heavier
or implying assurance-case system adoption.
```

Fail condition:

```text
It becomes a diagram/schema/process burden,
or starts treating notation/tooling/source-count as truth confidence.
```
