---
type: source
status: source-captured
title: '构建化学竞赛知识库'
source_id: bilibili-BV1UJddBGEAf
source_uri: bilibili:BV1UJddBGEAf
source_url: https://www.bilibili.com/video/BV1UJddBGEAf/
source_type: video
platform: bilibili
platform_id: BV1UJddBGEAf
author: '黄山是个老师'
publisher: '黄山是个老师'
published_at: '2026-04-19 14:53:28 +0800'
updated_at:
duration: 139s
captured_at: '2026-06-12 20:42:28 +08:00'
captured_by: Codex
raw_location: raw/videos/2026-06-12-bilibili-bv1ujddbgeaf-chem-olympiad-knowledge-base-source.md
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
transcript_location: raw/videos/2026-06-12-bilibili-bv1ujddbgeaf-chem-olympiad-knowledge-base-source/transcript.txt
segments_location: raw/videos/2026-06-12-bilibili-bv1ujddbgeaf-chem-olympiad-knowledge-base-source/segments.md
transcript_metadata_location: raw/videos/2026-06-12-bilibili-bv1ujddbgeaf-chem-olympiad-knowledge-base-source/transcript-meta.json
ledger_location: raw/videos/2026-06-12-bilibili-bv1ujddbgeaf-chem-olympiad-knowledge-base-source/acquisition-ledger.json
media_retention: deleted
source_status: active
topics:
  - video-intake
  - bilibili
  - ai-knowledge-base
  - education-knowledge-base
  - chemistry-olympiad
  - domain-spine
  - knowledge-digestion
  - graph-association
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

# 构建化学竞赛知识库

## 为什么收录

这是同一作者知识库思路的短展示版，重点在“化学竞赛知识点不是只被存进去，而是被 AI 切割、消化、关联成网络”。它对 VAKS 有价值的地方是验证了一个具体教育领域里的 `领域骨架 -> source digest -> candidate node -> relation activation -> query feedback` 闭环。

收录为 heavy source，是因为它会影响我们对“入库技能 / 资料库技能”的设计判断：入库不能只是 RAG 切块，还要有领域锚点、候选点生成、关联建议和反馈触发。但本卡只保存来源与候选理解，不提升为 reviewed knowledge。

## 来源卡

- 平台：Bilibili
- 原始链接：https://www.bilibili.com/video/BV1UJddBGEAf/
- 标题：构建化学竞赛知识库
- 作者 / UP 主：黄山是个老师
- 发布时间：2026-04-19 14:53:28 +0800
- 视频时长：139s
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
transcript_metadata_location: raw/videos/2026-06-12-bilibili-bv1ujddbgeaf-chem-olympiad-knowledge-base-source/transcript-meta.json
ledger_location: raw/videos/2026-06-12-bilibili-bv1ujddbgeaf-chem-olympiad-knowledge-base-source/acquisition-ledger.json
```

字幕 / ASR 是 raw/source text，不是 reviewed evidence。AI 摘要是 candidate comprehension，不是 truth。

## 人话摘要

作者展示了一个化学竞赛知识库：把教材、考纲里的知识点切成节点，再让 AI 建立知识点之间的逻辑关系。他强调这不是只存资料，而是“消化”：材料进入后变成一个包含大量节点和关系的知识网络。之后提问时，已有节点能回答就直接用；如果遇到没有的点，系统可以检索、形成新节点、再和已有知识体系建立关系，让知识库随着使用变强。

对我们来说，这像一个“教育领域版 VAKS 候选原型”：它强在领域知识结构化、关联增长和提问反馈；弱在把 AI 自动生成的关联说得太像已经可靠，没有清楚区分候选关系、证据支持、 reviewed relation 和 action basis。

## 关键实体置信度

```text
confirmed:
  - BVID: BV1UJddBGEAf
  - 标题: 构建化学竞赛知识库
  - 作者 / UP 主: 黄山是个老师
  - 发布时间: 2026-04-19 14:53:28 +0800
  - 视频主题: 化学竞赛知识库、教材/考纲知识点、AI 构建关系网络
  - 转写方式: public audio -> local faster-whisper small ASR

likely:
  - ASR 中的 "Android Capracy" 大概率指 Karpathy / Andrej Karpathy 相关知识库思路，但未做画面 OCR 或作者原文确认。
  - "印射" 大概率是 "映射"。
  - "随障" 大概率是 "随着"。

unclear:
  - ASR 中 "Survivor, Housecraft, Artkins, and Cladden" 是教材名转写错误的概率很高，不能按这个拼写入库。
  - 知识库具体工具、技术栈、数据结构、节点/关系生成算法未在本视频中清楚交代。

needs user visual check:
  - 视频画面里出现的具体教材名、工具名、界面文案、节点数量与关系数量截图。
```

## 时间轴 / 分段

- 00:00-00:09：未来每个老师可能都需要构建自己的知识库；作者展示化学竞赛知识库。
- 00:09-00:24：每个节点来自化学竞赛知识点，知识点来自教材或考纲，AI 自动构建逻辑关系；作者称为“消化过程”。
- 00:26-00:35：把教材给系统，让它自动切割、消化、产生关联。
- 00:35-00:52：作者称只给了四本经典教材，就形成约 8000 个节点、上万个逻辑关系的知识网络。教材名 ASR 不可靠。
- 00:52-01:08：教师可以结构化保存自己的知识，未来不只是出 PPT 或出题。
- 01:08-01:44：已有映射作为基座；提问时已有节点回答，未知问题触发检索、生成新节点、新关系，知识库随问答变强。
- 01:48-02:15：作者把这个过程类比为人脑在解新问题时长出新认知节点。

## 视频里直接说了什么

- 未来每个老师都可能需要自己的知识库。
- 知识点可以来自教材或考纲，逻辑关系可以由 AI 构建。
- “消化过程”包括切割、理解、产生关联。
- 结构化知识库未来能服务教学相关任务，不只是做 PPT 或出题。
- 使用中的新问题可以推动知识库生成新节点和新关联。

## 我的理解 / 推断

这个短视频最值得吸收的是“入库不是存储，而是消化”。在 VAKS 里，这不能变成自动写 reviewed truth，而应落成：

- raw source：教材、考纲、题库、视频转写。
- candidate comprehension：被抽出来的候选知识点。
- point collision / review_due：新问题暴露缺口或冲突。
- candidate relation suggestion：AI 建议关联，但不等于 reviewed relation。
- activation feedback：使用越多，越知道哪些点常被激活、哪些缺口需要补。

## 反漏提取检查

```text
pain point:
  - 教师知识和学科经验分散在教材、考纲、题库和个人经验里，普通 RAG 很难变成可持续增长的领域脑。

workflow:
  - 教材/考纲输入 -> 切割知识点 -> AI 建立逻辑关系 -> 形成知识网络 -> 提问触发回答或新节点生成。

tools / plugins:
  - 具体工具未确认；只能确认作者展示了某种 AI 知识库/智能体界面。

information structure:
  - 节点: 化学竞赛知识点；上位锚点: 教材/考纲；边: AI 生成的逻辑关系。

judgment mechanism:
  - 作者按“系统能否回答/能否产生新节点”判断知识库变强；缺少证据支持与人工 review 边界。

user experience:
  - 教师提问、知识库回答；未知问题进一步推动知识网络扩展。

automation boundary:
  - 视频倾向自动化生成节点/关系；VAKS 只能把它当候选生成和 review_due 触发。

risk:
  - 自动关联可能制造伪关系；节点数量/关系数量容易被误读成知识可靠性；教材名和工具名 ASR 低置信。

fit for us:
  - 高度贴合 Capture -> Understand -> Connect -> Activation / Feedback，但必须经过 Review 才能进入 reviewed relation 或 action basis。

challenge to us:
  - 我们的入库技能要避免只做摘要；需要显式产出领域锚点、候选点、候选关系、缺口/冲突和后续 review 路由。
```

## 可抽取 Candidate Points

- Candidate Point 1: 教育领域知识库的核心不是资料堆叠，而是把教材/考纲知识点转成可连接的候选节点网络。
- Candidate Point 2: “消化”可定义为切割、抽点、挂靠领域骨架、生成候选关系和记录来源锚点的组合步骤。
- Candidate Point 3: 提问反馈可以暴露 missing point，并生成新候选节点或 review_due，而不应自动提升为 truth。
- Candidate Point 4: 节点数量和关系数量只能说明覆盖/连接规模，不能说明证据充分或关系已 reviewed。

## 可借鉴

- 领域骨架优先：用考纲/任务体系做知识挂靠点，比只按文件夹或来源切块更适合教育类资料库。
- 入库动词从“保存”升级为“消化”：source -> point -> relation suggestion -> activation trace。
- 使用反馈驱动知识库增长：用户问不到、答得不稳、反复追问的地方，应该进入 missing_evidence / synthesis_needed / review_due。

## 不能直接借鉴

- 不能把 AI 自动建立的边当 reviewed relation。
- 不能把“回答看起来不错”当证据支持。
- 不能把知识库随提问长新节点直接接入 reviewed truth。
- 不能用节点/边规模替代来源锚点、证据包和 review。

## 风险和不确定

- 视频为短展示，缺少完整实现细节。
- ASR 对英文名、教材名和工具名不可靠。
- 教材/题库入库涉及版权和使用边界，后续若做教育 demo 需要单独处理。
- 教学场景有误导学生风险，action 输出必须保留 source anchor 和人工复核入口。

## VAKS 归位

```text
Capture: 教材、考纲、题库、视频转写作为 source/provenance。
Understand: 抽取候选知识点，形成 candidate comprehension。
Review: 自动节点/关系只能进入 review_due；重要教学结论需要 Evidence Packet。
Connect: AI 可建议候选关系，但 reviewed relation 需要证据和人工/规则审查。
Activation / Context Pack: 提问时激活相关教材、考纲、候选点、风险和缺口。
Decision / Action: 组卷、讲义、答疑属于 action/workbench，不能直接拿 raw/candidate 当最终依据。
Use Ledger / Feedback: 提问、满意/不满意、缺口、纠错可写 feedback/use ledger，推动再 review。
```

## 处理等级

当前等级：heavy source intake, candidate-only

升级到 heavy 的条件：已满足。同一作者两条视频合并后影响 VAKS 入库技能设计与架构借鉴，需要进入 outputs/review 做候选蒸馏。

## 下一步

- 与 `BV1Rko5BuEFg` 合并蒸馏，抽取“领域骨架 + 消化 + 反馈生长”的 VAKS 候选模式。
- 不写 reviewed claim；如后续要吸收为正式 pattern，需要走 Evidence-Aware Review。
