---
type: source
record_kind: source_card
status: source-captured
title: '我的 Obsidian 首页搭建：5 个模块 + 动态显示'
source_id: bilibili-BV1btEi6vEtz
source_uri: bilibili:BV1btEi6vEtz
source_url: https://www.bilibili.com/video/BV1btEi6vEtz/
source_type: video
platform: bilibili
platform_id: BV1btEi6vEtz
author: jz21a
publisher: jz21a
published_at: '2026-06-11 21:28:05 +0800'
updated_at:
duration: 322s
captured_at: '2026-06-13 19:24:00 +08:00'
captured_by: Codex
raw_location: raw/videos/2026-06-13-bilibili-bv1btei6vetz-obsidian-homepage-source.md
processing_tier: heavy
knowledge_status: raw
overlay_state: none
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
why_saved: capture raw video/transcript provenance for possible VAKS source-intake review; not reviewed knowledge
access_boundary: public
transcript_method: local_asr
transcript_location: raw/videos/2026-06-13-bilibili-bv1btei6vetz-obsidian-homepage-source/transcript.txt
segments_location: raw/videos/2026-06-13-bilibili-bv1btei6vetz-obsidian-homepage-source/segments.md
transcript_metadata_location: raw/videos/2026-06-13-bilibili-bv1btei6vetz-obsidian-homepage-source/transcript-meta.json
ledger_location: raw/videos/2026-06-13-bilibili-bv1btei6vetz-obsidian-homepage-source/acquisition-ledger.json
media_retention: deleted
source_status: active
topics:
  - video-intake
  - bilibili
  - obsidian-homepage
  - plugin-composition
  - workbench-homepage
  - quick-action-capture
  - dynamic-queue-view
  - template-launcher
  - activity-heatmap
  - dashboard-not-truth
  - vaks-reference
projects:
  - verified-action-knowledge-system
source_family: bilibili-obsidian-homepage-plugin-workbench
upstream_sources: []
verification_status: unverified
candidate_relation_suggestions: []
tags:
  - raw-video
  - bilibili
  - candidate-only
  - obsidian-plugin-stack
  - vaks-distill-candidate
---

# 我的 Obsidian 首页搭建：5 个模块 + 动态显示

## 为什么收录

这条视频是 Obsidian 首页/工作台搭建案例，不是知识真实性或资料库核心架构来源。它值得收录，是因为它把一堆分散插件组合成一个“低摩擦入口”：快捷记录、分场景导航、动态任务和笔记、常用模板、输出热力图都放在一页里。

对 VAKS 的价值在 UI/workbench 层：我们也需要一个能把 Capture、Dev Context、Review Queue、Recent Work、Templates、Vault Health 入口聚合起来的首页，但 dashboard 只能是入口和提示，不能成为 reviewed knowledge。

## 来源卡

- 平台：Bilibili
- 原始链接：https://www.bilibili.com/video/BV1btEi6vEtz/
- 标题：我的 Obsidian 首页搭建：5 个模块 + 动态显示
- 作者 / UP 主：jz21a
- 发布时间：2026-06-11 21:28:05 +0800
- 视频时长：322s
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
```

ASR 是 raw/source text，不是 reviewed evidence。插件名以 Bilibili 描述元数据为准，ASR 中的插件名、CSS 名和 UI 文案有误识别。

## 人话摘要

作者的问题很具体：Obsidian 里页面散在各处，虽然文件已经分类，但临时想记录灵感或打开常用页面时，还是要找半天；把所有链接堆成 list 又太长。于是他做了一个 Homepage：首页就是一个普通 Markdown 文件，加几个社区插件和一段 CSS，把常用动作、项目、任务、模板和热力图聚合成一页。

这个方案包含 5 个模块：快捷操作、分场景导航、动态任务和笔记、常用模板、热力图。技术上用 Homepage 自动打开首页，Dataview 生成动态列表，Templater 做一键新建，Contribution Graph 做活跃度热力图，Obsidian Echarts 做字数热力图，MCL Multi Column 这段 CSS 做多栏卡片布局。

## 关键实体置信度

```text
confirmed:
  - BVID: BV1btEi6vEtz
  - 标题: 我的 Obsidian 首页搭建：5 个模块 + 动态显示
  - 作者 / UP 主: jz21a
  - 发布时间: 2026-06-11 21:28:05 +0800
  - 插件/组件: Homepage, Dataview, Templater, Contribution Graph, Obsidian Echarts, MCL Multi Column
  - 5 个模块: 快捷操作、分场景导航、动态任务和笔记、常用模板、热力图
  - 作者说明: Markdown 文件 + 插件 + CSS，不依赖第三方主题私有接口

likely:
  - ASR 中 "手页" 是 首页。
  - ASR 中 "记录模仓" 是 记录摩擦。
  - ASR 中 "dash wheel" 大概率是 Dataview。
  - ASR 中 "自输热力" 是 字数热力图。
  - ASR 中 "MaticConnect" 大概率是 MCL Multi Column。
  - ASR 中 "CPU介绍" 大概率是 私有接口。

unclear:
  - 博客中的具体代码、Dataview 查询、Templater 脚本、CSS 细节未从视频中直接抓取。
  - 首页中各按钮的确切命名和路径结构需要看作者博客或画面。

needs user visual check:
  - 若要复刻 UI，需要检查视频画面或作者博客代码，而不能只靠 ASR。
```

## 时间轴 / 分段

- 00:00-00:41：痛点是 Obsidian 页面分散，快速记录灵感时找文件会打断思路；长 list 也不好用；核心目标是减少记录摩擦。
- 00:41-01:23：首页聚合常用功能，第一部分是快捷操作：今日笔记、本周总结、task、project、导入书籍/电影、快速记录等。
- 01:23-01:36：阅读相关入口，包括书库、影视库、阅读清单、阅读统计等。
- 01:36-01:56：第二个模块展示常用/长期项目，作者提到曾用 Dataview 动态显示但打开慢，改为静态页面。
- 01:56-02:24：包含被遗忘的笔记、todo/临时灵感页面、项目总览、任务总览、最近新建笔记、近期任务。
- 02:24-02:36：常用模板聚合到首页，方便频繁优化模板。
- 02:37-03:14：两张热力图：按每天创建文件数统计活跃度，按每天新增字数统计输出量。
- 03:14-04:00：搭建方式：安装 Homepage、Dataview、Templater、Contribution Graph、Obsidian Echarts。
- 04:00-04:41：下载 MCL Multi Column CSS，启用后实现多栏卡片、圆角、阴影、间距、深浅色主题适配。
- 05:05-05:20：整个 Homepage 是普通 Markdown + 插件 + CSS，不依赖第三方主题私有接口，换主题也不容易坏。

## 反漏提取检查

```text
pain point:
  - 快速记录和打开常用页面时，文件分散造成摩擦；长链接列表不好扫；动态查询太慢会拖累入口。

workflow:
  - 打开 Obsidian -> Homepage 自动打开固定首页 -> 点击快捷按钮新建/打开常用页面 -> 动态区查看任务/最近笔记 -> 模板区进入模板优化 -> 热力图区看输出状态。

tools / plugins:
  - Homepage, Dataview, Templater, Contribution Graph, Obsidian Echarts, MCL Multi Column CSS。

information structure:
  - 首页按动作、场景、任务/笔记、模板、指标分区；普通 Markdown 承载结构，插件负责动态内容和可视化。

judgment mechanism:
  - 作者用“减少记录摩擦”和“打开速度”判断设计是否好；发现 Dataview 动态项目打开慢时改为静态页面。

user experience:
  - 首页像仪表盘，减少翻找；入口固定；多栏卡片便于扫视；深浅主题自动适配。

automation boundary:
  - 插件可以动态列任务、最近笔记和热力图，但这些只是工作台提示，不是 review、truth 或行动依据。

risk:
  - 插件依赖多；Dataview 查询可能变慢；首页可能变成漂亮但维护重的仪表盘；热力图容易被误读为知识质量。

fit for us:
  - 适合 VAKS 的 UI/workbench：把 Capture、Review Queue、Dev Context、Recent Work、Templates、Vault Health 聚合。

challenge to us:
  - VAKS 现在文档边界强，但日常入口可能偏工程/文件化；需要一个不污染 truth core 的工作台入口。
```

## 可抽取 Candidate Points

- Candidate Point 1: VAKS 需要区分“知识架构”和“操作入口”，首页应是 workbench，不是 truth layer。
- Candidate Point 2: 快捷操作能降低 capture 摩擦，尤其是今日记录、项目记录、任务、导入源、快速想法。
- Candidate Point 3: 动态列表适合做 queue/view，但当性能或稳定性差时，应降级为静态入口。
- Candidate Point 4: 常用模板应该可被快速打开和迭代，模板本身是工作流资产。
- Candidate Point 5: 热力图适合显示 capture/output 活跃度，但不能表示知识质量、truth confidence 或 review readiness。

## VAKS 归位

```text
Capture: 快捷入口降低记录摩擦，可对应 source intake / quick note / task / project intake。
Understand: 首页不负责理解，只能入口到候选蒸馏或模板。
Review: 可显示 review queue 和 review_due，但不执行 review。
Connect: 可显示最近关系/项目入口，但不创建 reviewed relations。
Activation / Context Pack: 可作为 Dev Context / active project 的 landing page。
Decision / Action: 可显示待办和行动入口，但 action basis 仍需单独 gate。
Use Ledger / Feedback: 热力图和最近活动可提示使用痕迹，但不是 truth。
UI / Workbench: 这是最匹配层。
```

## 可借鉴

- `workbench-homepage`: 用一个普通 Markdown 首页聚合日常入口。
- `quick-action-capture`: 今日笔记、周总结、任务、项目、导入源、快速想法一键进入。
- `dynamic-queue-view`: Dataview 类动态列表显示最近笔记、任务、项目、review_due。
- `static-fallback-for-speed`: 高频入口如果动态查询慢，就改为静态入口。
- `template-launcher`: 常用模板作为可维护资产暴露出来。
- `activity-heatmap-not-truth`: 文件数/字数/活跃度只作为使用反馈和激励。

## 不能直接借鉴

- 不能把个人 homepage 当 VAKS 架构。
- 不能把热力图当 vault health、知识质量或 review readiness。
- 不能让首页增加普通 capture/query 的负担。
- 不能依赖某一套插件作为 VAKS 主能力；它只能是可替换 UI/workbench。

## 下一步

- 已进入强蒸馏输出作为候选参考。
- 若后续要吸收，建议只做一个 `vaks-workbench-homepage` 候选设计，不改 schema，不写 reviewed pattern。
