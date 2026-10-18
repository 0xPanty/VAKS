---
record_kind: candidate_distillation
status: draft
provisional: true
title: "Yozm Obsidian LLM Wiki：个人第二大脑构建案例候选蒸馏"
created_at: 2026-06-12
created_by: Codex
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: project_sidecar_created
review_pressure: none
derived_from:
  - raw/articles/2026-06-12-yozm-obsidian-llm-wiki-second-brain-source.md
  - raw/articles/2026-06-12-yozm-obsidian-llm-wiki-second-brain-source/capture-notes.md
  - outputs/review/project_lens_overlays/2026-06-12-yozm-obsidian-llm-wiki-second-brain-overlay.md
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
  - obsidian-workbench
  - llm-wiki
  - source-intake
  - query-workflow
  - lint-maintenance
  - context-entrypoint
  - sensitive-data-boundary
possible_project_refs:
  - verified-action-knowledge-system
point_anchor_refs:
  - raw/articles/2026-06-12-yozm-obsidian-llm-wiki-second-brain-source/capture-notes.md#Opening--summary
  - raw/articles/2026-06-12-yozm-obsidian-llm-wiki-second-brain-source/capture-notes.md#Claude-Code--CLI-and-root-manual
  - raw/articles/2026-06-12-yozm-obsidian-llm-wiki-second-brain-source/capture-notes.md#Ingest
  - raw/articles/2026-06-12-yozm-obsidian-llm-wiki-second-brain-source/capture-notes.md#Lint
  - raw/articles/2026-06-12-yozm-obsidian-llm-wiki-second-brain-source/capture-notes.md#Query
  - raw/articles/2026-06-12-yozm-obsidian-llm-wiki-second-brain-source/capture-notes.md#Limitations
borrow_value: strong
borrow_order:
  - "P1: ingest / query / lint as a compact operator-command surface for an LLM-maintained Obsidian wiki"
  - "P2: root operating manual plus session-start entrypoint for stable agent behavior, adapted through AGENTS / handoff / DEV_CONTEXT"
  - "P3: Obsidian + GitHub / mobile capture mechanics as storage and capture references only after security and official-doc checks"
avoid:
  - "Do not use full-vault query as a default without authority buckets, retrieval budget, and source anchors."
  - "Do not let Claude Code, Codex, hooks, or scheduled lint mutate reviewed knowledge, truth confidence, decisions, or action basis directly."
  - "Do not treat GitHub Private Repo as a complete privacy or security boundary."
  - "Do not rely on regex masking as sufficient sensitive-data protection."
  - "Do not merge personal and team contexts without explicit scope, access, and duplication rules."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "the active task is designing VAKS Obsidian operator commands, source-intake automation, query/lint workflows, or session-start context entry"
  support_when: "planning lightweight capture, root manuals, handoff loading, wiki linting, mobile/desktop capture surfaces, or context-aware querying"
  risk_when: "someone proposes full-vault prompting, direct AI-to-reviewed-wiki writes, schedule-driven auto-fixes, or sensitive-data ingestion"
  cold_references:
    - raw/articles/2026-06-12-yozm-obsidian-llm-wiki-second-brain-source.md
    - raw/articles/2026-06-12-yozm-obsidian-llm-wiki-second-brain-source/capture-notes.md
tags:
  - candidate
  - provisional
  - source-distillation
  - obsidian
  - llm-wiki
  - claude-code
  - source-intake
  - lint
  - query
  - candidate-only
---

# 候选蒸馏：Yozm Obsidian LLM Wiki

## 说人话

这篇文章讲的是：作者不想每次和不同 AI 工具说一遍“我是谁、我在做什么、我现在的项目上下文是什么”，于是用 Obsidian 做个人 wiki，用 GitHub 私有仓库同步，用 Claude Code / CLI 来整理、查询和检查这个 wiki。

对我们有用的不是“照抄他的个人第二大脑”，而是三个很清楚的小工具形状：

```text
/ingest：把新资料放进 wiki
/query：带着个人上下文问问题
/lint：定期查坏链、敏感信息、矛盾和孤儿页
```

VAKS 可以借这个操作面，但必须加自己的硬边界：raw 是来源，candidate 是理解，overlay 是项目侧车，reviewed 才能支撑行动。不能让“AI 看了全库”听起来像“AI 已经知道真相”。

## Candidate Point 1: 上下文疲劳要用可复用上下文解决，不是靠更长 prompt

文章的问题起点很实在：AI 工具越多，每个工具都要重新交代背景，人的上下文会被分散在不同工具、不同笔记、不同项目文件里。

VAKS 可以吸收这个判断：

```text
repeated context explanation
-> durable context surface
-> query-time activation
-> answer with project/history awareness
```

但 VAKS 不能把所有东西都丢进一个无差别上下文池。更安全的形状是：

```text
reviewed bucket
candidate bucket
raw/source bucket
project overlay bucket
risk / review_due bucket
```

查询时可以激活多桶材料，但答案必须知道每个材料的权威等级。

## Candidate Point 2: LLM Wiki 最小操作面可以是 ingest / query / lint

这篇文章最值钱的地方，是把个人 LLM Wiki 的日常操作压成三个命令：

| Command shape | 作用 | VAKS 候选借法 |
|---|---|---|
| `/ingest` | 读新资料并放入合适 wiki 页面 | raw snapshot / candidate distillation / routing |
| `/query` | 基于 wiki 上下文回答问题 | authority-bucketed retrieval / context pack |
| `/lint` | 检查敏感信息、矛盾、坏链、孤儿页 | maintenance manifest / review_pressure |

这比“做一个超级知识库”更可落地。它像一个很小的 cockpit 菜单：收、问、查。

VAKS 的版本应该保持：

```text
ingest writes raw/candidate only
query can use candidate as orientation only
lint creates maintenance findings, not automatic truth repairs
```

## Candidate Point 3: Root manual 和 SessionStart Hook 证明入口文件很关键

文章把 root `CLAUDE.md` 当成 wiki 操作手册，让新会话启动时读它；如果模型没看，就用 SessionStart Hook 强制注入规则或索引。

这和 VAKS 已经在做的事很像：

```text
AGENTS.md
00_handoff/
README / SOURCE_INTAKE / DEV_CONTEXT
templates
indexes
```

可借的不是具体文件名，而是这个原则：

```text
每个 agent 窗口都需要一个短入口，
入口必须指向本地真实文件，
而不是靠聊天记忆猜当前规则。
```

风险也很明显：hook 注入如果过期、过大、或把候选材料当规则，会把错误放大。所以 VAKS 的入口文件应该继续短、路由式、可恢复，而不是把整套架构塞进一个大系统 prompt。

## Candidate Point 4: Obsidian + GitHub 是存储/同步表面，不是安全结论

文章选择 Obsidian 作为本地文件 vault，用 GitHub Private Repo 做备份/同步，移动端通过 Obsidian Sync 或 Working Copy 访问。

这对 VAKS 的启发：

```text
Markdown 文件 + Git 历史 + 多端捕获
确实适合作为 AI 可操作的长期工作表面。
```

但不能吸收成：

```text
private repo = 足够安全
GitHub sync = 正式权限模型
所有个人材料都可以集中进 AI vault
```

VAKS 如果未来做移动捕获或同步，需要把“存储便利”和“隐私边界”分开讨论。

## Candidate Point 5: 敏感信息处理不能只靠正则遮罩

文章提到 ingest Notion / Google Keep 等个人数据时，会用正则检测密码、卡号、身份证号等敏感信息，并在写入 wiki 时遮罩；同时也承认正则并不完整，需要后续 lint 或人工检查。

这对 VAKS 是一个很好的风险样本：

```text
regex masking = first-pass guard
not = privacy proof
not = safe-to-ingest approval
```

更稳的 VAKS 形状：

```text
private/raw quarantine
-> sensitive scan
-> redaction candidate
-> human confirmation for high-risk material
-> retained source / redacted derivative separated
```

如果未来 agent 能自动读个人文档，这条必须进风险层。

## Candidate Point 6: Query 全库很诱人，也最容易混淆权威

文章说 `/query` 能让 AI 基于个人上下文给出更贴合实际的答案，这是 LLM Wiki 的核心收益之一。

VAKS 可以承认这个价值：

```text
personal/project context -> better relevance
history and current priorities -> better advice
```

但要加 VAKS 的刹车：

```text
full vault context != full vault truth
candidate orientation != reviewed support
generated summary != evidence
raw provenance != claim support
```

所以 VAKS 的 query 不能只是“把全库塞给模型”。更好的版本是：

```text
retrieve by scope
bucket by authority
show support / challenge / risk / missing anchors
only reviewed evidence can support action
```

## Candidate Point 7: Lint 应该成为 maintenance manifest，而不是自动修库机器人

文章的 `/lint` 会检查敏感信息、矛盾、孤儿页、坏链等，并用 Claude schedule 做周期检查。

这是强借鉴点。VAKS 已经有 maintenance-manifest 形状，可以把 lint 归到：

```text
broken link
missing source anchor
orphan candidate
sensitive data warning
authority-field violation
stale decision / review_due
contradiction pressure
```

但 lint 结果应当是：

```text
maintenance input
review pressure
candidate patch suggestion
```

不是：

```text
auto repair
truth mutation
reviewed relation creation
decision update
```

## Candidate Point 8: 个人 wiki 和团队 wiki 的边界不能靠 SSOT 口号解决

文章最后提到一个很真实的问题：个人 LLM Wiki 有大量私人信息，所以很难直接和团队共享；如果另建团队 wiki，又会出现信息重复和所谓 SSOT 的矛盾。

这对 VAKS 有用，因为它提醒我们：

```text
scope is part of truth applicability
personal context and project context are not interchangeable
```

VAKS 未来如果有个人 vault、项目 vault、团队 vault，需要明确：

```text
which source can cross boundary
which summary can be shared
which sensitive fields are excluded
which duplicate is authoritative for which action
```

## VAKS Mapping

| VAKS layer | Fit | Borrow |
|---|---:|---|
| Capture / Provenance | High | Web clipper, mobile share, temp folder, raw ingest are practical capture surfaces. |
| Candidate Comprehension | High | `/ingest` maps directly to candidate extraction and routing. |
| Knowledge Calibration | Medium | `/lint` can create contradiction and missing-anchor pressure. |
| Review / Consolidation | Low by default | Article does not supply evidence-aware review; VAKS must add gates. |
| Association / Reviewed Relations | Low | Obsidian links/graph are useful navigation, not reviewed relations. |
| Activation / Dev Context | High | Root manual, SessionStart, and `/query` map to activation. |
| Context Pack | Medium | Context-aware answers are useful if authority buckets remain visible. |
| Decision / Action | Risky | Full personal context advice needs intent confirmation and action-basis gate. |
| Feedback / Lint | High | Recurring lint and practical failures map well to maintenance manifests. |

## Borrow Gradient

```yaml
borrow_value: strong
borrow_order:
  - P1: ingest / query / lint operator-command surface
  - P2: root operating manual and session-start entrypoint
  - P3: Obsidian + GitHub / mobile capture mechanics after security checks
```

## Do Not Borrow

- Do not use full-vault query as the default retrieval mode.
- Do not let Claude Code, Codex, hooks, or schedules directly mutate reviewed knowledge.
- Do not let `/lint` auto-fix truth-bearing records.
- Do not treat Obsidian links or Graph View as reviewed relations.
- Do not treat GitHub Private Repo as enough security for sensitive personal data.
- Do not rely on regex masking as a complete privacy solution.
- Do not merge personal and team wiki contexts without explicit boundary rules.
- Do not turn this article into a mainline architecture decision without separate review.

## Open Questions

- Which VAKS operator command should come first if we prototype: intake, query, or lint?
- Should VAKS have a root runtime manual equivalent to `CLAUDE.md`, or should `AGENTS.md` + handoffs remain the only entry router?
- How would a VAKS `/query` display raw / candidate / overlay / reviewed buckets to avoid false authority?
- What privacy model is required before personal notes, screenshots, or mobile shares enter a VAKS-like vault?
- Can lint produce useful maintenance manifests without creating auto-repair pressure?

## Current Judgment

```yaml
direct_use: no
fork_or_run: no
design_only: yes
implementation_next: only_if_user_requests_vaks_operator_command_or_obsidian_workbench
mainline_change_now: no
reviewed_knowledge_created: false
action_basis_allowed: false
truth_mutation_allowed: false
borrow_value: strong
```
