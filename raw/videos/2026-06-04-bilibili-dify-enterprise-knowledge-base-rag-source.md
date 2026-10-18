---
type: source
status: source-captured
title: 'RAG实战  用dify搭建企业知识库demo'
source_id: bilibili-BV1bn5t6YEZw
source_uri: bilibili:BV1bn5t6YEZw
source_url: https://www.bilibili.com/video/BV1bn5t6YEZw/
source_type: video
platform: bilibili
platform_id: BV1bn5t6YEZw
author: '林爻linyao'
publisher: '林爻linyao'
published_at: '2026-05-11 22:23:44 +08:00'
updated_at:
duration: 696s
captured_at: '2026-06-04 21:42:05 +08:00'
captured_by: Codex
raw_location: raw/videos/2026-06-04-bilibili-dify-enterprise-knowledge-base-rag-source.md
processing_mode: runner
processing_level: medium
review_priority: low
review_owner: Codex
formalization_status: raw-only
access_boundary: public_no_cookies
transcript_method: local_asr
transcript_location: raw/videos/2026-06-04-bilibili-dify-enterprise-knowledge-base-rag-source/transcript.txt
segments_location: raw/videos/2026-06-04-bilibili-dify-enterprise-knowledge-base-rag-source/segments.md
transcript_metadata_location: raw/videos/2026-06-04-bilibili-dify-enterprise-knowledge-base-rag-source/transcript-meta.json
ledger_location: raw/videos/2026-06-04-bilibili-dify-enterprise-knowledge-base-rag-source/acquisition-ledger.json
media_retention: deleted
source_status: active
topics:
  - rag
  - dify
  - enterprise-knowledge-base
  - workflow
  - chunking
  - vector-retrieval
  - rerank
  - prompt-boundary
  - data-cleaning
  - candidate-only
  - video-intake
projects:
  - verified-action-knowledge-system
source_family: bilibili-dify-rag-demo
upstream_sources: []
verification_status: unverified
candidate_relation_suggestions: []
tags:
  - raw-video
  - bilibili
  - candidate-only
---

# 视频资料：Dify 搭企业知识库 RAG demo

## 为什么收录

这条视频是一个零基础视角的 Dify 企业知识库 demo。它不提供新架构，也不是严肃 RAG 评测，但对 VAKS 有一个实际价值：它用很具体的 UI 操作重复验证了 RAG 落地里最容易被忽略的事情不是“有没有向量库”，而是文档格式、分块、表格处理、召回测试、TopK / score threshold、rerank、提示词边界和最终发布形态。

本卡只记录 Bilibili 公开元数据、公开视频音频本地 ASR、以及 Codex 的候选理解。它不是 Dify 采纳建议，不是 RAG 可靠性证据，也不构成 VAKS 的 action basis。

## 来源卡

- 平台：Bilibili
- 原始链接：https://www.bilibili.com/video/BV1bn5t6YEZw/
- 标题：RAG实战  用dify搭建企业知识库demo
- 作者 / UP 主：林爻linyao
- 发布时间：2026-05-11 22:23:44 +08:00
- 视频时长：696 秒
- 收录时间：2026-06-04 21:42:05 +08:00
- 访问边界：public_no_cookies
- 来源限制：视频简介为空；内容理解主要来自本地 ASR。Dify UI 文案、模型名、按钮名和参数需要画面确认。

## 获取与转写

```yaml
subtitle_status:
  public_view_api: empty subtitle list
  public_subtitle_api_1: ok, empty
  public_subtitle_api_2: ok, empty
transcript_method: local_asr
asr_engine: faster-whisper
asr_model: small
asr_device: cuda
compute_type: float16
language: zh
language_probability: 1
segment_count: 515
text_chars: 5036
transcript_quality: medium
media_retention: deleted
scratch_cleanup: temporary public audio deleted after ASR
project_visible_artifacts: yes
transcript_location: raw/videos/2026-06-04-bilibili-dify-enterprise-knowledge-base-rag-source/transcript.txt
segments_location: raw/videos/2026-06-04-bilibili-dify-enterprise-knowledge-base-rag-source/segments.md
transcript_metadata_location: raw/videos/2026-06-04-bilibili-dify-enterprise-knowledge-base-rag-source/transcript-meta.json
ledger_location: raw/videos/2026-06-04-bilibili-dify-enterprise-knowledge-base-rag-source/acquisition-ledger.json
```

说明：

```text
字幕 / ASR 是 raw/source text，不是 reviewed evidence。
AI 摘要是 candidate comprehension，不是 truth。
本次没有使用 cookies，没有使用云 API。
ASR 多次把 Dify 识别成“敌贩/define”，把 RAG 识别成“REJ/RIJ”，把 embedding 识别成“Inviting/项量化”，把 Qwen / 通义千问识别成“通易签问/千万”等。
```

## 人话摘要

视频演示了用 Dify 搭一个企业知识库问答 demo。作者先讲 RAG 的基本流程：先准备私有文档，把文档切成 chunk，再做 embedding 存入向量数据库；用户提问时，问题也会 embedding 化，再和已存 chunk 做相似度检索，召回相关片段，必要时用 rerank 更精细筛选，最后把召回内容和问题交给大模型生成答案。

实操部分从 Dify 登录、配置模型供应商开始：Dify 提供搭建平台，但大模型、embedding 模型、rerank 模型需要自己接 API。视频里用了阿里云百炼 / 通义千问相关模型作为示例。随后作者只关注两个 Dify 模块：知识库和工作室。

知识库部分最有价值。作者把一份带表格的文档先拆开处理：普通文本建议导出为 Markdown，因为 Markdown 的一级/二级/三级标题能让系统更容易识别结构；PDF 不推荐，因为对机器来说更像图片，识别困难。上传 Markdown 后，作者观察 Dify 的默认分段，发现它把“如何添加组件”的多个方法切得太碎，于是改分段标识符，按标题层级切，让每个二级标题下面的内容作为更完整的语义块。还解释了最大分段长度、重叠长度、空格换行清洗等参数。

然后作者做召回测试：问“评论功能的使用方法”，看 TopK 召回的三个片段是否真的来自正确文档；再把 TopK 改成 2，或设置 score threshold 过滤掉低相似度片段。接着演示表格处理：同一张表如果导成 Markdown，后续 chunk 可能丢失表头语义；如果用 CSV，每一行带表头，结构更清楚。视频明确说数据清洗和数据分段是 RAG 里最耗时间和精力的地方。

最后作者在 Dify 工作室创建聊天助手，先不挂知识库时，模型会按自己已有知识乱答；挂上知识库后，答案能引用上传文件。提示词里最关键的是要求模型严格根据文档回答、结构化输出。完成后可以发布 demo URL，也可以把问答机器人嵌入网站或系统。

对 VAKS 来说，这条的价值不是 Dify 本身，而是把低代码 RAG 的关键边界演得很直观：source format、chunking、table structure、retrieval test、score threshold、prompt boundary 都只是 context preparation / activation；它们不能替代 evidence-aware review。

## 关键实体置信度

```text
confirmed:
  - Bilibili video id: BV1bn5t6YEZw
  - title: RAG实战  用dify搭建企业知识库demo
  - UP 主: 林爻linyao
  - published_at: 2026-05-11 22:23:44 +08:00
  - duration: 696s
  - subtitle endpoints checked and empty
  - transcript_method: local_asr, faster-whisper small, cuda, no cookies, no cloud API

likely:
  - “敌贩 / define” 指 Dify。
  - “REJ / RIJ” 指 RAG。
  - “Inviting / 项量化” 指 embedding / 向量化。
  - “Rank 模型” 指 rerank model。
  - “通易签问 / 千万” 指通义千问 / Qwen 系列模型。
  - 视频中的平台路径包括 Dify 的知识库、工作室、模型供应商设置、召回测试、聊天助手、发布和嵌入网站。

unclear:
  - 具体 Dify 版本、UI 文案、模型 ID、rerank 模型名、embedding 模型名需要画面确认。
  - TopK、score threshold、分段标识符的具体最终参数只按 ASR 推断，若后续引用需要截图/OCR。
  - 表格例子的原始数据和最终回答质量没有独立验证。

needs user visual check:
  - Dify UI 的按钮名、模型名、参数名。
  - Markdown 分段标识符到底填写的是几个 `#` 或换行符。
  - 表格 Markdown vs CSV 的具体切块展示。
  - 如果后续要写成正式 RAG 操作建议，需要实际复现或使用 Dify 官方文档。
```

## 时间轴 / 分段

- 00:00-00:28：展示目标：用 Dify 搭基于 RAG 的企业知识库 demo，回答基于上传文档。
- 00:28-01:36：回顾 RAG 基本流程：私有文档、chunk、embedding、向量库、问题 embedding、召回、rerank。
- 01:36-02:28：Dify 登录与模型供应商配置；需要外接 API key，示例为阿里云百炼 / 通义千问。
- 02:28-03:35：只关注知识库和工作室；创建知识库，上传文档；普通文本建议 Markdown，PDF 不推荐。
- 03:35-04:48：观察 Dify 默认分块，发现按空行/默认规则切得太碎；改用标题结构切分。
- 04:48-06:45：解释最大分段长度、重叠长度、文本预处理、embedding 模型、rerank、TopK。
- 06:45-07:56：召回测试：看召回片段、相似度分数、TopK 和 score threshold 的影响。
- 07:56-09:31：表格处理：Markdown 表格切块容易丢表头，CSV 每行带表头更适合结构化表格。
- 09:31-11:11：在工作室创建聊天助手，挂载知识库，提示词要求严格根据文档回答。
- 11:11-11:35：发布 demo URL，并可嵌入网站或系统。

## 视频里直接说了什么

- RAG 用来处理大模型知识过时或私有数据不可见的问题。
- RAG 有数据准备和用户提问两个阶段。
- chunk 应尽量语义完整，不能把上下文切断。
- embedding 把文本和问题转成向量，相似度检索用于召回片段。
- rerank 是更精细的筛选。
- Dify 是搭建平台，不自带大模型能力，需要配置模型供应商和 API key。
- 文档类内容建议导出成 Markdown；PDF 对机器识别不友好。
- 分块需要按具体文档结构调整，不同场景切分方式不同。
- 最大分段长度和重叠长度是为了防止极端情况下整篇不切或语义被横切。
- 表格数据用 CSV 可能比 Markdown 表格更清楚，因为每一行都带表头。
- 数据清洗和数据分段是 RAG 里最耗时间和精力的事情。
- 知识库挂到聊天助手后，模型回答才会基于上传文档。
- 提示词最关键的是要求严格根据文档回答。

## 我的理解 / 推断

这条视频是低代码 RAG 入门 demo，不是架构突破。它的候选价值在于“把基础做对”的重复压力：

```text
source format matters
chunking matters
table structure matters
retrieval test matters
prompt boundary matters
```

这和前面“RAG 翻车：切分、重排、Prompt 边界”的短视频互相印证。区别是前一条偏踩坑复盘，这条偏 UI 实操，尤其补了表格格式的例子：Markdown 表格在切块后可能丢表头，CSV 行记录对检索更友好。

对 VAKS 来说，这条最适合放在 RAG / context-pack workbench 的 candidate cluster 里，作为“普通低代码用户也会遇到 source-structure-first 问题”的样本。它不适合单独升 heavy，也不建议因为它去采用 Dify。

## 反漏提取检查

```text
pain point:
  - 大模型不知道私有文档，普通用户想快速搭一个基于自己文档回答的企业知识库 demo。
  - 用户容易以为 RAG 只是上传文件 + 选模型，但实际问题集中在文档格式、分块、表格结构、召回参数和提示词边界。

workflow:
  - 注册 / 登录 Dify。
  - 配置模型供应商和 API key。
  - 在知识库上传文档。
  - 对文档做格式选择和分段设置。
  - 选择 embedding 模型和 rerank 模型。
  - 设置 TopK、score threshold 等召回参数。
  - 用召回测试检查问题是否召回正确片段。
  - 在工作室创建聊天助手。
  - 挂载知识库。
  - 写系统提示词，要求严格根据文档回答。
  - 发布 demo URL 或嵌入网站。

tools / plugins:
  - Dify
  - 阿里云百炼 / API key
  - 通义千问 / Qwen 系列模型（ASR 推断，需 UI 确认）
  - embedding model
  - rerank model
  - Markdown
  - CSV
  - Dify knowledge base
  - Dify studio / chat assistant

information structure:
  - 普通文本：Markdown 标题层级可帮助机器识别结构。
  - 表格：CSV 每行带表头，比被切碎的 Markdown 表格更稳定。
  - chunk：应保持语义完整，按文档结构调整。
  - retrieval test：用具体问题检查召回片段和相似度分数。
  - prompt：要求严格根据文档回答并结构化输出。

judgment mechanism:
  - 看 chunk 预览是否符合原文语义。
  - 看召回测试是否找到了正确片段。
  - 用 TopK 控制召回数量。
  - 用 score threshold 过滤低相似度片段。
  - 用最终问答检查是否引用知识库而不是模型自带知识。

user experience:
  - Dify 让零代码用户能较快搭出 demo。
  - UI 预览 chunk / 召回片段对调参很友好。
  - 但用户仍需要理解文档结构和数据清洗，不是纯自动化。
  - API key / 模型供应商 / 参数设置对小白仍有门槛。

automation boundary:
  - Dify 可以自动切分、embedding、召回、rerank 和挂载知识库。
  - 用户仍需要人工检查 chunk、表格格式和召回测试。
  - prompt 可约束回答边界，但不能完成 evidence-aware review。
  - 相似度分数 / rerank / 引用文件只能说明检索命中，不能说明事实可靠。

risk:
  - 把 demo 能答对样例问题误认为系统可靠。
  - 把 Dify 引用文件误认为 evidence support。
  - 表格、PDF、Markdown 处理不当会让检索语义失真。
  - 提示词“严格根据文档回答”不能防止所有幻觉。
  - 模型供应商、API key 和数据上传有隐私 / 合规边界，需要单独评估。

fit for us:
  - 强化 VAKS 的 source structure preservation。
  - 可作为未来 context-pack preparation / retrieval workbench 的普通用户样本。
  - 说明 ingestion UI 需要 chunk preview、retrieval test、format warning 和 table handling。
  - 支持“retrieval hit != evidence support”的边界。

challenge to us:
  - VAKS 未来如果做检索工作台，不能只提供抽象 schema，需要给用户看 chunk 和召回效果。
  - 普通用户需要低摩擦 demo 体验；VAKS strict review 不能前置到 capture。
  - 但低代码 RAG 的便利性也容易制造 false authority。
```

## 可抽取 Candidate Points

- `source_format_before_embedding`: 进入 embedding 前应先处理文档格式；Markdown、PDF、CSV 对 chunk 质量影响很大。
- `chunk_preview_as_intake_workbench`: intake / retrieval workbench 应提供 chunk preview，让用户检查切分是否破坏语义。
- `table_rows_need_header_preservation`: 表格资料需要保留表头和行语义，否则切块后容易丢失字段关系。
- `retrieval_test_before_answer_demo`: RAG demo 上线前应做召回测试，查看 TopK、score threshold 和召回片段。
- `dify_as_low_code_rag_reference`: Dify 可作为低代码 RAG 工作流参考，但不是 VAKS truth/review 系统。
- `prompt_boundary_not_review`: “严格根据文档回答”是回答约束，不是 evidence-aware review。
- `retrieval_score_not_support`: 相似度分数和 rerank 结果是 retrieval signal，不是 evidence support 或 truth confidence。

## 可借鉴

- 在未来 VAKS intake/workbench 中提供 chunk preview。
- 对 Markdown / PDF / CSV 等格式给出不同处理策略和风险提示。
- 对表格保留表头，避免行/列关系在切块后丢失。
- 用 retrieval test 作为 context preparation 的诊断步骤。
- 对 RAG 参数暴露 TopK、score threshold、rerank 等调试面。
- 在回答层明确“只能基于文档”的提示词边界，但继续标注它不是 review。

## 不能直接借鉴

- 不直接采用 Dify 作为 VAKS 主系统。
- 不把 Dify 的知识库、引用文件或检索分数当 reviewed evidence。
- 不把 demo 问答成功当 RAG 可靠性评测。
- 不把上传私有文档到第三方平台作为默认方案；隐私、合规和数据留存需单独评估。
- 不把 RAG-first 改成 VAKS 主架构。

## 风险和不确定

- 当前没有实际复现 Dify demo，只有视频转写。
- ASR 对 Dify、RAG、embedding、rerank、Qwen 等词有明显误识别。
- 视频是新手 demo，不覆盖权限、隐私、版本、成本、数据隔离、评测和失败案例。
- 表格处理结论有直观价值，但若要成为正式规则，需要更多样本或本地测试。

## VAKS 归位

```text
Capture:
  Bilibili URL、公开元数据、ASR transcript、segments、metadata、ledger。

Understand:
  本卡摘要、反漏提取和 candidate points 属于 candidate comprehension。

Review:
  当前不进入 reviewed knowledge。若要 promotion，需要 Dify 官方文档、本地复现或更强工程来源。

Connect:
  可连接到 RAG failure chunking/rerank/prompt、RAGLab visual canvas、DISCO-RAG、miniopenclaw workbench。

Activation / Context Pack:
  可作为未来 retrieval/context-pack preparation UI 的候选样本，尤其用于 chunk preview、retrieval test、table handling。

Decision / Action:
  不构成 action basis；不能据此决定采用 Dify 或部署第三方知识库。

Use Ledger / Feedback:
  可记录为 RAG 入门/低代码工作流样本，不改变 truth confidence。
```

## 处理等级

```text
当前等级: medium

light:
  只保存来源卡、一句话摘要、为什么收录。

medium:
  当前已完成：来源卡、完整 ASR、时间轴、关键实体置信度、candidate points、可借鉴 / 不可借鉴、VAKS 归位。

heavy:
  只有当它和其他 RAG / Dify 资料一起进入 Direction Review，或准备正式设计 intake/retrieval workbench 时，才需要升级。
```

升级到 heavy 的条件：

- 准备比较 Dify、RAGLab、OpenKB、miniopenclaw 等作为 VAKS workbench 参考。
- 准备把 `chunk_preview_as_intake_workbench` 或 `table_rows_need_header_preservation` 写入正式 pattern。
- 本地复现 Dify 的文档切分、CSV/Markdown 表格处理和召回测试。
- 需要评估第三方平台数据上传的隐私/合规/授权边界。

## 价值判断

```text
设计启发价值: 中等
证据强度: 低到中
直接采纳价值: 低
进入 RAG/workbench Direction Review 价值: 中等
单独改主架构: 不建议
```

一句话：这是一个有用的“普通用户 RAG 实操样本”，能补强 source format / chunk preview / retrieval test / table handling 这些工程细节，但它不是新方向，也不值得单独推动架构调整。

## 下一步

- 保持 raw-only / candidate-only。
- 后续和 RAG 翻车短视频、RAGLab、DISCO-RAG、miniopenclaw 一起做 Direction Review。
- 暂不改 `SCHEMA.md`、`SOURCE_INTAKE.md`、`REVIEW_QUEUE.md` 或主架构文件。
