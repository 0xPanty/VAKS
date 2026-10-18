---
record_kind: candidate_distillation
status: candidate
title: "Fable 5 AI 建站接单文：agentic coding 服务化的可借鉴点与风险"
created_at: "2026-06-11 04:18:00 +08:00"
created_by: Codex
provisional: true
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: none
derived_from:
  - raw/articles/2026-06-11-noisy-fable-5-ai-website-business-source.md
  - raw/articles/2026-06-11-noisy-fable-5-ai-website-business-source/pasted-text.txt
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
v0_2_13_trigger: no
routing_hint:
  - ai-service-business
  - agentic-coding
  - productized-delivery
  - prompt-as-spec
  - delivery-risk
possible_project_refs:
  - misa-productization
  - casttune-productization
point_anchor_refs:
  - snapshot_ref: raw/articles/2026-06-11-noisy-fable-5-ai-website-business-source/pasted-text.txt
    selector_type: heading_or_section
    selector_value: "Three prompts that produce real results"
  - snapshot_ref: raw/articles/2026-06-11-noisy-fable-5-ai-website-business-source/pasted-text.txt
    selector_type: heading_or_section
    selector_value: "The stack that gets the most out of Fable 5"
  - snapshot_ref: raw/articles/2026-06-11-noisy-fable-5-ai-website-business-source/pasted-text.txt
    selector_type: heading_or_section
    selector_value: "The CLAUDE.md file that gives Fable 5 context"
  - snapshot_ref: raw/articles/2026-06-11-noisy-fable-5-ai-website-business-source/pasted-text.txt
    selector_type: heading_or_section
    selector_value: "The math that makes this a real business"
verification_refs:
  - https://www.anthropic.com/claude/fable
  - https://www.anthropic.com/news/claude-fable-5-mythos-5
  - https://platform.claude.com/docs/en/about-claude/models/overview
  - https://code.claude.com/docs/en/skills
borrow_value: medium
borrow_order: P2
evidence_strength: medium_for_workflow_framing_low_for_business_claims
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "future task is specifically about productized AI service delivery, client website SOP, or agentic coding QA gates"
  support_when: "designing prompts-as-specs, CLAUDE.md project contracts, skill-based delivery recipes, or staged testing gates"
  risk_when: "pricing, revenue, model availability, client delivery, privacy, or production-readiness claims are being used for action"
  cold_references:
    - raw/articles/2026-06-11-noisy-fable-5-ai-website-business-source.md
    - raw/articles/2026-06-11-noisy-fable-5-ai-website-business-source/pasted-text.txt
tags:
  - candidate
  - provisional
  - ai-business
  - agentic-coding
  - claude
  - source-distillation
---

# 候选蒸馏：Fable 5 AI 建站接单文

## Boundary

This note is provisional orientation.

It can help route attention, compare ideas, or suggest future project overlays. It is not reviewed knowledge, not a decision, not a formal pattern, and not action basis.

## 一句话

这篇材料是 `P2 / medium`：值得借鉴它把 AI coding 变成“可报价、可验收、可复用 SOP”的包装方式，但收入数字和限时窗口是营销高风险内容，不能直接当行动依据。

## 可借鉴的核心，不是“学生躺赚”

真正可借鉴的结构是：

```text
客户 brief
-> 结构化规格 prompt
-> 分阶段构建
-> 每步测试和修复
-> 人类验收和交付
-> CLAUDE.md / skills 复用
```

也就是说，人没有消失，只是职责变了：

```text
写代码的人
-> 产品经理 + QA + 架构审查 + 客户交付负责人
```

## Candidate Points

### 1. Prompt 应该写成规格和验收门，不只是需求描述

文中三个 prompt 共同点不是 stack，而是都要求：

- 明确业务目标。
- 明确输出物。
- 明确技术栈。
- 明确构建顺序。
- 每一步测试。
- 当前步骤不工作就不能前进。

这个点很值得保留。未来无论是建站、游戏、自动化，prompt 都应该像 mini-spec + acceptance criteria。

### 2. AI 服务的利润来自交付确定性，不来自模型本身

文章把 Fable 5 说成商业机会，但客户真正买的是：

- 问题被解决。
- 页面或脚本能跑。
- 交付有人负责。
- 后续能维护。
- 出错有人兜底。

因此候选结论是：AI 可以降低生产成本，但不能替代客户发现、需求澄清、验收、维护和责任边界。

### 3. `CLAUDE.md` 和 skills 是服务产品化的关键

文章中最稳的工程借鉴是把项目上下文写入 `CLAUDE.md`，再把常用流程沉淀成 skills。这样每次交付不用从零解释：

```text
project context
stack
rules
memory
never do
```

这可以迁移到任何 agentic delivery，但要加上权限、测试、版本和回退。

### 4. 每步可运行比一次性大生成更重要

文中反复出现的“keep every build playable / test after each step / do not move forward until current step works”是最值得吸收的质量门。

这比“模型能不能一次写完整项目”更可靠，也更适合真实客户交付。

### 5. 商业数字只能当市场假设，不能当证据

文中的 `$3,000-5,000 website`、`$9.99 subscription`、`1,000 subscribers`、`$500-2,000 automation` 都只能作为商业假设或营销文案样本。

它们缺少：

- 获客成本。
- 成交率。
- 客户行业。
- 维护成本。
- 退款/纠纷概率。
- 合同边界。
- 税务和平台风险。
- 真实案例链接。

所以不能进入 action basis。

### 6. 限时窗口是风险信号

文章强调 free window / June 22 / start this week。这种 urgency 可以激活动作，但也容易造成无审查行动。

VAKS 处理方式应该是：

```text
current product claim -> recheck official source
business decision -> require action-facing gate
income claim -> require independent evidence
workflow idea -> candidate-only borrowing allowed
```

## Borrow Gradient

```yaml
borrow_value: medium
borrow_order: P2
P1:
  - prompt-as-spec with acceptance gates
  - every-step-test-before-next-step delivery discipline
  - CLAUDE.md as reusable project contract
  - skills as reusable service recipes
P2:
  - productized website/game/automation offer framing
  - human role shift from coding to reviewing, testing, scoping, and delivery
  - using official model docs as a key-entity verification step
P3:
  - specific stacks and monetization examples as watch-only inspiration
avoid:
  - treating revenue examples as evidence
  - selling work without QA, contract, privacy, maintenance, and support boundaries
  - using time-limited access claims without rechecking official docs
  - using model hype as a substitute for product-market validation
  - letting generated code become production without human review and tests
```

## 适合放进哪些未来工作

- AI service / productized delivery SOP。
- Client website prompt template with acceptance criteria。
- Business automation intake checklist。
- Agentic coding QA gates。
- `CLAUDE.md` project contract template。
- Skills registry for repeatable delivery workflows。
- Risk checklist for AI-generated paid work。

## 不适合现在做什么

- 不根据这篇文章直接定价。
- 不把它变成“现在必须冲”的行动计划。
- 不把营销案例写成 reviewed knowledge。
- 不创建 VAKS 主架构决策。
- 不启动任何自动化、GitHub MCP、Stripe、Vercel 或客户交付流程。

## Official Check Summary

已用官方页面做轻量核对：

- Claude Fable 5 作为模型和 `claude-fable-5` API ID 可确认。
- 官方定价、可用范围、fallback 和 data retention 口径需要以 Anthropic 页面为准。
- Claude Code skills / `SKILL.md` 机制可确认。
- 文中商业结果、订阅价格策略和窗口期主张仍未验证。

## Judgment

```yaml
direct_use: no
fork: no
design_only: yes
fusion_decision: adapt_with_risk
architecture_change: no
workflow_value: medium
business_claim_value: low
implementation_cost: low_to_medium
reversibility: high
action_readiness: not_ready
suggested_project_overlay: no
```

## Open Questions

- 如果以后真的做 AI 建站/自动化接单，最低 QA gate 应该是什么？
- `CLAUDE.md` 和 skills 如何版本化，避免“旧 prompt 交付新项目”？
- 客户数据、账号、API key、支付和部署权限如何隔离？
- 怎么把“一次性生成”改成“可验收的阶段交付”？
- 哪些收入/定价主张需要真实市场证据后才能进入行动计划？

## Forbidden

```text
project_borrow_scope
project_non_borrow_scope
decision outcome
formal pattern
action basis
truth confidence
```
