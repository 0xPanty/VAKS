---
type: source
record_kind: source_card
status: source-captured
title: "Movez / The Self-Improving Loop: a 300-agent swarm on Kimi K2.6, verified by Opus 4.8"
source_id: x-movez-self-improving-loop-kimi-swarm-2026-06-23
source_uri: local_attachment:908f9b5e-a6c2-4505-ad1a-f5c5dd66ea3e/pasted-text.txt
source_url: unknown
source_type: article_pasted_text
author: "Movez / @0xMovez"
publisher: "X / Twitter pasted text"
published_at: unknown
updated_at:
captured_at: 2026-06-23T03:02:07+08:00
captured_by: Codex
version_or_commit:
source_integrity:
  source_hash: C9588B16C148648E9C493EA39FF681F37986986544DF9F7E56919CE80E7C6659
  snapshot_hash: C9588B16C148648E9C493EA39FF681F37986986544DF9F7E56919CE80E7C6659
  ingest_state: new
adapter_ingest:
  adapter_name: local-pasted-text-copy
  adapter_version: powershell Copy-Item
  capture_method: "User supplied pasted-text.txt attachment; copied into raw/articles for durable retention."
  extraction_trace: "Local line-number inspection of pasted text; no browser, X account, or external verification was used."
  known_limits:
    - "The original X post URL was not present in the attachment."
    - "The attachment appears to be copied from an X/Twitter UI and includes UI fragments."
    - "Kimi, Opus, pricing, benchmark, agent-count, step-count, and product-capability claims were not independently verified."
    - "The embedded Kimi/Moonshot post date appears as 4月23日 without a year in the pasted text."
    - "This source is treated as social-post / article-style orientation, not evidence support."
source_status: unknown
raw_location: raw/articles/2026-06-23-movez-self-improving-loop-kimi-swarm-source/pasted-text.txt
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
why_saved: "User asked to distill this article/post after two loop-engineering repository intakes; it adds a concrete self-improving swarm playbook with spec, decomposition review, verify gate, reusable skill, constraints, replay, and background-agent trigger."
topics:
  - agentic-loops
  - self-improving-loop
  - kimi-swarm
  - verify-gate
  - reusable-skills
  - constraints-file
  - background-agent
projects:
  - verified-action-knowledge-system
source_family:
  - article
  - pasted-text
  - social-post-thread
upstream_sources:
  - "Kimi.ai / @Kimi_Moonshot embedded post excerpt, unverified"
verification_status: source_text_copied_unverified
candidate_relation_suggestions: []
tags:
  - article-intake
  - social-post
  - agentic-loops
  - candidate-only
---

# 来源记录：Movez / The Self-Improving Loop

## 为什么收录

用户要求蒸馏这篇文章。它接在 `Agent-Loop-Skills` 和 `loop-engineer-template` 两个 Loop 源之后，提供了一个更偏实操 playbook 的自改进 swarm loop：

```text
spec
-> decomposition review
-> parallel swarm execution
-> structured files
-> independent verify gate
-> workflow saved as Skill
-> document/domain skills
-> constraints file
-> replay
-> background trigger
```

本记录只保存来源身份、原文快照和初步看点。它不代表 Kimi / Opus / benchmark / pricing / 300-agent / 4,000-step 等主张已经被 VAKS 验证，也不代表该 playbook 可以作为 reviewed knowledge 或 action basis。

## 来源信息

- 作者：Movez / `@0xMovez`
- 发布方：X / Twitter pasted text
- 原始链接：附件未包含
- 原始位置：`C:\Users\Administrator\.codex\attachments\908f9b5e-a6c2-4505-ad1a-f5c5dd66ea3e\pasted-text.txt`
- 资料库保留文本：`raw/articles/2026-06-23-movez-self-improving-loop-kimi-swarm-source/pasted-text.txt`
- source hash：`C9588B16C148648E9C493EA39FF681F37986986544DF9F7E56919CE80E7C6659`
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
| Source framing | `pasted-text.txt:7-13`, `pasted-text.txt:29-32` | Establishes the article's thesis: swarm work should leave reusable learning behind; verify gate prevents garbage from becoming a skill. |
| Spec discipline | `pasted-text.txt:36-50` | Strongest prompt-design pattern: write a spec with scope, validation rules, allowed sources, output format, conflict handling, and stop condition. |
| Decomposition review | `pasted-text.txt:53-65` | Important pre-execution gate: inspect agent count, dependencies, step budget, and quality-drop risk before spending tokens/time. |
| Parallel swarm execution | `pasted-text.txt:67-79` | Presents bounded-context subagents and structured merge as the reason swarm does not collapse like one long-context agent. |
| Real output target | `pasted-text.txt:81-93` | Pushes output-specific deliverables instead of chat answers. |
| Verify gate | `pasted-text.txt:95-99` | Separates generation from refutation; strongest VAKS-relevant safety point. |
| Skill capture | `pasted-text.txt:101-114` | Frames self-improvement as process capture, not weight retraining. |
| Document-to-skill | `pasted-text.txt:116-127` | Captures domain/style fingerprints from user documents as reusable skill context. |
| Constraints learning | `pasted-text.txt:129-139` | Converts verifier feedback into permanent project-level rules. |
| Replay and backgrounding | `pasted-text.txt:141-164` | Shows skill replay and background schedule/trigger with deviations-only reporting. |

## 初步看点

- The source's most useful idea is system-level self-improvement, not model-level self-improvement.
- It treats the spec as the seed artifact for a future reusable skill.
- It distinguishes cheap parallel generation from expensive independent verification.
- It converts verifier feedback into a constraints file so future runs avoid repeated mistakes.
- It ends with background execution only after a loop is stable and skill-backed.

## 明显疑点

- The article is promotional/social-post style and makes many unverified product and benchmark claims.
- The original post URL is missing, so the raw attachment is the stable source for this intake.
- "Verified by Opus 4.8" is a source claim. No Opus run or validation was performed here.
- "Every number is verified" is not accepted as true; it is only the article's claim about its playbook.
- Background agents and automatic skill application are high-risk for VAKS unless bounded by explicit user scope and review gates.

## 可抽取 Candidate Points

- Spec-first swarm execution.
- Pre-run decomposition review.
- Independent verify gate as refuter, not cheerleader.
- Workflow-to-skill capture as practical self-improvement.
- Verify feedback to `CONSTRAINTS.md`.
- Replay saved skill on new inputs.
- Promote to background agent only after stable, skill-backed loop and thresholded alerts.

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

