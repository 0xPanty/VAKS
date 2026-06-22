---
record_kind: candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: none
derived_from:
  - raw/papers/2026-06-07-aal-ruller-pkm-second-brain-ai-companian-source.md
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
  - second-brain
  - personal-ai-companion
  - activation-tier
  - context-pack-preparation
  - proactive-ai-boundary
  - privacy-autonomy-risk
  - ai-knowledge-graph
possible_project_refs:
  - verified-action-knowledge-system
point_anchor_refs:
  - source_ref: raw/papers/2026-06-07-aal-ruller-pkm-second-brain-ai-companian-source.md
    selector_type: crossref_metadata
    selector_value: "Crossref DOI metadata: title, authors, ACM, issued 2025-01-12, pages 90-93, proceedings-article"
  - source_ref: raw/papers/2026-06-07-aal-ruller-pkm-second-brain-ai-companian-source.md
    selector_type: group_2025_proceedings_lines
    selector_value: "GROUP proceedings lines 186-193: abstract on PKM -> second brain -> AI companion, multiple data streams, privacy, autonomy"
  - source_ref: raw/papers/2026-06-07-aal-ruller-pkm-second-brain-ai-companian-source.md
    selector_type: university_author_page_lines
    selector_value: "University of Siegen page lines 429-465: publication metadata and abstract"
  - source_ref: raw/papers/2026-06-07-aal-ruller-pkm-second-brain-ai-companian-source.md
    selector_type: access_limit
    selector_value: "ACM PDF access attempt returned 403 Forbidden; full-text architecture details pending verification"
reference_layer_tag: ref/pkm-to-personal-ai-companion
reference_layer_label_zh: PKM 到个人 AI 伴侣
reference_layer_scope: "second-brain / activation / proactive AI reference only"
borrow_value: strong
borrow_order:
  - "P1: PKM -> second brain -> personal AI companion trajectory as a clear future-facing framing for VAKS."
  - "P1: Active companion over passive organizer: the system should engage with context and suggest useful next attention, not merely store notes."
  - "P1: Privacy/autonomy/critical-thinking guardrail: proactive AI must augment human judgment, not replace it."
  - "P2: Multi-stream personal knowledge overview: multiple life/work data streams can feed a dynamic personal knowledge map, but only through source/provenance boundaries."
  - "P3: Specific implementation claims such as local server, encryption, and layer names remain pending full-text verification."
avoid:
  - "Do not treat proactive AI suggestions as reviewed knowledge, evidence support, or action basis."
  - "Do not auto-ingest all personal data streams into VAKS without explicit source boundaries, privacy rules, and user consent."
  - "Do not copy an AI companion architecture into VAKS core before full-text verification and separate architecture review."
  - "Do not treat citation count, venue prestige, or ACM publication status as truth confidence."
  - "Do not let the companion frame weaken user autonomy, critical thinking, or review gates."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "Designing VAKS second-brain, personal-AI-companion, proactive activation, or privacy-bounded agent-access architecture."
  support_when: "Discussing PKM evolution, second brain framing, personal knowledge graph, context suggestions, or proactive AI workbench behavior."
  risk_when: "Any proactive suggestion, data-stream ingestion, graph edge, assistant memory, or companion response starts being treated as truth, reviewed relation, source support, or action basis."
  cold_references:
    - raw/papers/2026-06-07-aal-ruller-pkm-second-brain-ai-companian-source.md
tags:
  - candidate
  - provisional
  - acm
  - group-2025
  - pkm
  - second-brain
  - personal-ai-companion
  - proactive-ai
  - graph-is-activation-not-truth
  - candidate-only
---

# Candidate Distillation: PKM to Second Brain to Personal AI Companian

## Boundary

This note is provisional orientation.

It distills accessible metadata and public abstract material for VAKS. It is not
reviewed knowledge, not a decision, not a formal pattern, and not action basis.

Important limitation:

```text
ACM PDF access returned 403 without authorized access.
This pass did not inspect the full PDF.
```

So the strongest use now is:

```text
high-level framing and candidate routing
```

not:

```text
detailed architecture adoption
```

## 一句话

这篇最值得先借的是一条路线：

```text
PKM 不是终点。
Second Brain 也不是终点。
下一步是有边界的 Personal AI Companion。
```

人话：

```text
资料库不能只是“把东西存好”。
更好的方向是：在当前任务里，把该出现的上下文、提醒、风险、旧经验和下一步建议主动拿出来。
```

但 VAKS 必须补上比普通 AI companion 更硬的边界：

```text
主动 ≠ 自动相信
召回 ≠ 证据
建议 ≠ 行动依据
陪伴感 ≠ 权威
```

## Candidate Points

### CP-001: `pkm_to_second_brain_to_ai_companion`

候选结论：

```text
PKM 的演进方向可以从信息组织工具，走向第二大脑，再走向主动型个人 AI companion。
```

VAKS 可借：

```text
public story / product framing:
  Capture -> Understand -> Review -> Connect -> Act and Learn
```

可以进一步说成：

```text
not just a vault,
but a bounded cognitive companion that helps prepare context and action.
```

不借：

```text
不要把 companion 变成无边界代理。
不要把陪伴/主动性包装成可信度。
```

### CP-002: `active_companion_over_passive_organizer`

候选结论：

```text
下一代系统不只是整理信息，而是主动处理上下文并给出个性化建议。
```

VAKS 可借：

```text
activation layer:
  current task
  relevant source/candidate/reviewed context
  known risks
  prior feedback
  possible next questions
```

边界：

```text
active suggestion = activation/support
not reviewed knowledge
not action basis
```

### CP-003: `multi_stream_personal_knowledge_overview`

候选结论：

```text
个人 AI companion 可以从多个数据流构建动态个人知识概览。
```

公开摘要支持的是：

```text
multiple data streams
dynamic personalized knowledge overview
personalized insights / decision support
```

用户摘要里提到的具体数据源：

```text
chat / email / notes / video
```

这部分需要全文确认。

VAKS 可借：

```text
source intake can eventually accept more source types,
but every stream must keep provenance, permission, scope, and review state.
```

不借：

```text
不要自动扫用户私域数据。
不要让跨源聚合制造虚假独立证据。
不要让 personal graph 成为 truth graph。
```

### CP-004: `ai_knowledge_graph_as_activation_map`

候选结论：

```text
AI-driven knowledge graph 的主要价值可以是动态上下文地图。
```

VAKS 可借：

```text
graph/retrieval/cache/viewer can help activate:
  source anchors
  candidate ideas
  reviewed relations
  risks
  feedback
  decision history
```

必须保留：

```text
graph rank != trust
graph edge != reviewed relation
generated relation != support
```

### CP-005: `privacy_autonomy_guardrail`

候选结论：

```text
个人 AI companion 越主动、越多源，就越需要隐私、自主性和批判思考边界。
```

VAKS 可借：

```text
privacy and user autonomy are not product polish;
they are architecture constraints.
```

可转成 VAKS 规则：

```text
private source access requires explicit authorization
assistant memory writes are quarantined
feedback does not mutate truth
action basis requires separate gate
```

### CP-006: `human_judgment_not_replaced`

候选结论：

```text
AI companion 应增强人的判断，而不是替代人的判断。
```

VAKS 可借：

```text
answer preparation can surface:
  what is supported
  what is candidate
  what is missing
  what is risky
  what needs review
```

但最终：

```text
review / decision / action gate remains separate.
```

### CP-007: `venue_prestige_not_truth`

候选结论：

```text
ACM/GROUP 身份说明来源质量较高，但不能直接变成 VAKS truth confidence。
```

VAKS 必须保留：

```text
publication venue = source metadata / review priority signal
not evidence support
not reviewed relation
not action basis
```

## Fusion Fit

### 对 VAKS 最强的帮助

```text
1. 给 VAKS 一个很清晰的下一代叙事：
   from vault to bounded personal AI companion.

2. 强化 activation/context-pack 层：
   资料库要能在当前任务里主动准备上下文。

3. 强化隐私与自主性：
   越 personal，越不能自动读、自动信、自动行动。

4. 强化 graph 边界：
   AI-driven graph 是 context map，不是 truth authority。
```

### 最小优雅吸收

现在先吸收一句：

```text
VAKS can become a bounded personal AI companion for context preparation,
while keeping truth/review/action gates separate.
```

中文：

```text
资料库可以主动帮你准备上下文，但不能替你相信、替你审核、替你行动。
```

不用现在吸收：

```text
完整本地服务器架构
自动读取聊天/邮件/视频
长期主动监控
全自动知识图谱构建
跨设备 companion runtime
```

这些需要全文锚点和单独架构评审。

## Open Questions

```text
1. VAKS 的 proactive suggestion 应该在哪些场景启动？
2. 哪些数据流可以进入 source intake，哪些必须保持私域隔离？
3. personal AI companion 的“主动”如何不越过 review/action gate？
4. graph/retrieval 层如何显示 uncertainty、candidate、reviewed、risk 的差异？
5. 全文里是否真的提出 data ingestion / graph construction / interaction 多层架构？
6. 全文里的 local server / encryption 设计是否足够具体，是否值得作为 VAKS privacy reference？
```

## Routing Hint

```yaml
route_to:
  - second-brain public story
  - activation-tier future design
  - context-pack preparation
  - agent memory quarantine
  - privacy and user autonomy guardrails
  - viewer / workbench / proactive suggestion UX
review_required_before:
  - reviewed pattern
  - architecture decision
  - private-source ingestion
  - proactive runtime implementation
  - action basis
```

## 不要误吸收

```text
不要因为 ACM/GROUP 就跳过 evidence-aware review。
不要把 AI companion 的建议当真值。
不要让多源数据流绕过 source card / provenance / consent。
不要把 generated personal knowledge graph 当 reviewed knowledge graph。
不要把 proactive AI 变成自动行动系统。
不要用“本地/加密”口号替代真实安全设计。
```

## Next Review Trigger

触发复查的条件：

```text
拿到 ACM PDF / authorized full-text
需要设计 VAKS personal AI companion 叙事
需要设计 proactive context preparation
需要设计多源 private data intake
需要设计本地 agent / MCP / viewer / cross-device runtime
```
