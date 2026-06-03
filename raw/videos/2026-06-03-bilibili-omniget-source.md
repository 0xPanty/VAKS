---
type: source
status: source-captured
title: "夯到爆！！Github 又出狠活神器！斩获 3.9K Stars，一款开源免费的全能下载软件，完全属于碾压同级别的存在！！"
source_id: bilibili-BV1LY5J6pEZD
source_uri: bilibili:BV1LY5J6pEZD
source_url: https://www.bilibili.com/video/BV1LY5J6pEZD/
source_type: video
platform: bilibili
platform_id: BV1LY5J6pEZD
author: 宝藏研究社
publisher: 宝藏研究社
published_at: "2026-05-10 23:56:44 +08:00"
updated_at:
duration: 102s
captured_at: "2026-06-03 19:53:10 +08:00"
captured_by: Codex
raw_location: raw/videos/2026-06-03-bilibili-omniget-source.md
processing_mode: immediate
processing_level: medium
review_priority: normal
review_owner: Codex
formalization_status: raw-only
access_boundary: public
transcript_method: local_asr
transcript_location: raw/videos/2026-06-03-bilibili-omniget-source/transcript.txt
segments_location: raw/videos/2026-06-03-bilibili-omniget-source/segments.md
asr_metadata_location: raw/videos/2026-06-03-bilibili-omniget-source/asr-meta.json
ledger_location: raw/videos/2026-06-03-bilibili-omniget-source/acquisition-ledger.json
media_retention: deleted
source_status: active
topics:
  - video-intake
  - download-tool
  - local-first
  - learning-workbench
projects:
  - verified-action-knowledge-system
source_family: omniget-video-intake-reference
upstream_sources: []
verification_status: unverified
candidate_relation_suggestions: []
tags:
  - raw-video
  - bilibili
  - candidate-only
---

# 视频资料：OmniGet 下载与本地学习工具介绍

## 为什么收录

这条视频是视频资料入口的首个 Obsidian 入库测试样例。它本身介绍 OmniGet，但对本项目更有价值的是它展示了一类“资源下载 + 本地整理 + 学习辅助”的工作流，可作为视频资料入口、批量链接、平台归档、本地优先和转写后资料卡生成的候选参考。

## 来源卡

- 平台：Bilibili
- 原始链接：https://www.bilibili.com/video/BV1LY5J6pEZD/
- 标题：夯到爆！！Github 又出狠活神器！斩获 3.9K Stars，一款开源免费的全能下载软件，完全属于碾压同级别的存在！！
- 作者 / UP 主：宝藏研究社
- 发布时间：2026-05-10 23:56:44 +08:00
- 视频时长：102 秒
- 收录时间：2026-06-03 19:53:10 +08:00
- 访问边界：public

## 获取与转写

```yaml
subtitle_status: public subtitle list empty
transcript_method: local_asr
asr_model: whisper small
asr_device: cuda
transcript_quality: medium
media_retention: deleted
scratch_cleanup: audio.m4s and audio.wav deleted after ASR
project_visible_artifacts: yes
transcript_location: raw/videos/2026-06-03-bilibili-omniget-source/transcript.txt
segments_location: raw/videos/2026-06-03-bilibili-omniget-source/segments.md
asr_metadata_location: raw/videos/2026-06-03-bilibili-omniget-source/asr-meta.json
ledger_location: raw/videos/2026-06-03-bilibili-omniget-source/acquisition-ledger.json
```

说明：

```text
字幕 / ASR 是 raw/source text，不是 reviewed evidence。
AI 摘要是 candidate comprehension，不是 truth。
本条视频无公开字幕；转写使用公开视频音频 + 本地 GPU ASR。
完整逐字稿、时间轴、ASR metadata 和 acquisition ledger 已复制到 `raw/videos/2026-06-03-bilibili-omniget-source/`，不依赖 `.codex` scratch。
```

## 人话摘要

视频介绍的是 OmniGet，一个开源桌面工具。口播把它包装成“全能下载神器”，核心逻辑是：用户在网上看到视频、课程、文档、图片、音频等资料后，常常下载到本地却缺少整理和学习工具；OmniGet 试图把“下载资源”和“本地学习辅助”放在一个软件里。

视频强调的功能包括：复制链接识别并下载、依赖 yt-dlp / FFmpeg、插件市场、下载路径和视频质量设置、按平台整理文件夹、字幕下载、部分课程平台支持、番茄钟、专注计时器、记忆闪卡、本地保存资料和笔记。

## 关键实体置信度

```text
confirmed:
  - OmniGet：通过视频封面 / 公开项目页面核对，ASR 初始误听为 Armigate。
  - Bilibili bvid：BV1LY5J6pEZD。
  - 视频无公开字幕：metadata / player subtitle endpoint 均为空。

likely:
  - DLP 指 yt-dlp。
  - FFM Pack 指 FFmpeg。
  - "中端" 是 ASR 把 "终端" 听错。
  - "文件家" 是 ASR 把 "文件夹" 听错。
  - "电子输" 是 ASR 把 "电子书" 听错。

unclear:
  - 课程平台能力是否稳定、是否需要登录或代理，视频口播不能证明。
  - "支持上千网站"、"3.9K stars" 等数字需要以项目仓库当前状态为准。

needs user visual check:
  - 如果要精确记录软件安装步骤，需要看 00:33-00:54 的画面或官方文档。
```

## 时间轴 / 分段

- 00:00-00:09：介绍 OmniGet，称其为开源全能下载工具，GitHub 约 3.9K stars。
- 00:09-00:17：提出痛点：优质视频、课程、文档下载后堆在硬盘，缺少管理和学习工具。
- 00:17-00:33：核心功能分为网络资源下载和本地学习辅助；复制链接即可识别下载视频、音频、图片等。
- 00:33-00:54：初次使用需要安装 yt-dlp / FFmpeg 一类依赖；自动安装失败时可能要手动通过终端安装。
- 00:54-01:07：主界面支持粘贴链接或搜索；插件市场可安装 / 卸载插件；设置可调主题、下载路径、视频质量。
- 01:07-01:20：支持按平台整理文件夹、字幕下载；部分课程平台需要代理和登录。
- 01:20-01:37：集成番茄钟、专注定时器、记忆闪卡；视频强调本地保存、无广告、适合大量课程和电子书用户。

## 视频里直接说了什么

- OmniGet 是一款电脑端开源下载工具。
- 它面向视频、课程、文档、音频、图片等资料下载和本地整理。
- 它把下载能力和本地学习辅助放在一起。
- 初次使用需要安装类似 yt-dlp 和 FFmpeg 的依赖。
- 它有插件市场、下载路径设置、视频质量设置、按平台整理、字幕下载等功能。
- 它有番茄钟、专注定时器和记忆闪卡。
- 视频声称它占用小、流畅、无弹窗广告、资料和笔记保存在本地。

## 我的理解 / 推断

OmniGet 更像“资源获取层 + 本地学习 workbench”，不是 verified knowledge system。它可以启发本项目的视频入口和批量处理体验，但不能替代 VAKS 的 candidate point、review、evidence boundary 和 action basis。

## 反漏提取检查

```text
pain point:
  用户在网上看到大量视频、课程、文档、音频、图片等资料后，下载和整理都很分散，后续学习也缺少统一入口。

workflow:
  复制链接 -> OmniGet 识别来源 -> 安装 / 调用 yt-dlp 与 FFmpeg 类依赖 -> 选择质量和路径 -> 下载资源 -> 按平台整理 -> 在本地播放器 / 阅读器 / 学习组件中使用。

tools / plugins:
  OmniGet、yt-dlp、FFmpeg、插件市场、字幕下载、课程平台入口、番茄钟、专注定时器、记忆闪卡。

information structure:
  视频强调按平台生成独立文件夹，并把下载资料和笔记保存在本地；没有展示 reviewed knowledge、candidate point 或证据审查结构。

judgment mechanism:
  视频没有明确判断资料可信度的方法，主要按“能下载 / 能整理 / 能学习”判断工具价值。

user experience:
  优点是复制链接即可下载、按平台归档、本地保存、学习组件集中；缺点是依赖安装可能失败，课程平台可能需要代理和登录。

automation boundary:
  链接识别、下载、归档、字幕下载偏自动；依赖安装、课程登录、代理配置、资料是否值得相信仍需人工判断。

risk:
  容易把“能下载很多资料”变成囤积资料；课程平台下载涉及授权和平台规则；ASR/口播宣传不能证明工具能力真实稳定。

fit for us:
  可借鉴批量链接、平台归档、本地优先、转写后资料卡、插件候选工作台；不需要把资料库做成下载器。

challenge to us:
  它提醒我们 UI / 队列 / 插件复用可能比自研框架更重要；如果我们的入口太重，用户会更倾向这种简单工具。
```

## 可抽取 Candidate Points

- 视频资料入口应该支持批量链接，而不是每条视频都手工单独处理。
- 视频来源卡应该记录平台身份、字幕 / ASR 方法、时间轴、转写质量和关键实体置信度。
- 视频临时下载只应服务于转写；成功后默认删除音视频 scratch。
- 视频里的产品介绍应先作为 candidate comprehension，不直接成为 reviewed claim。
- 工具名、仓库名、URL、命令、版本号和 star 数需要二次核验或用户看画面确认。

## 可借鉴

- 批量链接队列。
- 按平台自动归档。
- 本地优先，不把资料默认送云端。
- 下载 / 字幕 / 转写 / 资料卡形成一个入口闭环。
- 对学习资料增加轻量辅助信息，而不是只保存原链接。

## 不能直接借鉴

- 不把资料库做成下载器产品。
- 不默认处理私有收藏、会员视频、登录课程或 cookie 路径。
- 不把视频 UP 主的宣传语当事实。
- 不让 ASR、字幕、star 数、下载能力声称直接变成 reviewed knowledge。

## 风险和不确定

- ASR 对英文工具名、命令、项目名容易误听。
- 视频可能带有宣传和夸张表达。
- 课程平台下载能力可能涉及授权、登录、代理、平台规则和版权边界。
- GitHub star 数和支持平台会随时间变化。

## VAKS 归位

```text
Capture:
  视频链接、metadata、ASR 转写、时间轴分段进入 raw/videos。

Understand:
  人话摘要、关键实体置信度、可借鉴 / 不可借鉴。

Review:
  只有当某个视频观点要影响架构、决策或 action basis 时，才进入 REVIEW_QUEUE。

Connect:
  可连接到 source intake、batch queue、local-first、video research workflow。

Activation / Context Pack:
  可作为以后设计视频入口或批量资料处理时的参考材料。

Decision / Action:
  本条视频本身不产生采用决策。

Use Ledger / Feedback:
  本次用作 video-source 模板的首个实际测试样例。
```

## 处理等级

```text
light:
  只保存来源卡、一句话摘要、为什么收录。

medium:
  加完整转写、时间轴、关键实体置信度、candidate points、可借鉴 / 不可借鉴。

heavy:
  只有当视频里的想法会影响架构、决策、行动或 strong relation 时，才进入 REVIEW_QUEUE / outputs/review。
```

当前等级：medium

升级到 heavy 的条件：

- 准备把“批量视频导入队列”做成正式实现规则。
- 准备把“视频资料入口”写成正式 design pattern / decision。
- 准备用 OmniGet 或类似工具作为实现依赖或产品参考。

## 下一步

这条视频目前只作为视频入口测试样例和候选参考。下一步如果要采用其中具体设计，应核对 OmniGet 官方文档 / GitHub 仓库 / 当前版本，再写 REVIEW_QUEUE 项。
