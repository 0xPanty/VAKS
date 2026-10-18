---
type: source
record_kind: source_card
status: source-captured
title: "Anatoli Kopadze / Loops explained: Claude, GPT, Mira and what actually works"
source_id: x-anatoli-kopadze-loops-explained-2026-06-23
source_uri: local_attachment:62063956-9925-4bb1-abf5-09bd81c42dc5/pasted-text.txt
source_url: unknown
source_type: article_pasted_text
author: "Anatoli Kopadze / @AnatoliKopadze"
publisher: "X / Twitter pasted text"
published_at: unknown
updated_at:
captured_at: 2026-06-23T03:10:50+08:00
captured_by: Codex
version_or_commit:
source_integrity:
  source_hash: 939BDC7966CDACAF8B9EE33B7128287697C06B61DB502ACA7F891EA120509D6E
  snapshot_hash: 939BDC7966CDACAF8B9EE33B7128287697C06B61DB502ACA7F891EA120509D6E
  ingest_state: new
adapter_ingest:
  adapter_name: local-pasted-text-copy
  adapter_version: powershell Copy-Item
  capture_method: "User supplied pasted-text.txt attachment; copied into raw/articles for durable retention."
  extraction_trace: "Local line-number inspection of pasted text; no browser, X account, Mira account, Telegram account, Claude/Codex runtime, or external verification was used."
  known_limits:
    - "The original X post URL was not present in the attachment."
    - "The attachment appears to be copied from an X/Twitter UI and includes embedded repost/video UI fragments."
    - "Claims about Claude Code, Codex, Mira, Composio, app counts, model routing, pricing/cost ranges, codebase migration anecdotes, and product capabilities were not independently verified."
    - "The embedded Peter Steinberger post date appears as 6月8日 without a year in the pasted text."
    - "The Mira section is treated as product/promotion-oriented source material, not verified capability evidence."
source_status: unknown
raw_location: raw/articles/2026-06-23-anatoli-kopadze-loops-explained-source/pasted-text.txt
processing_tier: medium
knowledge_status: raw
overlay_state: none
review_pressure: none
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
review_priority: normal
review_owner: Codex
formalization_status: raw-only
why_saved: "User asked to distill this article/post in the ongoing Loop source-intake cluster; it adds a broad explainer on loop anatomy, when loops are worth building, cost/acceptance metrics, build order, manual self-check loops, and everyday/productized loops."
topics:
  - agentic-loops
  - loop-engineering
  - verify-state-stop
  - cost-per-accepted-change
  - self-checking-loop
  - automation-skill-verifier
  - everyday-loops
projects:
  - verified-action-knowledge-system
source_family:
  - article
  - pasted-text
  - social-post-thread
upstream_sources:
  - "Peter Steinberger / @steipete embedded post excerpt, unverified"
verification_status: source_text_copied_unverified
candidate_relation_suggestions: []
tags:
  - article-intake
  - social-post
  - agentic-loops
  - candidate-only
---

# 来源记录：Anatoli Kopadze / Loops explained

## 为什么收录

用户要求蒸馏这篇文章。它补充了前几条 Loop 源之外的一个更大众但很有用的角度：

```text
什么是 loop
loop 的必要构件是什么
什么时候值得做
什么时候是陷阱
重型 coding loop 成本在哪里
轻量 manual loop 怎么跑
产品化生活 loop 为什么吸引人
```

本记录只保存来源身份、原文快照和初步看点。它不代表 Claude、Codex、Mira、Composio、应用数量、成本、案例结果或产品能力主张已经被 VAKS 验证。

## 来源信息

- 作者：Anatoli Kopadze / `@AnatoliKopadze`
- 发布方：X / Twitter pasted text
- 原始链接：附件未包含
- 原始位置：`C:\Users\Administrator\.codex\attachments\62063956-9925-4bb1-abf5-09bd81c42dc5\pasted-text.txt`
- 资料库保留文本：`raw/articles/2026-06-23-anatoli-kopadze-loops-explained-source/pasted-text.txt`
- source hash：`939BDC7966CDACAF8B9EE33B7128287697C06B61DB502ACA7F891EA120509D6E`
- 采集方式：用户附件原文复制到 `raw/articles/`
- source_status：unknown

## Intake Boundary

```yaml
processing_tier: medium
knowledge_status: raw
overlay_state: none
review_pressure: none
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
```

Source records provide provenance and findability. They must not carry adopt/reject verdicts, truth scores, project borrowing conclusions, or action basis.

## Inspected Text Areas

| Area | Anchor | Why inspected |
|---|---|---|
| One-request habit vs loop | `pasted-text.txt:13-16`, `pasted-text.txt:28-40` | Establishes the article's core definition: loop is goal-driven repeated work with discover/plan/execute/verify/iterate, plus verify/state/stop. |
| Need-a-loop test | `pasted-text.txt:41-47` | Gives four conditions for when a loop is worth building. |
| Coding loop spec | `pasted-text.txt:48-63` | Provides a concrete loop spec with goal, iteration procedure, verify gate, stop condition, and stop summary. |
| Five building blocks | `pasted-text.txt:63-73` | Names automation, skill, sub-agents, connectors, and verifier. |
| Cost and failure mode | `pasted-text.txt:75-84` | Captures context re-read cost, maker/checker cost, cost per accepted change, and silent failure risk. |
| Build order | `pasted-text.txt:85-91` | Captures manual run -> skill -> loop -> schedule. |
| Self-checking light loop | `pasted-text.txt:92-124` | Shows a manual lightweight loop in any LLM and explains what it still lacks. |
| Mira/everyday loop claims | `pasted-text.txt:125-137`, `pasted-text.txt:188-200` | Shows the productized everyday-loop framing and the author's warning not to force loops everywhere. |

## 初步看点

- The strongest source-local insight is the triad: verify, state, stop.
- It gives a practical "do you even need one" filter, which protects VAKS from over-looping ordinary capture.
- It identifies `cost per accepted change` as a better loop metric than raw token spend or loop count.
- It distinguishes heavy engineering loops from light self-checking loops and productized everyday loops.
- It gives a good adoption order: one manual run reliable first, then skill, then loop, then schedule.

## 明显疑点

- The article mixes engineering explanation with Mira product promotion.
- Product and platform claims were not verified.
- "Claude Code and Codex now ship all five" is treated as source wording, not a confirmed current capability statement.
- Cost ranges, fleet examples, app counts, and everyday automation examples are not independent evidence.
- The manual self-checking loop still relies on model self-grading, so it is weaker than external tests or independent verification.

## 可抽取 Candidate Points

- Loop = goal + verify gate + state + stop rule.
- Loop is worth building only for repeated, objectively rejectable, end-to-end automatable tasks.
- Coding loops work first because code has hard gates.
- Five building blocks: automation, skill, sub-agents, connectors, verifier.
- Cost per accepted change is a key loop health metric.
- Build order: manual run -> skill -> loop -> schedule.
- Light self-check loops can help ordinary users, but they are not autonomous background systems.
- Productized everyday loops are useful as UX inspiration, but their claims need separate verification.

## Not Promoted

This source is not promoted to:

```text
wiki/claims
wiki/patterns
wiki/decisions
reviewed knowledge
Evidence Packet
action basis
```

