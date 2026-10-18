---
type: source
record_kind: video_source_card
status: source-captured
title: "智能分块 + 语义压缩 + Schema 结构化，这才是企业级知识库（2）"
source_id: bilibili-BV1JTGQ6CESE
source_uri: bilibili:BV1JTGQ6CESE
source_url: https://www.bilibili.com/video/BV1JTGQ6CESE/
source_type: video
platform: bilibili
platform_id: BV1JTGQ6CESE
author: "极客少年派"
publisher: "极客少年派"
published_at: "2026-05-28 10:13:26 +08:00"
updated_at:
duration: 840s
captured_at: "2026-06-12 20:34:11 +08:00"
captured_by: Codex
raw_location: raw/videos/2026-06-12-bilibili-bv1jtgq6cese-source.md
processing_mode: explicit_strong_distillation
processing_level: heavy
processing_tier: heavy
knowledge_status: raw
overlay_state: project_sidecar_created
review_pressure: none
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
review_priority: normal
review_owner: Codex
formalization_status: raw-only
access_boundary: public_no_cookies
transcript_method: local_asr
transcript_location: raw/videos/2026-06-12-bilibili-bv1jtgq6cese-source/transcript.txt
segments_location: raw/videos/2026-06-12-bilibili-bv1jtgq6cese-source/segments.md
transcript_metadata_location: raw/videos/2026-06-12-bilibili-bv1jtgq6cese-source/transcript-meta.json
ledger_location: raw/videos/2026-06-12-bilibili-bv1jtgq6cese-source/acquisition-ledger.json
media_retention: deleted
source_status: active
topics:
  - enterprise-knowledge-base
  - apex-knowledge
  - schema-extraction
  - structured-retrieval
  - semantic-compression
  - vector-retrieval
  - document-intake
  - industrial-drawings
  - rag-boundary
projects:
  - verified-action-knowledge-system
source_family:
  - enterprise-knowledge-base-schema-rag-reference
  - video-demo
upstream_sources: []
verification_status: unverified
candidate_relation_suggestions:
  - target: outputs/review/2026-06-12-bilibili-apex-knowledge-schema-rag-candidate-distillation.md
    relation_type: derived_from
    relation_state: candidate
    why_suggested: "The video presents schema-first extraction and object-aware retrieval for vertical enterprise documents, directly relevant to VAKS document intake and retrieval-layer design."
    source_anchor: raw/videos/2026-06-12-bilibili-bv1jtgq6cese-source/segments.md
    evidence_support:
      span_supports_target: transcript_anchor_only
      evidence_role: orientation
      reviewer_note: "ASR transcript and video demo are raw source text, not reviewed evidence."
    suggested_at: 2026-06-12
tags:
  - raw-video
  - bilibili
  - candidate-only
  - strong-distillation
  - schema-extraction
  - structured-retrieval
---

# 视频资料：Apex Knowledge Schema 结构化企业知识库

## 为什么收录

这条视频演示一个企业知识库方案：普通 RAG 分块容易丢掉文档整体语义，尤其处理工业图纸、制度文档、法律卷宗、银行报告这类垂直业务文档时，只靠向量相似度不够。视频主张先按业务定义 Schema，把文档抽成结构化 JSON / 对象，再生成一个短语义 brief 放进向量库，查询时把自然语言问题转成对象查询和语义召回组合。

对 VAKS 来说，它不是“证据治理”来源，而是很强的文档 intake / retrieval-layer 参考：

```text
source document
-> schema extraction
-> structured object
-> semantic brief
-> object-aware query
-> vector/context retrieval as auxiliary
```

这对 VAKS 的“文档先解析、再入库；检索先分桶、再召回；结构化结果不能直接变 truth”非常相关。

## 来源卡

- 平台：Bilibili
- 原始链接：https://www.bilibili.com/video/BV1JTGQ6CESE/
- 标题：智能分块 + 语义压缩 + Schema 结构化，这才是企业级知识库（2）
- 作者 / UP 主：极客少年派
- 发布时间：2026-05-28 10:13:26 +08:00
- 视频时长：840 秒
- 收录时间：2026-06-12 20:34:11 +08:00
- 访问边界：公开视频 metadata / public playurl audio；未使用 cookies、私有收藏、会员内容或云 ASR

## Intake Boundary

```yaml
processing_tier: heavy
knowledge_status: raw
overlay_state: project_sidecar_created
review_pressure: none
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
```

Video source records provide provenance, transcript location, and findability.
They do not create reviewed evidence, project borrowing conclusions, or action
basis.

## 获取与转写

```yaml
subtitle_status: public subtitle list empty
transcript_method: local_asr
asr_engine: faster-whisper
asr_model: small
asr_device: cuda
asr_compute_type: float16
transcript_quality: medium
media_retention: deleted
scratch_cleanup: public audio m4s deleted after transcript artifacts were saved
project_visible_artifacts: yes
transcript_location: raw/videos/2026-06-12-bilibili-bv1jtgq6cese-source/transcript.txt
segments_location: raw/videos/2026-06-12-bilibili-bv1jtgq6cese-source/segments.md
transcript_metadata_location: raw/videos/2026-06-12-bilibili-bv1jtgq6cese-source/transcript-meta.json
ledger_location: raw/videos/2026-06-12-bilibili-bv1jtgq6cese-source/acquisition-ledger.json
```

说明：

```text
字幕 / ASR 是 raw/source text，不是 reviewed evidence。
AI 摘要是 candidate comprehension，不是 truth。
视频无公开字幕；转写使用公开视频音频 + 本地 CUDA ASR。
完整逐字稿、时间轴、ASR metadata 和 acquisition ledger 已复制到 raw/videos/，不依赖 .codex scratch。
```

## 人话摘要

视频在讲企业知识库的第二个关键能力：不要只把文档切块丢进向量库。对很多企业文档来说，真正有价值的信息不是自然段落，而是业务对象和业务字段。

它用工业图纸举例：图纸里面有主视图、俯视图、零件拆解、几何尺寸、螺纹、深度、法兰座、总高度等字段。普通 RAG 很难理解这些字段之间的业务含义；更合理的做法是先为某类文档定义 Schema，把图纸抽成 JSON / 业务对象，再让用户用自然语言查“总高度 2000mm、带某种法兰座的扩散泵基础图纸”。

视频强调，结构化对象不能只是丢进向量库靠语义相似度搜。它需要把用户问题转成能搜索对象的 query。同时，为了让大模型理解这个 JSON 对象，还要生成一个约 100 字左右的 brief，作为语义压缩放进向量库。

视频最后说未来方向包括：动态 Schema 学习、跨 Schema 关联、多模态/图纸格式深度理解。整体思路是把企业文档变成“可检索的业务对象”，再服务 Agent 执行和业务指导。

## 关键实体置信度

```text
confirmed:
  - Bilibili bvid：BV1JTGQ6CESE。
  - 标题、UP 主、发布时间、时长：来自 Bilibili public view API。
  - 视频描述明确称产品 / 系统为 Apex Knowledge。
  - 视频描述明确提到智能文本分块、标题语义切片、上下文语义压缩、向量检索、Schema 结构化解析。
  - 视频无公开字幕：public subtitle APIs 返回空列表。
  - 转写使用 faster-whisper small / CUDA / float16；未使用 cookies、私有账号或云 ASR。

likely:
  - ASR 中的 “Skimmer / 斯里姆尔 / 事故” 多数应为 Schema。
  - ASR 中的 “RG” 应为 RAG。
  - ASR 中的 “大梦形容 / 大蒙显” 应为大模型。
  - ASR 中的 “相量库 / 相当数据库” 应为向量库 / 向量数据库。
  - ASR 中的 “接生结构 / 解诱化数据” 应为 JSON 结构 / JSON 化数据。
  - ASR 中的 “BombTree” 应为 BOM Tree。
  - ASR 中的 “多摩泰” 应为多模态。

unclear:
  - 视频提到动态 Schema 学习时的 “RCI RF” 音频不清，可能是某类反馈 / 强化学习机制，但不能记录为确定术语。
  - 工业图纸字段示例里的具体 UI 文案和模板名需要画面确认。
  - “应用效果非常好 / 查出来一定很准”是视频说法，未独立验证。

needs user visual check:
  - 如果要精确记录 Apex Knowledge UI 里的模板名、字段名、对象查询界面、图纸样例字段，需要看 02:57-04:28、05:30-07:28、12:12-13:04 的画面。
```

## 时间轴 / 分段

- 00:00-01:20：提出问题：普通分片/RAG 不能全局理解文档，容易片面和幻觉；企业垂直文档适合先定义 Schema。
- 01:20-02:54：工业图纸示例：图纸内含主视图、俯视图、零件、尺寸、结构等复杂信息，普通 RAG 难以处理。
- 02:57-04:31：上传图纸，选择工业图纸信息提取模板，系统将图纸要素转成结构化 JSON / 业务字段。
- 04:31-06:25：演示结构化搜索：用户用自然语言描述总高度、法兰座等条件，系统把问题转成对象查询，搜索符合条件的图纸。
- 06:25-07:29：扩展到法律卷宗等领域：不同文档可以转成不同结构化信息，再进行语义识别和结构化搜索。
- 07:29-08:00：视频声称 Schema 智能提取器在落地项目效果好，解决传统 RAG 太复杂、模糊、被动的问题。
- 08:00-09:10：未来方向一：动态 Schema 学习，从文档中自动总结结构化 Schema，减少人工适配。
- 09:10-11:08：未来方向二：跨 Schema 关联，例如图纸、BOM、上下游组件、产品之间的业务语义关联。
- 11:08-12:08：未来方向三：多模态和企业文档格式深度理解，例如 PDF 图纸、DXF 图层和标注信息。
- 12:08-13:05：补充语义 brief：Schema JSON 之外，还要生成短 brief 存入向量库，帮助大模型理解对象语义。
- 13:05-13:54：总结两条技术方向：长文档切片/上下文分段；结构化业务数据的抽取与检索。

## 视频里直接说了什么

- 传统知识库通常只是简单分片，分片后不能全局理解文档整体含义，可能产生片面幻觉。
- 企业业务和文档往往垂直、单一，可以定义固定 Schema 来建立知识库。
- 工业企业有大量图纸，技术人员常要搜索相近图纸、标准件/非标件修改、理解图纸信息。
- 普通 RAG 很难直接理解工业图纸中的主视图、俯视图、零件、尺寸、螺纹、深度等信息。
- 系统可以对图纸做 Schema 提取，转成 JSON 化数据，包括基本信息、几何信息、几何特征等字段。
- 搜索时不能简单把 Schema JSON 丢进向量库靠语义相似度；需要把自然语言问题转成搜索业务对象的 query。
- 类似方法可用于法律卷宗等结构化/半结构化业务文档。
- 未来方向包括动态 Schema 学习、跨 Schema 关联、多模态/格式理解。
- Schema 提取时还要生成一个短 brief，放入向量数据库，帮助大模型理解 JSON 对象的语义。
- 系统当前主要解决两件事：长文档分片与上下文压缩；结构化业务数据抽取与检索。

## 我的理解 / 推断

这条视频最有价值的不是产品演示，而是它把“企业知识库检索”拆成两条路：

```text
长文档语义路：
  chunk / title semantic slicing / context compression / brief / vector retrieval

业务对象路：
  domain schema / field extraction / JSON object / object query / cross-object relation
```

这和 VAKS 的路线很合：我们也不应该让一个向量检索层同时承担“找相关内容、判断真伪、理解结构、支撑行动”四件事。更稳的是先把文档类型、业务对象、字段、来源锚点、候选状态分开，再让检索只做激活和找锚点。

但视频里也有典型企业 demo 风险：它会说“结构化后一定很准”，但没有展示字段抽取的验证集、错误处理、schema 版本、人工复核、源锚点和反例。VAKS 可以借 schema-first 路线，不能借“抽出来就可信”。

## 反漏提取检查

```text
pain point:
  企业文档不是普通网页段落。工业图纸、法律卷宗、制度、银行报告等文档有固定业务结构；普通 chunk/RAG 看不到全局对象和字段关系，检索容易模糊、片面、幻觉。

workflow:
  上传业务文档 -> 选择/定义领域 Schema -> 抽取 JSON 化业务对象 -> 同时生成短 semantic brief -> 对象进入知识库 -> 用户自然语言查询 -> 查询被转成对象搜索 query -> 返回匹配对象和语义描述 -> 后续可给 Agent 或业务流程使用。

tools / plugins:
  Apex Knowledge；Schema 智能提取器；工业图纸信息提取模板；向量数据库；对象查询；语义 brief；未来的动态 Schema 学习、跨 Schema 关联、多模态解析。

information structure:
  一份文档可以形成两个表示：结构化 JSON / 对象表示，以及短 semantic brief。JSON 用于字段/对象查询，brief 用于语义理解和向量检索辅助。

judgment mechanism:
  视频主要依赖领域 Schema 和结构化字段来提高检索准确度。它没有展示 evidence review、字段置信度、source-span support、抽取错误回路或 schema version gate。

user experience:
  用户可以问业务化问题，不必知道字段名或查询语法。系统把问题转换成对象查询，返回相近图纸/文档和描述。

automation boundary:
  自动化覆盖 schema extraction、brief generation、query translation、object retrieval。不能自动完成字段正确性验证、业务行动许可、跨对象关系审查、或 truth/action basis 判定。

risk:
  Schema 抽取错误会比普通摘要错误更隐蔽，因为 JSON 看起来很确定；向量 brief 可能覆盖或歪曲对象细节；动态 Schema 学习可能污染 schema；跨 Schema 关联容易把业务相关性误当证据支持。

fit for us:
  强适配 VAKS document intake、retrieval layer、Evidence Packet prefill、source anchor manifest、context pack assembly。尤其适合把“文档解析结果”和“可行动知识”分开。

challenge to us:
  VAKS 不能只停留在 Markdown 摘要；对高价值企业文档，需要考虑 schema/object extraction 的候选层。但 VAKS 也不能因为结构化就放弃 review gate。
```

## 可抽取 Candidate Points

- `schema-first-document-intake`: 垂直业务文档应先抽成领域 Schema / JSON 对象，再进入候选检索层。
- `dual-representation-retrieval`: 结构化 JSON 负责对象字段检索，semantic brief 负责语义激活和模型理解。
- `query-to-object-query`: 用户自然语言问题需要先转成对象查询，而不是直接向量相似度召回。
- `schema-extraction-is-candidate`: Schema 抽取结果是候选结构化理解，不是 reviewed truth。
- `brief-is-activation-not-evidence`: 100 字 brief 适合激活和召回，不能作为证据支持。
- `cross-schema-relation-needs-review`: BOM/上下游组件/产品关系可用于候选关联，但不能自动创建 reviewed relation。
- `dynamic-schema-learning-risk`: 自动学习 Schema 有价值，但必须版本化、抽样验证、人工确认，避免污染字段体系。
- `business-object-anchor-manifest`: 每个抽取字段最好回连到原始文档区域、页码、图层、OCR/ASR/解析来源。

## 可借鉴

- Schema-first intake：对图纸、制度、合同、卷宗、报告先抽对象。
- JSON object + semantic brief 双表示。
- 自然语言 query -> object query 的检索路径。
- 对垂直文档按企业/部门定制 Schema。
- 把结构化对象与 Agent / 业务流程连接，但必须经过 action gate。
- 未来可以比较动态 Schema 学习、跨 Schema 关联、多模态解析。

## 不能直接借鉴

- 不能把 Schema 抽取结果当 reviewed knowledge。
- 不能让对象字段检索结果直接变 action basis。
- 不能把 brief 当证据支持。
- 不能让动态 Schema 学习直接改主 schema。
- 不能让跨 Schema 关系自动变 reviewed relation。
- 不能把产品 demo 的“很准”当验证结果。
- 不能绕过原文/图纸/页码/字段 source anchors。

## 风险和不确定

- ASR 质量中等，Schema / RAG / JSON / BOM / DXF 等词有多处误识别，已按上下文纠正但需画面核验。
- 视频是产品演示，不是独立 benchmark。
- 没有看到字段级抽取准确率、schema version、错误样本、人工复核流程。
- 视频中“Agent 执行和业务指导”触及行动层，VAKS 不能直接吸收为 action-ready。
- 工业图纸、多模态、DXF 解析需要专门解析器和样本验证，不是 LLM 提示词能单独保证。

## VAKS 归位

```text
Capture:
  强相关。视频提醒我们高价值企业文档不能只收链接/摘要，要保留源文件和解析 artifact。

Understand:
  强相关。Schema extraction / JSON object / brief 都属于 candidate comprehension。

Review:
  视频缺失 review gate。VAKS 必须补字段级 source anchor、抽取置信度、错误样本和人工复核。

Connect:
  中强相关。跨 Schema / BOM / 上下游关系可做 candidate_relation_suggestions。

Activation / Context Pack:
  强相关。brief 和对象查询可帮助 context pack 找到更准的锚点。

Decision / Action:
  高风险。企业流程/Agent 执行必须走 Evidence Sufficiency Gate 和 action-basis envelope。

Use Ledger / Feedback:
  中等相关。用户纠错可反馈 schema 字段、query translation、retrieval usefulness，但不能直接改 truth。
```

## 处理等级

```text
heavy
```

原因：

- 直接影响 VAKS document intake 和 retrieval-layer 设计。
- 涉及结构化抽取、语义压缩、对象查询、Agent/业务流程行动边界。
- 需要单独 candidate distillation 和项目 overlay，但不进入 reviewed knowledge。

## 下一步

- 已写候选蒸馏：`outputs/review/2026-06-12-bilibili-apex-knowledge-schema-rag-candidate-distillation.md`
- 已写 VAKS 项目 overlay：`outputs/review/project_lens_overlays/2026-06-12-apex-knowledge-schema-rag-retrieval-overlay.md`
- 不创建 reviewed claim / pattern / decision。
