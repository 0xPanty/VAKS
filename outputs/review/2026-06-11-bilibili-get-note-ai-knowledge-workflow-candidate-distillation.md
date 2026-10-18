---
type: candidate_distillation
record_kind: candidate_distillation
status: draft
provisional: true
title: "Get 笔记展示了消费级 AI 知识库的轻 capture 和问答闭环"
created_at: "2026-06-11"
created_by: Codex
processing_tier: medium
knowledge_status: candidate
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: none
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
v0_2_13_trigger: no
derived_from:
  - raw/videos/2026-06-11-bilibili-bv1kfea6keqy-source.md
projects:
  - verified-action-knowledge-system
topics:
  - ai-note
  - capture
  - source-grounded-qa
  - retrieval-workbench
  - context-pack
  - subscription-intake
  - consumer-knowledge-base
borrow_value: medium
borrow_order: P2
evidence_strength: low-medium
routing_hint:
  - retrieval-layer-workbench
  - capture-inbox
  - source-grounded-qa
possible_project_refs:
  - outputs/review/vaks-retrieval-layer-design-2026-06-11/
point_anchor_refs:
  - raw/videos/2026-06-11-bilibili-bv1kfea6keqy-source.md#可抽取-candidate-points
tags:
  - candidate-only
  - source-distillation
  - design-only
  - vaks-borrow-P2
---

# 候选蒸馏：Get 笔记展示了消费级 AI 知识库的轻 capture 和问答闭环

## 一句话

这条视频对 VAKS 的借鉴是 P2：它不是证据治理方案，但很好地展示了普通用户想要的知识库体验：

```text
先别让我分类、打标签、写模板。
让我把语音、链接、图片、文件丢进去。
系统先帮我整理，再让我按主题问、按来源看、最后加工成输出。
```

VAKS 可以借鉴它的轻入口和问答体验，但必须保留 raw / candidate / reviewed / action-basis 边界。

## Borrow Tag

```yaml
borrow_value: medium
borrow_order: P2
borrow_scope:
  - light-capture
  - inbox
  - multimodal-input
  - source-grounded-qa
  - single-source-drilldown
  - context-pack-qa
  - subscription-intake-as-future-lane
not_borrow_scope:
  - reviewed truth
  - evidence support
  - reviewed relation
  - action basis
  - source-of-truth storage
```

## Candidate Point

VAKS 的用户入口可以借鉴 Get 笔记的外层体验，但内部语义要更严格：

```text
Get 笔记式体验:
  丢进去 -> 自动整理 -> 建知识库 -> 自然语言问答 -> 输出

VAKS 化之后:
  capture -> raw/source -> candidate comprehension -> source-grounded activation
  -> review/sufficiency gate when needed -> action/use feedback
```

重点不是照搬产品，而是吸收一个 UX 原则：

```text
普通 capture 要轻。
严格治理要懒加载。
回答必须带来源。
来源不能自动等于证据支持。
```

## 应该吸收

- 多入口 capture：语音、链接、图片、文件都能先落到 raw/candidate。
- 自动整理优先服务“可读、可找、可继续处理”，不承担判真。
- 主题知识库适合作为 project workspace 或 scope filter。
- 单篇问答可以对应 source drilldown。
- 全库问答可以对应 context-pack QA。
- AI 回答应显示来源笔记/段落，帮助用户回查。
- 输出不是终点：AI 提供素材和框架，人再加工并记录使用反馈。

## 不应该吸收

- 不要让自动摘要、OCR、链接抓取直接创建 reviewed knowledge。
- 不要把平台私有知识库当 VAKS 的 source of truth。
- 不要把“回答标了来源”误当“证据支持已经成立”。
- 不要让订阅源自动写主库或污染检索默认范围。
- 不要用自然语言问答替代 Evidence Sufficiency Gate。
- 不要把视频中的免费/付费能力当稳定事实。

## 对 VAKS 检索层的具体启发

```text
检索结果不应该只是文件列表。

更好的形态:
  answer draft
  cited source anchors
  candidate/reviewed/action-basis badges
  source drilldown
  related notes
  known gaps
  next action options
```

Get 笔记的“单篇对话”和“全库对话”可以拆成 VAKS 两个能力：

```text
source drilldown:
  只围绕当前 source / transcript / note 追问。

context-pack QA:
  在明确范围内聚合多个 source 和 candidate/reviewed notes。
```

## 对 VAKS Capture 的具体启发

```text
Capture Inbox:
  voice_note
  link_note
  image_ocr
  file_upload
  subscription_item

每条进入时默认:
  knowledge_status: raw
  action_basis_allowed: false
  truth_mutation_allowed: false
```

订阅源可以作为未来 lane，但要加三道闸：

```text
dedupe:
  避免重复入库。

rate_limit / source_scope:
  避免自动信息洪水。

review_pressure only:
  自动订阅最多生成候选点和 review pressure，不能直接提升 truth。
```

## 与现有 VAKS 层级的关系

```text
Capture:
  最强借鉴点。低摩擦、多格式、先收进来。

Understand:
  自动整理、摘要、转写、OCR 属于 candidate comprehension。

Review:
  视频没有 review 机制；VAKS 必须补上 evidence-aware review。

Connect:
  自动关联只做 candidate_relation。

Activation / Context Pack:
  单篇问答和全库问答可作为激活层体验。

Decision / Action:
  行动清单只能是 draft，需要 action-basis gate。

Use Ledger / Feedback:
  用户把 AI 提取内容加工成输出后，记录结果、纠错和复用价值。
```

## Risk / Inhibition

```text
risk:
  自动整理制造过度信任。
  链接抓取和订阅源制造信息洪水。
  段落来源被误读成证据支持。
  平台私有化导致可迁移性和可审计性下降。
  模型能力和价格边界会变。

inhibition:
  所有输入默认 raw/candidate。
  来源锚点与 evidence support 分离。
  自动订阅默认进 inbox/sandbox。
  输出前按风险触发 sufficiency / scope / action gate。
  关键材料保留 Markdown 或项目可见 artifact。
```

## 融合判断

```text
fusion_decision: adapt / watch
borrow_value: medium
borrow_order: P2
evidence_strength: low-medium
implementation_cost: medium
integration_fit: medium-high
reversibility: high
```

## 后续行动

- 放入 VAKS 检索层 / capture workbench 的参考池。
- 当前不建议改 `SCHEMA.md`。
- 如果未来设计轻 capture 或 source-grounded QA，可把这条和已有的 Obsidian / cBrain / ai-reverse-toolkit 材料一起比较。
