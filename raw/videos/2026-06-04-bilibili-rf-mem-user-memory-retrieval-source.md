---
type: source
status: source-captured
title: '[Agent记忆] ICLR26-RF-Mem-熟悉度驱动的快慢双路径记忆检索'
source_id: bilibili-BV1WuLH66EHg
source_uri: bilibili:BV1WuLH66EHg
source_url: https://www.bilibili.com/video/BV1WuLH66EHg/
source_type: video
platform: bilibili
platform_id: BV1WuLH66EHg
author: Agent智能体深度研究院
publisher: Agent智能体深度研究院
published_at: '2026-05-18 08:00:00 +08:00'
updated_at:
duration: 542s
captured_at: '2026-06-04 19:28:30 +08:00'
captured_by: Codex
raw_location: raw/videos/2026-06-04-bilibili-rf-mem-user-memory-retrieval-source.md
processing_mode: runner
processing_level: medium
review_priority: normal
review_owner: Codex
formalization_status: raw-only
access_boundary: public
transcript_method: local_asr
transcript_location: raw/videos/2026-06-04-bilibili-rf-mem-user-memory-retrieval-source/transcript.txt
segments_location: raw/videos/2026-06-04-bilibili-rf-mem-user-memory-retrieval-source/segments.md
transcript_metadata_location: raw/videos/2026-06-04-bilibili-rf-mem-user-memory-retrieval-source/transcript-meta.json
ledger_location: raw/videos/2026-06-04-bilibili-rf-mem-user-memory-retrieval-source/acquisition-ledger.json
media_retention: deleted
source_status: active
topics:
  - video-intake
  - rf-mem
  - agent-memory
  - memory-retrieval
  - recollection-familiarity
  - personalization
  - activation
  - bilibili
projects:
  - verified-action-knowledge-system
source_family: bilibili-video-source
upstream_sources:
  - raw/papers/2026-06-04-rf-mem-recollection-familiarity-source.md
verification_status: unverified
candidate_relation_suggestions: []
tags:
  - raw-video
  - bilibili
  - candidate-only
---

# [Agent记忆] ICLR26-RF-Mem-熟悉度驱动的快慢双路径记忆检索

## 为什么收录

这条视频解读论文 `Evoking User Memory: Personalizing LLM via Recollection-Familiarity Adaptive Retrieval`，也就是 RF-Mem。它的核心价值是把长期记忆检索从固定 Top-K / 固定多轮，改成按熟悉度切换快慢路径。

本卡只记录视频公开元数据和本地 ASR。RF-Mem 的事实性细节以原论文 source card 为准：`raw/papers/2026-06-04-rf-mem-recollection-familiarity-source.md`。视频解读本身属于 candidate comprehension，不是 reviewed knowledge。

## 来源卡

- 平台：Bilibili
- 原始链接：https://www.bilibili.com/video/BV1WuLH66EHg/
- 标题：[Agent记忆] ICLR26-RF-Mem-熟悉度驱动的快慢双路径记忆检索
- 作者 / UP 主：Agent智能体深度研究院
- 发布时间：2026-05-18 08:00:00 +08:00
- 视频时长：542 秒
- 收录时间：2026-06-04 19:28:30 +08:00
- 访问边界：public_no_cookies
- 原论文：https://arxiv.org/pdf/2603.09250

## 获取与转写

```yaml
subtitle_status:
  view_api: empty
  player_api: empty
transcript_method: local_asr
asr_engine: faster-whisper
asr_model: small
asr_device: cuda
asr_compute_type: float16
language: zh
segment_count: 231
text_chars: 2959
transcript_quality: medium
media_retention: deleted
scratch_cleanup: downloaded public audio deleted after ASR
project_visible_artifacts: yes
transcript_location: raw/videos/2026-06-04-bilibili-rf-mem-user-memory-retrieval-source/transcript.txt
segments_location: raw/videos/2026-06-04-bilibili-rf-mem-user-memory-retrieval-source/segments.md
transcript_metadata_location: raw/videos/2026-06-04-bilibili-rf-mem-user-memory-retrieval-source/transcript-meta.json
ledger_location: raw/videos/2026-06-04-bilibili-rf-mem-user-memory-retrieval-source/acquisition-ledger.json
```

说明：

```text
公开字幕检查为空，所以本次走公开视频音频 + 本地 GPU ASR。
没有使用 cookies，没有使用云 API。
临时音频已删除，只保留 transcript、segments、metadata、ledger。
字幕 / ASR 是 raw/source text，不是 reviewed evidence。
本卡摘要是 candidate comprehension，不是 truth。
```

## 人话摘要

视频把 RF-Mem 讲成一个运行时检索调度器：长期记忆系统不只是“记得多”，还要判断当前问题到底该秒查一下，还是值得多花几轮去重构上下文。熟悉的问题走 Familiarity 快路径，不熟或不确定的问题走 Recollection 慢路径。

它先做 probe retrieval，拿到候选记忆和相似度分数，再用平均相似度和分布熵判断熟悉度。熟悉度高或候选集中，就直接返回 Top-K；熟悉度低或候选分散，就把候选记忆做 KMeans 聚类，用 cluster centroid 和 query 做 alpha mix，生成新的 recollect query，多轮扩展证据链。

视频强调 RF-Mem 和 MemGAS 是互补关系：MemGAS 更像是在问记忆库怎么组织成多粒度关联结构；RF-Mem 更像是在问面对当前 query，要不要启动更深的在线回忆。

对 VAKS 来说，它最值得借鉴的是“把不确定性前置到检索控制里”：不是所有查询都重，也不是所有查询都轻；普通 activation 保持快，模糊/长尾/需要多段证据的问题才打开更深检索。但这仍属于 activation / context-pack preparation，不是 truth confidence。

## 关键实体置信度

```text
confirmed:
  - Bilibili video BV1WuLH66EHg
  - title: [Agent记忆] ICLR26-RF-Mem-熟悉度驱动的快慢双路径记忆检索
  - UP 主: Agent智能体深度研究院
  - published_at: 2026-05-18 08:00:00 +08:00
  - duration: 542s
  - arXiv PDF: https://arxiv.org/pdf/2603.09250

likely:
  - RF-Mem
  - Recollection-Familiarity Memory Retrieval
  - PersonaMem
  - PersonaBench
  - LongMemEval
  - MemoryBank
  - HyDE
  - Search-o1
  - MemGAS

unclear:
  - ASR 把 RF-Mem 识别成 RFMAM。
  - ASR 把 Dense Retrieval 识别成 Dance Retrieval。
  - ASR 把 entropy 识别成“商”。
  - ASR 把 embedding / retriever / query 等技术词识别不稳定。

needs independent verification:
  - 所有实验数字、模型设置、benchmark 细节，以原论文为准。
  - 视频中关于 MemGAS 的互补判断，需要结合已有 MemGAS source/review 再判断。
```

## 时间轴 / 分段

- 00:00-00:39：定位 RF-Mem：它问的是记忆运行时怎么找，不是记忆库怎么存。
- 00:39-01:09：论文正式信息、作者机构和 Recollection / Familiarity 双加工理论。
- 01:09-01:48：传统 dense Top-K 对应 Familiarity，快但容易抓表层相似。
- 01:49-02:28：probe retrieval、平均相似度、分布熵，以及快慢路径切换。
- 02:29-03:07：快路径例子：明确匹配的问题直接 Top-K。
- 03:07-04:19：慢路径例子和实现：Top-N、KMeans、centroid、alpha mix、recollect query。
- 04:19-05:00：beam width、fanout、maximum rounds 控制预算。
- 05:00-06:21：实验：PersonaMem、PersonaBench、LongMemEval、准确率和延迟。
- 06:21-07:09：RF-Mem 是轻量取舍，不是单表碾压；可叠加 MemoryBank、HyDE、Search-o1。
- 07:09-07:52：和 MemGAS 互补：结构组织 vs 在线检索调度。
- 07:52-08:39：工程价值和局限：不确定性前置、熵只是代理、embedding 质量影响判断。
- 08:39-09:01：伦理边界：更强记忆唤起需要防止敏感信息意外回流。

## 视频里直接说了什么

- RF-Mem 研究的是个性化 LLM 用户记忆检索。
- 它不是改变记忆如何存，而是改变记忆如何找。
- Familiarity 是快速熟悉感；Recollection 是较慢的情境重构。
- RF-Mem 先做 probe retrieval，用平均相似度和分布熵判断是否熟悉。
- 快路径直接返回 Top-K，低延迟、低成本。
- 慢路径用 KMeans 聚类候选记忆，再用 alpha mix 扩展 query，多轮找证据链。
- 慢路径受 beam width、fanout、maximum rounds 限制，不是无限搜索。
- RF-Mem 相比固定 Top-K 和固定 Recollection only 更符合产品预算。
- RF-Mem 和 MemGAS 互补：一个偏在线检索策略，一个偏记忆结构组织。
- 局限包括熵代理不完美、embedding 空间校准、文本记忆范围、时间更新、记忆冲突和敏感信息风险。

## 我的理解 / 推断

这条视频对 VAKS 的意义是强化 Activation Tier / context activation 的运行时策略：

```text
hot / familiar:
  直接读早、查快，不代表更可信。

uncertain / scattered:
  启动更深召回，用更多预算找到多段候选记忆。

retrieval control:
  用不确定性决定检索深度。

truth boundary:
  检索深度、相似度、熵、记忆命中都不能改变 truth confidence。
```

它不是一个 review/truth 方法，而是一个 activation / personalization retrieval 方法。对 VAKS 最小吸收是：

```text
ordinary query:
  走轻检索。

ambiguous / long-tail / memory-dependent / user-specific query:
  允许更深 activation，但输出仍是 candidate context。

risk-sensitive answer:
  深召回之后仍要 evidence support、temporal applicability、sensitive memory gate。
```

## 反漏提取检查

```text
pain point:
  - 全量用户历史太贵，一次性 Top-K 太浅，固定多轮又太慢。

workflow:
  - probe retrieval。
  - 计算平均相似度和分布熵。
  - 熟悉问题走 Familiarity Top-K。
  - 不熟或分散问题走 Recollection。
  - Recollection 通过 KMeans + alpha mix 多轮扩展。
  - beam / fanout / rounds 控制预算。

tools / plugins:
  - RF-Mem
  - dense retriever / embedding space
  - KMeans
  - MemoryBank / HyDE / Search-o1 as adaptive integrations

information structure:
  - user memory
  - query embedding
  - probe candidates
  - similarity scores
  - entropy
  - cluster centroid
  - recollect query

judgment mechanism:
  - 视频以论文实验为主要依据。
  - 当前事实核验以原论文 source card 为准。

user experience:
  - 熟悉问题保持低延迟。
  - 不确定问题获得更充分上下文。

automation boundary:
  - 自动检索路由只决定 activation depth。
  - 自动检索路由不能决定 truth、relation strength、source reliability 或 action readiness。

risk:
  - 更强记忆唤起可能带回敏感历史。
  - 相似度和熵可能误判熟悉度。
  - embedding 空间偏差会影响路由。
  - 个性化检索可能放大过时偏好或错误用户画像。

fit for us:
  - 支持 VAKS 的 Activation Tier：hot means read early, not believe more。
  - 支持把 retrieval depth 做成 lazy gate。
  - 支持 feedback / missed-memory 作为未来检索策略校准信号，但不直接改 truth。

challenge to us:
  - VAKS 需要防止“记忆召回更深 = 更可信”的误解。
  - VAKS 的个性化记忆必须加 sensitive memory / consent / scope gate。
```

## 可抽取 Candidate Points

1. `familiarity_uncertainty_as_activation_router`

候选结论：可以用检索结果的集中度和相似度作为轻量 activation-depth 路由信号。

VAKS 边界：它只决定读多少候选记忆，不决定相信什么。

2. `recollection_path_as_budgeted_deep_activation`

候选结论：不熟悉或分散的问题可以启动预算受控的深召回，而不是固定 Top-K。

VAKS 边界：深召回输出仍是 candidate context。

3. `online_memory_retrieval_complements_memory_structure`

候选结论：RF-Mem 与 MemGAS 互补：一个偏在线检索策略，一个偏离线/近线记忆结构组织。

VAKS 边界：两者都不能成为 truth layer。

4. `sensitive_memory_resurfacing_gate`

候选结论：更强的长期记忆唤起需要敏感信息重现保护、scope 限制和用户意图确认。

VAKS 边界：隐私/安全 gate 是 action/process boundary，不是 truth confidence。

## 可借鉴

- 用不确定性路由决定 activation 深度。
- 熟悉问题快查，不熟问题慢查。
- 把深召回预算显式化：beam、fanout、rounds。
- 把 RF-Mem 放在 MemoryBank / MemGAS 这类 memory structure 上层，作为 online retrieval controller。
- 把 missed feedback、scope mismatch、bad recall 作为未来检索路由校准信号。

## 不能直接借鉴

- 不把相似度、熵、召回路径当 truth confidence。
- 不把 RF-Mem 的 benchmark 分数当本项目效果保证。
- 不直接实现用户记忆长期唤起，除非有 consent、sensitive-memory gate 和 retention policy。
- 不把 personalized memory retrieval 与 reviewed knowledge 混成一层。

## 风险和不确定

- 无公开字幕，当前文本来自 ASR。
- 视频解读依赖论文，技术事实以论文 source card 为准。
- RF-Mem 的 benchmark 是文本对话记忆，不等于 VAKS 多类型资料库。
- 个性化记忆召回涉及隐私、过期偏好、冲突记忆和敏感信息。

## VAKS 归位

```text
Capture:
  作为 raw video source card 保存 provenance、ASR、segments、ledger。

Understand:
  本卡摘要和 candidate points 属于 candidate comprehension。

Review:
  当前不进入 reviewed knowledge。论文 source card 可作为后续 Direction Review 输入。

Connect:
  连接到 Activation Tier、MemGAS、Feedback Ledger、agent memory quarantine、retrieval is not truth。

Activation / Context Pack:
  可作为 activation-depth router 候选。

Decision / Action:
  当前不支持实现 RF-Mem；需要隐私/安全/本地 fixture review。

Use Ledger / Feedback:
  可将 bad recall / missed memory / over-personalization 作为未来 retrieval calibration 信号。
```

## 处理等级

当前等级：`medium`

理由：

```text
视频本身已完整覆盖论文主张，但事实细节需以原论文为准。
已保留转写、时间轴、关键实体、candidate points 和 VAKS fit。
```

升级到 `heavy` 的条件：

- 用户要求把 RF-Mem 纳入 Direction Review。
- 需要和 MemGAS / Activation Tier / Feedback Ledger 形成候选蒸馏包。
- 需要做本地 memory retrieval fixture，测试快慢路由是否减少 missed memory。

## 下一步

```text
建议保留为 raw-only / candidate-only source card。
原论文另存 paper source card。
暂不改主架构。
未来可归入 "personalized memory activation / retrieval-depth routing" Direction Review。
```
