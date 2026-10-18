---
type: review_output
record_kind: candidate_distillation
status: candidate_only
provisional: true
created_at: 2026-06-13
created_by: Codex
source_title: 如何用一套流程搞定读书笔记 ：2 年读书笔记实践分享
source_ref: raw/videos/2026-06-13-bilibili-BV1tNLG6pEJJ-book-note-workflow-source.md
source_record: raw/videos/2026-06-13-bilibili-BV1tNLG6pEJJ-book-note-workflow-source.md
source_url: https://www.bilibili.com/video/BV1tNLG6pEJJ/
author: reminds_AI卡片笔记
platform: bilibili
transcript_method: local_asr
asr_engine: openai-whisper
asr_model: small
processing_tier: medium
knowledge_status: candidate
overlay_state: none
review_pressure: review_due
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: review_input_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
review_priority: high
borrow_value: strong
borrow_order: P1_candidate_for_reading_source_intake_loop
fit_layers:
  - Capture / Provenance
  - Candidate Comprehension
  - Knowledge Calibration / Point Collision
  - Association / Activation
  - Context Pack
  - Use Ledger / Feedback
  - Cooling / Reactivation
  - UI / Workbench
blocked_layers:
  - Reviewed Knowledge
  - Reviewed Relation
  - Truth Confidence
  - Action Basis
tags:
  - vaks-distill-candidate
  - book-note-workflow
  - reading-highlight-inbox
  - own-language-candidate-card
  - atomic-knowledge-card
  - quote-paraphrase-split
  - index-card-as-candidate-context-pack
  - whiteboard-synthesis-workbench
  - ai-framework-as-candidate-orientation
  - active-recall-feedback-loop
  - cross-source-association-candidate
  - remembered-is-not-truth
---

# 读书笔记流程强蒸馏

## 说人话结论

这条视频讲的是一套很完整的读书笔记加工链：先宽松捕获划线，再每天固定时间筛选，把有价值的内容改写成自己的话；一张卡片只放一个知识点；原文引用和自己转述分开；读完一本书后用白板和索引卡把全书串起来；之后每天主动回忆和迭代。

对 VAKS 来说，它最值得借的不是 reminds 这个工具，而是这条顺序：

```text
raw highlight
-> candidate comprehension card
-> source/quote/paraphrase split
-> index/synthesis card
-> active recall and rewrite
-> cross-source association candidate
-> review_due when evidence/action is needed
```

这和我们的架构很合：它补的是 `Capture -> Candidate Comprehension -> Association/Activation -> Use Ledger/Feedback` 之间的人侧工作流。但边界必须咬死：用自己的话写出来，不等于有证据；回顾得很熟，不等于是真的；AI 生成框架，不等于 reviewed relation。

## VAKS 现有类似逻辑

我们已经有这些相近层：

- `Capture / Provenance`：源记录、转写、来源、ledger。
- `Candidate Comprehension`：把原始材料理解成候选点。
- `Point Collision / Review Queue`：冲突、缺证据、低置信、综合需求进入队列。
- `Association / Activation`：相关材料被点亮，但 activation 不是 truth。
- `Context Pack`：为回答或行动聚合上下文。
- `Use Ledger / Feedback`：使用结果、失败、纠错、遗漏形成反馈。
- `Cooling / Reactivation`：冷却材料在需要时再激活。

这条视频补的是更细的人侧操作：

- 阅读时先不要重流程，先把触动点划下来。
- 整理时必须从原文摘录推进到自己的话。
- 每个知识点尽量原子化。
- 引用和转述分开，避免把原话、理解、总结混成一团。
- 一本书结束后做索引卡，连接分散卡片。
- 回顾时继续改写和压缩，而不是只“看一眼”。
- 跨书联想只先做候选关联。

## Source Anchors

- `raw/videos/2026-06-13-bilibili-BV1tNLG6pEJJ-book-note-workflow-source/segments.md` 00:17-01:47：旧方法是 Notion 长文档和原文划线，回顾压力大，最后看过就忘。
- `raw/videos/2026-06-13-bilibili-BV1tNLG6pEJJ-book-note-workflow-source/segments.md` 00:31-00:44：新方法是一张卡片一个知识点，最后用一张卡片把一本书的知识串起来。
- `raw/videos/2026-06-13-bilibili-BV1tNLG6pEJJ-book-note-workflow-source/segments.md` 02:14-03:08：微信读书划线/想法同步到 reminds 闪念箱，按章节聚合，再在整理时筛选。
- `raw/videos/2026-06-13-bilibili-BV1tNLG6pEJJ-book-note-workflow-source/segments.md` 03:10-04:02：每天早上半小时，用自己的话写卡片；写不出来先保留作者原话，回顾时再加工。
- `raw/videos/2026-06-13-bilibili-BV1tNLG6pEJJ-book-note-workflow-source/segments.md` 04:02-04:25：用书名标签管理笔记，原文引用用引用标签区分。
- `raw/videos/2026-06-13-bilibili-BV1tNLG6pEJJ-book-note-workflow-source/segments.md` 04:25-05:31：建立索引卡，把笔记拖到白板上分类，必要时用 AI 看框架角度，再自己写卡片串联整本书。
- `raw/videos/2026-06-13-bilibili-BV1tNLG6pEJJ-book-note-workflow-source/segments.md` 05:31-07:17：每天回顾 16 张卡片，主动回忆和填空式回顾，回顾中继续改写。
- `raw/videos/2026-06-13-bilibili-BV1tNLG6pEJJ-book-note-workflow-source/segments.md` 07:17-07:52：回顾时发生跨书联想，把不同书中的思考力观点连起来。

## 最值得借鉴的点

### 1. Highlight Inbox 只能算 Capture

作者的第一步是宽松划线：触动自己的、解决疑惑的、解释原理的、能实现的方法，先都划下来，整理时再筛选。

VAKS 可吸收为：

```text
highlight / clipping / transcript segment
= raw capture or source-like inbox
!= candidate point
!= reviewed knowledge
!= action basis
```

这对我们很关键。入库不要一开始就逼用户做重 review，但也不能把原始划线当知识。

### 2. Own-Language Rewrite 是 Candidate Comprehension

作者说用自己的话写出来，相当于一次练习和理解检验。这一点很适合 VAKS，但要加一句硬边界：

```text
own-language card = candidate comprehension
not = evidence support
not = truth confidence
```

我们可以借这个作为候选点生成规则：如果用户或模型还不能用自己的话说清楚，它就不应该进入候选点，只能留在 raw/inbox。

### 3. One Card One Knowledge Point

“一张卡片一个知识点”非常贴合 VAKS 的 candidate point 原子化。它能减少大段总结带来的混杂风险。

VAKS 标签可写成：

```yaml
architecture_tag: atomic-candidate-point
rule: one_card_one_candidate_point
risk_if_ignored: mixed_claims_hide_missing_evidence
```

### 4. Quote / Paraphrase Split

作者用书名标签管理卡片，用引用标签区分原文摘录。这个点值得直接吸收：

```text
direct_quote -> source anchor / quote item
own_words -> candidate comprehension
ai_summary -> model-generated candidate
review_packet -> evidence-aware support check
```

这是防止“原文、我的理解、AI 总结”搅成一锅的好办法。

### 5. Index Card 是候选 Context Pack

读完一本书后做索引卡，把全书知识串起来。对 VAKS 来说，它像一个轻量 context pack 或 synthesis card。

边界：

```text
index card = candidate synthesis / navigation layer
not = reviewed relation
not = evidence packet
not = final truth graph
```

索引卡可以帮人理解结构，但里面的关系要成为正式关系，仍然要经过 review。

### 6. Whiteboard Clustering 是 Synthesis Workbench

把卡片拖到白板上移动、分类、找框架，这不是知识本体，而是一个 workbench。VAKS 可以借这个做候选点聚类和冲突发现。

适合放在：

```text
outputs/review workbench
review queue triage
candidate point clustering
context pack preparation
```

不适合直接写入 reviewed graph。

### 7. AI Framework 只能做候选视角

作者卡住时会让 AI 生成一个框架，看 AI 从哪个角度处理。这个用法很健康：AI 给视角，人自己判断和重写。

VAKS 可借：

```text
AI generated framework
-> candidate orientation
-> compare with source anchors
-> human/model review
-> possible index card draft
```

不能做：

```text
AI framework -> final taxonomy
AI framework -> reviewed relation
AI framework -> action basis
```

### 8. Active Recall 是 Activation / Feedback，不是 Truth

每天 16 张卡片、15-30 分钟回顾、AI 挖空填空、主动回忆，这些都适合进入 VAKS 的人侧 activation。

边界必须明确：

```text
forgot / hard / wrong / revised
-> feedback event
-> reactivation schedule
-> maybe review_due
-> never truth confidence
```

记得越熟，只能说明它对用户更可调用，不能说明它更真实。

### 9. Cross-Book Spark 是 Association Candidate

作者在回顾时由《认知觉醒》想到《为什么学生不喜欢上学》，产生“阅读/事实性知识/思考力”的连接。这很像 VAKS 的 Association Neighborhood Activation。

但它仍是候选关系：

```text
cross-source spark
-> association candidate
-> source anchors from both sides
-> scope/risk check
-> reviewed relation only after review
```

## Suggested Labels For VAKS

```yaml
architecture_tags:
  - reading-highlight-inbox
  - source-like-raw-capture
  - own-language-candidate-comprehension
  - atomic-candidate-point
  - quote-paraphrase-split
  - source-anchor-preservation
  - book-index-card
  - index-card-as-candidate-context-pack
  - whiteboard-synthesis-workbench
  - ai-framework-as-candidate-orientation
  - active-recall-reactivation
  - review-time-rewrite
  - cross-source-association-candidate
  - remembered-is-not-truth
  - comprehension-is-not-evidence
  - capture-is-not-learning
  - activation-is-not-truth

vaks_layers:
  - Capture / Provenance
  - Candidate Comprehension
  - Knowledge Calibration / Point Collision
  - Review Queue
  - Association / Activation
  - Context Pack
  - Use Ledger / Feedback
  - Cooling / Reactivation
  - UI / Workbench

risk_tags:
  - tool-lock-in-risk
  - asr-entity-error-risk
  - ai-framework-overfit-risk
  - quote-source-boundary-risk
  - fluent-recall-not-evidence
  - unsourced-synthesis-risk

promotion_gates:
  - source_anchor_required
  - quote_vs_paraphrase_required
  - evidence_packet_required_for_promotion
  - reviewed_relation_required_for_graph_edge
  - use_feedback_cannot_change_truth
```

## Candidate Points

### CP1 - 阅读划线应进入 raw/inbox，而不是直接进知识层

划线阶段适合宽进，降低捕获摩擦；筛选、重写和证据检查应该发生在后面。

```yaml
candidate_status: review_due
fit: high
layer: Capture / Provenance
rule: highlight_is_raw_capture
```

### CP2 - 用自己的话重写是 VAKS 的候选理解门槛

如果一个点不能被重新说清楚，它更适合留在 source excerpt 或 pending comprehension，而不是进入 candidate point。

```yaml
candidate_status: review_due
fit: high
layer: Candidate Comprehension
hard_boundary: comprehension_is_not_evidence
```

### CP3 - 一张卡片一个知识点可作为候选点原子化规则

一个 candidate point 不应混合多个判断、方法、事实、建议，否则后续 evidence support 和 point collision 都会变难。

```yaml
candidate_status: review_due
fit: high
possible_pattern: atomic-candidate-point
```

### CP4 - 原文引用、自己转述、AI 总结必须分层

引用可以保留 source voice；转述可以保留理解；AI 总结只能候选。三者不能互相冒充。

```yaml
candidate_status: review_due
fit: critical_boundary
possible_pattern: quote-paraphrase-split
```

### CP5 - 索引卡可以作为候选 context pack

一本书的索引卡适合做导航、结构化理解和后续 context pack seed，但不能跳过 evidence-aware review。

```yaml
candidate_status: review_due
fit: medium_high
layer: Context Pack / Synthesis
blocked: reviewed_relation
```

### CP6 - 每日回顾可进入 feedback/reactivation

主动回忆、忘记、填错、重写、压缩表达，都能产生使用反馈和再激活节奏。

```yaml
candidate_status: review_due
fit: high
layer: Use Ledger / Cooling / Reactivation
hard_boundary: remembered_is_not_truth
```

### CP7 - 跨书联想应先进 association candidate

跨来源火花很有价值，但必须保留两边 source anchor，不能直接变成 reviewed graph edge。

```yaml
candidate_status: review_due
fit: high
layer: Association / Point Collision
promotion_gate: reviewed_relation_required
```

## Adoption Judgment

```yaml
borrow_value: strong
borrow_order: P1_candidate_for_reading_source_intake_loop
adoption_now: candidate_only
schema_change_now: no
recommended_shape:
  - add as reference pattern for future reading/source intake workflow
  - keep source/highlight inbox light
  - require own-language candidate card before review queue
  - preserve quote/paraphrase/model-output distinction
  - treat index cards as candidate context packs
  - treat daily recall as activation/use-feedback
must_not_do:
  - do not treat highlights as reviewed knowledge
  - do not treat own-language rewrite as evidence support
  - do not let AI framework create reviewed relations
  - do not let recall metrics update truth confidence
  - do not depend on reminds as VAKS core runtime
```

## Minimal Absorption Suggestion

暂时不要改 schema。先把它作为 `reading-source-intake-loop` 候选模式放进 review queue：未来如果要做“普通读书/文章/视频轻量入库”的用户流程，可以借它的顺序：

```text
1. raw highlight inbox
2. own-language candidate card
3. quote/paraphrase/model-output split
4. index card as candidate context pack
5. active recall as feedback/reactivation
6. association candidate with source anchors
```

这条适合做 VAKS 的用户侧 intake/workbench 参考，不适合进 truth core。
