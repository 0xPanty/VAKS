---
type: review_output
record_kind: video_source_set_candidate_distillation
status: candidate_only
created_at: 2026-06-12
created_by: Codex
source_set_title: 黄山是个老师 - 化学竞赛 AI 知识库双视频强蒸馏
source_family: bilibili-education-ai-knowledge-base
source_records:
  - raw/videos/2026-06-12-bilibili-bv1ujddbgeaf-chem-olympiad-knowledge-base-source.md
  - raw/videos/2026-06-12-bilibili-bv1rko5buefg-build-knowledge-base-from-zero-source.md
source_urls:
  - https://www.bilibili.com/video/BV1UJddBGEAf/
  - https://www.bilibili.com/video/BV1Rko5BuEFg/
author: 黄山是个老师
platform: bilibili
transcript_method: local_asr
asr_engine: faster-whisper
asr_model: small
asr_device: cuda
processing_tier: heavy
knowledge_status: candidate
overlay_state: candidate_only
review_pressure: review_due
promotion_gate: evidence_aware_review_required
action_basis_allowed: false
truth_mutation_allowed: false
review_priority: high
borrow_value: high
borrow_order: P1_candidate_for_intake_skill
fit_layers:
  - Capture
  - Understand
  - Connect
  - Activation
  - Context Pack
  - Use Ledger / Feedback
blocked_layers:
  - Reviewed Knowledge
  - Reviewed Relation
  - Action Basis
tags:
  - vaks-distill-candidate
  - video-source-set
  - ai-knowledge-base
  - education-knowledge-base
  - chemistry-olympiad
  - domain-spine-guided-ingestion
  - syllabus-scaffold
  - knowledge-digestion
  - candidate-relation-suggestion
  - association-activation
  - query-feedback-growth
  - hallucination-grounding
  - review-boundary-risk
---

# 黄山是个老师 - 化学竞赛 AI 知识库双视频强蒸馏

## 说人话结论

这两条视频讲的是同一套东西：作者想做一个化学竞赛老师自己的 AI 知识库。它不是把教材丢进 RAG 里等检索，而是把教材、考纲、题库“消化”成一个知识网络：PDF 转 Markdown，抽关键点，用考纲当骨架，把知识点挂上去，再让教材之间、题库考点之间产生关系。之后老师提问时，知识库从这个网络里找答案；问到新东西时，它会形成新的候选节点和关系，像一个会继续长的学科脑。

对我们 VAKS 来说，这个思路很值得借鉴，但必须换成我们的边界语言：它适合做 `入库技能` 的候选参考，不适合直接作为 truth 写入方式。我们可以借它的“领域骨架 + 消化 + 反馈生长”，但不能借它的“AI 自动建边就像已经懂了”。

一句话：这套视频对 VAKS 最大价值是把“入库”从保存资料，升级成“把资料挂到领域骨架上，生成候选点和候选关系，再通过提问反馈暴露缺口”；最大风险是把自动关联、引用和回答质量误当成 reviewed knowledge。

## Source Set

- `BV1UJddBGEAf`：构建化学竞赛知识库，2026-04-19，短展示版。
- `BV1Rko5BuEFg`：从零开始搭建知识库完整版，2026-04-24，完整动机和流程版。
- 作者/UP 主：黄山是个老师。
- 采集边界：公开 Bilibili 元数据和公开音频，无 cookies，无私有收藏，无会员内容。
- 字幕状态：未发现公开字幕。
- 转写方式：local faster-whisper small, cuda, float16。
- ASR 质量：主旨清楚，专名低置信。英文名、教材名、工具名、界面文案不能仅靠 ASR 入库。

## 查重结论

在写入前，已按两个 BVID、两个标题和作者名在本项目 `raw/`、`wiki/`、`outputs/` 中查重，未发现已有对应记录。因此本次按新 source set 处理。

这是本地项目内查重，不代表未来不会和其他已吸收概念发生 point collision。后续如果要提升为 pattern，仍需要走 REVIEW_QUEUE。

## Key Entity Confidence

```text
confirmed:
  - 视频 1: BV1UJddBGEAf / 构建化学竞赛知识库 / 2026-04-19 / 黄山是个老师
  - 视频 2: BV1Rko5BuEFg / 从零开始搭建知识库完整版 / 2026-04-24 / 黄山是个老师
  - 主题: 教师/化学竞赛知识库、教材/题库/考纲、AI 助教、知识点网络
  - 明确流程词: 上传资料、切割、向量化、PDF 转 Markdown、提取关键点、考纲关联、消化、题库分析、组卷

likely:
  - ASR 中 "Android Capracy" / "capacity" 大概率指 Karpathy 或作者借用的 Karpathy 式知识库想法，但未做画面 OCR。
  - ASR 中 "知识铺" 大概率为 "知识库"。
  - ASR 中 "相辆化" 大概率为 "向量化"。
  - ASR 中 "烤缸" 大概率为 "考纲"。
  - ASR 中 "engast" 大概率是 "ingest" 或作者口中的导入/消化。
  - ASR 中 "formal 焦虑" 大概率为 "FOMO 焦虑"。

unclear:
  - 具体产品/公司/工具名称。
  - 四本化学竞赛教材的准确书名。
  - 节点图背后的真实数据结构、关系生成算法、校验机制。
  - “小黄”智能体的实现方式。
```

## Source Anchors

- `raw/videos/2026-06-12-bilibili-bv1ujddbgeaf-chem-olympiad-knowledge-base-source/segments.md` 00:09-00:24：知识点来自教材或考纲，逻辑关系由 AI 构建，作者称为消化过程。
- `raw/videos/2026-06-12-bilibili-bv1ujddbgeaf-chem-olympiad-knowledge-base-source/segments.md` 00:46-00:52：作者称形成约 8000 节点、上万个逻辑关系。
- `raw/videos/2026-06-12-bilibili-bv1ujddbgeaf-chem-olympiad-knowledge-base-source/segments.md` 01:23-01:44：未知问题触发检索、新节点、新关系，知识库随问答变强。
- `raw/videos/2026-06-12-bilibili-bv1rko5buefg-build-knowledge-base-from-zero-source/segments.md` 01:14-01:51：教学场景不能放心让学生直接问大模型，幻觉是核心痛点。
- `raw/videos/2026-06-12-bilibili-bv1rko5buefg-build-knowledge-base-from-zero-source/segments.md` 02:01-02:22：普通知识库流程是上传资料、切割、向量化。
- `raw/videos/2026-06-12-bilibili-bv1rko5buefg-build-knowledge-base-from-zero-source/segments.md` 05:53-06:29：教材转 Markdown、提取关键点、用 2024 化学竞赛考纲关联。
- `raw/videos/2026-06-12-bilibili-bv1rko5buefg-build-knowledge-base-from-zero-source/segments.md` 07:31-07:58：15 分钟导入第三本物化教材，完成格式转换、公式整理、章节切割、考纲双向连接。
- `raw/videos/2026-06-12-bilibili-bv1rko5buefg-build-knowledge-base-from-zero-source/segments.md` 08:00-08:24：提问越多，知识库越知道如何关联，作者称它越来越懂化学。

## 最值得借鉴的点

### 1. Domain Spine Guided Ingestion

作者真正厉害的地方不是“用了知识库”，而是用 `考纲` 充当领域骨架。教材不是孤立上传，而是被抽成关键点后挂到考纲条目上；同一条目下的新点自然形成候选关系，教材之间也能在考纲外补充关系。

映射到 VAKS：

```text
source capture
-> candidate point extraction
-> domain spine mapping
-> candidate relation suggestion
-> review_due / activation candidate
```

这可以直接启发我们的入库技能：不同领域应该允许有自己的 `domain_spine`，比如考纲、课程标准、项目模块树、法条体系、API surface、产品功能树。入库时先问“挂到哪个骨架”，比事后靠搜索补关联更稳。

### 2. Digest Before Retrieve

普通 RAG 是上传、切块、向量化；作者强调的是“消化”：转 Markdown、抽关键点、整理公式/化学式、章节切割、挂考纲、建关系。

VAKS 应吸收这个动词，但重新定义边界：

```text
digest = normalize + extract candidate points + anchor to source + map to domain spine + suggest relations + mark uncertainty
```

它不是 review，也不是 truth mutation。

### 3. Query Feedback Growth

作者最有生命力的想法是：知识库被问得越多，越知道哪里缺、哪里相关，甚至长新节点。

VAKS 已经有类似骨架，但要落成我们的规则：

```text
good answer -> usage evidence / activation hint
bad answer -> feedback_event / review_due
unknown question -> missing_evidence or missing_point candidate
repeated query cluster -> synthesis_needed
new node -> candidate point only
new edge -> candidate relation suggestion only
```

这能直接强化 `Use Ledger / Feedback`：反馈改善 activation、usefulness、scope fit，不直接改 truth confidence。

### 4. Question Bank As Workbench Corpus

题库在作者这里不只是资料来源，而是工作台数据：问某考点考过几次、有哪些考法、考点分布、甚至组卷。

VAKS 可以借鉴为：

```text
raw question bank
-> candidate topic tagging
-> coverage / frequency workbench
-> teaching action draft
-> evidence/context pack
-> teacher review
```

但组卷和答疑是 `Decision / Action`，不能直接从 raw/candidate 出最终依据。

### 5. Expert Workflow Externalization

作者提到资深教师脑子里本来就有一套体系，调教知识库也会让老师更理解自己的工作流和方法论。

这对我们很关键：入库技能不只是“把材料变成笔记”，还可以逼出专家的隐性结构。VAKS 可以把这种专家结构存成候选的 `workflow pattern`、`domain spine`、`decision heuristic`，但要和 evidence/review 分开。

## 和 VAKS 当前架构的对应关系

```text
Capture:
  教材、考纲、题库、视频转写、元数据、ledger。

Understand:
  PDF/文本归一化、Markdown 化、关键点抽取、候选摘要。

Knowledge Calibration / Point Collision:
  新材料和考纲条目、旧节点、题库统计发生冲突或重复时，进入 review_due。

Review / Consolidation:
  教学结论、强关系、考点判断、组卷依据需要 Evidence Packet，不因 AI 自动建边而通过。

Association / Reviewed Relations:
  自动生成的边只是 candidate relation suggestion；只有 reviewed relation 才能支撑 action。

Activation / Context Pack:
  提问时激活教材段落、考纲条目、题库样例、候选点、风险提示、已有决策。

Decision / Action:
  答疑、讲义、PPT、组卷、教学设计是 action/workbench 输出，需要来源锚点和人工复核。

Use Ledger / Feedback:
  学生/教师追问、纠错、满意度、缺口暴露写入 feedback/use ledger，推动再 review 或再消化。
```

## 我们已经有的类似逻辑

有，而且比作者视频里的边界更严：

- VAKS 的 `Capture -> Understand -> Review -> Connect -> Act and Learn` 已经覆盖 source、candidate、review、relation、action、feedback。
- `Point Collision` 类似作者说的“问到没有的节点”，但我们把它当 review input。
- `Association / Activation` 类似作者的知识网络激活，但我们明确它不是 truth。
- `Use Ledger / Feedback` 类似作者的“越问越聪明”，但我们只允许它改善激活和暴露缺口，不直接改置信度。
- `Evidence Support Check / Evidence Packet` 是我们比这套视频更硬的地方：有出处不等于证据支持，有链接不等于支持了这个点。

所以这条资料不是推翻 VAKS，而是给 VAKS 的“入库技能体验层”提供了一个很好用的领域样板。

## 不能照搬的地方

- `有引用` 不能等于 `可靠`：引用可能只是召回到了附近内容，未必支持具体结论。
- `答案来自资料` 不能等于 `不会幻觉`：抽取、拼接、推理、统计都可能错。
- `AI 自动建关系` 不能等于 `reviewed relation`。
- `节点多、边多` 不能等于 `知识强`；它最多说明覆盖和连接规模。
- `问得越多越聪明` 不能直接写进主库；要变成 feedback_event、missing_point、review_due、synthesis_needed。
- 教材/题库导入涉及版权和教学风险，不能当成默认可复制实践。

## Candidate Points

### CP1 - 领域骨架比文件夹更适合做入库锚点

教育知识库可以用考纲/课程标准作为 `domain_spine`，把教材和题库材料挂到稳定的领域骨架上，而不是只按来源文件夹组织。

```yaml
candidate_status: review_due
fit: high
vaks_layer: Understand / Connect
possible_pattern: domain-spine-guided-ingestion
needs_review:
  - domain_spine 如何建模
  - source anchor 如何保留
  - 自动挂靠错误如何回收
```

### CP2 - 消化比向量化更接近 VAKS 入库目标

入库应该包含格式归一、候选点抽取、来源锚点、领域挂靠和候选关系建议；向量化只是 retrieval substrate，不是知识理解本身。

```yaml
candidate_status: review_due
fit: high
vaks_layer: Capture / Understand
possible_pattern: digest-before-retrieve
```

### CP3 - 查询反馈可以驱动候选增长，但不能驱动 truth mutation

用户问题暴露的未知点、重复点、冲突点和满意/不满意反馈，可以生成新候选点、review_due、synthesis_needed 或 activation hint。

```yaml
candidate_status: review_due
fit: high
vaks_layer: Use Ledger / Feedback
hard_boundary: no_direct_truth_mutation
```

### CP4 - 题库是 action workbench，不只是 source

题库可以用于考点分布、频次、考法归纳和组卷草稿，但这些输出属于 action/workbench，需要 context pack、来源锚点和人工复核。

```yaml
candidate_status: review_due
fit: medium_high
vaks_layer: Decision / Action
risk: teaching_misguidance
```

### CP5 - 专家方法论可以通过入库过程被显化

资深教师调教知识库时，会把隐性教学判断、分类方式和工作流说出来；这类内容应作为 candidate workflow/pattern 进入资料库，而不是混入事实层。

```yaml
candidate_status: review_due
fit: high
vaks_layer: Understand / Feedback
```

### CP6 - 自动关系网络适合做 activation map，不适合做 reviewed graph

作者展示的知识网络很像 VAKS 的 association neighborhood，但在我们这里只能作为激活地图或候选关系图，不能直接成为 reviewed relation graph。

```yaml
candidate_status: review_due
fit: high
vaks_layer: Association / Activation
hard_boundary: graph_rank_is_not_trust
```

## Suggested Labels For VAKS

这些标签是按我们当前架构写的，避免泛标签：

```yaml
architecture_tags:
  - domain-spine-guided-ingestion
  - digest-before-retrieve
  - syllabus-scaffold
  - candidate-point-extraction
  - candidate-relation-suggestion
  - association-neighborhood-activation
  - query-feedback-growth
  - question-bank-workbench
  - expert-workflow-externalization
  - hallucination-grounding-risk
  - source-grounding-not-truth
  - reviewed-relation-boundary
  - no-direct-truth-mutation

intake_skill_tags:
  - source-normalization
  - pdf-to-markdown
  - domain-anchor-mapping
  - source-anchor-retention
  - uncertainty-labeling
  - review-due-routing
  - use-ledger-feedback

risk_tags:
  - asr-entity-low-confidence
  - citation-is-not-support
  - auto-linking-risk
  - teaching-action-risk
  - copyrighted-corpus-risk
```

## Adoption Judgment

```yaml
borrow_value: high
adoption_now: candidate_only
recommended_next_action: create_candidate_pattern_after_user_confirmation
pattern_candidate:
  id: domain-spine-guided-ingestion
  summary: Use a domain spine such as syllabus, module tree, law taxonomy, API surface, or product function map to anchor source digestion before retrieval.
why_not_promote_now:
  - videos are ASR-derived
  - exact tool implementation is unclear
  - claims about reliability need evidence-aware review
  - VAKS boundary must be preserved
```

## Review Queue Suggestion

建议后续进入 REVIEW_QUEUE，但现在不自动写入 reviewed pattern：

```yaml
queue_item_type: synthesis_needed
priority: high
reason: Two related videos provide a concrete domain-ingestion pattern that can improve VAKS intake skills.
candidate_pattern: domain-spine-guided-ingestion
collision_check:
  - GraphRAG / LightRAG: graph retrieval inspiration, but graph rank is not trust.
  - HippoRAG: association activation inspiration, but activation is not support.
  - RKA: review queue and decision gates, but runtime/actions are not truth.
  - Karpathy LLM Wiki: wiki maintenance inspiration, but not automatic truth promotion.
boundary:
  - candidate only
  - evidence-aware review required before promotion
  - no action basis
```

## Minimal Implementation Hint

如果之后要把它变成我们的入库技能，可以先做最小版本：

```text
1. Ask / infer domain_spine:
   - syllabus, module tree, product area, API surface, legal taxonomy, project architecture map.

2. Normalize source:
   - PDF/video/article/repo -> text/Markdown/source card.

3. Extract candidate points:
   - atomic point + source anchor + uncertainty.

4. Map to domain spine:
   - candidate anchor only; low confidence mappings must be marked.

5. Suggest relations:
   - same spine item, cross-source support/challenge, prerequisite, overlap, missing evidence.

6. Route:
   - raw only, candidate, review_due, synthesis_needed, missing_evidence.

7. Feedback:
   - query success/failure/unknown/correction updates activation and review pressure only.
```

这正好对应我们现在的原则：普通 capture 轻，promotion 严，action basis 可审计。

## Boundary Statement

本文件是候选蒸馏，不是 reviewed knowledge。它可以用于后续架构讨论、入库技能设计和 REVIEW_QUEUE 路由；不能作为事实判断、教学输出、正式 pattern 或 action basis。
