---
type: source
record_kind: source_card
status: source-captured
title: "模块化Obsidian官方网站｜正式上线"
source_id: bilibili-BV1RK556vE3E
source_uri: bilibili:BV1RK556vE3E
source_url: https://www.bilibili.com/video/BV1RK556vE3E/
source_type: video
platform: bilibili
platform_id: BV1RK556vE3E
author: 鱼先生的模块化Obsidian
publisher: 鱼先生的模块化Obsidian
published_at: "2026-05-13 20:30:00 +08:00"
updated_at:
duration: 122s
captured_at: "2026-06-08 16:11:22 +08:00"
captured_by: Codex
raw_location: raw/videos/2026-06-08-bilibili-modular-obsidian-official-site-source.md
processing_tier: medium
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
access_boundary: public
transcript_method: local_asr
transcript_location: raw/videos/2026-06-08-bilibili-modular-obsidian-official-site-source/transcript.txt
segments_location: raw/videos/2026-06-08-bilibili-modular-obsidian-official-site-source/segments.md
transcript_metadata_location: raw/videos/2026-06-08-bilibili-modular-obsidian-official-site-source/transcript-meta.json
ledger_location: raw/videos/2026-06-08-bilibili-modular-obsidian-official-site-source/acquisition-ledger.json
media_retention: deleted
source_status: active
topics:
  - obsidian
  - modular-obsidian
  - onboarding
  - official-site
  - feedback-loop
  - course-entry
  - plugin-ecosystem
projects:
  - verified-action-knowledge-system
source_family: obsidian-productized-onboarding-feedback
upstream_sources: []
verification_status: unverified
candidate_relation_suggestions: []
tags:
  - raw-video
  - bilibili
  - candidate-only
why_saved: see_body_or_legacy_record
---

# 视频资料：模块化 Obsidian 官方网站上线

## 为什么收录

这条视频介绍“模块化 Obsidian”官方网站上线。它强调官网作为生态入口：提供入门视频课程、意见反馈渠道、整体情况介绍，并围绕开箱即用仓库、视频教程、上手任务、专属插件、数据视图、快速检索和反馈跟踪来构建一个更完整的用户支持系统。

对 VAKS 的价值不在知识真伪或 source review，而在产品化外层：如果未来 VAKS 要让普通用户上手，不能只有架构文档，还需要 onboarding 入口、课程、最小任务、反馈入口和可持续维护的生态说明。

## 来源卡

- 平台：Bilibili
- 原始链接：https://www.bilibili.com/video/BV1RK556vE3E/
- 标题：模块化Obsidian官方网站｜正式上线
- UP 主：鱼先生的模块化Obsidian
- 发布时间：2026-05-13 20:30:00 +08:00
- 视频时长：122 秒
- 收录时间：2026-06-08 16:11:22 +08:00
- 访问边界：public metadata and public audio；未使用 cookies、私有收藏、会员内容或云 ASR

## Intake Boundary

```yaml
processing_tier: medium
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
```

Video source records provide provenance, transcript location, and findability.
They do not create reviewed evidence, project borrowing conclusions, or action
basis.

## 获取与转写

```yaml
subtitle_status: public subtitle list empty
transcript_method: local_asr
asr_model: faster-whisper small
asr_device: cuda
asr_compute_type: float16
transcript_quality: medium
media_retention: deleted
scratch_cleanup: audio.m4a, audio.wav, playurl.json deleted after project-visible artifacts were copied
project_visible_artifacts: yes
transcript_location: raw/videos/2026-06-08-bilibili-modular-obsidian-official-site-source/transcript.txt
segments_location: raw/videos/2026-06-08-bilibili-modular-obsidian-official-site-source/segments.md
transcript_metadata_location: raw/videos/2026-06-08-bilibili-modular-obsidian-official-site-source/transcript-meta.json
ledger_location: raw/videos/2026-06-08-bilibili-modular-obsidian-official-site-source/acquisition-ledger.json
```

说明：

```text
字幕 / ASR 是 raw/source text，不是 reviewed evidence。
AI 摘要是 candidate comprehension，不是 truth。
视频无公开字幕；转写使用公开视频音频 + 本地 CUDA ASR。
完整逐字稿、时间轴、ASR metadata 和 acquisition ledger 已复制到 raw/videos/，不依赖 .codex scratch。
```

## 人话摘要

视频讲的是“模块化 Obsidian”官网正式上线。官网不是单纯宣传页，而是生态入口：用户可以了解模块化 Obsidian 的整体情况，看入门视频课程，完成上手任务，反馈意见，并通过统一入口让作者跟踪和采纳反馈。

视频还强调模块化 Obsidian 是一个“开箱即用仓库”，配套视频教程、20+ 专属插件、数据视图、快速检索和可视化管理，目标是降低用户从零搭建 Obsidian 的试错成本。

## 关键实体置信度

```text
confirmed:
  - Bilibili bvid：BV1RK556vE3E。
  - 标题、UP 主、发布时间、时长：来自 Bilibili public view API。
  - 视频描述明确写有“提供入门视频课程｜反馈意见入口”。
  - 无公开字幕：x/player/v2 subtitle list 返回 subtitles: []。
  - 转写使用 faster-whisper small / CUDA / float16；未使用 cookies、私有账号或云 ASR。

likely:
  - ASR 中的 “摩快画OB” 应为“模块化 OB / 模块化 Obsidian”。
  - ASR 中的 “生害” 应为“生态”。
  - ASR 中的 “开箱机用仓库” 应为“开箱即用仓库”。
  - ASR 中的 “卢曼卡天笔记工作流” 应为“卢曼卡片笔记工作流”。
  - ASR 中的 “OBCDN” 应为 Obsidian。

unclear:
  - 官网 URL 需要看评论区蓝链或画面确认，公共 metadata 没有直接给出。
  - “20+ 专属插件”的具体插件列表、授权和可用边界未确认。
  - “数据视图 / 快速检索 / 可视化管理”的具体实现方式未确认。

needs user visual check:
  - 如果要记录官网 URL、课程入口、反馈入口字段或插件列表，需要看视频画面/评论区蓝链。
```

## 时间轴 / 分段

- 00:00-00:12：宣布模块化 Obsidian 官网正式上线，官网提供意见反馈渠道和入门视频课程。
- 00:12-00:27：官网也用于了解模块化 Obsidian 整体情况；模块化 Obsidian 是完整生态的一部分。
- 00:27-00:37：提供视频教程和上手任务，降低从零搭建的试错成本。
- 00:37-00:48：定位为卢曼卡片笔记工作流实践，从闪念笔记到项目笔记，再到永久笔记。
- 00:48-00:57：作者开发了 20+ 专属插件，后续还会继续完善。
- 00:57-01:04：提到数据视图、快速检索、可视化管理，让笔记管理更简单高效。
- 01:04-01:28：官网为新手提供详细入门视频教程，从零到一帮助理解 Obsidian。
- 01:28-01:49：官网也是反馈入口，用于收集、跟踪、回复和采纳用户意见。
- 01:49-02:01：作者强调持续建设模块化 Obsidian 专属知识管理生态。

## 视频里直接说了什么

- 模块化 Obsidian 官网正式上线。
- 官网是生态的一部分，提供入门课程和反馈入口。
- 模块化 Obsidian 是开箱即用仓库，帮助用户省去从零搭建的试错和时间成本。
- 其工作流覆盖闪念笔记、项目笔记、永久笔记。
- 作者开发了 20+ 专属插件，并会持续完善。
- 数据视图、快速检索、可视化管理能让笔记管理更简单高效。
- 统一反馈入口有助于收集、跟踪、回复和采纳用户意见。

## 我的理解 / 推断

这条视频的核心不是某个 Obsidian 技术点，而是“知识系统产品化”：让用户通过官网、课程、任务、反馈、插件和开箱仓库进入一个可持续维护的生态。它提醒 VAKS：如果未来要给人使用，不能只把系统解释成一堆文件、schema 和 review gate，还要给一个能上手、能反馈、能学习、能持续改进的入口。

对 VAKS 的借鉴是 P2：它影响 onboarding、官网、反馈入口和外层产品化，不直接影响 source truth core。

## 反漏提取检查

```text
pain point:
  Obsidian 从零搭建成本高，新手不知道如何上手；用户反馈分散，不利于维护者跟踪和采纳。

workflow:
  用户进入官网 -> 了解整体生态 -> 看入门视频课程 -> 完成上手任务 -> 使用开箱仓库 / 插件 / 数据视图 -> 通过统一入口提交反馈 -> 作者回复、跟踪、采纳。

tools / plugins:
  模块化 Obsidian、Obsidian、专属插件、官网、视频课程、反馈入口、数据视图、快速检索。

information structure:
  官网作为生态首页；课程作为学习路径；反馈入口作为 Use Ledger / Feedback 类入口；插件和仓库作为开箱使用包。

judgment mechanism:
  通过用户反馈持续完善生态；但没有证据审查、truth confidence 或 action readiness 判断。

user experience:
  降低从零搭建门槛；让新手有课程和任务可跟；让反馈有统一入口。

automation boundary:
  视频没有讲自动化，重点是产品入口和维护反馈闭环。

risk:
  官网和课程容易把具体工作流包装成“唯一正确路径”；插件生态也可能让用户误以为装得多就是系统成熟。

fit for us:
  适合借鉴到 VAKS onboarding、使用说明、反馈入口、课程/任务式上手路径和外层 viewer。

challenge to us:
  VAKS 如果只有严格边界和文档，没有低门槛入口，普通用户很难开始。
```

## 可抽取 Candidate Points

- VAKS 未来需要一个 onboarding / 官网入口，而不只是 repo README。
- 新用户学习路径应是课程 + 上手任务，而不是直接读完整架构文档。
- 统一反馈入口可以支持 VAKS 的 Use Ledger / Feedback，而不是散落在聊天里。
- 开箱仓库 / starter vault 可以降低用户从零搭建成本。
- 专属插件 / 数据视图适合作为外层 workbench，不应进入 truth core。

## 可借鉴

- 官网作为 VAKS 入口：整体介绍、课程、反馈、上手任务。
- 任务式 onboarding：从最小闭环开始，逐步进入进阶功能。
- 统一反馈入口：记录需求、问题、采纳状态、后续跟踪。
- 开箱模板 / starter vault：帮助用户先用起来。

## 不能直接借鉴

- 不能把某套 Obsidian 工作流包装成 VAKS 唯一路径。
- 不能用插件数量证明系统成熟。
- 不能让官网 / 课程 / 反馈变成 reviewed knowledge。
- 不能把反馈直接改 truth confidence。

## 风险和不确定

- ASR 中存在明显错字，官网 URL、插件列表和课程结构需要画面确认。
- 视频是发布介绍，不是架构说明。
- 对 VAKS 是产品化 / onboarding 借鉴，不是核心证据边界借鉴。

## VAKS 归位

```text
Capture:
  官网/课程可解释如何开始 capture，但不是 capture engine。

Understand:
  课程帮助用户理解系统，不改变 knowledge_status。

Review:
  不触及 evidence-aware review。

Connect:
  数据视图 / 快速检索是外层 workbench，不是 reviewed relation。

Activation / Context Pack:
  官网和上手任务可作为 activation / onboarding surface。

Decision / Action:
  不支持直接行动。

Use Ledger / Feedback:
  统一反馈入口是最值得借鉴的点。
```

## 处理等级

```text
medium:
  本次采用。保留 transcript / segments / metadata / ledger，并抽取候选点。

heavy:
  暂不采用。除非后续要专门设计 VAKS 官网 / 反馈入口 / onboarding 课程。
```
