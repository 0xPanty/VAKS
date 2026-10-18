---
type: source
status: source-captured
title: '[Agent记忆] ICLR26-MemGAS-多粒度记忆关联与自适应选择'
source_id: bilibili-BV1T7LE6BERV
source_uri: bilibili:BV1T7LE6BERV
source_url: https://www.bilibili.com/video/BV1T7LE6BERV/
source_type: video
platform: bilibili
platform_id: BV1T7LE6BERV
author: 'Agent智能体深度研究院'
publisher: 'Agent智能体深度研究院'
published_at: '2026-05-17 16:42:45 +08:00'
updated_at:
duration: 530s
captured_at: '2026-06-04 22:53:05 +08:00'
captured_by: Codex
raw_location: raw/videos/2026-06-04-bilibili-memgas-multi-granularity-memory-source.md
processing_mode: runner
processing_level: medium
review_priority: normal
review_owner: Codex
formalization_status: raw-only
access_boundary: public_no_cookies
transcript_method: local_asr
transcript_location: raw/videos/2026-06-04-bilibili-memgas-multi-granularity-memory-source/transcript.txt
segments_location: raw/videos/2026-06-04-bilibili-memgas-multi-granularity-memory-source/segments.md
transcript_metadata_location: raw/videos/2026-06-04-bilibili-memgas-multi-granularity-memory-source/transcript-meta.json
ledger_location: raw/videos/2026-06-04-bilibili-memgas-multi-granularity-memory-source/acquisition-ledger.json
media_retention: deleted
source_status: active
topics:
  - memgas
  - agent-memory
  - multi-granularity-memory
  - activation-tier
  - context-pack
  - association-activation
  - ppr
  - gmm
  - long-term-memory
  - candidate-only
  - video-intake
  - bilibili
projects:
  - verified-action-knowledge-system
source_family: bilibili-memgas-multi-granularity-memory
upstream_sources:
  - https://arxiv.org/pdf/2505.19549
  - outputs/review/2026-05-30-memgas-multi-granularity-memory-activation-alpha.md
verification_status: unverified-video-summary
candidate_relation_suggestions:
  - candidate:multi_granularity_activation_views
  - candidate:memory_association_graph_as_activation_not_relation
  - candidate:entropy_routing_as_uncertainty_proxy_not_truth
  - candidate:gmm_edge_selection_as_recall_filter_not_support
  - candidate:ppr_memory_spread_as_context_activation
  - candidate:llm_filter_after_retrieval_not_review
  - candidate:sensitive_memory_recall_scope_gate
  - candidate:memgas_rfmem_complementarity
tags:
  - raw-video
  - bilibili
  - candidate-only
---

# 视频资料：MemGAS 多粒度长期记忆

## 为什么收录

这条视频解读论文 `From Single to Multi-Granularity: Toward Long-Term Memory Association and Selection of Conversational Agents`，也就是 MemGAS。它不是一个新的主证据来源；项目里已经有过 MemGAS 论文与代码的 alpha review：

```text
outputs/review/2026-05-30-memgas-multi-granularity-memory-activation-alpha.md
```

本视频的价值是中文讲解补充：它把 MemGAS 的核心讲成一句很适合 VAKS 的话：

```text
会记住还不够，关键是会在正确粒度上想起来。
```

VAKS 边界：

```text
Bilibili URL = source provenance
ASR = raw source text
本卡摘要 = candidate comprehension
MemGAS / GMM / PPR / entropy routing = activation / context preparation
memory graph / association edge != reviewed relation
retrieval score / entropy / PPR rank != truth / support / action basis
promotion / action basis = 后续 evidence-aware review
```

## 来源卡

- 平台：Bilibili
- 原始链接：https://www.bilibili.com/video/BV1T7LE6BERV/
- BV 号：BV1T7LE6BERV
- 标题：[Agent记忆] ICLR26-MemGAS-多粒度记忆关联与自适应选择
- UP 主：Agent智能体深度研究院
- 发布时间：2026-05-17 16:42:45 +08:00
- 视频时长：530 秒
- 视频描述里的论文链接：https://arxiv.org/pdf/2505.19549
- 收录时间：2026-06-04
- 访问边界：public_no_cookies

## 获取与转写

```yaml
subtitle_status: public_subtitle_checked_empty
transcript_method: local_asr
asr_engine: faster-whisper
asr_model: base
asr_device: cuda
compute_type: float16
language: zh
segment_count: 244
text_chars: 2778
elapsed_seconds: 47.92
media_retention: deleted
cloud_api: false
cookies: false
project_visible_artifacts: true
transcript_location: raw/videos/2026-06-04-bilibili-memgas-multi-granularity-memory-source/transcript.txt
segments_location: raw/videos/2026-06-04-bilibili-memgas-multi-granularity-memory-source/segments.md
transcript_metadata_location: raw/videos/2026-06-04-bilibili-memgas-multi-granularity-memory-source/transcript-meta.json
ledger_location: raw/videos/2026-06-04-bilibili-memgas-multi-granularity-memory-source/acquisition-ledger.json
```

说明：

- 公开视频字幕接口为空。
- 默认研究模型 `small` 初次尝试时遇到 HuggingFace TLS EOF，未完成转写；随后用本地 `base` 模型完成 quick-draft ASR。
- 本卡依赖视频描述与既有 MemGAS alpha review 做关键实体校准；ASR 本身对专有名词误识别较多。

## 人话摘要

视频讲的是长期对话 Agent 的记忆问题：用户和 Agent 聊了几个月之后，系统到底该记住整段会话、每一句细节、摘要，还是关键词？MemGAS 的回答是不能只选一个，因为单一粒度会两头失衡：粗粒度保留上下文但噪声大，细粒度保留事实细节但容易丢掉跨会话关系，摘要和关键词又可能过度压缩。

MemGAS 的方法是给每段对话保留四种记忆视图：session、turn、summary、keyword。新记忆加入时，系统用相似度和 GMM 判断哪些历史记忆值得建立关联，只把相关记忆连进关联图。查询时，它看不同粒度上的相似度分布和熵：如果某个粒度匹配很集中，就提高这个粒度的权重；如果匹配很散，就降低权重。随后用 Personalized PageRank 在记忆关联图上传播相关性，再由 LLM 过滤重复、无关或噪声记忆。

视频的核心结论和项目已有 alpha review 一致：MemGAS 适合借鉴为 `Multi-Granularity Activation Views`，帮助系统在不同记忆/资料视图之间选择更合适的上下文；它不负责判断知识是否真实，也不能把记忆图边当作 reviewed relation。

## 关键实体置信度

```text
confirmed:
  - Bilibili video BV1T7LE6BERV
  - title: [Agent记忆] ICLR26-MemGAS-多粒度记忆关联与自适应选择
  - UP 主: Agent智能体深度研究院
  - published_at: 2026-05-17 16:42:45 +08:00
  - duration: 530s
  - arxiv pdf in video description: https://arxiv.org/pdf/2505.19549
  - existing project review: outputs/review/2026-05-30-memgas-multi-granularity-memory-activation-alpha.md

confirmed_by_existing_alpha_review:
  - paper title: From Single to Multi-Granularity: Toward Long-Term Memory Association and Selection of Conversational Agents
  - official code URL: https://github.com/Applied-Machine-Learning-Lab/ICLR2026_MemGAS
  - observed commit in prior review: c2d4e9fdc331074802a711baf4371197f9194399
  - four memory views: session / turn / summary / keyword
  - GMM association and Personalized PageRank retrieval path

likely:
  - LoCoMo, LongMemEval s, LongMemEval m, Long MT Bench plus
  - Full History, Contriever, SeCom, HippoRAG 2, RAPTOR, A-Mem
  - entropy routing as query-time granularity selection

unclear_or_asr_noisy:
  - ASR often says MemGuess / mangas for MemGAS.
  - ASR says 减所 / 照回 / 机力度 for retrieval / recall / granularity.
  - ASR metric names like F1 / Recall@3 / NDCG need paper table confirmation before exact citation.

needs paper/source check before reuse:
  - all benchmark numbers
  - author/institution details
  - seed node and temperature values
  - cost and latency claims
```

## 时间轴 / 分段

- 00:00-00:42：提出长期对话记忆问题：整段、细节、摘要、关键词不能只选一种。
- 00:43-01:36：定位到 agent 系统地图：MemGAS 处理用户长期对话怎样保存、联想和召回。
- 01:37-02:20：介绍论文来源、机构、四种记忆粒度：session、turn、summary、keyword。
- 02:20-03:10：说明新记忆加入时用 GMM 判断相关/无关历史记忆，并建立关联图。
- 03:10-03:57：查询时通过不同粒度的相似度分布和熵选择权重。
- 03:57-04:48：种子节点、Personalized PageRank 和受限联想扩散。
- 04:48-05:33：用跨会话课程数量例子说明多粒度关联如何补全上下文。
- 05:33-06:00：图传播会带噪声，所以用 LLM 过滤重复和无关记忆。
- 06:00-07:18：实验基准、代表指标、消融实验。
- 07:18-08:24：成本、延迟、与知识图谱 RAG / 技能图的区别。
- 08:24-08:49：真实产品风险：摘要/关键词不稳、相似度误联想、隐私、冲突更新、成本。
- 08:49-08:49：总结：长期记忆要拆粒度、建关联、按问题选择和传播。

## 视频里直接说了什么

- 长期记忆不只是检索最相似片段，而是要同时建多粒度记忆、跨记忆关联，并在每次查询时自适应选择合适粒度。
- 单一粒度会失衡：session 级可能噪声大，turn 级可能丢上下文，summary / keyword 可能压缩或简化。
- MemGAS 维护 session、turn、summary、keyword 四类记忆。
- 新对话进入时，MemGAS 用相似度和 GMM 把历史记忆分成相关集合与无关集合，相关记忆才连边。
- 查询时，用不同粒度的相似度分布和熵来判断哪个粒度更确定。
- PPR 在关联图上传播相关性，让稳定相连的记忆也被带出。
- 图传播可能带来不相关内容，所以还需要 LLM 过滤。
- 实验里 MemGAS 在多个长期记忆基准上优于若干 baseline，但具体数字要以论文表格为准。
- MemGAS 的图不是技能执行图，也不是知识图谱 RAG；它是记忆关联图。
- 真实产品中仍有摘要/关键词生成不稳、错误联想、隐私、冲突更新、成本控制等问题。

## 我的理解 / 推断

这条视频对 VAKS 的新增架构价值不高，因为核心材料已经在 2026-05-30 的 MemGAS alpha review 里处理过。它的价值是“中文解释 + 和 RF-Mem/CoMe 候选簇形成互证压力”。

它进一步帮助我们给三类东西排位置：

```text
MemGAS:
  记忆库内部怎么分粒度、建关联、按查询选择视图。

RF-Mem:
  当前问题是否值得启动更慢、更深的回忆检索。

CoMe:
  长期 memory store 如何组织成可递归检索的结构。
```

对 VAKS 最重要的边界依然是：

```text
多粒度记忆 / 关联图 / PPR / 熵路由
= activation / context preparation
!= truth confidence / reviewed relation / action basis
```

## 反漏提取检查

```text
pain point:
  - Agent 长期对话历史越来越多，flat top-k 或单一摘要不能同时保留细节、关系和上下文。

workflow:
  - 对话进入 memory store。
  - 生成 session / turn / summary / keyword 四类视图。
  - 新旧记忆相似度比较。
  - GMM 选择相关旧记忆建边。
  - 查询时按粒度相似度分布和熵加权。
  - 选 seed nodes。
  - PPR 图传播。
  - LLM 过滤冗余/无关记忆。
  - 输出候选上下文给回答模型。

tools / methods:
  - GMM
  - Personalized PageRank
  - entropy-based granularity routing
  - LLM summary / keyword generation
  - LLM filtering

information structure:
  - session memory
  - turn memory
  - summary memory
  - keyword memory
  - association graph
  - seed nodes
  - filtered context

judgment mechanism:
  - 相似度分布和熵只是匹配确定性代理。
  - GMM / PPR 只是召回与扩散机制。
  - LLM 过滤只是上下文准备。
  - 没有任一环节等于 evidence-aware review。

user experience:
  - 更像“想起正确上下文”，不是“记忆越多越好”。

automation boundary:
  - 可自动选择记忆粒度和扩展关联记忆。
  - 不能自动创建 reviewed relation。
  - 不能自动把 recalled memory 作为 action basis。

risk:
  - 错误联想。
  - 摘要/关键词失真。
  - 敏感记忆意外重现。
  - 旧记忆过期或与新记忆冲突。
  - PPR rank / entropy 被误当作信任。

fit for us:
  - 支持 VAKS 的 Activation Tier / Association Neighborhood Activation / Context Pack。

challenge to us:
  - 未来如果做 agent memory，必须把“记忆召回强度”和“证据/行动资格”分得更硬。
```

## 可抽取 Candidate Points

- `multi_granularity_activation_views`：长期记忆应支持多种视图，按 query 选择合适粒度，而不是只检索一个平面 chunk。
- `memory_association_graph_as_activation_not_relation`：记忆关联图可以帮助 recall，但图边不是 reviewed relation。
- `entropy_routing_as_uncertainty_proxy_not_truth`：相似度分布熵可做检索确定性代理，但不能做 truth confidence。
- `gmm_edge_selection_as_recall_filter_not_support`：GMM 选择相关记忆只是边创建/召回过滤，不是 evidence support。
- `ppr_memory_spread_as_context_activation`：PPR 可以让相关记忆扩散召回，但 PPR rank 不是信任分。
- `llm_filter_after_retrieval_not_review`：LLM 过滤冗余上下文是 context preparation，不是 human/evidence-aware review。
- `sensitive_memory_recall_scope_gate`：强长期记忆召回需要隐私、意图确认、scope 限制和 temporal applicability。
- `memgas_rfmem_complementarity`：MemGAS 偏记忆结构组织，RF-Mem 偏在线快慢检索调度，两者互补。
- `memory_view_selection_for_context_pack`：Context Pack 可记录使用了哪些 activation view，但只有 reviewed evidence 能支撑行动。

## 可借鉴

- 把 memory/context activation 拆成多个视图：raw span、turn-level detail、summary、keyword/theme、decision trace、feedback event、review_due item。
- Context pack 可以记录 `activation_view_used` 和 `activation_reason`，但必须标 `activation_is_truth: false`。
- Agent 长期记忆系统需要先选“该看哪类历史”，而不是一律向量 top-k。
- 对长期用户记忆，应增加敏感信息重现保护和 scope gate。
- 与 RF-Mem、CoMe 一起进入 memory retrieval / activation Direction Review。

## 不能直接借鉴

- 不实现完整 GMM/PPR pipeline 作为主架构。
- 不把 memory graph 变成知识图谱 truth layer。
- 不把 summary / keyword memory 当 source evidence。
- 不把 entropy、PPR、recall、NDCG、LLM judge 当 truth confidence。
- 不让 recalled memory 直接进入 action basis。
- 不因为视频讲解清楚就重复 promotion 已有 alpha 结论。

## 风险和不确定

- 本次 ASR 是 `base` quick draft，专有名词噪声明显。
- 视频是论文讲解，不是 primary source；关键数字和表格应回到 arxiv / OpenReview / repo。
- 旧 alpha review 已做过 paper + read-only code review，本视频不新增强证据。
- benchmark 数字、成本、延迟、seed/temp 参数不能只从视频或 ASR 复制。

## VAKS 归位

```text
Capture:
  - URL、BV 号、公开视频元数据、ASR transcript、segments、ledger。

Understand:
  - 本卡摘要、时间轴、反漏提取、candidate points。

Review:
  - 已有 MemGAS alpha review 可作为更强上游材料。
  - 本视频本身不进入 reviewed knowledge。

Connect:
  - 连接到 MemGAS alpha review、RF-Mem 视频/论文、CoMe repo review、HippoRAG / GraphRAG / Association Neighborhood Activation。

Activation / Context Pack:
  - 高相关：用于说明 multi-granularity activation views。
  - Memory graph / PPR / entropy / LLM filtering 都是 context preparation。

Decision / Action:
  - 当前不能作为 action basis。
  - 不触发主架构改动。

Use Ledger / Feedback:
  - 可作为后续 memory retrieval / activation Direction Review 的补充输入。
```

## 处理等级

当前等级：medium。

理由：

- 有完整 ASR、segments、metadata、ledger。
- 主题与 VAKS Activation Tier / Context Pack 高相关。
- 但 paper/code 已有 alpha review；视频只是补充讲解，不需要 heavy。

升级到 heavy 的条件：

- 用户要做 MemGAS / RF-Mem / CoMe 综合 Direction Review。
- 需要把视频中的解释和论文表格、代码路径重新逐项对齐。
- 准备把 multi-granularity activation 写入主线文档时，必须走 evidence-aware review。

## 价值判断

价值：中等到中高，但偏补充，不是新突破。

它值得收，因为它把 MemGAS 的“多粒度记忆 + 关联召回 + 查询时自适应选择”讲得很清楚，并且和 RF-Mem、CoMe 正好形成一个长期记忆检索候选簇。它不值得单独升级，因为项目已经有更强的 MemGAS alpha review，且这条视频没有新增论文/代码证据。

一句话：

```text
收录为 MemGAS 中文解释补充源；
保留 candidate-only；
未来和 RF-Mem / CoMe 一起做 Direction Review；
不改主架构。
```

## 下一步

- 同步 source card 和 retained text artifacts 到正式 Obsidian vault。
- 后续若做 memory retrieval Direction Review，把本卡作为中文讲解源，主证据仍回到论文 / repo / existing alpha review。
