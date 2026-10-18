---
type: source
status: source-captured
title: '复旦大学DISCO-RAG方案让RAG从搜索变分析'
source_id: bilibili-BV1zadJBtErG
source_uri: bilibili:BV1zadJBtErG
source_url: https://www.bilibili.com/video/BV1zadJBtErG/
source_type: video
platform: bilibili
platform_id: BV1zadJBtErG
author: '大模型论文解读'
publisher: '大模型论文解读'
published_at: '2026-04-18 07:58:17 +08:00'
updated_at:
duration: 488s
captured_at: '2026-06-04 19:24:13 +08:00'
captured_by: Codex
raw_location: raw/videos/2026-06-04-bilibili-disco-rag-search-to-analysis-source.md
processing_mode: runner
processing_level: medium
review_priority: normal
review_owner: Codex
formalization_status: raw-only
access_boundary: public
transcript_method: local_asr
transcript_location: raw/videos/2026-06-04-bilibili-disco-rag-search-to-analysis-source/transcript.txt
segments_location: raw/videos/2026-06-04-bilibili-disco-rag-search-to-analysis-source/segments.md
transcript_metadata_location: raw/videos/2026-06-04-bilibili-disco-rag-search-to-analysis-source/transcript-meta.json
ledger_location: raw/videos/2026-06-04-bilibili-disco-rag-search-to-analysis-source/acquisition-ledger.json
media_retention: deleted
source_status: active
topics:
  - video-intake
  - disco-rag
  - rag
  - structured-reading
  - argument-tree
  - cross-document-relations
  - context-pack-preparation
  - evidence-support
  - bilibili
projects:
  - verified-action-knowledge-system
source_family: bilibili-video-source
upstream_sources: []
verification_status: unverified
candidate_relation_suggestions: []
tags:
  - raw-video
  - bilibili
  - candidate-only
---

# 复旦大学DISCO-RAG方案让RAG从搜索变分析

## 为什么收录

这条视频介绍 DISCO-RAG，重点不是“怎么搜到更多资料”，而是“搜到资料后怎么读懂、组织、处理冲突”。它对 VAKS 有候选价值，因为 VAKS 的 context pack / evidence envelope / action basis 也不能只靠召回材料，还需要区分主次、条件、支持、反驳、补充和冲突。

本卡只记录视频公开元数据和本地 ASR。视频里对论文成绩、benchmark、模型配置、实验结论的描述没有原始论文锚点支撑，不能直接进入 reviewed knowledge。

## 来源卡

- 平台：Bilibili
- 原始链接：https://www.bilibili.com/video/BV1zadJBtErG/
- 标题：复旦大学DISCO-RAG方案让RAG从搜索变分析
- 作者 / UP 主：大模型论文解读
- 发布时间：2026-04-18 07:58:17 +08:00
- 视频时长：488 秒
- 收录时间：2026-06-04 19:24:13 +08:00
- 访问边界：public_no_cookies
- 来源限制：公开视频无公开字幕；当前 transcript 来自本地 ASR，不是人工校对稿；视频简介没有给论文链接。

## 获取与转写

```yaml
subtitle_status:
  view_api: empty
  player_api: empty_or_failed_tls
transcript_method: local_asr
asr_engine: faster-whisper
asr_model: small
asr_device: cuda
asr_compute_type: float16
language: zh
segment_count: 199
text_chars: 2753
transcript_quality: medium
media_retention: deleted
scratch_cleanup: first metadata/playurl run hit TLS EOF; public audio mirror 0 incomplete; mirror 1 succeeded; downloaded public audio deleted after ASR
project_visible_artifacts: yes
transcript_location: raw/videos/2026-06-04-bilibili-disco-rag-search-to-analysis-source/transcript.txt
segments_location: raw/videos/2026-06-04-bilibili-disco-rag-search-to-analysis-source/segments.md
transcript_metadata_location: raw/videos/2026-06-04-bilibili-disco-rag-search-to-analysis-source/transcript-meta.json
ledger_location: raw/videos/2026-06-04-bilibili-disco-rag-search-to-analysis-source/acquisition-ledger.json
```

说明：

```text
公开字幕检查为空或受 TLS 影响失败，所以本次走公开视频音频 + 本地 GPU ASR。
没有使用 cookies，没有使用云 API。
临时音频已删除，只保留 transcript、segments、metadata、ledger。
字幕 / ASR 是 raw/source text，不是 reviewed evidence。
本卡摘要是 candidate comprehension，不是 truth。
```

## 人话摘要

视频提出一个 RAG 常见误区：回答错不一定是“没搜到”，很多时候是“搜到了但没读懂”。传统 RAG 会把检索回来的段落平铺给模型，段落内部哪句是核心结论、哪句是前提条件，段落之间是支持、反驳、补充还是无关，都容易被抹平。结果是材料里明明有正确文档，模型仍然可能混用冲突资料，生成错误答案。

DISCO-RAG 的思路被概括成三步。第一步，对每个段落画论证树，把段落拆成最小语义单元，标记核心内容、辅助说明和单元之间的关系。第二步，对检索回来的段落做两两关系分析，形成支持、反驳、补充、无关等跨段关系网。第三步，综合用户问题、原始段落、论证树和关系网，先生成提纲，再按提纲写最终答案。

视频还声称该方法在长文档推理、问答、科学摘要等任务上表现好，并通过 ablation 说明论证树、关系网、提纲三个模块都重要；部署上可用小模型做结构分析、大模型做最终生成。但这些实验和模型配置都需要找到原始论文或代码再核验。

对 VAKS 来说，这条视频的价值是强化一个边界：retrieval hit 不是 evidence support。正确资料被召回，只是 context preparation 的起点；要进入 action basis，仍需要支撑关系、反驳关系、scope 条件、冲突处理和可审计提纲。

## 关键实体置信度

```text
confirmed:
  - Bilibili video BV1zadJBtErG
  - title: 复旦大学DISCO-RAG方案让RAG从搜索变分析
  - UP 主: 大模型论文解读
  - published_at: 2026-04-18 07:58:17 +08:00
  - duration: 488s

likely:
  - DISCO-RAG
  - Fudan University / 复旦大学
  - RAG
  - argument tree / 论证树
  - cross-passage relation graph / 段落关系网
  - outline-then-answer
  - ablation experiment
  - Llama 3.1 8B
  - Llama 3.3 70B

unclear:
  - ASR 大量把 RAG 识别成 "ARG"。
  - ASR 把 DISCO-RAG 识别成 "Disco ARG / Scoff ARG"。
  - ASR 把 LLM 识别成 "ALM"。
  - ASR 对 benchmark 名称、模型版本、指标名称均不可靠。

needs independent verification:
  - DISCO-RAG 原始论文标题、作者、机构、arXiv / GitHub 链接。
  - 长文档推理 25 万 tokens、问答和科学摘要评测成绩。
  - "8B DISCO-RAG 超过 70B 普通 RAG"。
  - "不训练超过微调普通 RAG"。
  - 具体三模块 ablation 结果。
```

## 时间轴 / 分段

- 00:00-01:16：提出问题：RAG 回答错不一定是检索错，可能是模型不会读。
- 01:16-01:46：传统优化如 rerank、query rewrite、chunk compression、多轮检索仍主要优化“搜”。
- 01:46-02:08：DISCO-RAG 核心：从“搜”转向“读”，构建结构化理解。
- 02:08-02:34：第一步：给段落画论证树，拆最小语义单元、标主次和关系。
- 02:34-02:59：第二步：对全部检索段落做两两关系分析，形成支持/反驳/补充/无关关系网。
- 02:59-03:17：第三步：先列提纲，再生成答案。
- 03:17-04:30：实验表现、长文档推理、问答、科学摘要、ablation、噪声稳健性。
- 04:30-05:31：部署策略：小模型做结构分析，大模型做生成；结构信息比单纯增大模型更有效。
- 05:31-06:14：深层意义：自然语言文本有逻辑骨架，不能只当句子堆。
- 06:14-07:09：应用价值：检索已优化但回答质量上不去时，从“读”的环节入手。
- 07:09-08:07：未来方向：结构化理解可能扩展到摘要、翻译、问答等任务。

## 视频里直接说了什么

- RAG 失败不总是检索失败，很多时候是模型不知道如何理解和组织召回材料。
- 传统 RAG 会抹平段落内部的主次、条件和逻辑关系，也抹平段落之间的支持/反驳关系。
- DISCO-RAG 做三件事：段落论证树、跨段关系网、先提纲再回答。
- 论证树把段落拆成最小语义单元，并标注核心/辅助和关系类型。
- 跨段关系网判断召回段落之间是支持、反驳、补充还是无关。
- 提纲把用户问题、原始段落、论证树、关系网组织成回答计划。
- 视频声称三个模块缺一不可，光加普通规划不够。
- 视频声称可以用小模型做结构分析、大模型做生成，降低部署成本。
- 视频强调自然语言文本有逻辑骨架，结构化理解可能比单纯找更多资料更重要。

## 我的理解 / 推断

这条视频和 VAKS 当前边界非常贴合，但仍然只能作为候选压力。它提醒的是：

```text
retrieval:
  找到相关材料。

structured reading:
  判断每段里的 claim / condition / warrant / caveat。

relation analysis:
  判断材料之间 support / challenge / refine / scope-limit。

outline:
  形成可审计的回答计划。

answer/action basis:
  只有经过 support check、conflict exposure、scope/risk check 后才可能 action-ready。
```

对 VAKS 的最小吸收不是新建 DISCO-RAG 模块，而是把它放进已有 lazy gate：

```text
普通 query:
  不需要完整论证树。

risk_sensitive_answer / action basis / strong relation / challenged point:
  可以考虑 evidence envelope + relation map + outline-before-answer。
```

## 反漏提取检查

```text
pain point:
  - RAG 找到了正确材料，但模型没理解材料内部主次、条件和材料之间冲突，导致答案仍错。

workflow:
  - 检索候选段落。
  - 对每段构建论证树。
  - 对段落两两分析关系。
  - 生成回答提纲。
  - 按提纲产出最终回答。

tools / plugins:
  - DISCO-RAG
  - RAG
  - LLM-based structural analysis
  - Llama 3.1 8B / Llama 3.3 70B as claimed by video

information structure:
  - paragraph / passage
  - semantic unit
  - argument tree
  - relation graph
  - outline
  - generated answer

judgment mechanism:
  - 视频使用论文实验、benchmark 和 ablation 叙述作为判断来源。
  - 当前没有原始论文链接或代码，因此只能作为 candidate comprehension。

user experience:
  - 优点是回答更有结构，能处理长文档、冲突材料和噪声。
  - 风险是结构分析本身如果错，会制造更有组织的错误。

automation boundary:
  - 自动结构分析可以做 review input / context preparation。
  - 自动结构分析不能直接决定证据支持、truth confidence 或 action readiness。

risk:
  - ASR 对关键术语误识别严重。
  - 视频对实验成绩的描述需要原文核验。
  - 段落关系预测如果由 LLM 自动生成，可能把错误 relation 伪装成结构化事实。
  - 结构化提纲可能增强说服力，反而掩盖证据不足。

fit for us:
  - 强化 VAKS 的 evidence-aware review、known challenge exposure、context-pack coverage 和 action-basis lazy gate。
  - 支持把 "known support / known counterevidence / known gaps / known conflicts" 做成重要回答前的结构化草案。
  - 支持 GraphRAG / relation-neighborhood 只能作为 activation；reviewed relation 仍需 evidence-aware review。

challenge to us:
  - 如果 VAKS 只做召回和摘要，不做结构化 support/challenge 检查，就会在高风险回答里出问题。
  - 未来 context pack 可能需要 outline-before-answer，但不能让所有普通 query 都变重。
```

## 可抽取 Candidate Points

1. `retrieval_hit_not_structured_understanding`

候选结论：检索命中并不等于模型理解了材料；高风险回答需要显式处理段落内部主次、条件和跨段冲突。

VAKS 边界：直接强化 `retrieval hit != evidence support`。

2. `argument_tree_as_review_input`

候选结论：段落论证树可作为 evidence packet / review input 的候选形式，帮助区分 claim、condition、warrant、caveat。

VAKS 边界：自动论证树不是 reviewed knowledge。

3. `cross_passage_relation_map_as_candidate_collision`

候选结论：跨段支持/反驳/补充关系图可作为 point collision 和 known challenge exposure 的候选辅助。

VAKS 边界：自动关系图是 candidate relation suggestions，不是 reviewed relation。

4. `outline_before_answer_for_risk_sensitive_context`

候选结论：风险敏感回答或 action basis 可以先生成可审计提纲，再写答案。

VAKS 边界：普通 query 不强制；action-ready 仍需 evidence support / sufficiency。

## 可借鉴

- 把“读懂材料”从“召回更多材料”中分离出来。
- 在重要 context pack 里暴露 support / challenge / condition / scope limit。
- 对长文档和多来源冲突问题，先生成 relation map 和 outline。
- 用小模型做候选结构分析、大模型做最终表达，作为未来成本策略候选。

## 不能直接借鉴

- 不把 DISCO-RAG 实验成绩当 reviewed fact。
- 不把自动论证树当 source evidence。
- 不把自动关系网当 reviewed relation。
- 不因为视频说“轻量即插即用”就直接实现或安装。
- 不让结构化输出的整齐外观变成 authority signal。

## 风险和不确定

- 无公开字幕，ASR 把 RAG / DISCO-RAG / LLM 等关键术语识别不稳定。
- 视频没有给原始论文链接，需要单独找 paper / code。
- 所有 benchmark、模型配置、ablation 结论都未核验。
- 自动结构分析有二次幻觉风险，必须保留 source anchor 和 human review gate。

## VAKS 归位

```text
Capture:
  作为 raw video source card 保存 provenance、ASR、segments、ledger。

Understand:
  本卡摘要和 candidate points 属于 candidate comprehension。

Review:
  当前不进入 reviewed knowledge。若后续找到 DISCO-RAG 原始论文，可另做 paper source card。

Connect:
  连接到 Evidence Packet、known challenge exposure、point collision、context-pack coverage、GraphRAG is not truth。

Activation / Context Pack:
  可作为 high-risk context pack 的候选结构：argument tree + relation map + outline。

Decision / Action:
  当前不支持直接采用 DISCO-RAG；需要原论文、代码、评测和本地 fixture。

Use Ledger / Feedback:
  若未来测试此类结构化 reading gate，应记录 missed challenge、bad relation、bad outline 和 answer correction。
```

## 处理等级

当前等级：`medium`

理由：

```text
已保留完整转写、时间轴、关键实体置信度、candidate points、可借鉴 / 不可借鉴和 VAKS fit。
它对高风险 context pack / evidence-aware review 有候选价值，但原始论文和实验结果未核验。
```

升级到 `heavy` 的条件：

- 找到 DISCO-RAG 原始论文 / arXiv / GitHub。
- 用户要求进入 RAG / evidence-envelope Direction Review。
- 需要用本项目 fixture 测试 argument tree / relation map / outline-before-answer 是否降低遗漏和冲突误用。

## 下一步

```text
建议保留为 raw-only / candidate-only source card。
暂不改主架构。
后续若继续出现同类 "structured reading after retrieval" 资料，可和 GraphRAG / evidence packet / context-pack coverage 一起做 Direction Review。
```
