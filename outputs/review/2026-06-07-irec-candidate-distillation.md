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
  - raw/papers/2026-06-07-irec-source.md
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
  - activation-tier
  - context-pack-preparation
  - ai-pkm
  - metacognitive-recall
  - feedback-ledger
  - viewer-workbench
possible_project_refs:
  - verified-action-knowledge-system
point_anchor_refs:
  - source_ref: raw/papers/2026-06-07-irec-source.md
    selector_type: arxiv_abstract
    selector_value: "arXiv abstract lines 38-42: Insight Recall, dynamic knowledge graph, hybrid retrieval, LLM similarity, human-in-the-loop construction, Guided Inquiry, v1 note"
  - source_ref: raw/papers/2026-06-07-irec-source.md
    selector_type: tex_lines
    selector_value: "engtest.tex lines 132-186: core definitions and JITAI mapping"
  - source_ref: raw/papers/2026-06-07-irec-source.md
    selector_type: tex_lines
    selector_value: "engtest.tex lines 221-327: three-path recall, reranking, tag mapping, fallback"
  - source_ref: raw/papers/2026-06-07-irec-source.md
    selector_type: tex_lines
    selector_value: "engtest.tex lines 386-435: limitations, future work, code availability"
reference_layer_tag: ref/context-triggered-insight-recall
reference_layer_label_zh: 即时洞察召回
reference_layer_scope: "activation / reflection / AI-PKM design reference only"
borrow_value: strong
borrow_order:
  - "P1: JITAI framing for context-triggered recall: define decision point, tailoring variables, intervention options, decision rule, and the option to show nothing."
  - "P1: Treat personal past insights as activation scaffolds for reflection, not as reviewed truth or action support."
  - "P2: Hybrid retrieval shape: semantic vector + full-text keyword + tag/graph expansion, then multi-signal reranking."
  - "P2: Human-in-the-loop tag mapping with LLM branch selection, precise selection, and explicit fallback."
  - "P3: Guided Inquiry as optional Socratic deepening after recall, useful only with fixation and evidence guardrails."
avoid:
  - "Do not treat recalled personal insight as a verified claim."
  - "Do not treat generated tags, graph edges, or similarity scores as reviewed relations."
  - "Do not copy Neo4j, static rerank weights, or proactive sensing into VAKS core just because the paper proposes them."
  - "Do not present Irec v1 as empirically validated; the paper itself says controlled studies and v2 code/reproducibility package are still future work."
  - "Do not let Guided Inquiry become an answer verifier or truth authority."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "Designing VAKS activation/context-pack/workbench features specifically around context-triggered recall of prior user insights."
  support_when: "Discussing AI-PKM, insight reuse, metacognitive scaffolds, query-time activation, or low-friction graph maintenance."
  risk_when: "Any recalled note, generated tag, similarity score, graph edge, or AI tutor dialogue starts being treated as evidence, truth confidence, reviewed relation, or action basis."
  cold_references:
    - raw/papers/2026-06-07-irec-source.md
tags:
  - candidate
  - provisional
  - irec
  - ai-pkm
  - metacognitive-scaffold
  - activation
  - context-triggered-recall
  - graph-is-activation-not-truth
  - candidate-only
---

# Candidate Distillation: Irec / Just-in-Time Insight Recall

## Boundary

This note is provisional orientation.

It distills Irec as an AI + PKM design reference for VAKS. It is not reviewed
knowledge, not a decision, not a formal pattern, and not action basis.

## 一句话

Irec 最值得借的不是某个数据库或算法，而是这句人话：

```text
人在新问题里卡住时，系统把他过去真正想通的那个“顿悟”及时拿回来。
```

对 VAKS 来说，这很像：

```text
activation/context pack 不只是找资料，
而是在当前问题旁边召回过去有用的思考痕迹。
```

但边界必须钉死：

```text
召回 = 帮人想起来
不等于证明它是真的
不等于可以直接行动
```

## 为什么相关

Irec 对 Obsidian / Logseq 类 PKM 的判断和 VAKS 当前问题很贴：

```text
双链和知识图谱能支持网络化思考，
但手动标签、链接、图谱维护会变成额外认知负担。
```

Irec 的解法是：

```text
personal learning history
-> dynamic knowledge graph
-> context-triggered retrieval
-> LLM similarity filtering
-> just-in-time insight presentation
-> optional Socratic guided inquiry
```

这不是 VAKS 的 truth layer。它更像 VAKS 的 activation / workbench / feedback
侧参考。

## Candidate Points

### CP-001: `context_triggered_insight_recall`

候选结论：

```text
有些历史笔记不该按固定时间复习，而该在当前上下文相似时被召回。
```

VAKS 可借：

```text
query / task / decision context
-> activate prior insight, prior mistake, prior review note, prior feedback event
-> present as reflection scaffold
```

不借：

```text
不把 recall 命中当 support。
不把 past insight 当 reviewed claim。
不把相似度当 confidence。
```

### CP-002: `insight_as_personal_cognitive_artifact`

候选结论：

```text
insight 是个人解题或工作过程里产生的思考产物，不是标准答案。
```

VAKS 可借：

```text
把使用过程中的 aha moment、踩坑、纠偏、复盘写成 feedback/candidate/use-memory 输入。
```

它可以帮助：

```text
activation
review routing
future query framing
project overlay hints
```

但不能直接帮助：

```text
truth confidence
reviewed relation
action basis
source reliability
```

### CP-003: `jitai_for_context_activation`

候选结论：

```text
JITAI 的六件事可以给 VAKS 的召回/干预设计一个轻量语言。
```

可借字段：

```text
distal_outcome: 长期目标是什么
proximal_outcome: 当下希望触发什么思考
decision_point: 什么时候判断要不要召回
intervention_options: 展示什么，或什么都不展示
tailoring_variables: 用哪些上下文变量
decision_rule: 用什么规则决定召回
```

特别值得借的是：

```text
providing nothing is a valid intervention option
```

人话：

```text
系统不确定时，安静也是一种好设计。
```

不借：

```text
不做默认常驻主动监控。
不因为 JITAI 听起来高级就把每个查询变成干预系统。
```

### CP-004: `hybrid_recall_plus_intent_reranking`

候选结论：

```text
召回可以分层：语义相似、关键词命中、标签/图谱扩展各自召回，再合并重排。
```

Irec 的原型形状：

```text
vector similarity
full-text keyword
tag hierarchy expansion
-> normalization / merge weights / multi-match bonus
-> learning mode adjusted reranking
```

VAKS 可借：

```text
low-level anchors + lexical lookup + reviewed/candidate neighborhood activation
mode-specific reranking: learning / review / balanced 类似于 task intent
multi-path hit = higher recall priority, not higher truth
```

不借：

```text
不把 Neo4j 作为 VAKS 必选底座。
不把静态权重写进架构核心。
不把多路命中当 evidence support。
```

### CP-005: `human_ai_tag_mapping_with_fallback`

候选结论：

```text
AI 可以降低标签和层级维护负担，但必须有人类确认和失败回退。
```

Irec 的思路：

```text
LLM first selects high-level branch
then maps to existing tag or suggests new tag
fallback uses similarity/confidence and hierarchy depth
```

VAKS 可借：

```text
source/candidate routing tags can be suggested by AI
stable high-level buckets should be preferred under uncertainty
new tag creation should be reviewable
```

不借：

```text
不让 LLM 标签创建 reviewed relations。
不让 tag hierarchy 反向定义 schema。
不让图谱清洁感替代证据支持。
```

### CP-006: `guided_inquiry_as_reflection_deepener`

候选结论：

```text
召回还不够时，可以把当前问题 + 历史 insight 交给 LLM 做苏格拉底式追问。
```

VAKS 可借：

```text
for learning / design / reflection mode:
  current question
  recalled prior insight
  known risk/gap
  ask user to compare, abstract, self-explain
```

边界：

```text
Guided Inquiry 是反思增强器，不是答案验证器。
```

### CP-007: `recall_can_fixate`

候选结论：

```text
过去的 insight 可能把人带回旧套路，也可能强化错误经验。
```

VAKS 必须保留这个风险：

```text
recalled insight should travel with challenge / scope / stale / contradiction hints when available
```

不借：

```text
不要只展示相似历史成功案例。
不要让 personal history 形成单人回音室。
不要让 AI tutor 继续强化错误前提。
```

## Fusion Fit

### 对当前 VAKS 最强的帮助

```text
Activation Tier / Context Pack:
  从“找相关资料”升级为“召回当前问题最该看见的旧思考痕迹”。

Feedback Ledger:
  用户纠错、顿悟、踩坑和成功迁移，都可以成为未来 activation 的候选输入。

Workbench / Obsidian View:
  可以显示 recall reason、source/candidate/reviewed boundary、risk hint，而不只是图谱连接。
```

### 最小优雅吸收

先只吸收一个轻规则：

```text
context-triggered recall is activation, not truth.
```

再加一个小字段思想：

```text
when_to_show_nothing: if recall confidence/support/scope is weak, do not interrupt.
```

不用现在引入：

```text
Neo4j runtime
automatic graph construction pipeline
proactive sensing
BCI/cognitive-load monitoring
static rerank formulas
learning analytics dashboard
```

## Open Questions

```text
1. VAKS 的 feedback event 里，哪些内容可视为 reusable insight？
2. recall reason 应该怎么显示，才能说明“为什么召回”，又不暗示“这是真的”？
3. recalled insight 是否需要绑定 risk/challenge/counterexample 一起展示？
4. future workbench 是否需要一个 mode：learning / review / action-prep / architecture-design？
5. v2 代码发布后，Irec 的真实实现质量、prompt、模型和测试包是否足够复查？
```

## Routing Hint

```yaml
route_to:
  - DEV_CONTEXT support reference
  - MEMORY_TIER / Activation Tier future design
  - SOURCE_INTAKE answer-preparation context envelope
  - FEEDBACK Ledger future insight reuse
  - Viewer / Obsidian workbench UX
review_required_before:
  - reviewed pattern
  - action basis
  - implementation commitment
  - mainline architecture merge
```

## 不要误吸收

```text
Irec 不是 VAKS 的 truth architecture。
Irec 不是证据审查系统。
Irec 不是“自动图谱 = 知识已整理好”的证明。
Irec v1 不是成熟开源实现。
Irec 的学习场景不能直接等同于 VAKS 的 action-facing 场景。
```

## Next Review Trigger

触发复查的条件：

```text
arXiv v2 发布
public GitHub repo 发布
reproducibility package 发布
出现受控实验或用户研究
VAKS 开始设计 activation / context-triggered recall / workbench recall reason
```
