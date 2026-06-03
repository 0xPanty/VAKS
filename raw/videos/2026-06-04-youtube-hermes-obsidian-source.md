---
type: source
status: source-captured
title: "Hermes Obsidian Is Absolutely Wilde(FREE!) 🤯"
source_id: youtube-mjju1qYAV2w
source_uri: youtube:mjju1qYAV2w
source_url: https://www.youtube.com/watch?v=mjju1qYAV2w
source_type: video
platform: youtube
platform_id: mjju1qYAV2w
author: Julian Goldie Agency
publisher: Julian Goldie Agency
published_at: "2026-06-02 01:09:19 -07:00"
updated_at:
duration: 483s
captured_at: "2026-06-04 01:54:41 +08:00"
captured_by: Codex
raw_location: raw/videos/2026-06-04-youtube-hermes-obsidian-source.md
processing_mode: immediate
processing_level: medium
review_priority: normal
review_owner: Codex
formalization_status: raw-only
access_boundary: public
transcript_method: public_subtitle
transcript_location: raw/videos/2026-06-04-youtube-hermes-obsidian-source/transcript.txt
segments_location: raw/videos/2026-06-04-youtube-hermes-obsidian-source/segments.md
transcript_metadata_location: raw/videos/2026-06-04-youtube-hermes-obsidian-source/transcript-meta.json
ledger_location: raw/videos/2026-06-04-youtube-hermes-obsidian-source/acquisition-ledger.json
media_retention: not_downloaded
source_status: active
topics:
  - video-intake
  - obsidian
  - agent-memory
  - dev-context
  - content-workflow
  - hermes
projects:
  - verified-action-knowledge-system
source_family: hermes-obsidian-youtube-agent-memory-reference
upstream_sources: []
verification_status: unverified
candidate_relation_suggestions: []
tags:
  - raw-video
  - youtube
  - candidate-only
---

# 视频资料：Hermes + Obsidian 作为 AI 业务记忆工作流

## 为什么收录

这条视频不是 verified knowledge 资料，也不是 Hermes 或 Obsidian 的官方技术文档。它是一个面向内容/社群业务的公开视频示范，展示了一种很主流、低门槛的做法：把 Obsidian 当作 AI 代理的共享业务记忆，让 Hermes、Claude 等工具在执行内容任务前读取相同的项目上下文。

对 VAKS 有价值的不是它的营销判断，而是它暴露了一类真实用户需求：普通用户希望 AI 不要每次从零开始，希望有一个简单的“项目脑 / master context / vault primer”让代理快速进入任务状态。它可以用来校准我们的 Dev Context、Activation、Context Pack 和 Agent Access 边界。

## 来源卡

- 平台：YouTube
- 原始链接：https://www.youtube.com/watch?v=mjju1qYAV2w
- 标题：Hermes Obsidian Is Absolutely Wilde(FREE!) 🤯
- 作者 / 频道：Julian Goldie Agency
- 发布时间：2026-06-02 01:09:19 -07:00
- 视频时长：483 秒
- 收录时间：2026-06-04 01:54:41 +08:00
- 访问边界：public

## 获取与转写

```yaml
subtitle_status: public auto caption found
transcript_method: public_subtitle
subtitle_language: en-orig
subtitle_format: json3
extraction_tool: yt-dlp 2026.3.17
transcript_quality: medium
media_retention: not_downloaded
scratch_cleanup: no audio/video downloaded; public subtitle JSON was used as extraction input
project_visible_artifacts: yes
transcript_location: raw/videos/2026-06-04-youtube-hermes-obsidian-source/transcript.txt
segments_location: raw/videos/2026-06-04-youtube-hermes-obsidian-source/segments.md
transcript_metadata_location: raw/videos/2026-06-04-youtube-hermes-obsidian-source/transcript-meta.json
ledger_location: raw/videos/2026-06-04-youtube-hermes-obsidian-source/acquisition-ledger.json
```

获取记录：

```text
1. YouTube oEmbed / watch page metadata succeeded.
2. YouTube watch page exposed one English auto-generated caption track.
3. Direct timedtext requests returned empty bodies.
4. Installed and used yt-dlp from Python user environment to download public auto subtitles only.
5. No cookies, private account data, member-only content, audio, or video were used.
```

说明：

```text
字幕 / ASR 是 raw/source text，不是 reviewed evidence。
AI 摘要是 candidate comprehension，不是 truth。
本条没有下载音频或视频；只使用 YouTube 公开自动字幕。
完整逐字稿、时间轴、metadata 和 acquisition ledger 已复制到 `raw/videos/2026-06-04-youtube-hermes-obsidian-source/`，不依赖 `.codex` scratch。
```

## 人话摘要

视频的核心意思很简单：很多人把 Hermes 或 Claude 当成一次性问答工具，每天重新解释业务背景、受众、内容风格和目标，导致浪费时间，输出也很泛。视频建议用 Obsidian 建一个“AI business brain”式的 vault，把内容策略、受众研究、社群洞察、过去 AI 输出、目标和 offer 等材料放进去，再创建一个 master context file，让 Hermes 在任务开始前读取或被提示读取这套上下文。

它展示的工作流更像“轻量业务上下文工作台”，不是 verified knowledge system。它关心的是让 AI 记住业务、产出内容更快、更贴近受众；它没有处理来源审查、证据支持、review gate、truth confidence、关系审查或 action readiness。

## 关键实体置信度

```text
confirmed:
  - YouTube video id: mjju1qYAV2w。
  - 视频标题、频道、发布时间、时长：来自 YouTube oEmbed / watch metadata / yt-dlp metadata。
  - Obsidian：视频直接提到 obsidian.md 和 Obsidian vault。
  - Claude：字幕中直接提到 Claude。
  - Hermes：视频标题、描述和字幕均直接提到 Hermes。
  - AI Profit Boardroom / AI Success Lab：视频描述和字幕中出现。

likely:
  - "master context file" 是讲者推荐创建的中心上下文文件。
  - "AI business brain" 是示范 vault 命名 / 类比，不是标准产品名。
  - "Agent OS" 是视频描述中的营销入口或课程入口，未单独验证其产品边界。

unclear:
  - Hermes 的准确产品身份、版本、文件读取方式和权限模型，视频没有给出官方技术锚点。
  - 视频中称 AI 工具可从同一 vault 工作，但字幕只清楚展示了 context primer / 手动上下文激活；没有证明自动文件读取或完整自动同步。
  - "free community of over 38,000 people"、商业增长效果、模板/课程价值没有独立核验。

needs user visual check:
  - 如果要精确复刻界面、提示词或 Hermes 连接步骤，需要看 03:30-04:30 的画面和视频描述中的模板链接。
```

## 时间轴 / 分段

- 00:00-00:52：提出问题：很多人每天把 Hermes 当搜索引擎用，问一次、关掉、第二天从零开始；对内容业务、社群、客户管线来说，这会拖慢增长。
- 00:52-02:02：说明泛化输出问题：Hermes、Claude 等工具不知道业务历史、受众、最佳视频、会员问题或转化最好的 offer，因此输出只能依赖当前输入。
- 02:02-02:52：提出 Obsidian memory vault 方案：让 AI 读取内容支柱、lead magnet、社群问题等上下文，减少反复 briefing。
- 02:52-03:28：展示 vault 结构：content strategy、audience research、community insights、past AI outputs、goals and offers；强调是普通 Markdown 文件。
- 03:28-04:14：创建 master context file：用 Hermes 或 Claude 生成业务概览、内容策略、offer、社群使命、成员画像、主题、语气等结构化上下文，再粘贴进 Obsidian。
- 04:14-04:58：连接 Hermes 到 vault：在任务开头粘贴 context primer，让 Hermes 先激活记忆系统，不再反复询问频道、受众、语气。
- 04:58-05:48：共享脑：Claude、Hermes 和其他工具从同一 vault 获取策略、受众、目标和历史输出；周一 newsletter 重点可被周三社媒任务复用。
- 05:48-06:46：recall layer：过去 Q&A 中的社群问题被保存后，可在之后生成 lead magnet 或内容时被重新引用。
- 06:46-08:02：三个业务用例：YouTube 内容生产、社群互动、模板/课程/社群推广；强调用旧问题、旧输出、内容历史生成更贴近受众的计划和跟进内容。

## 视频里直接说了什么

- 很多人用 Hermes 像用搜索引擎：提问、拿答案、关闭，第二天从零开始。
- 如果在做内容业务、社群或客户管线，每天从零开始会浪费大量时间。
- Hermes、Claude 等工具默认不知道你的业务、受众、历史内容、会员问题和 offer 表现。
- Obsidian vault 可以作为 AI 的业务记忆：保存策略、受众、工作流、成功案例、内容历史。
- 建议创建一个干净 Obsidian vault，包含 content strategy、audience research、community insights、past AI outputs、goals and offers 等文件夹。
- 第一个 note 是 master context file，每次任务开始前让 Hermes 读取。
- 可以用 Hermes 或 Claude 生成结构化 master context，包括 business overview、content strategy、offers、community mission、member avatar、weekly themes、tone 等。
- 在 Hermes 任务开头粘贴 context primer，激活这套 memory system。
- Claude、Hermes 和其他工具可以从同一个 vault 工作，形成 shared brain。
- newsletter、社媒内容、社群 Q&A、lead magnet 等内容可以互相复用和延续。
- 视频把这一套包装为让 AI 输出更快、更个性化、更适合内容/社群业务增长。

## 我的理解 / 推断

这条视频的底层模式是：

```text
业务上下文 -> Obsidian Markdown vault -> master context / context primer -> Hermes / Claude task -> 输出回写 vault -> 下次任务复用
```

它不是在做“知识可信度治理”，而是在做“AI 工作记忆复用”。它的强点是低门槛、好懂、能立刻减少重复 briefing；弱点是很容易把 AI 输出、营销口径、旧社群问题和业务判断混在一起，缺少 review、source anchor、scope / stale 检查和 action basis 边界。

对 VAKS 来说，它更像 Dev Context / Activation / Context Pack 的朴素民间版：用一个 master context file 让 agent 快速进入项目状态。它不能替代我们的 truth core。

## 反漏提取检查

```text
pain point:
  AI 工具每天没有业务记忆，用户要反复解释受众、目标、语气、历史输出和社群问题；输出泛化，内容生产和运营速度变慢。

workflow:
  创建 Obsidian vault -> 建 content strategy / audience research / community insights / past AI outputs / goals and offers 等结构 -> 创建 master context file -> 用 Hermes/Claude 生成业务上下文 -> 粘贴进 Obsidian -> 每次 Hermes 任务前粘贴 context primer -> 让多个 AI 工具共享同一套业务信息 -> 把 newsletter、社群 Q&A、AI 输出继续保存到 vault -> 后续任务召回复用。

tools / plugins:
  Hermes、Claude、Obsidian、Markdown vault、context primer、master context file。视频描述还提到 Agent OS、Skool 社群、AI Profit Boardroom、AI Success Lab，但没有技术细节。

information structure:
  主要是业务文件夹和中心上下文文件：content strategy、audience research、community insights、past AI outputs、goals and offers、master context file。它没有 claim / pattern / decision / review queue / evidence packet 结构。

judgment mechanism:
  视频的判断标准是“是否减少重复 briefing、是否让输出更贴近业务和受众、是否帮助内容/社群增长”。它没有判断资料真伪、证据充分性、来源独立性或 action readiness 的机制。

user experience:
  优点是极低门槛：Obsidian + Markdown + 一个 master context 文件 + 每次任务开头的 context primer。用户不需要理解 schema 或 review queue。缺点是依赖手动维护，context primer 可能变长、变旧、变泛，AI 也可能误读或过度相信旧内容。

automation boundary:
  自动或半自动的部分是 AI 根据上下文生成内容计划、帖子、邮件、lead magnet 等。人工仍要维护 vault、保存关键输出、选择哪些内容进入上下文、检查是否过时。视频没有展示可靠的自动同步、自动审查或权限控制。

risk:
  1. 把 AI 输出当长期业务事实。
  2. 把社群 Q&A / 旧内容当作当前行动依据，缺少时间和范围检查。
  3. master context file 一旦过时，会让所有任务沿着旧假设输出。
  4. 多个 AI 工具共享同一 vault，如果没有写入边界，可能制造污染。
  5. 视频是营销型内容，商业效果和模板价值没有独立证据。

fit for us:
  可借鉴到 Dev Context / Activation / Context Pack 层：项目级 master context、context primer、共享 agent 只读上下文、旧问答/旧输出作为 activation input、低门槛任务启动方式。

challenge to us:
  它提醒我们：普通用户首先要的是“AI 不要每天失忆”，不是完整证据审查。如果 VAKS 的入口太重，会输给这种简单 master context 工作流。我们需要保留轻入口，让 strict gate 只在 promotion / decision / action basis 时出现。
```

## 可抽取 Candidate Points

- VAKS 可以有一个项目级 `master context / context primer` 入口，但它应该归入 Dev Context / Activation，不是 reviewed truth。
- Agent 读取 Obsidian vault 的能力应默认是 read-only 或 suggest-only，不能直接写 formal reviewed knowledge。
- 过去 AI 输出、newsletter、社群 Q&A、coaching call notes 可以改善内容生成的 activation，但不能自动变成 claim support。
- 业务上下文文件需要 temporal applicability / stale 检查，否则旧 offer、旧受众画像、旧内容主题会污染新任务。
- 低门槛的“任务开始前加载上下文”是重要 UX，不应该被 schema 和 review queue 压到前台。
- 一个中心 master context file 很方便，但也可能成为单点过时源；更稳的做法是 context pack / dev context pack 带来源、scope、风险和刷新条件。
- 多工具共享同一个 vault 能提高连续性，但也需要 agent access tier 和写入隔离。

## 可借鉴

- 用普通 Markdown vault 做 agent 共享业务上下文。
- 为每个项目准备一个简明 context primer，帮助 AI 快速进入任务。
- 将业务目标、受众画像、内容风格、offer、历史输出、社群问题放入项目 workbench。
- 将过去 Q&A / coaching call 问题转化为后续内容选题候选。
- 让多个 AI 工具读取同一套上下文，减少重复 briefing。
- 把“AI 记忆”解释成用户能懂的 master context，而不是一上来讲 schema / graph / review。

## 不能直接借鉴

- 不能把 master context file 当 truth layer。
- 不能把 AI 输出、社群问题、内容表现、营销话术直接当 reviewed knowledge。
- 不能默认多个 agent 都有写入 vault 的权限。
- 不能把“能生成更个性化内容”当作证据充分或行动可用。
- 不能把 Obsidian 文件夹结构当作 VAKS schema。
- 不能让 context primer 无限膨胀，替代 source anchor、review、risk 和 scope check。

## 风险和不确定

- YouTube 自动字幕质量中等，Hermes / Agent OS / Skool 等关键产品边界需要视觉或官方页面确认。
- 视频没有提供 Hermes 如何实际读取本地 vault 的技术细节；可能只是手动粘贴 context primer。
- 商业增长、社区人数、模板价值属于营销主张，未核验。
- 视频没有展示写入边界、版本更新、过期上下文处理或冲突处理。
- 对内容生产有启发，但不能作为 VAKS 架构采纳证据。

## VAKS 归位

```text
Capture:
  YouTube URL、metadata、公开自动字幕、时间轴进入 raw/videos。

Understand:
  人话摘要、工作流、信息结构、关键实体置信度、candidate points。

Review:
  本条不创建 reviewed knowledge。若以后要正式采用 master context / context primer 作为 VAKS 操作规则，需要进入 REVIEW_QUEUE 或 evidence-aware review。

Connect:
  可连接到 DEV_CONTEXT、Activation Tier、agent access tier、context pack、conversation-derived feedback、source-to-content workflow。

Activation / Context Pack:
  这是本条最相关层。视频展示的是低门槛 context activation，不是 truth review。

Decision / Action:
  不产生采用决策。最多作为后续批量对照样本之一。

Use Ledger / Feedback:
  可启发“过去任务输出和社群反馈如何帮助下一次内容生成”，但反馈不能改 truth。
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

- 准备把 `master context / context primer` 正式写成 VAKS 的 Dev Context 操作规则。
- 准备用 Hermes / Obsidian shared brain 作为 agent access 或 context pack 的实现参考。
- 后续 5-10 个外部样本反复支持“低门槛 context primer 是必要入口”。

## 下一步

本条先作为候选样本保留，不改主架构。后续如果多条外部资料都指向同一个结论，可以把“context primer / master context as activation surface”作为 review queue item，比较它和现有 `DEV_CONTEXT.md` / `templates/dev-context-pack.md` 的关系。

## 公开自动字幕时间轴

```text
00:00 Most people using Hermes right now are
00:01 making one mistake and it is costing
00:03 them hours every single week. They keep
00:06 opening it like a search engine. It's a
00:07 question. Get an answer. Close it
00:10 tomorrow. Start from zero again. And
00:12 that is fine if you are just messing
00:14 around. Trying to build something real,
00:16 a content business, a community, a
00:18 client pipeline. Starting from zero
00:19 every day is the slowest possible way to
00:21 grow. What I'm going to show you right
00:23 now is how to plug Hermes into a system
00:25 that remembers everything. strategy,
00:27 your audience, your workflows, your wins
00:30 stored, everything connected, everything
00:31 ready to go the second you open a new
00:33 task. This changes how fast you can
00:36 produce content, how sharp your AI
00:38 outputs are, and how much your entire
00:39 operation can scale without adding more
00:41 people to your team. Going to walk you
00:43 through the full setup step by step, and
00:46 I will show you exactly how I use it to
00:48 run an AI, content, and community
00:49 business. Let's get into it. Right, let
00:52 me show you what this actually looks
00:53 like in practice before I explain how to
00:55 set it up. Here is the situation most AI
00:57 content creators are stuck in right now.
00:59 You have got Hermes, you have got
01:01 Claude, maybe you have got a few other
01:02 tools running and every single one of
01:04 them wakes up in the morning with zero
01:06 memory of who you are or what you are
01:08 building. Hey, if we haven't met
01:09 already, I'm the digital avatar of
01:11 Julian Goldie, CEO of Goldie Agency.
01:13 Whilst Julian is out working with
01:15 clients to help them get more leads and
01:16 customers, I'm here to bring you the
01:18 sharpest AI systems and workflows you
01:20 can put to work today. Julian reads
01:22 every single comment, so let him know
01:24 what you think below.
01:27 Now multiply that tasks a day, multiple
01:30 team members, it's turning into months.
01:32 You are not just wasting time on admin.
01:34 You are actively slowing down your
01:36 content output, your lead generation,
01:38 your community growth, everything that
01:39 matters. The worst part, even after all
01:41 that setup work, the outputs still feel
01:43 generic because the AI only has what you
01:45 just typed, does not have the full
01:47 picture, does not know what your best
01:49 performing video was last month, does
01:51 not know what your members are asking
01:53 about right now, does not know what
01:55 offer converted best last quarter. That
01:57 gap between what your AI knows and what
01:59 it actually needs to know to give you
02:01 great outputs, that is the problem
02:02 Obsidian solves. When you connect Hermes
02:05 to an obsidian memory vault, your AI
02:07 stops being a tool you have to prep
02:08 every morning and starts being an
02:10 operator that already knows your entire
02:11 business. Talking about Hermes knowing
02:13 your content pillars before you type a
02:15 single word. Knowing which lead magnets
02:17 work for your audience, knowing what
02:19 coaching call questions came up last
02:21 week so it can suggest content that
02:23 actually answers what your community is
02:24 asking right now. Before we touch Hermes
02:26 at all, let me show you what the vault
02:28 looks like when it is set up properly.
02:30 Before I show you the final piece of
02:31 this system, quick one. If you want the
02:33 full vault template we use, the exact
02:34 prompts I showed you today, and weekly
02:36 coaching calls where we can get your
02:38 Hermes and Obsidian system set up and
02:40 running together live, that is inside
02:42 the AI profit boardroom. Best place to
02:44 automate your content, grow your
02:46 community, and scale your operations
02:48 with AI. Link is in the comments and
02:50 description. Check it out. Now, let's
02:52 finish this. You can see here I have got
02:53 a clean Obsidian vault. Inside it, you
02:56 will see folders. one for content
02:57 strategy, one for audience research, one
03:00 for community insights, one for past AI
03:02 outputs, and one for goals and offers.
03:04 These are not fancy documents. They are
03:06 plain markdown files text. This is
03:09 exactly what Hermes will read every time
03:11 it starts a new task. Now, here is the
03:13 first thing you want to do. If you do
03:14 not have Obsidian yet, go to obsidian.md
03:17 and download it. Free. It's about 2
03:20 minutes to install. Once you have it
03:22 installed, create a new vault to call
03:24 mine AI business brain. You can name
03:26 yours whatever you like. Now, inside
03:28 this vault, you are going to create your
03:29 first note. This is the note Hermes is
03:31 going to read every single time you give
03:33 it a task. I call it the master context
03:36 file. Here is the prompt I used to fill
03:38 this note. Copy this exactly and paste
03:40 it into Hermes or Claude to generate
03:42 your own version. Look at what comes
03:43 back. Fully structured context file,
03:46 business overview. Let's break down
03:48 content strategy offers. Clean markdown
03:51 format for the AI profit boardroom. This
03:53 file would include things like the
03:55 community's mission around AI automation
03:57 education. The member avatar, which is a
03:59 business owner or creator trying to use
04:01 AI to save time and scale, the weekly
04:03 content themes, the flagship coaching
04:05 program, the tone, which is direct,
04:07 practical, no fluff. Now, you copy that
04:09 output and paste it directly into your
04:10 Obsidian Master context file note. That
04:12 is layer 1 done. Your vault now has a
04:14 brain. Step two, connecting Hermes to
04:17 the vault. Now we need to tell Hermes
04:19 where to find this vault and how to use
04:20 it and start a new task. The top of any
04:24 task you give it from now on, you are
04:26 going to paste this context primer. This
04:28 is what activates the memory system
04:30 before Hermes asks what the channel is
04:32 about, who the audience is, what tone to
04:35 use, three or four back and forth
04:37 messages just to get it oriented. It
04:39 goes straight to work. The AI profit
04:42 boardroom covers AI tools and automation
04:44 for business owners. knows the content
04:47 style, knows recent themes from the
04:49 vault. To the AI profit boardroom
04:51 audience, that right there is the
04:53 difference a memory vault makes, just
04:55 faster, genuinely smarter outputs. Step
04:58 three, building the shared brain. Here
05:00 is where the system gets really
05:02 powerful. Vault is not just for Hermes.
05:04 AI agent you use can read from the same
05:06 place. That means Claude, Hermes, and
05:08 any other tool you run are all working
05:10 from identical information. on version
05:12 of your strategy, on version of your
05:14 audience, on version of your goals. For
05:16 the AI profit boardroom, this is a
05:18 massive unlock. Picture this. Your team
05:20 uses Claude on Monday to write the
05:22 weekly community newsletter. Those key
05:24 talking points get saved as a note in
05:26 the vault. On Wednesday, Hermes is
05:28 creating social media post, reads the
05:30 newsletter note, and automatically ties
05:32 the social content back to what went out
05:33 in the email and connects. Came from the
05:36 same place. Now that note lives in the
05:38 vault. Next time any agent starts a
05:40 task, it has access to what was built
05:42 this week. The continuity is automatic.
05:45 You are not managing it manually. The
05:47 system manages itself. Step four, the
05:49 recall layer. This is the layer most
05:52 people never think about until they see
05:53 it work. And when they see it, it
05:55 changes everything. Your vault gets
05:57 better over time. Note you add, every
05:59 output you save, every insight you
06:01 capture makes every future task sharper.
06:04 Here is a real example of how this plays
06:06 out for the AI profit boardroom. Back in
06:08 January, the community ran a live Q&A
06:10 session. The top questions members asked
06:12 were saved as a note in the vault. Fast
06:14 forward to now. You ask Hermes to build
06:16 a new lead magnet for the community.
06:18 Hermes reads the January Q&A note, sees
06:21 the top three questions members had
06:23 about automating their content workflow,
06:25 builds the lead magnet around exactly
06:27 those pain points. That is not just
06:29 relevant, that is precisely targeted,
06:31 and it came from data you already had.
06:33 You did not have to brief Hermes on any
06:35 of it. The vault did that work for you.
06:37 How it is referencing specific things
06:39 from the vault. Specific audience
06:41 language pain. This is what personalized
06:44 AI output actually looks like. Cases for
06:47 the AI profit boardroom. Let me show you
06:49 three specific ways this system directly
06:51 grows an AI community business. It's
06:54 case one. YouTube content production.
06:56 Week. Hermes reads the vault, checks
06:58 what content has already been covered,
07:00 identifies what topics members are
07:01 asking about right now, and drafts a
07:03 full content plan with titles, hooks,
07:05 and scripts. No briefing, no
07:07 reexplaining. Just open a task and get a
07:10 plan that is already built around your
07:11 audience and your goals. Here's case
07:13 two, community engagement. Every
07:15 coaching call, the key questions and
07:17 insights get saved to the vault. Hermes
07:20 reads those notes and generates
07:21 follow-up posts, email responses, and
07:23 content ideas that directly address what
07:25 members brought up. Your community feels
07:27 heard, and your content stays perfectly
07:29 matched to what they actually need. If
07:31 you want the full system, the vault
07:33 template, every prompt from today's
07:35 video, and weekly live sessions where we
07:37 build this together, come join the AI
07:39 profit boardroom. Best place to scale
07:41 your content, automate your workflows,
07:43 and grow your community with AI. It is
07:46 already there waiting for you. link is
07:48 in the comments and description. And if
07:49 you want to keep learning with a free
07:51 community of over 38,000 people already
07:54 using AI to build serious operations,
07:56 join the AI success lab. All the video
07:58 notes, templates, and a community of
08:00 people doing the actual work. See you in
08:02 the next one.
```
