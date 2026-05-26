---
type: anti-pattern
status: active
source:
  - [[2026-05-26-obsidian-second-brain-source]]
related:
  - [[copying-full-second-brain-runtime-before-schema-stabilizes]]
confidence: high
tags:
  - anti-pattern
  - automation
  - schema
---

# Automatic Agentic Vault Rewrite Before Schema Stability

## Anti-Pattern

Enabling scheduled agents, background agents, automatic ingest rewrite, and automatic conflict resolution before the vault schema is stable.

## Why It Is Dangerous

This creates hidden drift:

- old pages get rewritten before source/claim boundaries are clear
- facts, opinions, decisions, and guesses can merge
- contradictions may be "resolved" without enough evidence
- useful negative evidence may disappear into a rewritten synthesis
- the system looks smarter while becoming harder to audit

## Where It Appears

`obsidian-second-brain` intentionally pushes toward a self-rewriting vault with background/scheduled maintenance. That is powerful for mature personal workflows, but too aggressive for our current architecture design stage.

## Our Boundary

Before automation:

```text
SCHEMA.md stable
templates stable
manual propagation tested
health check reports only
diff review habit established
candidate -> accepted gate defined
```

Allowed now:

- manual source analysis
- manual pattern/claim extraction
- manual index/handoff update
- source snapshots
- health-check design

Not allowed now:

- background rewrite
- scheduled reconciliation
- auto-accept decisions
- auto-delete or auto-merge
- agent-owned truth resolution

