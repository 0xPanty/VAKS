---
type: pattern
status: candidate
source:
  - [[2026-05-26-obsidian-second-brain-source]]
related:
  - [[schema-md-as-ai-wiki-contract]]
  - [[source-verification-and-trust-model]]
confidence: high
adoption_layer: schema
tags:
  - ai-first
  - schema
  - vault-contract
---

# AI-First Vault Operating Contract

## Pattern

Vault notes should not only be readable by humans. They should be structured so a future AI agent can quickly decide:

- what this note is
- why it exists
- when it was created or updated
- which claims are current
- which sources support it
- how confident the system is
- what related nodes it should traverse next

`obsidian-second-brain` implements this with universal frontmatter, a short future-reader preamble, recency markers, source URLs, wikilinks, and confidence markers.

## Why It Matters

Our资料库最终要给 agent 调用。如果笔记只是自然语言散文，未来 agent 每次都要重新理解上下文，容易遗漏来源、时间和不确定性。

AI-first contract 可以把 Markdown 变成可操作的 knowledge record。

## Our Adaptation

不照搬 `## For future Claude` 这个名字，但吸收它的结构：

```text
frontmatter metadata
-> short context preamble
-> current synthesis
-> evidence / claims
-> relations
-> risks / gaps
-> timeline
```

进入 `SCHEMA.md` 的候选字段：

- `type`
- `status`
- `created`
- `updated`
- `source_status`
- `verification_status`
- `evidence_level`
- `confidence`
- `sources`
- `negative_evidence`
- `relations`
- `valid_from`
- `valid_until`
- `last_verified`
- `next_review`

## Risk

AI-first 不等于人类不可读。若 preamble 和 metadata 过重，资料库会变成模板负担。

最小规则是：重要节点必须结构化；临时 source 可以轻量。

