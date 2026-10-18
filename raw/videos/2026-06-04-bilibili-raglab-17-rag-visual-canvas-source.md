---
type: source
status: source-captured
title: "图解17种rag知识库画布graphrag向量知识图谱分析pageindex企业问答搭建案例分享"
source_id: bilibili-BV1iSVG6eEsj
source_uri: bilibili:BV1iSVG6eEsj
source_url: https://www.bilibili.com/video/BV1iSVG6eEsj/
source_type: video
platform: bilibili
platform_id: BV1iSVG6eEsj
author: AGI_Ananas
publisher: AGI_Ananas
published_at: "2026-05-30 15:13:43 +08:00"
updated_at:
duration: 996s
captured_at: "2026-06-04 20:48:21 +08:00"
captured_by: Codex
raw_location: raw/videos/2026-06-04-bilibili-raglab-17-rag-visual-canvas-source.md
processing_mode: immediate
processing_level: heavy
review_priority: normal
review_owner: Codex
formalization_status: raw-only
access_boundary: public_no_cookies
transcript_method: local_asr
transcript_location: raw/videos/2026-06-04-bilibili-raglab-17-rag-visual-canvas-source/transcript.txt
segments_location: raw/videos/2026-06-04-bilibili-raglab-17-rag-visual-canvas-source/segments.md
transcript_metadata_location: raw/videos/2026-06-04-bilibili-raglab-17-rag-visual-canvas-source/transcript-meta.json
ledger_location: raw/videos/2026-06-04-bilibili-raglab-17-rag-visual-canvas-source/acquisition-ledger.json
visual_observations_location: raw/videos/2026-06-04-bilibili-raglab-17-rag-visual-canvas-source/visual-observations.md
visual_contact_sheet_location: raw/videos/2026-06-04-bilibili-raglab-17-rag-visual-canvas-source/visual/contact-sheet-30s-480p.jpg
visual_frames_location: raw/videos/2026-06-04-bilibili-raglab-17-rag-visual-canvas-source/visual/frames-480p/
visual_metadata_location: raw/videos/2026-06-04-bilibili-raglab-17-rag-visual-canvas-source/visual/visual-frames-480p.json
media_retention: deleted
source_status: active
topics:
  - rag
  - raglab
  - graphrag
  - retrieval
  - visual-workbench
  - context-pack
  - evaluation
  - pageindex
projects:
  - verified-action-knowledge-system
source_family: bilibili-video-source
upstream_sources: []
verification_status: unverified
candidate_relation_suggestions:
  - target: "[[Context Pack]]"
    relation_type: refines
    relation_state: candidate
    why_suggested: "The visual RAGLab canvas shows retrieval variants as context-pack preparation strategies, not truth support."
  - target: "[[Evidence Support Check]]"
    relation_type: risk_of
    relation_state: candidate
    why_suggested: "RAGAS-style evaluation and retrieved chunks can be mistaken for evidence support unless VAKS keeps the boundary explicit."
tags:
  - raw-video
  - bilibili
  - candidate-only
  - visual-source
---

# 图解17种 RAG 知识库画布

## 为什么收录

这条视频不是单纯口播，它的主要信息在画面里的 RAGLab 画布：节点、数据流、右侧结果面板、评估面板和下拉列表共同构成内容。只看 ASR 会漏掉结构。

收录原因：

```text
它用可视化白盒画布拆解多个 RAG / 知识库架构。
它展示了文档处理、chunk、embedding、向量检索、BM25、RRF、query rewriting、HyDE、context window、agentic retrieval、GraphRAG、PageIndex 等路线。
它对 VAKS 的价值在于 retrieval / activation / context-pack / workbench 设计压力，而不是 truth confidence。
```

## 来源卡

- 平台：Bilibili
- BV：`BV1iSVG6eEsj`
- 标题：图解17种rag知识库画布graphrag向量知识图谱分析pageindex企业问答搭建案例分享
- UP 主：AGI_Ananas
- 发布时间：2026-05-30 15:13:43 +0800
- 时长：996 秒
- 原始链接：`https://www.bilibili.com/video/BV1iSVG6eEsj/`
- 访问边界：public no cookies

## 获取与转写

```yaml
subtitle_status: public subtitle APIs checked, empty
transcript_method: local_asr
asr_engine: faster-whisper
asr_model: small
asr_device: cuda
asr_compute_type: float16
segment_count: 438
text_chars: 5243
media_retention: deleted
cloud_api_used: false
cookies_used: false
visual_sampling:
  source: public video-only stream
  resolution: 852x480
  method: frame sampled every 30 seconds
  retained:
    - contact sheet
    - 34 key frames
    - dropdown crop for 17-item list
    - visual observations
```

说明：

```text
ASR 是 raw/source text，不是 reviewed evidence。
关键帧观察是 candidate observation，不是 truth。
RAGLab 画布、RAGAS 评估、检索分数、可视化节点、右侧面板都不能直接变成 VAKS truth confidence。
```

## 人话摘要

视频作者用 RAGLab 画布把一组 RAG / 知识库方案串起来讲。它不是只讲“向量检索”，而是把企业问答里常见的问题拆出来：文档可能是表格、跨页、编号、同物多名；机械 chunk 会切坏表格；纯向量容易漏精确编号；混合检索可以补关键词；query rewriting / HyDE / context window 可以改善召回；agentic / adaptive 路由会增加调用成本和判断风险；GraphRAG 用实体关系和三元组把 chunk 连接起来；PageIndex / TreeIndex 用文档层级模拟人类阅读。

对 VAKS 的核心启发：

```text
retrieval strategy should be visible and inspectable.
context-pack preparation should expose where chunks, entities, relations, and evaluation came from.
evaluation is diagnostic, not truth.
graph/entity/relation extraction is candidate connection, not reviewed relation.
```

## 关键实体置信度

```text
confirmed by metadata / visual frame:
  - RAGLab
  - Bilibili BV1iSVG6eEsj
  - AGI_Ananas
  - Simple RAG
  - Fusion Retrieval
  - Chunk Size
  - Semantic Chunking
  - Query Rewriting
  - HyDE
  - Reranking
  - Context Enrichment Window
  - RAPTOR
  - Self-RAG
  - CRAG
  - Adaptive RAG
  - Agentic RAG
  - RAG + RAGAS
  - GraphRAG
  - PageIndex
  - TreeIndex
  - BM25
  - RRF

likely:
  - RAGAS metrics discussed include faithfulness / answer relevancy / context precision style evaluation.
  - The sample dataset is a cat / pet registration style enterprise QA fixture.

unclear:
  - Some Chinese subtitles in the dropdown are low-resolution; English item names are clearer than the Chinese sublabels.
  - ASR garbles many technical terms, so ASR wording is not reliable for entity names.

needs user visual check:
  - If later we need exact UI copy, exact RAGAS numeric table, or exact Chinese sublabel for every dropdown entry.
```

## 时间轴 / 画面锚点

- 00:00-01:30：总览 RAGLab 画布；GraphRAG / 知识图谱画布，右侧显示节点说明和图谱结果。
- 01:00：示例源文档是“喵星球宠物店 - 品种登记册 v2024”，含表格和条目。
- 01:58-05:30：Simple RAG：文档加载、文本切分、Embedding、向量数据库、向量检索、Prompt 拼接、LLM 生成、RAGAS 评估。
- 03:00：展示 Markdown 表格源文档，说明机械 chunk 可能切碎表格。
- 04:30-05:10：向量检索结果、Top-K、RAGAS 评估；作者提到正确性需要人工标准或已审核标准答案。
- 06:30-08:30：Fusion Retrieval：BM25 + 向量检索 + RRF 融合，补编号/关键词类查询。
- 08:30-09:40：Chunk Size / Semantic Chunking：分块大小影响答案；语义分块对复杂表格仍不足。
- 10:00-10:30：Query Rewriting：把口语化问题改写成更精准查询，多一次 LLM 调用。
- 10:30-11:00：HyDE：先让 LLM 生成假设答案，再用假设文本做检索。
- 11:00-12:00：Context Enrichment Window：对命中的 chunk 做前后文扩展，召回更多但噪声增加。
- 12:30-13:30：Adaptive RAG / Agentic RAG：路由或多轮检索，收益是动态策略，风险是判断错误和延迟。
- 13:00：下拉菜单显示 17 类架构项。
- 13:30-15:00：GraphRAG：实体关系 / 三元组抽取、社区/图算法，连接不同 chunk。
- 15:30-16:10：PageIndex：文档树/标题层级式检索，模拟“大标题看选项，小标题定位”。
- 16:30：弹出溯源/原文预览，强调回答可以对应文本块。

## 17 项画面列表

从 13:00 左右下拉菜单视觉确认：

1. Simple RAG
2. Fusion Retrieval
3. Chunk Size
4. Semantic Chunking
5. Query Rewriting
6. HyDE
7. Reranking
8. Context Enrichment Window
9. RAPTOR
10. Self-RAG
11. CRAG
12. Adaptive RAG
13. Agentic RAG
14. RAG + RAGAS
15. GraphRAG
16. PageIndex
17. TreeIndex

## 视频里直接说了什么

- 作者认为企业问答场景里，知识库是很多 AI 工具的基础。
- 示例数据故意包含表格、跨页、编码、不同视角命名等复杂点。
- Simple RAG 的基础链路是文档加载、文本切分、embedding、向量库、Top-K 检索、Prompt 拼接、LLM 回答、评估。
- 正确性需要人工标准或已审核答案才能计算。
- 机械 chunk 会破坏表格整体性。
- BM25 可补精确词、编号、关键名词；与向量检索可用 RRF 融合。
- Query rewriting、HyDE、context window、agentic retrieval 都是提高召回或重构查询的策略，但会增加调用、噪声或延迟。
- GraphRAG 通过实体关系 / 三元组 / 社区等图算法连接 chunk。
- PageIndex 通过文档层级/标题目录做检索，模拟人类阅读定位。

## 我的理解 / 推断

这条视频最有用的不是具体“17 种方案哪个最好”，而是画布形态：

```text
source node
-> transform node
-> retrieval node
-> prompt/context assembly node
-> answer node
-> evaluation / trace node
```

这和 VAKS 的方向高度一致，但边界必须更严格：

```text
检索节点输出 = candidate context
评估节点输出 = diagnostic / benchmark signal
图谱节点输出 = candidate relation
溯源预览 = source anchor / provenance
reviewed knowledge = 另一个 evidence-aware review 阶段
```

## 反漏提取检查

```text
pain point:
  - 企业知识库不只是普通文本，常见表格、编号、跨页、多名同物、不同视角。
  - 单一向量 Top-K 容易丢编号、表格上下文和关系。

workflow:
  - 文档加载 -> chunk / embedding / index -> query transform -> retrieval -> context assembly -> LLM answer -> RAGAS / trace / source preview.

tools / plugins:
  - RAGLab
  - RAGAS
  - vector retrieval
  - BM25
  - RRF
  - GraphRAG
  - PageIndex / TreeIndex

information structure:
  - 画布节点 + 右侧节点说明 / 结果面板 / 检索列表 / 评估结果。
  - 不同 RAG 策略作为可切换 pipeline。

judgment mechanism:
  - RAGAS-style evaluation, retrieved chunk scores, source preview.
  - 作者提到正确性需要人工标准答案或已审核结果。

user experience:
  - 白盒画布让 pipeline 可检查、可解释，比纯黑盒 RAG demo 更适合学习和调试。

automation boundary:
  - pipeline 可自动运行，但正确性、证据支持、关系可信度不能自动成立。

risk:
  - 把检索结果、评估分数、图谱关系、可视化节点误读成 truth。
  - 画面中 RAGAS 评估可能给人“自动验证”的错觉。

fit for us:
  - 很适合作为 VAKS future workbench / context-pack preparation / retrieval strategy taxonomy 的候选参考。

challenge to us:
  - VAKS 如果未来有 UI，应该让 retrieval/context/evidence/review 层级可视化，不能只有文件和文字规则。
```

## Candidate Points

1. `visual_white_box_context_pipeline`

候选结论：VAKS 未来 workbench 可考虑把 capture / transform / retrieval / context assembly / answer / review trace 分成可视节点。

边界：节点可视化只是 workflow visibility，不是 truth authority。

2. `retrieval_strategy_taxonomy_as_activation_options`

候选结论：Simple RAG、hybrid retrieval、query rewriting、HyDE、context window、adaptive/agentic retrieval、GraphRAG、PageIndex 都应归为 activation / context-pack preparation 的候选策略。

边界：策略选择不产生 truth confidence。

3. `evaluation_is_diagnostic_not_review`

候选结论：RAGAS 可作为回答/检索质量的诊断参考，但视频里也承认 correctness 需要人工标准答案或已审核答案。

边界：RAGAS 分数不是 evidence support，也不是 reviewed knowledge。

4. `source_structure_preservation_pressure`

候选结论：企业文档里的表格、跨页、编号和多视角命名要求 VAKS intake 保留 source structure / anchors，不能只做纯文本 chunk。

边界：保留结构是 provenance/context quality，不等于支持某个 claim。

5. `graph_edges_are_candidate_relations`

候选结论：GraphRAG 的实体/关系/三元组可以帮助发现 candidate relations 和 context neighborhoods。

边界：自动抽取关系不能进入 reviewed relations。

6. `hierarchical_index_as_human_reading_simulation`

候选结论：PageIndex / TreeIndex 这类层级索引对长文档可能比纯向量更贴近人类阅读路径。

边界：层级索引是 source navigation / activation，不是 evidence review。

## 可借鉴

- 白盒画布式 pipeline UI。
- 每个节点都能点开输入、输出、说明、风险和评估。
- retrieval strategy taxonomy。
- 把 query rewrite / HyDE / context window / agentic loop 显示为可选 activation path。
- 把源文档结构、chunk、检索结果、answer、RAGAS、source preview 放在同一个调试界面。
- 对表格和编号类资料保持警惕。

## 不能直接借鉴

- 不把 RAGAS、检索分数、chunk 命中、图谱关系当 truth confidence。
- 不让“可视化看起来很完整”替代 evidence-aware review。
- 不把自动实体关系抽取写成 reviewed relation。
- 不把 17 种 RAG 策略扩成 VAKS 主架构模块。
- 不为了覆盖所有检索策略而加重普通 capture/query。

## 风险和不确定

- ASR 术语错误较多；术语以画面和常见技术名为准。
- 公开视频最高可用帧是 480p，小字不能完全精读。
- 视频是教学/演示性质，未提供可复现实验代码或独立 benchmark。
- RAGAS 评估结果、画布结果和示例数据只能作为候选理解。
- 视频强调多个架构，但没有证明某个方案在 VAKS 场景下最佳。

## VAKS 归位

```text
Capture:
  source structure preservation pressure, especially tables and identifiers.

Understand:
  visual candidate comprehension of RAG pipelines.

Review:
  RAGAS and evaluation are diagnostic only; correctness still requires reviewed standards.

Connect:
  GraphRAG-style entities and relations can suggest candidate points / candidate relations.

Activation / Context Pack:
  main fit. Retrieval variants are activation/context-pack preparation strategies.

Decision / Action:
  no direct action basis.

Use Ledger / Feedback:
  evaluation and user feedback may improve retrieval usefulness/scope fit, not truth.
```

## 当前处理等级

```text
heavy video source record
candidate-only
no promotion
no reviewed relation
no action basis
```

升级条件：

- 后续 Direction Review 要整理 retrieval / context-pack / workbench 设计压力。
- 用户要求把 RAGLab 式画布纳入 UI/workbench alpha。
- 需要把“表格/编号/跨页/多视角命名”的 source structure pressure 写入更正式的 source intake review。

## 下一步

```text
保留 source card、ASR、segments、visual frames、visual observations。
不改主架构。
进入 Direction Review 的 retrieval / activation / visual workbench / source-structure 分组。
```
