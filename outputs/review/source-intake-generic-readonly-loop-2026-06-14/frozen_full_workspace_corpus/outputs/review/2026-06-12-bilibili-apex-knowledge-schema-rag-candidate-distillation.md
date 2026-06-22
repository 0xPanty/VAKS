---
type: candidate_distillation
record_kind: candidate_distillation
status: draft
provisional: true
title: "Apex Knowledge 视频：Schema-first 企业知识库与对象检索候选蒸馏"
created_at: "2026-06-12"
created_by: Codex
processing_tier: heavy
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
  - raw/videos/2026-06-12-bilibili-bv1jtgq6cese-source.md
  - raw/videos/2026-06-12-bilibili-bv1jtgq6cese-source/transcript.txt
  - outputs/review/project_lens_overlays/2026-06-12-apex-knowledge-schema-rag-retrieval-overlay.md
projects:
  - verified-action-knowledge-system
topics:
  - document-intake
  - schema-extraction
  - structured-retrieval
  - semantic-compression
  - retrieval-layer
  - action-boundary
borrow_value: strong
borrow_order:
  - "P1: schema-first document intake for vertical business documents"
  - "P1: dual representation: structured object plus semantic brief"
  - "P1: query-to-object-query before retrieval for structured business data"
  - "P2: cross-schema relation as candidate relation, not reviewed relation"
  - "P3: dynamic schema learning and multimodal parsing only after controlled pilots"
avoid:
  - "Do not treat extracted JSON fields as reviewed knowledge."
  - "Do not let semantic briefs count as evidence support."
  - "Do not let cross-schema/BOM relations become reviewed relations automatically."
  - "Do not let product-demo accuracy claims become benchmark evidence."
  - "Do not connect object retrieval to Agent action without action-basis gates."
evidence_strength: low-medium
routing_hint:
  - retrieval-layer-design
  - document-intake
  - schema-extraction
  - source-anchor-manifest
  - evidence-packet-prefill
possible_project_refs:
  - outputs/review/vaks-retrieval-layer-design-2026-06-11/
point_anchor_refs:
  - raw/videos/2026-06-12-bilibili-bv1jtgq6cese-source.md#可抽取-candidate-points
  - raw/videos/2026-06-12-bilibili-bv1jtgq6cese-source/segments.md#0000.43-0080.27
  - raw/videos/2026-06-12-bilibili-bv1jtgq6cese-source/segments.md#0216.31-0265.03
  - raw/videos/2026-06-12-bilibili-bv1jtgq6cese-source/segments.md#0313.03-0352.55
  - raw/videos/2026-06-12-bilibili-bv1jtgq6cese-source/segments.md#0732.92-0783.24
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "the active task is designing VAKS document intake, schema extraction, structured retrieval, or action-basis use of extracted fields"
  support_when: "comparing retrieval-layer candidates, designing source-anchor manifests, or drafting Evidence Packet prefill from documents"
  risk_when: "someone proposes treating extracted objects, semantic briefs, query results, or product-demo claims as reviewed support"
  cold_references:
    - raw/videos/2026-06-12-bilibili-bv1jtgq6cese-source.md
    - raw/videos/2026-06-12-bilibili-bv1jtgq6cese-source/transcript.txt
tags:
  - candidate-only
  - source-distillation
  - strong-borrow
  - schema-extraction
  - structured-retrieval
  - enterprise-knowledge-base
---

# 候选蒸馏：Schema-first 企业知识库与对象检索

## 一句话

这条视频对 VAKS 是强借鉴：它讲清楚了企业知识库里一个很关键的点：

```text
不是所有资料都适合先切块。
有些企业文档应该先抽成业务对象，再检索。
```

它比普通 RAG 多了一层：

```text
文档 -> Schema 抽取 -> JSON / 对象 -> brief -> 对象查询 + 语义召回
```

VAKS 可以借这个“结构化候选理解”路径，但必须加边界：抽出来的字段不是 reviewed truth，brief 不是证据，对象检索结果不是 action basis。

## 借鉴等级

```yaml
borrow_value: strong
borrow_order:
  P1:
    - schema-first document intake
    - structured object + semantic brief dual representation
    - natural-language query -> object query
  P2:
    - cross-schema candidate relation
    - domain-specific schema templates
  P3:
    - dynamic schema learning
    - multimodal / DXF / industrial drawing parsing
```

在 VAKS 借鉴池里的位置：

```text
不是 Obsidian 操作台参考。
不是证据治理参考。
它是 document-intake / retrieval-layer 的一线参考。
```

## Candidate Point 1: 对垂直企业文档，Schema-first 比 chunk-first 更强

普通 chunk-first 适合自然语言段落，但工业图纸、法律卷宗、制度、银行报告这类资料通常有固定业务结构。

视频的核心启发是：

```text
先识别文档类型。
再定义 / 选择领域 Schema。
再抽取字段和对象。
最后才进入检索。
```

VAKS 化之后应该是：

```text
raw source file
-> parser / extractor
-> candidate structured object
-> source-anchor manifest
-> candidate distillation / review queue
```

不要直接：

```text
PDF / 图纸 / 卷宗 -> 向量切块 -> 问答
```

## Candidate Point 2: 双表示很关键：JSON 对象 + semantic brief

视频补充了一个很好的细节：Schema JSON 不一定能让大模型理解“这个对象到底是什么”，所以要同时生成一个短 brief，存进向量库辅助语义召回。

这对 VAKS 很有价值：

```text
structured_object:
  stable fields
  values
  source anchors
  validation status

semantic_brief:
  short orientation
  retrieval activation
  human-readable description
```

边界必须写死：

```text
JSON object = candidate extraction
brief = activation / orientation
neither = reviewed evidence
```

## Candidate Point 3: 查询不能只做 vector similarity，要先转对象查询

视频说得很对：把 Schema JSON 丢进向量库再靠语义相似度搜，很多结构化问题搜不准。

比如用户问：

```text
找总高度 2000mm、带某种法兰座的图纸
```

这类问题需要：

```text
natural-language query
-> parse constraints
-> object query
-> retrieve candidates
-> optional semantic rerank / brief explanation
```

VAKS retrieval layer 可以吸收为：

```text
bucket filter first
intent / object query second
hybrid recall third
evidence/action gate last
```

## Candidate Point 4: Schema 抽取要进候选层，不进 truth 层

视频的 demo 语气容易让人觉得“抽成结构化就准确”。这正是 VAKS 要拦住的地方。

更稳的版本：

```yaml
record_kind: extracted_candidate_object
knowledge_status: candidate
source_file:
source_ranges:
schema_version:
extractor:
field_confidence:
validation_status: unreviewed | checked | disputed
action_basis_allowed: false
truth_mutation_allowed: false
```

字段级的可靠性必须回到 source anchor，而不是靠 JSON 的样子看起来严肃。

## Candidate Point 5: 跨 Schema 关联很有价值，但不能自动变 reviewed relation

视频提到图纸、BOM、上下游组件、产品之间的关系。这非常接近 VAKS 的 association / reviewed relation 主题。

可借：

```text
object A -> candidate relation -> object B
query expands through business relation
context pack includes related objects
```

不能借：

```text
系统推出来相关
-> 就是 reviewed relation
-> 可以支撑行动
```

VAKS 里应该是：

```text
cross-schema relation = candidate_relation_suggestions
reviewed relation = later evidence-aware review
```

## Candidate Point 6: 动态 Schema 学习是 P3，不是现在的主路

自动从文档中学习 Schema 很诱人，但风险也大：

```text
字段漂移
schema 污染
抽取口径变化
旧对象不可比
用户标签反馈被误当 truth
```

所以 VAKS 现在应该借它作为远期方向，而不是马上实现：

```text
schema suggestion
-> sandbox
-> sample extraction
-> human approval
-> versioned schema
-> migration / invalidation note
```

## 对 VAKS 的直接价值

| VAKS layer | Fit | Borrow |
|---|---:|---|
| Capture | High | 高价值文档要保留 source file、解析 artifact 和 source metadata。 |
| Understand | Very high | Schema extraction 是 candidate comprehension 的强形态。 |
| Review | Medium | 视频缺 review；VAKS 要补字段级 anchor / validation。 |
| Connect | High | 跨 Schema 关系适合 candidate relation。 |
| Activation / Context Pack | High | object query + brief 可生成更准 anchor queue。 |
| Decision / Action | Risky | Agent/业务流程必须走 action-basis gate。 |
| Feedback | Medium | 用户纠错可改善 extractor/schema/query，不直接改 truth。 |

## 对当前 VAKS 的挑战

这条视频提醒我们：如果 VAKS 未来处理企业文档，只做 Markdown 摘要和普通向量检索是不够的。

我们需要至少保留这个设计位置：

```text
raw document
-> candidate structured object
-> field anchors
-> semantic brief
-> bucket-filtered retrieval
-> review/action gate
```

这个位置不一定现在主线化，但 retrieval-layer 设计里必须有它。

## 不应该吸收

- 不把 Schema JSON 当 reviewed knowledge。
- 不把 semantic brief 当 evidence support。
- 不把 object search result 当 action basis。
- 不把 demo 准确性当 benchmark。
- 不让动态 Schema 自动改主 schema。
- 不让跨 Schema 关联自动创建 reviewed relation。
- 不让 Agent 直接根据 candidate object 执行业务流程。

## 融合判断

```yaml
fusion_decision: adapt_as_candidate_design
borrow_value: strong
borrow_order: P1_for_document_intake_and_retrieval_layer
evidence_strength: low-medium
implementation_cost: medium-high
integration_fit: high
reversibility: medium
mainline_change_now: no
needs_pilot_before_adoption: yes
```

## 建议最小试验

```text
选一种文档类型：
  例如制度条款、合同条款、论文方法卡、软件项目 README。

定义一个很小的 schema：
  5-8 个字段，不要贪多。

抽取候选对象：
  每个字段必须带 source anchor。

生成 brief：
  brief 只进 activation，不进 evidence。

做 10 个查询：
  比较普通 chunk / vector / schema object query。

验收：
  看 recall、字段正确率、source-anchor correctness、boundary violation。
```

## 后续行动

- 放入 VAKS retrieval-layer design 的 P1 参考池。
- 当前不改 `SCHEMA.md`。
- 若未来做 document-intake pilot，优先复用这条的“双表示 + 字段锚点 + 对象查询”。
