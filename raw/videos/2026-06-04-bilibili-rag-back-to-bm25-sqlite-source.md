---
type: source
status: source-captured
title: '为什么最强的RAG开发者都在“倒退”？'
source_id: bilibili-BV1AxzNBJEoQ
source_uri: bilibili:BV1AxzNBJEoQ
source_url: https://www.bilibili.com/video/BV1AxzNBJEoQ/
source_type: video
platform: bilibili
platform_id: BV1AxzNBJEoQ
author: LLM-X-Factors
publisher: LLM-X-Factors
published_at: '2026-01-23 16:30:00 +08:00'
updated_at:
duration: 393s
captured_at: '2026-06-04 19:13:52 +08:00'
captured_by: Codex
raw_location: raw/videos/2026-06-04-bilibili-rag-back-to-bm25-sqlite-source.md
processing_mode: runner
processing_level: medium
review_priority: normal
review_owner: Codex
formalization_status: raw-only
access_boundary: public
transcript_method: local_asr
transcript_location: raw/videos/2026-06-04-bilibili-rag-back-to-bm25-sqlite-source/transcript.txt
segments_location: raw/videos/2026-06-04-bilibili-rag-back-to-bm25-sqlite-source/segments.md
transcript_metadata_location: raw/videos/2026-06-04-bilibili-rag-back-to-bm25-sqlite-source/transcript-meta.json
ledger_location: raw/videos/2026-06-04-bilibili-rag-back-to-bm25-sqlite-source/acquisition-ledger.json
media_retention: deleted
source_status: active
topics:
  - video-intake
  - rag
  - bm25
  - sqlite
  - fts5
  - vector-search
  - hybrid-retrieval
  - code-search
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

# 为什么最强的RAG开发者都在“倒退”？

## 为什么收录

这条视频讨论 RAG / 检索实现选型，核心观点是：很多场景不应该一上来就用向量数据库，BM25、全文检索、SQLite FTS5、trigram、ripgrep 和混合检索可能更合适。

它对 VAKS 的候选价值在 implementation / activation 层，不在 truth 层：它可以提醒未来检索和 context-pack preparation 先用低成本、可解释、可维护的检索方案，再按需要加向量和 rerank。视频里的数字、开发者数量和工具优劣判断尚未独立核验，不能直接作为 reviewed claim。

## 来源卡

- 平台：Bilibili
- 原始链接：https://www.bilibili.com/video/BV1AxzNBJEoQ/
- 标题：为什么最强的RAG开发者都在“倒退”？
- 作者 / UP 主：LLM-X-Factors
- 发布时间：2026-01-23 16:30:00 +08:00
- 视频时长：393 秒
- 收录时间：2026-06-04 19:13:52 +08:00
- 访问边界：public_no_cookies
- 来源限制：公开视频无公开字幕；当前 transcript 来自本地 ASR，不是人工校对稿。

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
segment_count: 217
text_chars: 2446
transcript_quality: medium
media_retention: deleted
scratch_cleanup: downloaded public audio deleted after ASR
project_visible_artifacts: yes
transcript_location: raw/videos/2026-06-04-bilibili-rag-back-to-bm25-sqlite-source/transcript.txt
segments_location: raw/videos/2026-06-04-bilibili-rag-back-to-bm25-sqlite-source/segments.md
transcript_metadata_location: raw/videos/2026-06-04-bilibili-rag-back-to-bm25-sqlite-source/transcript-meta.json
ledger_location: raw/videos/2026-06-04-bilibili-rag-back-to-bm25-sqlite-source/acquisition-ledger.json
```

说明：

```text
公开字幕多路检查为空，所以本次走公开视频音频 + 本地 GPU ASR。
没有使用 cookies，没有使用云 API。
临时音频已删除，只保留 transcript、segments、metadata、ledger。
字幕 / ASR 是 raw/source text，不是 reviewed evidence。
本卡摘要是 candidate comprehension，不是 truth。
```

## 人话摘要

视频的主线是反向提醒：RAG 不等于向量数据库。作者认为很多实战开发者正在回到 BM25、全文检索和 SQLite，不是技术倒退，而是发现简单、可解释、低运维成本的方案在大部分场景已经够用。

视频把向量数据库被高估的原因分成几类：代码搜索需要精确匹配函数名、变量名和路径，embedding 的语义模糊反而可能不合适；有些业务数据本来有结构化字段，先做字段匹配就能解决大部分查询；向量方案有隐藏成本，包括重新跑 embedding、GPU/CPU 消耗、黑盒调试和基础设施复杂度。

作者给的候选路径是：个人或小规模文档先从 SQLite FTS5 开始；确认需要语义搜索后再加 sqlite-vec 或嵌入式向量方案；团队已有 Postgres 时可以考虑 pgvector；自然语言文档可以做 BM25 + 向量 + rerank 的混合检索；代码搜索优先 BM25 / trigram / ripgrep，不要把整个代码库直接 embedding。

对 VAKS 来说，这条视频的价值是提醒未来 query / context pack / source activation 不要过早工程化。检索层应该先能回源、能解释、能低成本维护；向量、rerank、GraphRAG 都只是 activation / context preparation 的工具，不能变成 trust、evidence support 或 truth confidence。

## 关键实体置信度

```text
confirmed:
  - Bilibili video BV1AxzNBJEoQ
  - title: 为什么最强的RAG开发者都在“倒退”？
  - UP 主: LLM-X-Factors
  - published_at: 2026-01-23 16:30:00 +08:00
  - duration: 393s
  - 视频简介列出的工具链接：
    - SQLite FTS5: https://www.sqlite.org/fts5.html
    - sqlite-vec: https://github.com/asg017/sqlite-vec
    - pgvector: https://github.com/pgvector/pgvector
    - plpgsql_bm25: https://github.com/jankovicsandras/plpgsql_bm25
    - LanceDB: https://lancedb.com/
    - Meilisearch: https://www.meilisearch.com/
    - mdbr-leaf-ir: https://huggingface.co/MongoDB/mdbr-leaf-ir

likely:
  - BM25 / TF-IDF / n-gram / trigram
  - SQLite FTS5
  - sqlite-vec
  - pgvector
  - LanceDB
  - Meilisearch
  - reranking
  - ONNX Runtime
  - ripgrep
  - FAISS CPU
  - IVF / HNSW

unclear:
  - ASR 把 RAG 多次识别成 "RA计" 或 "RA级"。
  - ASR 把向量数据库识别成 "销量数据库 / 相量数据库 / 香料数据库"。
  - ASR 把 embedding 识别成 "embatings / Ambedding"。
  - ASR 把 trigram、pgvector、LanceDB、ripgrep、Claude Code、Tree-sitter 等术语识别不稳定。

needs independent verification:
  - "126 位开发者" 的样本来源。
  - "85% 的情况下不需要向量搜索"。
  - "BM25 / 全文检索被提及 42 次、混合检索 31 次、纯向量数据库 28 次、SQLite 23 次"。
  - Google 从 BM25 换到 BERT embedding 后用户体验变差的说法。
```

## 时间轴 / 分段

- 00:00-00:52：提出核心观点：RAG 不等于向量数据库，经验越丰富越倾向简单方案。
- 00:52-01:16：向量数据库被高估的原因：代码搜索要精确匹配，embedding 对代码正文不一定合适。
- 01:16-01:40：有结构化字段时，先匹配字段；很多场景不需要语义搜索。
- 01:40-01:56：向量方案的隐藏成本：重新 embedding、算力、黑盒调试、基础设施复杂度。
- 01:56-02:33：推荐 SQLite FTS5 + sqlite-vec + 本地 LLM / rerank 作为轻量方案。
- 02:33-02:53：Postgres + pgvector 适合已有 Postgres 团队。
- 02:53-03:20：混合检索：BM25 做关键词、向量做语义、rerank 重排。
- 03:20-04:00：按数据量、场景、GPU 条件给出决策树。
- 04:00-04:43：几个案例：个人 RAG、企业知识库、Markdown 文档。
- 04:43-05:20：代码 RAG 建议：ripgrep、Tree-sitter / 静态分析、LSP、文件路径和函数签名 embedding，代码内容 BM25 + trigram。
- 05:20-06:13：给个人开发者和技术决策者的路线建议。
- 05:13-05:53：更深层判断：信息检索和大语言模型不是同一个问题，不要混为一谈。
- 05:53-06:28：总结三句话：代码搜索用 BM25，不要默认 embedding；很多场景 SQLite 够用；混合检索有效但要先验证需要。

## 视频里直接说了什么

- 很多 RAG 场景不该默认从向量数据库开始。
- 代码搜索需要精确匹配函数名、变量名和路径，BM25 + trigram 往往更合适。
- 结构化字段能解决的问题，不必先上语义搜索。
- 向量数据库有隐藏成本：embedding 更新、算力、黑盒调试、基础设施复杂度。
- 小规模或个人开发可以先用 SQLite FTS5。
- 有语义搜索需要时，再加 sqlite-vec、LanceDB、pgvector 或混合检索。
- 混合检索常见结构是 BM25 / 全文检索 + 向量相似度 + rerank。
- 团队已有 Postgres 时，pgvector 可能比引入新系统更合适。
- 代码 RAG 不建议对整个代码库做 embedding；可以考虑文件路径和函数签名 embedding，代码正文仍用 BM25 + trigram。
- 信息检索和大语言模型是不同问题，不要把 LLM 热潮自动投射到检索选型。

## 我的理解 / 推断

这条视频对 VAKS 的意义很明确：它支持 "retrieval-first, not vector-first" 的工程策略，但不改变 VAKS 的知识分层。

可吸收的是实现优先级：

```text
small/local vault:
  Markdown source + SQLite FTS5 / BM25-like search first.

source activation:
  exact path/title/entity/source_id matching before semantic expansion.

code/source review:
  ripgrep / BM25 / trigram / AST-ish anchors before whole-repo embedding.

semantic recall:
  only after exact/full-text retrieval misses important cases.

hybrid retrieval:
  useful for context-pack preparation, but output仍是候选召回。
```

不能吸收成 truth 的是：

```text
BM25 ranking != trust
SQLite result != evidence support
vector score != truth confidence
rerank score != reviewed relation
retrieval hit != action basis
```

## 反漏提取检查

```text
pain point:
  - 很多 RAG 项目把向量数据库当前置默认，结果引入复杂基础设施和调试成本，却没有先验证是否真的需要语义搜索。

workflow:
  - 先做 exact / metadata / full-text / BM25 检索。
  - 判断是否有语义召回缺口。
  - 小规模用 SQLite FTS5。
  - 需要语义时加 sqlite-vec / LanceDB / pgvector。
  - 需要生产级召回质量时做混合检索和 rerank。

tools / plugins:
  - SQLite FTS5
  - sqlite-vec
  - pgvector
  - plpgsql_bm25
  - LanceDB
  - Meilisearch
  - mdbr-leaf-ir
  - BM25 / TF-IDF / trigram / n-gram
  - ripgrep
  - LSP
  - FAISS CPU
  - ONNX Runtime

information structure:
  - 小规模 Markdown 文档。
  - 结构化字段。
  - 代码路径、函数签名、变量名。
  - chunks / embeddings / rerank results。

judgment mechanism:
  - 视频使用开发者讨论频次和案例经验作为判断来源。
  - 当前没有把原始讨论样本、统计口径或 benchmark 作为可核验 evidence packet。

user experience:
  - 简单方案更快落地、依赖少、可调试。
  - 重型向量栈可能把开发时间从业务逻辑转移到基础设施维护。

automation boundary:
  - 检索系统可以推荐候选资料。
  - 检索系统不能决定资料可信、关系成立或 action ready。

risk:
  - 视频标题和数字偏营销化。
  - ASR 对工具名和技术术语误识别较多。
  - "85%" 和 "126 位开发者" 缺少本卡可见原始样本。
  - 传统检索和向量检索的选择高度依赖语料、语言、查询类型和评估集。

fit for us:
  - 支持 VAKS 当前不急着上重型 RAG / vector / GraphRAG。
  - 支持先做 Markdown source + full-text / BM25 / path-aware retrieval。
  - 支持把 retrieval 归入 activation / context-pack preparation，而不是 truth layer。

challenge to us:
  - 如果未来 VAKS search 一开始就上复杂向量栈，可能违背 light capture / lazy gate 原则。
  - VAKS 应该为 code/source review 保留 exact anchor / path / source_id 检索，不要只靠 semantic similarity。
```

## 可抽取 Candidate Points

1. `retrieval_first_not_vector_first`

候选结论：VAKS 的早期检索实现应先支持 exact / metadata / full-text / BM25-like retrieval，再按缺口加入向量、hybrid 和 rerank。

VAKS 边界：这是 implementation candidate，不是 reviewed architecture change。

2. `code_search_exact_before_embedding`

候选结论：代码和 source-review 场景优先路径、符号、函数名、变量名、BM25 / trigram / ripgrep 等精确检索；whole-repo embedding 不应作为默认入口。

VAKS 边界：适合作为 future code/source review retrieval design pressure。

3. `sqlite_fts5_as_local_first_search_candidate`

候选结论：小规模 Markdown vault / local-first source activation 可以优先评估 SQLite FTS5，而不是直接引入向量数据库。

VAKS 边界：需结合项目实际数据量和中文分词支持再 review。

4. `hybrid_retrieval_is_candidate_preparation`

候选结论：BM25 + vector + rerank 是 context-pack preparation 候选方案，但输出仍是候选召回，不是 evidence support。

VAKS 边界：直接强化现有 "retrieval is not truth" 边界。

## 可借鉴

- 先做简单、可解释、低依赖的检索入口。
- 把 source_id、path、title、entity、frontmatter 字段检索放在语义召回之前。
- 代码/仓库材料优先 `rg` / exact anchor / function signature / path-aware search。
- 向量、sqlite-vec、pgvector、LanceDB、rerank 作为后续可插拔层，而不是 MVP 默认。

## 不能直接借鉴

- 不把 "85% 场景 SQLite 够用" 当作 VAKS 当前事实。
- 不把开发者讨论频次当作 benchmark 或 source independence。
- 不把视频列出的工具直接写成推荐安装清单。
- 不把 BM25 / SQLite 检索结果当作 truth confidence、reviewed relation 或 action basis。

## 风险和不确定

- 无公开字幕，当前文本来自 ASR，技术名词有明显误识别。
- 视频没有给出完整原始样本和评估方法。
- 中文 Markdown vault 的 FTS5 效果取决于分词 / tokenizer / 字段设计。
- VAKS 未来是否需要向量层，要看实际 query-run 和 missed-feedback，而不是按视频结论直接决定。

## VAKS 归位

```text
Capture:
  作为 raw video source card 保存 provenance、ASR、segments、ledger。

Understand:
  本卡摘要和 candidate points 属于 candidate comprehension。

Review:
  当前不进入 reviewed knowledge。若未来做 retrieval implementation review，可和 SQLite FTS5 / qmd / BM25 / vector / GraphRAG 材料一起审。

Connect:
  连接到 VAKS 已有边界：BM25、vector、GraphRAG、rerank 都只是 candidate retrieval / activation / context-pack preparation。

Activation / Context Pack:
  可作为 future local search MVP 的候选压力：先 full-text / exact / source_id，再 semantic / hybrid。

Decision / Action:
  当前不支持直接选型或安装工具；需要独立 benchmark / fixture / query-run。

Use Ledger / Feedback:
  后续如果真实 query misses 说明 full-text 不够，再用 feedback 推动向量或 hybrid review。
```

## 处理等级

当前等级：`medium`

理由：

```text
已保留完整转写、时间轴、关键实体置信度、candidate points、可借鉴 / 不可借鉴和 VAKS fit。
它对 implementation priority 有候选价值，但证据链不足以进入正式决策。
```

升级到 `heavy` 的条件：

- 用户要求进入 VAKS 检索实现选型 review。
- 找到视频所称开发者调研的原始样本、统计方法或 benchmark。
- 用本项目实际 vault query-run 对 SQLite FTS5 / BM25 / vector / hybrid 做本地对比。

## 下一步

```text
建议保留为 raw-only / candidate-only source card。
暂不改主架构。
可在未来 Direction Review / retrieval implementation review 中作为 "start simple before vector" 的候选压力。
```
