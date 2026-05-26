---
type: pattern
status: candidate
source:
  - [[2026-05-26-obsidian-second-brain-source]]
related:
  - [[reference-implementation-extraction-notes]]
confidence: high
adoption_layer: workflow
tags:
  - writeback
  - qa
  - workflow
---

# Two-Output Rule: Answer Plus Knowledge Writeback

## Pattern

Every meaningful AI interaction should produce two outputs:

```text
1. answer to the user
2. durable vault update
```

`obsidian-second-brain` uses this to prevent useful decisions, insights, tasks, and patterns from disappearing after the conversation ends.

## Why It Matters

This directly matches the user's requirement: important reasoning should be written back into files, not left in chat.

For our资料库, the durable output is usually one of:

- `outputs/qa/...`
- `wiki/summaries/...`
- `wiki/patterns/...`
- `wiki/claims/...`
- `wiki/anti-patterns/...`
- `wiki/decisions/...`
- `00_handoff/...`

## Our Adaptation

Use the rule for high-signal analysis turns:

```text
repo analysis
  -> source record
  -> summary
  -> patterns / anti-patterns / claims
  -> QA output
  -> index + handoff update
```

Not every casual answer needs writeback. The trigger is whether the result changes architecture, schema, adoption, or future implementation.

## Risk

If applied to every small chat, the vault fills with noise.

Boundary:

- writeback when it affects architecture, schema, implementation, decision, or reusable pattern
- skip writeback for quick clarifications unless the user asks

