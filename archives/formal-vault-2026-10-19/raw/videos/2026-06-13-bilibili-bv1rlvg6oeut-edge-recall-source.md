---
type: source
status: source-captured
title: '收藏≠学会｜把“看过”变成“记住”'
source_id: bilibili-BV1RLVG6oEut
source_uri: bilibili:BV1RLVG6oEut
source_url: https://www.bilibili.com/video/BV1RLVG6oEut/
source_type: video
platform: bilibili
platform_id: BV1RLVG6oEut
author: 鱼先生的模块化Obsidian
publisher: 鱼先生的模块化Obsidian
published_at: '2026-05-30 20:30:00 +0800'
updated_at:
duration: 312s
captured_at: '2026-06-13 19:18:00 +08:00'
captured_by: Codex
raw_location: raw/videos/2026-06-13-bilibili-bv1rlvg6oeut-edge-recall-source.md
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
transcript_location: raw/videos/2026-06-13-bilibili-bv1rlvg6oeut-edge-recall-source/transcript.txt
segments_location: raw/videos/2026-06-13-bilibili-bv1rlvg6oeut-edge-recall-source/segments.md
transcript_metadata_location: raw/videos/2026-06-13-bilibili-bv1rlvg6oeut-edge-recall-source/transcript-meta.json
ledger_location: raw/videos/2026-06-13-bilibili-bv1rlvg6oeut-edge-recall-source/acquisition-ledger.json
media_retention: deleted
source_status: active
topics:
  - video-intake
  - bilibili
  - obsidian-plugin
  - edge-recall
  - active-recall
  - spaced-repetition
  - contextual-review
  - source-anchored-recall
  - no-source-pollution
  - mobile-review
  - review-dashboard
  - vaks-reference
projects:
  - verified-action-knowledge-system
source_family: bilibili-modular-obsidian-edge-recall
upstream_sources: []
verification_status: unverified
candidate_relation_suggestions: []
tags:
  - raw-video
  - bilibili
  - candidate-only
  - edge-recall
  - vaks-distill-candidate
---

# 收藏≠学会｜把“看过”变成“记住”

## 为什么收录

这条视频不是讲资料库怎么抽取知识，而是讲 Obsidian 里的记忆复习插件 Edge Recall：把“收藏/看过”推进到“主动回忆/长期记忆”。它对 VAKS 的价值在于补足人侧的使用闭环：资料被捕获、理解、激活之后，用户是否真的记住、复习、修正和再次激活。

本卡只记录来源和候选理解，不创建 reviewed knowledge。视频中对插件效果、算法和产品对比的说法都需要后续验证。

## 来源卡

- 平台：Bilibili
- 原始链接：https://www.bilibili.com/video/BV1RLVG6oEut/
- 标题：收藏≠学会｜把“看过”变成“记住”
- 作者 / UP 主：鱼先生的模块化Obsidian
- 发布时间：2026-05-30 20:30:00 +0800
- 视频时长：312s
- 访问边界：public, no cookies

## Intake Boundary

```yaml
processing_tier: heavy
knowledge_status: raw
overlay_state: none
review_pressure: review_due
promotion_gate: evidence_aware_review_required
action_basis_allowed: false
truth_mutation_allowed: false
```

## 获取与转写

```yaml
subtitle_status: no_public_subtitle_found
transcript_method: local_asr
asr_engine: openai-whisper
asr_model: small
asr_device: cuda / fp16
transcript_quality: medium
media_retention: deleted
scratch_cleanup: temporary audio deleted after transcript artifacts were saved
project_visible_artifacts: yes
fallback_note: faster-whisper small failed because model fetch hit HuggingFace TLS EOF; cached openai-whisper small.pt was used instead
```

ASR 是 raw/source text，不是 reviewed evidence。专名、UI 文案、插件效果和算法细节不能只靠 ASR 判断。

## 人话摘要

视频的主张很直接：AI 时代越强，越不能把所有理解都外包给 AI；收藏、看过、问过 AI，都不等于学会。作者推出模块化 OB 的专属插件 Edge Recall，想把注意力拉回主动记忆。

插件设计重点是：在原笔记里创建和复习记忆卡，不往原文塞特殊符号；点击状态栏或侧边栏能跳到待复习卡片；卡片可分组；用间隔重复算法选择复习难度；点击色条显示/隐藏答案；所有操作都在原文上下文里完成，支持图片、代码块、表格、callout 等 Obsidian 原生格式；移动端也能创建和复习；还有数据图表展示复习成果。

## 关键实体置信度

```text
confirmed:
  - BVID: BV1RLVG6oEut
  - 标题: 收藏≠学会｜把“看过”变成“记住”
  - 作者 / UP 主: 鱼先生的模块化Obsidian
  - 发布时间: 2026-05-30 20:30:00 +0800
  - 视频描述明确提到: Edge Recall, Anki 复习卡, 模块化 OB 第 22 款专属插件, 不支持单卖
  - 主题: Obsidian 复习卡、主动回忆、间隔重复、原文内复习、移动端复习

likely:
  - ASR 中 "Ubsidian" 是 Obsidian。
  - ASR 中 "Anti-类型" 是 Anki 类型。
  - ASR 中 "幻行" 是空行。
  - ASR 中 "弹桩" 是弹窗。
  - ASR 中 "Karlis" 大概率是 callouts。
  - ASR 中 "AdgerCore" 大概率是 Edge Core 或 Edge Recall 生态里的核心支持。

unclear:
  - Edge Recall 的具体间隔重复算法、数据结构、插件 API、可迁移性。
  - “正式弃用 Spaced Repetition 等复习插件”是作者/产品宣称，未独立验证。
  - 模块化 OB 专属插件市场的安装/授权细节。

needs user visual check:
  - 具体 UI 文案、卡片数据字段、图表维度、移动端界面细节。
```

## 时间轴 / 分段

- 00:00-00:32：AI 时代更要把知识记在脑子里，反对任何问题都问 AI 却不思考不记忆。
- 00:32-00:47：推出模块化 OB 第 22 款专属插件 Edge Recall，把注意力转回大脑记忆过程。
- 00:47-01:25：对比 Anki 类型插件，强调创建卡片更方便，不需要在原文添加问号、冒号等特殊符号，只需问题和答案之间留空行。
- 01:25-01:45：状态栏显示待复习卡片，可快速跳转到原笔记位置，不需要在弹窗中切换。
- 01:45-02:18：也可在左侧工作区面板操作，支持自定义卡组、分组和记忆难度。
- 02:18-02:51：点击色条显示/隐藏答案；所有操作在原笔记位置完成，形成上下文场景式记忆。
- 02:51-03:31：原文内编辑和复习让二次编辑、修正答案、保留 Obsidian 原生格式更容易，支持图片、代码、表格、callout 等格式。
- 03:31-03:50：插件加入模块化 OB 生态，提供数据图表检验复习成果。
- 03:58-04:41：移动端支持创建和复习卡片，适合随时随地记忆复习。
- 04:44-04:58：上架模块化 OB 专属插件市场，可下载安装使用。

## 反漏提取检查

```text
pain point:
  - 收藏、看过、问过 AI 不等于记住；普通复习插件容易污染原文、脱离上下文、移动端体验弱。

workflow:
  - 在原笔记中用空行区分问题/答案 -> 创建复习卡 -> 状态栏/侧栏进入待复习 -> 原文内显示/隐藏答案 -> 选择难度 -> 间隔重复安排下次复习 -> 数据图表反馈成果。

tools / plugins:
  - Edge Recall；模块化 OB 专属插件市场；Obsidian；Anki 类型复习卡概念；Spaced Repetition 被作者作为对比对象。

information structure:
  - 复习卡锚定原笔记位置；支持卡组分组；复习状态在状态栏/侧栏暴露；复习结果进入数据图表。

judgment mechanism:
  - 用户按记忆难度反馈；间隔重复算法安排后续复习；图表展示复习成果。

user experience:
  - 不在弹窗里脱离上下文复习；不往原文写特殊标记；原文可直接编辑、修正、保留格式；移动端可复习。

automation boundary:
  - 自动安排复习节奏可以借鉴；但复习难度和复习次数不能证明知识可靠，也不能改变 VAKS truth confidence。

risk:
  - 插件闭源/专属生态；算法细节未验证；复习数据容易被误读成理解程度或事实可靠性；人类记住错误内容会强化错误。

fit for us:
  - 适合作为 VAKS 的人侧记忆/再激活工作台参考，特别是 source-anchored recall 和 use-ledger feedback。

challenge to us:
  - VAKS 现在有 Activation/Cooling/Feedback，但偏系统上下文激活；缺少“用户把关键知识真正记住”的轻量 UI/workbench。
```

## 可抽取 Candidate Points

- Candidate Point 1: `收藏/看过` 应与 `记住/会用` 分层，资料库不应把 capture 当 learning completion。
- Candidate Point 2: 复习卡应锚定原文位置和上下文，避免把记忆任务从知识语境中剥离。
- Candidate Point 3: 复习卡创建应尽量不污染源笔记内容，特别是不强迫用户写特殊符号。
- Candidate Point 4: 难度反馈和复习记录适合进入 Use Ledger / Feedback，但只能影响 reactivation 和 usefulness，不能影响 truth。
- Candidate Point 5: 移动端微复习是冷却/再激活的自然入口。
- Candidate Point 6: 数据图表可以促进坚持复习，但仪表盘不是知识可靠性证据。

## VAKS 归位

```text
Capture: 视频 source card、转写、元数据、ledger；插件里的复习卡来源于原笔记。
Understand: 把原文中的问答关系转成 recall candidate，但不等于 reviewed claim。
Review: 复习答案内容如果用于行动，仍需 evidence-aware review；记住不等于真。
Connect: recall card 应链接回原笔记锚点和相关上下文。
Activation / Context Pack: 待复习卡是人侧 activation queue；打开卡片时激活原文上下文。
Decision / Action: 不直接支撑行动；只能作为学习/记忆辅助。
Use Ledger / Feedback: 难度、复习结果、错题/忘记可写 use ledger，驱动再激活和 review_due。
Cooling / Reactivation: 间隔重复是人侧 cooling/reactivation 的强参考。
```

## 可借鉴

- `source-anchored-recall-card`: 复习卡锚定原笔记位置，而不是孤立弹窗。
- `no-source-pollution`: 创建复习卡不污染原文，不强迫特殊符号。
- `contextual-active-recall`: 在上下文场景中显示/隐藏答案，增强长期记忆。
- `difficulty-feedback-to-reactivation`: 用户选择难度后调整下一次复习，但不改 truth。
- `mobile-micro-reactivation`: 移动端随时复习，适合 cold/warm material 的再激活。
- `review-dashboard-as-motivation`: 图表用于坚持和自检，不作为证据。

## 不能直接借鉴

- 不能把复习次数、记忆难度、图表成绩当成 truth confidence。
- 不能把记忆插件并入 VAKS 核心 truth/review 层。
- 不能为了复习功能增加普通 capture/query 的负担。
- 不能依赖专属插件生态作为 VAKS 基础能力。

## 下一步

- 已进入合并强蒸馏输出，作为候选设计参考。
- 若后续要正式吸收，应先作为 `contextual-active-recall-workbench` 候选 pattern，而不是修改 schema 或原架构。
