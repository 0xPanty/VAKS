---
type: pattern
status: candidate
source:
  - [[2026-05-26-obsidian-second-brain-source]]
related:
  - [[claude-md-index-md-navigation-layer]]
  - [[verified-vault-api-for-agent-brain]]
confidence: high
adoption_layer: context-pack
tags:
  - context-loading
  - handoff
  - agent
---

# Progressive Vault Context Loader

## Pattern

Do not load the whole vault. Load context by levels.

`obsidian-second-brain` uses `/obsidian-world`:

```text
L0 identity / critical facts
L1 index / operation log
L2 current state / daily / boards
L3 deep context only on demand
```

## Why It Matters

Our资料库会越来越大。新窗口和 future agent 不能靠“全读一遍”恢复上下文。

需要一个固定加载顺序：

```text
purpose.md
SCHEMA.md
knowledge-graph-index.md
architecture decision
latest handoff
active source / claim / pattern / decision nodes
specific raw material only when needed
```

## Our Adaptation

未来 implementation blueprint 应定义：

```text
L0: purpose.md + SCHEMA.md + handoff
L1: indexes + active architecture decision
L2: current working repo/source summaries
L3: raw source snapshots and implementation code
```

This also becomes the shape of future `POST /context-pack`.

## Risk

如果 L0 文件不断膨胀，context loader 会变成新的大 prompt。

Boundary:

- L0 only loads rules and current anchors
- detailed evidence stays linked and pulled on demand

