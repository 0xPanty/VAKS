---
type: source
record_kind: source_card
status: source-captured
title: "A student with a $20 subscription is selling websites for $5,000. Here's how it works with Fable 5"
source_id: noisy-fable-5-ai-website-business-pasted-2026-06-11
source_uri: codex-attachment:718167d5-0cc3-4755-a833-6270b68057cd/pasted-text.txt
source_url:
source_type: pasted-text-social-article
author: "I'm Noisy"
publisher: unknown-social-platform
published_at:
updated_at:
captured_at: "2026-06-11 04:18:00 +08:00"
captured_by: user-attached-pasted-text
version_or_commit:
source_integrity:
  source_hash: sha256:06810094b4e7892747c17f5a9aad8c49af1e7833f0f9b3e6b78ac6d8ced9654a
  snapshot_hash: sha256:06810094b4e7892747c17f5a9aad8c49af1e7833f0f9b3e6b78ac6d8ced9654a
  ingest_state: captured_user_paste
adapter_ingest:
  adapter_name: codex-attachment-pasted-text-plus-official-web-check
  adapter_version: manual-2026-06-11
  capture_method: user supplied pasted text attachment; limited official-source verification for volatile product claims
  extraction_trace:
    - read attachment from Codex local attachment path
    - copied retained raw text into project-visible article artifact
    - checked official Anthropic pages for Claude Fable 5, models overview, and Claude Code skills
  known_limits:
    - original social URL was not provided in the attachment
    - author identity, platform, and social metrics were not independently checked
    - freelancer income examples, subscriber math, and named usage counts were not independently verified
    - pricing, access, and availability are time-sensitive and must be rechecked before action use
source_status: partially_verified_current_product_claims
raw_location: raw/articles/2026-06-11-noisy-fable-5-ai-website-business-source/pasted-text.txt
processing_mode: explicit_distillation
processing_level: medium
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
topics:
  - ai-service-business
  - agentic-coding
  - claude-fable-5
  - claude-code
  - skills
  - productized-services
  - client-delivery
  - workflow-risk
projects: []
source_family: ai-agent-business-playbook
upstream_sources:
  - https://www.anthropic.com/claude/fable
  - https://www.anthropic.com/news/claude-fable-5-mythos-5
  - https://platform.claude.com/docs/en/about-claude/models/overview
  - https://code.claude.com/docs/en/skills
verification_status: partial_official_check
candidate_relation_suggestions: []
tags:
  - raw-article
  - pasted-text
  - ai-business
  - claude
  - candidate-only
---

# 来源记录：Fable 5 AI 建站接单商业化长文

## 为什么收录

这篇社媒长文把 Claude Fable 5 包装成“低成本个人也能交付高价网站、游戏、自动化”的商业机会。它的可用价值不是收入承诺本身，而是把 agentic coding 的服务化流程说得很直白：

```text
客户问题
-> 结构化 brief
-> AI 生成和测试
-> 人类审查与交付
-> 可复用 CLAUDE.md / skills / stack
```

对资料库来说，它适合作为“AI 服务商业化、agentic delivery、提示词即规格、测试门槛、技能复用、营销风险”的候选材料。它不适合作为投资、收入、定价、模型能力或具体接单策略的行动依据。

## 来源信息

- 作者字段：`I'm Noisy`，来自附件正文自述。
- 标题：`A student with a $20 subscription is selling websites for $5,000. Here's how it works with Fable 5`。
- 原始链接：未提供。
- 发布平台：未核验。
- 收录方式：用户提供 Codex 附件中的 pasted text。
- 保留原文：`raw/articles/2026-06-11-noisy-fable-5-ai-website-business-source/pasted-text.txt`。
- 原文 SHA256：`06810094b4e7892747c17f5a9aad8c49af1e7833f0f9b3e6b78ac6d8ced9654a`。

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

Source records provide provenance and findability. They do not create reviewed evidence, project borrowing conclusions, truth confidence, or action basis.

## 人话摘要

作者认为 Claude Fable 5 降低了建站、浏览器游戏和业务自动化的交付门槛，普通人可以用 prompt + agentic coding 快速交付可收费作品。文章给了三个可复用 prompt 方向：客户网站、订阅制浏览器游戏、业务自动化脚本，并建议围绕 Claude Code、skills、GitHub MCP、subagents、`CLAUDE.md` 做一套交付栈。

更朴素地说，这篇文章讲的是：

```text
不要把 AI 当聊天工具
要把 AI 当可测试的交付工人
人负责需求、验收、风控、客户沟通和定价包装
```

## Key Entity / Current Claim Check

官方页面可确认的部分：

- Anthropic 已发布 Claude Fable 5；官方页面显示发布日期为 2026-06-09。
- 官方页面显示 Claude Fable 5 可用于长周期、复杂和异步任务，并可在 Claude Code 等 agent harness 中工作。
- 官方页面显示定价为每百万 input tokens 10 美元、每百万 output tokens 50 美元；API 文档也列出 `claude-fable-5`。
- 官方页面显示 Fable 5 在生物/网络安全等受保护领域可能 fallback 到 Opus 4.8。
- Claude Code 官方文档确认 skills 使用 `SKILL.md`，用于复用特定任务或工作流 instructions。
- Anthropic 公告页提到 Stripe 在早测中报告过大型 Ruby codebase 迁移案例。

附件文本中未验证或高漂移的部分：

- `$20 subscription`、`free until June 22`、`Pro/Max/Team/Enterprise free access` 未在本次打开的官方页面中确认。
- `$3,000-5,000 per website`、`$500-2,000 automation`、`1,000 subscribers = $9,990/month` 是商业包装或算术示例，不是市场验证。
- `5,838 developers switched` 未独立核验。
- `student with phone`、`same-day delivery`、`weekend game subscription business` 是强营销叙事，不能当可复现结论。

## 可抽取 Candidate Points

- AI 建站/自动化的核心变化不是“无需能力”，而是交付职责迁移：人从写每一行代码转为写需求、拆阶段、验收、测试、修复和沟通。
- 高价值 prompt 的本质是规格书和验收清单，不是魔法咒语。最值得保留的是“每个组件后测试、失败就修、不要跳到下一步”这种 gate。
- `CLAUDE.md` 和 skills 可以把一次性 prompt 变成可复用工作流，但需要版本、权限、测试和回退。
- 产品化服务的商业价值来自客户问题、交付确定性、售后和信任，不来自模型名称本身。
- 收入数字、限时窗口和“一周内赚钱”的叙事容易制造行动冲动，应进入风险提示而不是行动依据。

## 明显疑点

- 这是一篇营销色彩很强的社媒长文，原始链接和发布时间缺失。
- 官方模型能力可部分确认，但具体商业案例没有独立证据。
- 文中把技术可行性、客户愿付价格和长期盈利压成了一条线，中间缺少获客、需求澄清、验收、维护、合同、退款、合规、税务和平台风险。
- prompt 模板没有包括隐私、授权、客户数据处理、生产环境监控、交付后的维护责任。
- 若直接照做，容易变成“AI 生成快，但交付债务由人偿还”。

## 当前处理等级

```text
medium
```

升级到 heavy 的条件：

- 用户要把它变成真实接单 SOP、Misa/CastTune 产品化交付流程或 VAKS agentic delivery 模板。
- 找到原始社媒链接、作者主页和可核验案例。
- 独立核验 pricing/access、Claude Code skills、GitHub MCP、skills repo、subagent 框架和部署链。
- 需要形成行动计划、报价模板、合同风险或客户交付标准。

## 下一步

进入候选蒸馏层，作为 AI 服务商业化与 agentic coding 交付流程的 P2 借鉴材料；不进入 reviewed knowledge，不作为收费建议或行动依据。
