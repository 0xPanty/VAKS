---
type: source
status: source-captured
title: '从零开始搭建知识库完整版'
source_id: bilibili-BV1Rko5BuEFg
source_uri: bilibili:BV1Rko5BuEFg
source_url: https://www.bilibili.com/video/BV1Rko5BuEFg/
source_type: video
platform: bilibili
platform_id: BV1Rko5BuEFg
author: '黄山是个老师'
publisher: '黄山是个老师'
published_at: '2026-04-24 16:29:25 +0800'
updated_at:
duration: 603s
captured_at: '2026-06-12 20:42:28 +08:00'
captured_by: Codex
raw_location: raw/videos/2026-06-12-bilibili-bv1rko5buefg-build-knowledge-base-from-zero-source.md
processing_mode: runner
processing_level: heavy
processing_tier: heavy
knowledge_status: raw
overlay_state: none
review_pressure: review_due
retrieval_policy:
  policy_kind: source_with_candidate_comprehension
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: source_card_not_reviewed_knowledge
promotion_gate: evidence_aware_review_required
action_basis_allowed: false
truth_mutation_allowed: false
review_priority: high
review_owner: Codex
formalization_status: raw-only
access_boundary: public
transcript_method: local_asr
transcript_location: raw/videos/2026-06-12-bilibili-bv1rko5buefg-build-knowledge-base-from-zero-source/transcript.txt
segments_location: raw/videos/2026-06-12-bilibili-bv1rko5buefg-build-knowledge-base-from-zero-source/segments.md
transcript_metadata_location: raw/videos/2026-06-12-bilibili-bv1rko5buefg-build-knowledge-base-from-zero-source/transcript-meta.json
ledger_location: raw/videos/2026-06-12-bilibili-bv1rko5buefg-build-knowledge-base-from-zero-source/acquisition-ledger.json
media_retention: deleted
source_status: active
topics:
  - video-intake
  - bilibili
  - ai-knowledge-base
  - education-knowledge-base
  - chemistry-olympiad
  - domain-spine
  - syllabus-scaffold
  - knowledge-digestion
  - source-grounded-answering
  - question-bank-analysis
  - query-feedback-growth
  - vaks-reference
projects:
  - verified-action-knowledge-system
source_family: bilibili-education-ai-knowledge-base
upstream_sources: []
verification_status: unverified
candidate_relation_suggestions: []
tags:
  - raw-video
  - bilibili
  - candidate-only
  - source-set-huangshan-knowledge-base
  - vaks-distill-candidate
---

# 从零开始搭建知识库完整版

## 为什么收录

这是同一作者知识库思路的完整版，补足了短视频没有讲清楚的动机和流程：教学场景怕大模型幻觉，所以用自有材料做知识库；普通 RAG 只上传、切块、向量化，维护成本高；作者进一步用智能体把教材转 Markdown、抽关键点、挂到 2024 化学竞赛考纲上，再建立教材间与考纲内外的关联。

这条对 VAKS 的强借鉴点是“用领域骨架管理 source digest”：不是先堆资料，而是先有考纲/任务骨架，再让新材料挂靠、补边、暴露缺口。它很适合作为我们未来“入库技能”的参考，但必须保留 candidate-only 和 review gate。

## 来源卡

- 平台：Bilibili
- 原始链接：https://www.bilibili.com/video/BV1Rko5BuEFg/
- 标题：从零开始搭建知识库完整版
- 作者 / UP 主：黄山是个老师
- 发布时间：2026-04-24 16:29:25 +0800
- 视频时长：603s
- 收录时间：2026-06-12 20:42:28 +08:00
- 访问边界：public, no cookies

## Intake Boundary

```yaml
processing_tier: heavy
knowledge_status: raw
overlay_state: none
review_pressure: review_due
retrieval_policy:
  policy_kind: source_with_candidate_comprehension
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: source_card_not_reviewed_knowledge
promotion_gate: evidence_aware_review_required
action_basis_allowed: false
truth_mutation_allowed: false
```

Video source records provide provenance, transcript location, and findability.
They do not create reviewed evidence, project borrowing conclusions, or action
basis.

## 获取与转写

```yaml
subtitle_status: no_public_subtitle_found
transcript_method: local_asr
asr_model: faster-whisper small
asr_device: cuda / float16
transcript_quality: medium
media_retention: deleted
scratch_cleanup: temporary audio deleted; retained text artifacts copied into project
project_visible_artifacts: yes
transcript_metadata_location: raw/videos/2026-06-12-bilibili-bv1rko5buefg-build-knowledge-base-from-zero-source/transcript-meta.json
ledger_location: raw/videos/2026-06-12-bilibili-bv1rko5buefg-build-knowledge-base-from-zero-source/acquisition-ledger.json
```

字幕 / ASR 是 raw/source text，不是 reviewed evidence。AI 摘要是 candidate comprehension，不是 truth。

## 人话摘要

作者从教师视角解释为什么要搭知识库：大模型能回答很多问题，但教学场景不能容忍幻觉；简单知识库把资料上传、切割、向量化，能让回答来自指定材料，但如果模型不懂领域，前期切分、标注、更新会很费人力。后来他把教材、题库、考纲放进更智能的知识库/智能体流程：教材转 Markdown，提取关键点，先和 2024 化学竞赛考纲关联，再让同一考纲条目下的新知识点、不同教材之间的相关点互相连接。作者把这个叫“消化”。

最有意思的是：作者不是只想避免幻觉，而是想让知识库像老师/学生一样学习一个学科。它把教材和题库变成可提问、可分析、可组卷、可继续生长的领域脑。对 VAKS 来说，这是很好的“领域资料库入库技能”素材，但我们要把自动化增长限制在候选层和反馈层。

## 关键实体置信度

```text
confirmed:
  - BVID: BV1Rko5BuEFg
  - 标题: 从零开始搭建知识库完整版
  - 作者 / UP 主: 黄山是个老师
  - 发布时间: 2026-04-24 16:29:25 +0800
  - 主题: 教师/化学竞赛知识库搭建、教材/题库/考纲 ingest、知识点关联、AI 助教
  - 转写方式: public audio -> local faster-whisper small ASR
  - 作者明确提到: 上传资料、切割、向量化、PDF 转 Markdown、提取关键点、考纲关联、题库分析、组卷

likely:
  - ASR 中 "capacity" 大概率仍指 Karpathy 相关思路或作者上一条视频中的三层结构知识库，但未做画面 OCR。
  - "知识铺" 多处大概率是 "知识库"。
  - "相辆化" 大概率是 "向量化"。
  - "烤缸" 大概率是 "考纲"。
  - "engast" 大概率是 "ingest" 或作者口中的导入/消化动作。
  - "formal 焦虑" 大概率是 "FOMO 焦虑"。

unclear:
  - 具体使用的国内公司、产品、工具名未确认。
  - "笔记本" 可能指某类 NotebookLM-like 工具，但不能直接写成特定产品。
  - "能工智人" 可能是 ASR 错误，含义接近人工图书管理员/人工标注者。
  - "小黄" 是作者自己的智能体/助理称呼，具体实现未确认。

needs user visual check:
  - 视频画面中出现的工具名称、产品界面、教材名、考纲版本截图、节点图细节。
```

## 时间轴 / 分段

- 00:00-00:51：作者说明这是对上一条知识库视频的完整补充，同一套化学竞赛知识库思路。
- 01:14-01:51：动机是教师想用 AI 助教，但大模型幻觉在教学场景难以接受。
- 02:01-02:22：普通知识库原理：上传资料、切割、向量化；回答应来自导入资料。
- 02:24-03:05：普通方式的问题是建库过程需要大量人工，特别是领域模型不可靠时，切割和标注要人工做。
- 03:29-04:29：作者提到更智能的知识库/笔记本可以快速消化教材，每句话有引用出处，适合教师使用。
- 04:30-05:12：题库也可以导入，用于查询某考点出现次数、考法、分布，甚至辅助组卷。
- 05:28-06:29：作者最近用智能体手搓化学竞赛知识库：教材导入、PDF 转 Markdown、提取关键点、用 2024 考纲作锚点、把教材知识点拉到考纲相关条目。
- 06:29-07:29：知识点挂到同一考纲条目，也可在考纲之外建立教材间关系；消化完成后形成知识网络。
- 07:31-07:58：导入第三本物化教材，15 分钟完成 PDF 转 Markdown、公式/化学式整理、章节切割、考纲双向连接，并创建 8 个新考纲连接。
- 08:00-08:24：未来提问会从教材或知识库调取相关内容，生成相关页面；问得越多，知识库越懂化学。
- 08:24-08:54：作者认为这不只是避免幻觉，也是在让 Agent 学习人的专业体系；教师在调教助理时也更理解自己的工作流和方法论。
- 09:08-09:59：作者倡导先用工具创造价值，避免过度陷入取代/FOMO 焦虑。

## 视频里直接说了什么

- 教学场景下，大模型幻觉是关键痛点。
- 简单知识库的基础流程是上传资料、切割、向量化。
- 如果模型对专业理解有偏差，切割和标注需要大量人工。
- 教材和题库都可以导入知识库，用于答疑、考点统计、考法分析、组卷。
- 作者自己的做法是让智能体把教材转 Markdown，提取关键点，用 2024 化学竞赛考纲做关联锚点。
- 新知识点会与同一考纲条目下的内容发生关系，教材之间也能在考纲外建立关系。
- 作者把这个 ingest/吸收过程叫“消化”。
- 提问越多，知识库越知道其中的相关系，作者认为它会越来越懂化学。

## 我的理解 / 推断

这条视频提供了比短视频更完整的入库技能原型：

```text
source capture
-> format normalization: PDF -> Markdown
-> point extraction
-> domain spine mapping: syllabus / 考纲
-> local relation suggestion: same syllabus item
-> cross-source relation suggestion: textbook-to-textbook
-> retrieval / generated page
-> query feedback creates missing-point pressure
```

VAKS 已经有相似逻辑，但边界更严：作者的视频把“答案来自资料”“每句有出处”“越问越聪明”说得比较顺滑；我们要拆成 provenance、candidate comprehension、evidence support、reviewed relation、activation trace、feedback ledger 几层。

## 反漏提取检查

```text
pain point:
  - 教师想用 AI 助教，但学生答疑不能接受幻觉；普通知识库建库和更新成本高。

workflow:
  - 上传资料 -> 切割/向量化 -> 教材/题库问答 -> PDF 转 Markdown -> 抽关键点 -> 挂到考纲 -> 建立教材间关系 -> 提问反馈继续生长。

tools / plugins:
  - 具体产品未确认；确认存在 AI 知识库/笔记本工具和作者自建智能体“小黄”。

information structure:
  - 三类核心源: 教材、题库、考纲；核心结构: 考纲作骨架，教材知识点和题目挂载其上，跨教材补充边。

judgment mechanism:
  - 作者重视引用出处、题库统计、节点关系和使用反馈；缺少明确 evidence support check / reviewed relation gate。

user experience:
  - 教师用自然语言问考点、考法、题库覆盖、教材知识，知识库返回有来源的回答或生成相关页面。

automation boundary:
  - 作者允许智能体自动抽点、挂考纲、建边、越问越懂；VAKS 只能自动生成候选和反馈压力，不能自动改真。

risk:
  - 来源材料版权、ASR/界面识别错误、伪引用、伪关系、题库统计误差、教学误导风险。

fit for us:
  - 极适合 VAKS 的入库技能、领域骨架、candidate relation suggestion、activation feedback、question-bank workbench。

challenge to us:
  - 我们需要把“体验上像智能成长”拆成可审计的 candidate growth、review_due、feedback ledger，而不是为了体验牺牲边界。
```

## 可抽取 Candidate Points

- Candidate Point 1: 面向教学的知识库应优先解决“幻觉不可接受”问题，但 source grounding 只能降低风险，不能自动保证正确。
- Candidate Point 2: 领域骨架可以来自考纲/课程标准/能力模型，它比来源文件夹更适合作为教材和题库的挂靠结构。
- Candidate Point 3: 入库消化链路至少包含格式归一、知识点抽取、领域骨架映射、候选关系生成、来源锚点保留。
- Candidate Point 4: 题库不只是检索素材，也可以成为考点分布、考法分析和生成试卷的 workbench 数据源。
- Candidate Point 5: 专家教师调教知识库的过程会反过来显化自己的工作流和方法论。
- Candidate Point 6: 查询反馈应进入 missing_evidence / synthesis_needed / review_due，而不是自动写 reviewed truth。

## 可借鉴

- `syllabus_as_domain_spine`: 用考纲作为领域知识骨架。
- `digest_before_retrieve`: 入库时先做抽点和挂靠，不只是向量化。
- `question_bank_as_usage_corpus`: 题库用于考点覆盖、频次、考法和出题工作台。
- `agent_as_ingestion_assistant`: 智能体辅助 PDF -> Markdown、公式/化学式整理、章节切割、候选挂靠。
- `query_feedback_growth`: 提问暴露缺口，推动新候选点和关系建议。
- `expert_workflow_externalization`: 教师通过调教助理反向理解自己的教学方法论。

## 不能直接借鉴

- “每句话有出处”不能等于证据支持；出处可能只是背景引用或错误召回。
- “资料没问题就不会乱造”不能直接成立；检索、摘要、推理仍可能错。
- “越问越懂”不能自动写入主库；只能写入反馈、候选点、review_due。
- 组卷/答疑是 action 输出，需要上下文包、来源锚点、风险提示和必要人工确认。

## 风险和不确定

- 未确认具体工具和实现细节。
- 视频 ASR 对关键名词有多处错误，必须依赖 metadata + timestamp，不能用 ASR 拼写入实体库。
- 教材/题库导入涉及版权、许可和学生使用边界。
- 自动切割和挂靠可能造成学科上错误的关联。
- 教学场景属于高误导风险场景，需要比普通笔记更严的 evidence/action gate。

## VAKS 归位

```text
Capture: 教材、题库、考纲、视频转写、元数据、采集 ledger。
Understand: PDF/文本归一化、关键点抽取、候选摘要、候选知识点。
Review: 教学结论、考点判断、组卷依据需要 Evidence Packet 或人工复核。
Connect: 考纲挂靠和教材间关系先是 candidate relation suggestion。
Activation / Context Pack: 问题触发相关教材段落、考纲条目、题库样例、候选点、风险提示。
Decision / Action: 答疑、讲义、组卷、教学设计属于 action/workbench，不能从 raw/candidate 直出最终依据。
Use Ledger / Feedback: 追问、纠错、满意度、覆盖缺口写入 feedback/use ledger，推动 review_due。
```

## 处理等级

当前等级：heavy source intake, candidate-only

升级到 heavy 的条件：已满足。该视频提供完整入库流程，对 VAKS 入库技能、领域骨架和反馈闭环有直接架构借鉴价值。

## 下一步

- 与 `BV1UJddBGEAf` 合并为同一作者同一知识库思路的强蒸馏输出。
- 若后续要正式吸收，优先提炼为候选 pattern：`domain-spine-guided-ingestion`，并用 VAKS review gate 重新审查。
