---
type: source
record_kind: source_card
status: source-captured
title: "0xJeff / The Hermes Sensei Loop"
source_id: x-0xjeff-hermes-sensei-loop-2026-06-23
source_uri: local_attachment:030edce6-df18-4128-ae65-0087678cb0b8/pasted-text.txt
source_url: unknown
source_type: article_pasted_text
author: "0xJeff / @0xJeff"
publisher: "X / Twitter pasted text; Teknium repost context included in attachment"
published_at: unknown
updated_at:
captured_at: 2026-06-23T03:07:06+08:00
captured_by: Codex
version_or_commit:
source_integrity:
  source_hash: DA2DEAD629955F928CBA56C917533231C2B928DD2394C7EEE3775447CE89A933
  snapshot_hash: DA2DEAD629955F928CBA56C917533231C2B928DD2394C7EEE3775447CE89A933
  ingest_state: new
adapter_ingest:
  adapter_name: local-pasted-text-copy
  adapter_version: powershell Copy-Item
  capture_method: "User supplied pasted-text.txt attachment; copied into raw/articles for durable retention."
  extraction_trace: "Local line-number inspection of pasted text; no browser, X account, Hermes account, Loop Library page, or external verification was used."
  known_limits:
    - "The original X post URL was not present in the attachment."
    - "The attachment appears to be copied from an X/Twitter UI and includes UI fragments."
    - "Hermes product behavior, Matthew Berman Loop Library details, cron behavior, scores, and workflow outcomes were not independently verified."
    - "The embedded Matthew Berman post date appears as 6月19日 without a year in the pasted text."
    - "This source is treated as social-post / article-style orientation, not evidence support."
source_status: unknown
raw_location: raw/articles/2026-06-23-0xjeff-hermes-sensei-loop-source/pasted-text.txt
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
why_saved: "User asked to distill this Hermes Sensei Loop article/post after several loop-engineering intakes; it adds a research-agent loop pattern centered on Champion Loop holdout promotion, Feedback Sweep, research cron quality, and adversarial thesis stress testing."
topics:
  - agentic-loops
  - hermes
  - research-agents
  - champion-loop
  - holdout-promotion
  - feedback-sweep
  - research-crons
projects:
  - verified-action-knowledge-system
source_family:
  - article
  - pasted-text
  - social-post-thread
upstream_sources:
  - "Matthew Berman / Loop Library embedded post excerpt, unverified"
verification_status: source_text_copied_unverified
candidate_relation_suggestions: []
tags:
  - article-intake
  - social-post
  - agentic-loops
  - candidate-only
---

# 来源记录：0xJeff / The Hermes Sensei Loop

## 为什么收录

用户要求蒸馏这篇文章。它补充了前几条 Loop 源之外的一个新角度：

```text
不是 coding loop
而是 research cron / research agent loop
```

文章核心是：Hermes 类研究代理的日常 cron 会出现输出变 stale、AI 过度顺从、缺少 adversarial review、缺少 thesis stress test、依赖人类反馈才能改进的问题。作者借用 Loop Library 中的两个 loop：

```text
Self-Improving Champion Loop
Feedback Sweep Loop
```

本记录只保存来源身份、原文快照和初步看点。它不代表 Hermes 产品能力、Loop Library 数量、作者工作流结果、holdout 分数或投资/交易结论已经被 VAKS 验证。

## 来源信息

- 作者：0xJeff / `@0xJeff`
- 发布方：X / Twitter pasted text；附件中带 Teknium repost UI 片段
- 原始链接：附件未包含
- 原始位置：`C:\Users\Administrator\.codex\attachments\030edce6-df18-4128-ae65-0087678cb0b8\pasted-text.txt`
- 资料库保留文本：`raw/articles/2026-06-23-0xjeff-hermes-sensei-loop-source/pasted-text.txt`
- source hash：`DA2DEAD629955F928CBA56C917533231C2B928DD2394C7EEE3775447CE89A933`
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
| Problem framing | `pasted-text.txt:9-17` | Establishes the article's problem: agentic crons learn from human feedback but still lack adversarial review and thesis stress tests. |
| Research-loop goals | `pasted-text.txt:19-22` | Captures the target use case: improve research cron quality, validate/invalidate theses, and make the agent more autonomous. |
| Champion Loop | `pasted-text.txt:36-52` | Defines champion/challenger prompt improvement with holdout promotion and must-pass rules. |
| Overfit warning | `pasted-text.txt:53-59` | Gives the strongest intuition: never promote on the same examples used for editing. |
| Feedback Sweep | `pasted-text.txt:60-62` | Defines feedback collection as input to Champion Loop. |
| Current workflows and bootstrapping | `pasted-text.txt:63-68` | Shows Equities Daily, Top 7 Synthesis, and Alpha Triage as research-cron applications needing working/holdout sets. |
| Structured feedback / autonomy | `pasted-text.txt:69-72` | Frames loop bootstrapping as delegating reasoning, execution, and feedback while training the human to provide structured feedback. |

## 初步看点

- The strongest idea is holdout-gated prompt improvement for recurring research outputs.
- It explicitly targets AI sycophancy / agreeableness by adding adversarial review and thesis stress testing.
- It separates feedback collection from prompt promotion: complaints are collected and ranked, then the Champion Loop decides what to fix.
- It has a good "one change at a time" rule that supports attribution.
- It treats structured human feedback as bootstrapping data before agent feedback can take over.

## 明显疑点

- This is a social-post/article, not official Hermes documentation or a reproducible benchmark.
- The post does not provide the actual scoring rubric, ground-truth labels, holdout records, or implementation artifacts.
- Investment/research workflow examples are source claims, not validated outcomes.
- "Agent feedback replaces human feedback" is aspirational and risky unless bounded by review and action gates.
- Research crons that emit buy/hold/sell or portfolio advice are action-adjacent and require far stronger evidence/action controls than this article provides.

## 可抽取 Candidate Points

- Research-agent loop needs adversarial thesis stress testing, not just helpful summarization.
- Champion/challenger prompt improvement should use holdout data, defined margin, and must-pass rules.
- Never promote on the working set.
- Feedback Sweep can convert repeated complaints into ranked improvement backlog.
- Working/holdout set construction is a prerequisite before loop automation.
- Structured human feedback is part of loop bootstrapping.

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

