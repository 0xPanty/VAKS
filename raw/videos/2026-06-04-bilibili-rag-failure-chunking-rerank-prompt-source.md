---
type: source
status: source-captured
title: '搭了个RAG知识库被骂不靠谱排查一整夜后我终于明白问题出在哪自建RAG知识库频频翻车、回答离谱被吐槽。通宵排查后摸清核心症结：粗暴文本切'
source_id: bilibili-BV1CeRJBAEna
source_uri: bilibili:BV1CeRJBAEna
source_url: https://www.bilibili.com/video/BV1CeRJBAEna/
source_type: video
platform: bilibili
platform_id: BV1CeRJBAEna
author: '海云日记'
publisher: '海云日记'
published_at: '2026-05-06 00:03:06 +08:00'
updated_at:
duration: 230s
captured_at: '2026-06-04 21:04:41 +08:00'
captured_by: Codex
raw_location: raw/videos/2026-06-04-bilibili-rag-failure-chunking-rerank-prompt-source.md
processing_mode: runner
processing_level: medium
review_priority: low
review_owner: Codex
formalization_status: raw-only
access_boundary: public_no_cookies
transcript_method: local_asr
transcript_location: raw/videos/2026-06-04-bilibili-rag-failure-chunking-rerank-prompt-source/transcript.txt
segments_location: raw/videos/2026-06-04-bilibili-rag-failure-chunking-rerank-prompt-source/segments.md
transcript_metadata_location: raw/videos/2026-06-04-bilibili-rag-failure-chunking-rerank-prompt-source/transcript-meta.json
ledger_location: raw/videos/2026-06-04-bilibili-rag-failure-chunking-rerank-prompt-source/acquisition-ledger.json
media_retention: deleted
source_status: active
topics:
  - rag
  - retrieval
  - chunking
  - rerank
  - prompt-boundary
  - source-structure
  - candidate-only
  - video-intake
projects:
  - verified-action-knowledge-system
source_family: rag-practice-failure
upstream_sources: []
verification_status: unverified
candidate_relation_suggestions: []
tags:
  - raw-video
  - bilibili
  - candidate-only
---

# 视频资料：RAG 知识库翻车复盘：切分、重排、Prompt 边界

## 为什么收录

这是一个很短的 RAG 落地复盘视频，信息密度不高，但和前面多条 RAG / GraphRAG / RAGLab 资料形成重复信号：RAG 翻车常常不是模型本身的问题，而是来源结构、切分、召回、重排和 prompt 边界没有处理好。

收录价值是中低到中等：它不新增 VAKS 主架构，但适合作为 Direction Review 里的“工程痛点重复出现”样本。

## 来源卡

- 平台：Bilibili
- 原始链接：https://www.bilibili.com/video/BV1CeRJBAEna/
- 标题：搭了个RAG知识库被骂不靠谱排查一整夜后我终于明白问题出在哪自建RAG知识库频频翻车、回答离谱被吐槽。通宵排查后摸清核心症结：粗暴文本切
- 作者 / UP 主：海云日记
- 发布时间：2026-05-06 00:03:06 +08:00
- 视频时长：230s
- 收录时间：2026-06-04 21:04:41 +08:00
- 访问边界：public_no_cookies

## 获取与转写

```yaml
subtitle_status: public subtitle endpoints checked, empty
transcript_method: local_asr
asr_engine: faster-whisper
asr_model: small
asr_device: cuda
compute_type: float16
language: zh
transcript_quality: medium
media_retention: deleted
scratch_cleanup: temporary public audio deleted after ASR
project_visible_artifacts: yes
transcript_metadata_location: raw/videos/2026-06-04-bilibili-rag-failure-chunking-rerank-prompt-source/transcript-meta.json
ledger_location: raw/videos/2026-06-04-bilibili-rag-failure-chunking-rerank-prompt-source/acquisition-ledger.json
```

说明：

```text
字幕 / ASR 是 raw/source text，不是 reviewed evidence。
AI 摘要是 candidate comprehension，不是 truth。
本视频没有公开字幕，使用公开视频音频 + 本地 GPU ASR；未使用 cookies，未使用云 API。
ASR 中出现 RAG/RAT、prompt/prominent、向量/项量等误听，工具名和数字不能只按 ASR 采信。
```

## 人话摘要

视频讲了一个内部 RAG 知识库上线后回答混乱的故事。讲述者认为问题不在于换哪个大模型，而在于工程链条太粗糙：文档按固定 500 字机械切分，破坏了语义和文档结构；纯向量召回面对口语问题和书面资料之间的表达差异时容易召回不准；prompt 只是简单粘贴资料，没有约束模型只能使用参考资料、无资料时不要编、并标注资料来源。

视频给出的改进方向是：按文档结构和资料类型切分；先向量召回多个候选，再用重排序模型筛出少量高相关候选；必要时把用户问题改写成三到五个变体后分别检索再去重；prompt 要根据问题类型动态调整，并显式设置参考资料使用边界。

对 VAKS 来说，这条资料的意义是再次验证“source structure first”和“retrieval hit != evidence support”。它支持我们把 RAG 放在 activation / context-pack preparation，而不是把检索结果、重排结果或 prompt 约束当作 reviewed knowledge。

## 关键实体置信度

```text
confirmed:
  - Bilibili source id: BV1CeRJBAEna
  - 视频标题、UP 主、发布时间、时长来自 Bilibili public metadata
  - transcript_method: local_asr, faster-whisper small, cuda
  - 主题为 RAG 知识库落地翻车，标题和转写都支持

likely:
  - 文档切分建议包括按 Markdown 标题层级 / 文档结构处理
  - 检索建议包括向量召回 + rerank
  - 查询扩展建议包括把用户问题改写成 3-5 个变体后检索
  - prompt 建议包括只使用参考资料、无资料不要编、标注资料来源

unclear:
  - ASR 中“bg1 加 muverse”很可能是 BGE + Milvus，但没有视觉/页面证据确认
  - “提升 40 个点”“满意度 7 成”是视频叙事里的示例数字，未验证
  - ASR 中个别词如“单元路件”“prominent”“RAT”明显存在误听

needs user visual check:
  - 如果后续要引用具体工具名、模型名或数字，需要检查视频画面/字幕/简介，而不能只靠 ASR
```

## 时间轴 / 分段

- 00:00-00:24：内部 RAG 知识库上线后回答乱套，换模型没有解决问题。
- 00:24-00:31：发现文档按每 500 字机械切分，讲述者认为核心问题在这里。
- 00:41-01:08：第一类坑是文档切分；按字数切不等于按语义/结构切，Markdown 资料应优先按标题层级等结构处理。
- 01:09-01:40：第二类坑是纯向量召回；口语问题和书面资料表达差异大时，单纯语义向量可能召回不准。
- 01:40-02:08：建议两阶段检索：先向量召回较多候选，再用重排序模型精选少量候选；进一步可做 query expansion。
- 02:08-02:42：第三类坑是 prompt 写得太粗糙；需要约束模型只用参考资料、无资料不要编、标注资料来源。
- 02:42-03:20：更进一步是按问题类型动态调整 prompt 格式。
- 03:20-03:49：把 RAG 项目写进简历时，应写出问题、方案、评估背景和数据，而不是只写“用某工具搭了系统”。

## 视频里直接说了什么

- 自建 RAG 知识库回答离谱时，不应只归咎于模型。
- 机械按字数切文档会破坏语义和结构。
- 更可靠的切分要遵循资料类型和文档结构。
- 纯向量检索在口语问题与书面资料差距较大时会失准。
- 可以先召回多个候选，再用 rerank 精选。
- 可以把用户问题改写成多个变体后分别检索并去重。
- prompt 需要明确“只用参考资料”“没有资料不要编”“标注资料来源”。
- 面试/简历里更有价值的是写清楚踩过什么坑、怎么解决、怎么评估。

## 我的理解 / 推断

这条视频不是在提出新的 RAG 架构，而是在用短案例强调几个基础但常被忽略的工程边界。它和我们前面 intake 的 RAGLab / RF-Mem / CoMe / DISCO-RAG 方向相互印证：检索系统真正的价值不只是“找相似文本”，而是把来源结构、候选召回、候选筛选、上下文组织和回答边界串起来。

但它的证据强度不高：数字、工具名和具体案例没有独立证据，更多是经验型叙述。所以它只适合作为候选方向压力，不适合作为 reviewed knowledge 或 action basis。

## 反漏提取检查

```text
pain point:
  - RAG 知识库上线后回答混乱，用户认为“不靠谱”。
  - 团队容易误判为模型问题，而忽略文档切分、召回和 prompt。

workflow:
  - 文档进入知识库。
  - 如果按固定字数粗暴切分，会破坏结构。
  - 用户提问后，向量召回候选。
  - 用 rerank / query expansion 提高候选匹配。
  - prompt 约束模型根据参考资料回答。

tools / plugins:
  - RAG 知识库。
  - 向量检索。
  - rerank model。
  - query expansion。
  - 可能提到 BGE / Milvus，但 ASR 未确认。

information structure:
  - Markdown 标题层级。
  - 文档类型。
  - 资料来源标注。
  - 参考资料片段。

judgment mechanism:
  - 视频口径更偏经验判断和项目叙事。
  - 相关性提升、满意度等数字未被独立验证。

user experience:
  - 普通用户只看到回答离谱，不会关心底层切分是否合理。
  - 面试官会追问文档切分策略、召回策略和踩坑经验。

automation boundary:
  - query expansion、rerank、dynamic prompt 可以自动化。
  - 自动检索和 prompt 约束不能替代证据审查。

risk:
  - 把“检索到了”误认为“资料支持了”。
  - 把示例指标当成真实可复用效果。
  - ASR 对工具名和专业词有误听。

fit for us:
  - 强化 source structure / context-pack preparation 的重要性。
  - 支持把 rerank、query rewriting、prompt boundary 放在 activation 层。
  - 可作为 RAG 方向聚类中的“基础工程痛点”样本。

challenge to us:
  - VAKS 若未来做 RAG/workbench，不能只做向量检索。
  - 原始来源结构、段落边界、表格/标题层级需要尽早保留。
```

## 可抽取 Candidate Points

- 固定字数切分是 RAG 知识库的常见失败源，尤其会破坏标题层级、段落语义、表格和上下文边界。
- 纯向量检索在表达差异较大的场景中容易漏召回或错召回；rerank 和 query expansion 是候选召回质量改进手段。
- prompt 边界可以降低模型乱编风险，但 prompt 约束本身不是 evidence review。
- RAG 项目的可靠性叙述需要包含问题背景、处理链条、评估方式和失败案例，而不是只列工具名。

## 可借鉴

- 在 VAKS 的未来 retrieval / context-pack workbench 中，把 source structure preservation 放在向量化之前。
- 对候选检索使用“先多召回、再筛选、再组织上下文”的思路。
- 在候选回答层明确资料引用边界：无资料时不应假装有资料。
- Direction Review 可以把“机械切分导致 RAG 失真”记作重复设计压力。

## 不能直接借鉴

- 不能把 rerank 分数、向量相似度或 query expansion 命中当作 truth confidence。
- 不能把 prompt 的“只使用参考资料”当成已经完成 evidence-aware review。
- 不能把视频里未验证的工具名、提升幅度或满意度数字写成事实。
- 不能因为短视频反复强调 RAG，就把 VAKS 主架构改成 RAG-first。

## 风险和不确定

- 视频偏经验/求职讲法，缺少代码、数据集、评测细节和可复现实验。
- ASR 对专业词误听较多，具体工具名需要视觉或外部来源确认。
- 指标数字只适合作为叙事线索，不适合作为证据。

## VAKS 归位

```text
Capture:
  Bilibili URL、公开元数据、ASR 转写、segments、ledger。

Understand:
  这是一条 RAG 落地翻车复盘，候选理解集中在切分、召回、重排、prompt 边界。

Review:
  当前不进入 reviewed knowledge；只作为候选点和设计压力样本。

Connect:
  可连接到 RAGLab、DISCO-RAG、RF-Mem、CoMe 等资料里的 activation / context-pack 方向。

Activation / Context Pack:
  可在后续 RAG 方向聚类复盘时激活，尤其用于“source structure first”与“retrieval hit != support”。

Decision / Action:
  当前不形成 action basis，不调整主架构。

Use Ledger / Feedback:
  如果后续 Direction Review 证明这类问题反复出现，可记录为 activation/usefulness 反馈，不直接改变 truth。
```

## 处理等级

```text
当前等级: medium

light:
  如果只做收藏，本视频一句话摘要即可。

medium:
  当前已完成：来源卡、完整 ASR、时间轴、关键实体置信度、candidate points、VAKS 归位。

heavy:
  只有当它和其他 RAG 资料一起进入 Direction Review，或其中某个候选点要被提升为设计原则时，才需要 evidence-aware review。
```

升级到 heavy 的条件：

- 同类资料中持续出现“机械切分 / source structure loss / pure vector failure”并影响 VAKS 未来检索工作台设计。
- 需要引用具体工具名、指标或工程方案作为 action basis 时，必须补充独立来源或可复现实验。

## 下一步

- 保持 raw-only / candidate-only。
- 在后续 RAG 资料聚类中，把它作为“基础工程失败案例”计入重复设计压力。
- 不建议为这条短视频单独改主架构。
