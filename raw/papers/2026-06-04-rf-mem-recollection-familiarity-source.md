---
type: source
status: source-captured
title: "Evoking User Memory: Personalizing LLM via Recollection-Familiarity Adaptive Retrieval"
source_id: 2026-06-04-rf-mem-recollection-familiarity-source
source_uri: https://arxiv.org/abs/2603.09250
source_url: https://arxiv.org/pdf/2603.09250
source_type: paper
author: "Yingyi Zhang; Junyi Li; Wenlin Zhang; Penyue Jia; Xianneng Li; Yichao Wang; Derong Xu; Yi Wen; Huifeng Guo; Yong Liu; Xiangyu Zhao"
publisher: arXiv
published_at: 2026-03-10
updated_at:
captured_at: 2026-06-04
captured_by: Codex
version_or_commit: "arXiv:2603.09250v1; accepted by ICLR 2026"
source_status: preprint
raw_location: raw/papers/2026-06-04-rf-mem-recollection-familiarity-source.md
processing_mode: immediate
processing_level: heavy
review_priority: normal
review_owner: Codex
formalization_status: candidate-generated
topics:
  - rf-mem
  - personalized-llm
  - user-memory
  - memory-retrieval
  - recollection-familiarity
  - activation
  - retrieval-depth-routing
projects:
  - verified-action-knowledge-system
source_family: personalized-memory-retrieval
upstream_sources: []
verification_status: primary-source-captured
candidate_relation_suggestions: []
tags:
  - source
  - paper
  - architecture-reference
  - candidate-only
---

# Evoking User Memory: Personalizing LLM via Recollection-Familiarity Adaptive Retrieval

## 为什么收录

这篇论文提出 RF-Mem，把个性化 LLM 的用户记忆检索做成 Recollection / Familiarity 双路径。它对 VAKS 有候选价值，因为 VAKS 已经有 Activation Tier、Feedback Ledger、MemGAS 候选和 agent memory quarantine 边界；RF-Mem补的是在线检索策略：面对当前问题，是否值得启动更深的回忆。

当前收录是 candidate-only：论文结果可以作为设计压力，不能直接变成本项目检索实现、truth confidence、reviewed relation 或 action basis。

## 来源信息

- 标题：Evoking User Memory: Personalizing LLM via Recollection-Familiarity Adaptive Retrieval
- arXiv：https://arxiv.org/abs/2603.09250
- PDF：https://arxiv.org/pdf/2603.09250
- 提交日期：2026-03-10
- 会议状态：Accepted by ICLR 2026
- 作者：Yingyi Zhang, Junyi Li, Wenlin Zhang, Penyue Jia, Xianneng Li, Yichao Wang, Derong Xu, Yi Wen, Huifeng Guo, Yong Liu, Xiangyu Zhao
- 机构：Dalian University of Technology, City University of Hong Kong, Huawei Technologies Ltd., University of Science and Technology of China

## 人话总览

论文要解决的问题是：个性化 LLM 需要调用用户长期历史、偏好和上下文。把所有历史塞进 prompt 太贵、不可扩展；一次性 dense Top-K 很快，但容易只抓表层相似，遇到模糊、长尾、跨片段证据或个性化推理时召回不足。

RF-Mem 借鉴 Recollection-Familiarity 双加工理论，把 Familiarity 映射成快速、粗略的熟悉识别，把 Recollection 映射成较慢、链式的情境重构。系统先做 probe retrieval，用候选记忆的平均相似度和分布熵估计熟悉度；熟悉就直接 Top-K，不熟或候选分散就进入 Recollection。

Recollection 路径不是让大模型无限思考，而是在 embedding space 里做预算受控的检索扩展：取候选、KMeans 聚类、用 cluster centroid 和 query 做 alpha mix，形成新的 recollect query，多轮扩展证据。beam width、fanout、maximum rounds 控制成本。

## 原文补充点

相对视频和用户提供的 11 点，原论文还补强了几个重要边界：

1. RF-Mem 被作者明确定位为 retrieval component / online retrieval layer。它可以叠加在 MemoryBank 这类 offline index building 方法、HyDE query expansion、Search-o1 iterative retrieval 上，不是替代所有记忆系统。
2. 作者为了公平，将主要基线限制在 retrieval-only 方法上：Zero Memory、Full Context、Dense Retrieval、Recollection-only 和 RF-Mem。这说明它主要证明检索策略，不是证明全系统产品。
3. 论文把 Full Context 的问题写得很硬：32K 还能跑但 token 很高，128K 显著退化，1M 直接 out-of-context。这个支持“全量历史不是长期方案”。
4. Recollection 路径的公式化实现是 retrieve -> cluster -> alpha-mix -> iterate；它的输出仍是候选 memory set，不是证据审查。
5. 理论部分给了复杂度/覆盖 trade-off：Familiarity 是 O(K) 级别的快路径，Recollection 的成本受 B/F/R 控制，并在 BF + RF 远小于 memory size 时低于 full-context。
6. Limitations 里明确承认：当前主要验证 dialogue-style personalized memory；list entropy 只是轻量 uncertainty proxy；相似度和熵不能完全捕捉语义歧义；静态 embedding index 没处理 temporal updates 和 long-term memory conflicts；更强长期记忆唤起需要防止敏感信息意外重现。

## 方法结构

```text
input:
  user query
  indexed user memories

probe:
  one-shot retrieval
  collect top-k probe candidates and scores
  compute mean score
  compute entropy over score distribution

route:
  high mean score or low entropy -> Familiarity
  low mean score or high entropy -> Recollection

Familiarity:
  direct top-K similarity retrieval
  low latency
  suitable when query is clear/familiar

Recollection:
  retrieve top-N candidates
  cluster candidate embeddings with KMeans
  compute cluster centroids
  alpha-mix current query, centroid, and original query
  continue with beam search
  stop when enough unique memories collected or max rounds reached

generation:
  selected memory texts are fed to LLM for personalized answer generation
```

## 实验摘要

论文在三个 benchmark / task family 上评估：

```text
PersonaMem:
  personalized generation accuracy
  memory corpus sizes: 32K, 128K, 1M tokens

PersonaBench:
  personalized memory retrieval
  metrics include Recall@5 / Recall@10

LongMemEval:
  long-memory retrieval
  metrics include Recall@5 / Recall@50
```

代表结果：

```text
PersonaMem 32K:
  RF-Mem overall accuracy: 0.6350
  Full Context: 0.6129
  Dense Retrieval: 0.5908
  Recollection-only: 0.6214
  RF-Mem retrieval time: 5.09ms
  Recollection-only retrieval time: 7.09ms

PersonaMem 128K:
  RF-Mem overall accuracy: 0.5394
  Dense Retrieval: 0.5259
  Recollection-only: 0.5288
  Full Context: 0.3231

PersonaMem 1M:
  RF-Mem overall accuracy: 0.4589
  Dense Retrieval: 0.4518
  Recollection-only: 0.4544
  Full Context: out-of-context
```

解读边界：

```text
这些结果支持 RF-Mem 在论文设置下的 accuracy/latency trade-off。
它不证明 RF-Mem 适用于 VAKS 的所有资料类型。
它不证明相似度/熵能可靠判断用户意图。
它不证明被召回的 memory 可以直接成为 action basis。
```

## 和 MemGAS 的关系

已有 VAKS 候选里，MemGAS 更关注：

```text
memory structure
multi-granularity views
association graph / propagation
which memory shape to search
```

RF-Mem 更关注：

```text
online retrieval strategy
whether this query is familiar
whether to spend more retrieval budget
how to expand evidence in embedding space
```

最小吸收判断：

```text
MemGAS: memory organization / activation structure candidate
RF-Mem: retrieval-depth routing candidate

They are complementary activation-layer ideas.
Neither is a truth layer.
```

## VAKS 候选价值

1. `uncertainty_guided_activation_depth`

候选结论：VAKS 未来可以考虑用轻量 uncertainty signal 决定 activation 深度，而不是所有 query 固定 Top-K 或固定多轮检索。

边界：uncertainty signal 只控制 retrieval budget，不控制 truth confidence。

2. `familiarity_fast_path_for_ordinary_query`

候选结论：普通、明确、已有强匹配的问题走快路径，保持低延迟。

边界：fast path 是 activation convenience，不是“更熟所以更可信”。

3. `recollection_slow_path_for_ambiguous_memory_query`

候选结论：模糊、长尾、多段证据、个性化推理问题可触发慢路径。

边界：slow path 输出仍是 candidate memory/context，需要后续 support / scope / privacy gate。

4. `sensitive_memory_resurfacing_risk`

候选结论：越能唤起长期用户历史，越需要敏感记忆重现保护。

边界：隐私保护、同意、范围限制和 retention policy 是必须前置的过程约束。

5. `feedback_for_retrieval_calibration_not_truth`

候选结论：missed memory、bad recall、over-personalization 可以校准 retrieval routing。

边界：feedback 仍不能直接改变 truth confidence。

## 不能直接吸收

```text
do_not_absorb:
  - 不直接实现 RF-Mem。
  - 不把 list entropy 当作通用用户意图识别器。
  - 不把 embedding 相似度分布当 evidence sufficiency。
  - 不把 benchmark 数字当 VAKS 本地效果证明。
  - 不让长期用户记忆自动进入回答上下文。
  - 不把 personalized memory retrieval 与 reviewed knowledge 合并。
```

## 风险和局限

```text
limitations_from_paper:
  - 当前评估集中在 dialogue-style personalized memory。
  - 未覆盖跨模态历史和跨域记忆。
  - list entropy 是轻量 uncertainty proxy，不能完整捕捉任务难度和用户意图。
  - similarity score + entropy 不能完整捕捉 semantic ambiguity。
  - static embedding index 没建模 temporal updates。
  - 未解决 long-term memory conflicts。
  - 更强长期记忆唤起可能意外重现敏感信息。

vaks_extra_risks:
  - activation depth 可能被误读为 confidence。
  - recalled personal preference may be stale, scoped, or user-revoked。
  - user memory may conflict with reviewed knowledge or action safety.
  - feedback-driven routing can overfit to recent conversation.
```

## VAKS 归位

```text
Capture:
  论文作为 primary paper source record 保存。

Understand:
  本卡提炼属于 candidate comprehension。

Review:
  可进入未来 Direction Review，但当前不写入 SCHEMA / MEMORY_TIER / FEEDBACK。

Connect:
  Activation Tier / MemGAS / Feedback Ledger / Temporal Applicability / Agent memory quarantine。

Activation / Context Pack:
  可作为 retrieval-depth lazy gate 候选。

Decision / Action:
  当前不支持工程实现；需要本地 fixture、隐私 gate、用户同意和安全 review。

Use Ledger / Feedback:
  可把 missed memory / stale memory / sensitive resurfacing 作为 feedback-event 候选。
```

## 建议下一步

```text
保持 candidate-only。
暂不改主架构。
若同类 personalized memory retrieval 资料继续增加，再做 Direction Review：
  - MemGAS: memory structure
  - RF-Mem: online retrieval routing
  - Feedback Ledger: routing calibration
  - Activation Tier: read early, not believe more
  - Sensitive memory gate: privacy/scope safety
```
