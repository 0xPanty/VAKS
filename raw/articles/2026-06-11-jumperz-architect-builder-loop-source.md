---
type: source
record_kind: source_card
status: source-captured
title: "The Architect Loop: Fable thinks, Codex builds, repo remembers, you judge"
source_id: jumperz-architect-builder-loop-2026-06-11
source_uri: user-provided-social-post-and-screenshot
source_url:
source_type: social-post-image-text
author: "JUMPERZ / @jumperz"
publisher: unknown-social-platform
published_at:
updated_at:
captured_at: "2026-06-11 04:16:49 +08:00"
captured_by: user-pasted-text-and-screenshot
version_or_commit:
source_integrity:
  source_hash: sha256:4dd8c624fc9ac051cbc2e06e181f333ecaae985f9d0f4513ed86f9a797d63ef3
  snapshot_hash: sha256:c8683e61019eb2770fdef356fc40652fc23c3c271601417d488850d2462948c5
  ingest_state: captured_user_paste_and_image
adapter_ingest:
  adapter_name: user-paste-plus-local-image-snapshot-plus-official-web-check
  adapter_version: manual-2026-06-11
  capture_method: user provided translated post text and screenshot; limited official-source verification for OpenAI / Anthropic product claims
  extraction_trace:
    - copied screenshot into project-visible article artifact
    - saved user-provided translated post text into project-visible artifact
    - visually inspected screenshot text
    - checked official OpenAI pages for GPT-5.5 in Codex and /goal
    - reused current official Anthropic Fable 5 check from this intake session
  known_limits:
    - original social URL was not provided
    - original English wording was not captured
    - publication time is relative only: "3 hours"
    - "20 dollar subscription" and subscription-vs-API cost claim were not independently verified
    - Fable-as-architect / Codex-as-builder is a workflow proposal, not a measured benchmark
source_status: partially_verified_workflow_entities
raw_location: raw/articles/2026-06-11-jumperz-architect-builder-loop-source/pasted-text.txt
image_snapshot_location: raw/articles/2026-06-11-jumperz-architect-builder-loop-source/architect-loop.png
processing_mode: explicit_knowledge_fragment_distillation
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
  - architect-builder-loop
  - agentic-coding
  - codex-goal
  - handoff-memory
  - repository-as-memory
  - spec-gates
  - reviewer-agent
  - human-judgment
projects:
  - verified-action-knowledge-system
source_family: agentic-development-operating-loop
upstream_sources:
  - https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex
  - https://developers.openai.com/codex/use-cases/follow-goals
  - https://developers.openai.com/codex/changelog
  - https://openai.com/index/introducing-gpt-5-5/
  - https://www.anthropic.com/claude/fable
verification_status: partial_official_check
candidate_relation_suggestions: []
tags:
  - raw-article
  - social-post
  - screenshot
  - agentic-coding
  - codex
  - candidate-only
---

# 来源记录：JUMPERZ Architect Loop

## 为什么收录

这条图文把双模型开发协作压成一个很清楚的操作循环：

```text
Fable thinks
-> Codex builds
-> repo remembers
-> human judges
```

它对 VAKS / Codex 工作流有直接借鉴价值，因为它强调了几个我们已经反复踩中的边界：仓库文件是共享记忆，成功标准要在结果之前冻结，构建者不能给自己打分，分歧必须显性化，人类和架构师负责裁决。

## 来源信息

- 作者字段：`JUMPERZ / @jumperz`，来自用户粘贴文本和截图。
- 原始链接：未提供。
- 发布时间：用户粘贴为 `3小时`，未换算绝对发布时间。
- 文字 artifact：`raw/articles/2026-06-11-jumperz-architect-builder-loop-source/pasted-text.txt`。
- 截图 artifact：`raw/articles/2026-06-11-jumperz-architect-builder-loop-source/architect-loop.png`。
- 文本 SHA256：`4dd8c624fc9ac051cbc2e06e181f333ecaae985f9d0f4513ed86f9a797d63ef3`。
- 截图 SHA256：`c8683e61019eb2770fdef356fc40652fc23c3c271601417d488850d2462948c5`。

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

## Screenshot Reading

截图标题为 `the architect loop`，副标题为：

```text
fable thinks · codex builds · repo remembers · you judge
```

图中三块：

- `01 - architect`: Claude Fable 5，负责 specs / rulings / kill calls。
- `02 - builder`: GPT 5.5 Codex，包含 lane a、lane b、reviewer。
- `03 - memory`: repo - `HANDOFF.md`，包含 specs / frozen gates / raw results。

中心是 `you / gate calls`。底部总结为：architect 是 edge，builder 是 hands，repo 是 brain。

## Key Entity / Current Claim Check

官方可确认的部分：

- OpenAI 官方 Codex 文档说明 `/goal` 用于让 Codex 围绕一个 durable objective 跨 turn 工作，并带有 completion condition、success check 和 constraints。
- OpenAI Codex changelog 显示 GPT-5.5 已可用于 Codex，适合 implementation、refactors、debugging、testing、validation 等任务。
- OpenAI GPT-5.5 公告显示 GPT-5.5 在 Codex 中用于工程工作，并可用于实现、重构、调试、测试和验证。
- Anthropic 官方页面显示 Claude Fable 5 是面向长周期复杂任务的模型，可在 Claude Code 等 agent harness 中运行，并可进行规划、委派和检查工作。

未确认或需要保守处理：

- `20 dollar subscription` 是否足以覆盖该流程的实际使用量，未核验。
- `30 minutes of Fable is enough` 是 workflow 经验，不是通用事实。
- `Fable as architect + GPT 5.5 Codex as builder` 是人设化分工，不是官方推荐架构。
- multi-lane subagents / reviewer agent 的具体实现方式取决于工具环境，不应从图文直接推导为可运行系统。

## 可抽取 Candidate Points

- 架构师模型应负责裁决、范围控制、下一切片规格和 kill calls，而不是写实现代码。
- 构建者模型应负责执行、测试、修复和提交 raw results，不应自评“成功”。
- repo 内 `docs/HANDOFF.md` 可以作为跨模型共享记忆，减少重复上下文和口头状态漂移。
- 成功标准和 shared contracts 应在编码前冻结，避免结果出现后移动门柱。
- 分歧不是噪音，而是必须被记录和裁决的设计输入。
- reviewer agent 的职责应是按冻结 docs、spec 和 tests 给出 APPROVE 或编号缺陷，不写功能代码。

## 明显疑点

- 这是一条社媒 workflow 图文，不是经过实测的工程报告。
- 如果 `HANDOFF.md` 只记录构建者叙述，而不记录 raw results、test evidence 和 unresolved disagreements，会变成漂亮但不可靠的项目日记。
- `commit + push every slice` 对某些工作区风险偏高；VAKS 仍需要用户显式授权 commit/push。
- 架构师/构建者分工可以减少混乱，但不能替代真实文件、测试、官方 API/格式核验和人类 gate。

## 当前处理等级

```text
medium
```

升级到 heavy 的条件：

- 用户要求把这条流程变成 VAKS / Misa / CastTune 的正式开发 SOP。
- 有一次真实仓库试跑结果：handoff 更新、frozen docs、parallel lanes、reviewer output、PR/commit 证据。
- 需要形成主线规则、模板、命令或 automation。

## 下一步

进入候选知识碎片层，并给 VAKS 写一个 project overlay。不要进入 reviewed knowledge，不改 `AGENTS.md` / `SOURCE_INTAKE.md` / 主架构文档，不启动 goal、agent、commit 或 push。
