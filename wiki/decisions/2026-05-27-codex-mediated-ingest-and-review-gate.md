---
type: decision
status: active
created: 2026-05-27
updated: 2026-05-27
decision: "Adopt Codex-mediated intake and review gate as the default operation model."
decision_scope:
  - ingest
  - review
  - automation-boundary
  - verified-truth-layer
related_projects:
  - verified-action-knowledge-system
based_on:
  - "[[SCHEMA]]"
  - "[[ARCHITECTURE_PRINCIPLES]]"
  - "[[2026-05-27-automated-vault-feedback-loop-review]]"
patterns:
  - "[[frictionless-capture-to-review-inbox]]"
  - "[[daily-brief-as-knowledge-return-loop]]"
  - "[[weekly-synthesis-thesis-and-gap-review]]"
  - "[[review-gated-compile-queue]]"
anti_patterns:
  - "[[automated-brief-as-truth-without-review]]"
  - "[[direct-compile-to-truth-layer-without-review]]"
outcome: adopted
verification_status: active
evidence_level: synthetic
evidence_strength: high
confidence: high
negative_evidence:
  - "Fully automated daily/weekly brief can overstate weak connections if promoted without review."
  - "External agents writing formal wiki nodes directly would bypass the verified truth layer."
replaces:
superseded_by:
migration_path:
  - "Add processing_mode to source records."
  - "Route automatic capture to raw/inbox or source-specific raw folders."
  - "Route daily/weekly synthesis outputs to outputs/review or outputs/qa."
  - "Promote only reviewed candidates into wiki nodes."
rollback_path:
  - "Disable automation and keep manual Codex/user reviewed intake only."
last_verified: 2026-05-27
next_review: 2026-06-03
epistemic_type: decision
gaps:
  - "REVIEW_QUEUE.md is not created yet, so candidate file contract is still pending."
  - "Automation scripts are not implemented yet."
evidence_timeline:
  - date: 2026-05-27
    source: "[[2026-05-27-automated-vault-feedback-loop-review]]"
    observation: "Automated capture and daily/weekly briefs are useful as feedback loops, but unsafe as truth writers."
    effect: refines
    confidence: high
relations:
  - target: "[[SCHEMA]]"
    type: refines
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-27-codex-mediated-ingest-and-review-gate]]"
    rationale: "The decision adds inbox/immediate processing modes to the schema without changing the verified node model."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[ARCHITECTURE_PRINCIPLES]]"
    type: refines
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-27-codex-mediated-ingest-and-review-gate]]"
    rationale: "The decision clarifies that Codex/user review is the default promotion gate for formal wiki nodes."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[automated-brief-as-truth-without-review]]"
    type: risk_of
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-27-codex-mediated-ingest-and-review-gate]]"
    rationale: "Automated briefs are useful only if treated as review candidates, not formal truth."
    created: 2026-05-27
    last_verified: 2026-05-27
tags:
  - decision
  - ingest
  - review-gate
  - codex-mediated
---

# Codex-mediated ingest and review gate

## AI-readable preamble

This decision defines how new material enters the vault.

Automatic systems may capture material, but they do not create verified truth. Codex is the default review and promotion gate, while the user remains final authority.

The goal is low-friction capture without losing the verified knowledge contract.

## Decision

Adopt this default operation model:

```text
automatic capture / user paste / external agent suggestion
-> raw source or raw/inbox
-> Codex review or scheduled candidate generation
-> outputs/review candidate
-> Codex/user promotion
-> formal wiki node
```

## Two Intake Modes

### Inbox mode

Use this for normal capture.

```text
article saved
tweet saved
voice note transcript
quick thought
browser clip
external agent suggestion
```

It lands in `raw/inbox/` or a source-specific raw directory. Later daily/weekly processing may generate review candidates, but not formal truth.

### Immediate mode

Use this when the user explicitly asks for a source to be processed now.

Examples:

```text
提炼这篇
分析这个链接
马上整理
把这篇入库
```

Codex must still preserve the raw source first, then generate summary / claim / pattern / anti-pattern / decision candidates, then promote only what passes review.

## Boundary

Allowed:

```text
automation writes raw captures
automation writes daily/weekly review outputs
Codex writes reviewed formal nodes
user makes final adoption decisions
```

Not allowed:

```text
daily brief directly edits wiki/claims
weekly synthesis directly creates decisions
external agent writes formal wiki nodes
scheduled job resolves contradictions
retrieval result becomes truth
```

## Why

The user intends most intake to happen through Codex. That is useful because it creates a single review gate instead of many uncontrolled writers.

This keeps the system practical:

```text
low friction at capture
strict review at promotion
clear action basis at decision time
```

## Consequences

- `processing_mode: inbox | immediate` should be available on source records.
- Daily brief and weekly synthesis become feedback/review mechanisms.
- `REVIEW_QUEUE.md` should define the candidate record format next.
- Automation can grow, but only behind the raw/review boundary.
