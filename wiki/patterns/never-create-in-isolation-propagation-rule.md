---
type: pattern
status: candidate
source:
  - [[2026-05-26-obsidian-second-brain-source]]
related:
  - [[provenance-safe-source-lifecycle]]
  - [[async-review-queue-for-ai-ingest]]
confidence: high
adoption_layer: workflow
tags:
  - propagation
  - workflow
  - graph-health
---

# Never Create In Isolation Propagation Rule

## Pattern

Every write should ask: what else must know about this change?

`obsidian-second-brain` treats isolated notes as vault rot. Creating or updating a project, person, task, decision, or source should update the relevant indexes, logs, daily notes, boards, and related entity pages.

## Why It Matters

Our资料库如果只新增文件，很快会出现：

- source 没有 summary
- summary 没有 claim
- claim 没有 pattern
- pattern 没有 evidence
- decision 没有反例
- output 没有回链

这不是知识系统，只是文件堆。

## Our Adaptation

写入传播规则应进入 `SCHEMA.md` 或 implementation blueprint：

```text
new raw source
  -> source record
  -> summary candidate
  -> extracted claims
  -> candidate patterns / anti-patterns
  -> index update
  -> QA output if there was user-facing analysis
  -> operation log
```

```text
new pattern
  -> supporting sources
  -> contradicting sources if any
  -> related patterns
  -> risks
  -> adoption status
  -> index update
```

```text
new decision
  -> accepted/rejected alternatives
  -> evidence timeline
  -> confidence
  -> review date
  -> supersedes/replaces links
```

## Risk

Propagation can become noisy if every tiny note updates many files.

Boundary:

- high-signal source / claim / pattern / decision must propagate
- low-value inbox capture can stay unpropagated until review

