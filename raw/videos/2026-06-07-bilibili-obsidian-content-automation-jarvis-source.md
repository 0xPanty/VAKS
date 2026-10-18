---
type: source
status: source-captured
title: 'Obsidian从1到2｜超越Karpathy，最全内容创作自动化全流程！把你的Ai训练成贾维斯～'
source_id: bilibili-BV1JWdfBTEcy
source_uri: bilibili:BV1JWdfBTEcy
source_url: https://www.bilibili.com/video/BV1JWdfBTEcy/
source_type: video
platform: bilibili
platform_id: BV1JWdfBTEcy
author: '超级TANG-'
publisher: '超级TANG-'
published_at: '2026-04-19 23:26:03 +08:00'
updated_at:
duration: 981s
captured_at: '2026-06-07 21:08:13 +08:00'
captured_by: Codex
raw_location: raw/videos/2026-06-07-bilibili-obsidian-content-automation-jarvis-source.md
processing_mode: runner
processing_level: medium
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
transcript_location: raw/videos/2026-06-07-bilibili-obsidian-content-automation-jarvis-source/transcript.txt
segments_location: raw/videos/2026-06-07-bilibili-obsidian-content-automation-jarvis-source/segments.md
transcript_metadata_location: raw/videos/2026-06-07-bilibili-obsidian-content-automation-jarvis-source/transcript-meta.json
ledger_location: raw/videos/2026-06-07-bilibili-obsidian-content-automation-jarvis-source/acquisition-ledger.json
media_retention: deleted
source_status: active
topics:
  - video-intake
  - obsidian
  - automation
  - content-creation
  - claude-code
  - vaks-candidate
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
  - borrow-p1-project-manual
  - borrow-p1-feedback-constraints
  - borrow-p1-executable-markdown
---

# Obsidian从1到2｜超越Karpathy，最全内容创作自动化全流程！把你的Ai训练成贾维斯～

## 为什么收录

这条视频讲的不是单个 Obsidian 插件，而是一套“本地资料 + AI + 项目说明书 + feedback + Git 回退 + 发布工具”的内容创作自动化链路。对 VAKS 有价值的地方在于：它把知识库从静态 Wiki 变成可执行工作台，但也暴露了几个必须守住的边界：AI 能自动写文件，不代表它能自动改真理层；反馈能改善输出，不代表反馈能提升事实置信度；自动发布很省事，但必须有版本控制和人工门槛。

## 来源卡

- 平台：Bilibili
- 原始链接：https://www.bilibili.com/video/BV1JWdfBTEcy/
- 标题：Obsidian从1到2｜超越Karpathy，最全内容创作自动化全流程！把你的Ai训练成贾维斯～
- 作者 / UP 主：超级TANG-
- 发布时间：2026-04-19 23:26:03 +08:00
- 视频时长：981 秒
- 收录时间：2026-06-07 21:08:13 +08:00
- 访问边界：public_no_cookies

## Intake Boundary

```yaml
processing_tier: medium
knowledge_status: raw
overlay_state: none
review_pressure: none | review_due | blocked
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
subtitle_status: public subtitle endpoints returned empty
transcript_method: local_asr
asr_engine: openai-whisper
asr_model: small
asr_device: cuda
transcript_quality: medium
media_retention: deleted
scratch_cleanup: temporary public audio deleted after ASR
project_visible_artifacts: yes
transcript_location: raw/videos/2026-06-07-bilibili-obsidian-content-automation-jarvis-source/transcript.txt
segments_location: raw/videos/2026-06-07-bilibili-obsidian-content-automation-jarvis-source/segments.md
transcript_metadata_location: raw/videos/2026-06-07-bilibili-obsidian-content-automation-jarvis-source/transcript-meta.json
ledger_location: raw/videos/2026-06-07-bilibili-obsidian-content-automation-jarvis-source/acquisition-ledger.json
```

说明：

```text
字幕 / ASR 是 raw/source text，不是 reviewed evidence。
AI 摘要是 candidate comprehension，不是 truth。
如果音视频为转写临时下载，成功后默认删除，只保留文字稿、时间轴、元数据和 ledger。
这些保留物必须在本项目或正式 Obsidian vault 中可见；不能只留在 .codex scratch。
`transcript_metadata_location` 同时用于公开字幕 metadata 和 ASR metadata；不要把公开字幕强行写成 ASR。
```

## 人话摘要

视频的主张是：不要只把 Obsidian 做成“会收藏链接的 Wiki”，而要把它变成一个本地项目工作台。做法是先把项目资料、角色设定、风格标准、流程说明、进度状态、反馈记录都沉淀成 Markdown 文件，再让 AI 每次工作前读取这些文件。这样 AI 不只是临时聊天，而是按项目状态和规则执行。

视频用“小李飞刀漫画创作”举例：一开始只有一本 PDF，让 AI 直接画会出现人物不一致、风格漂移、台词不准等问题；后来把人物形象、剧情分解、文件结构、工作流说明书、风格参考、禁止项和专属 skill 都固定下来，AI 的出片质量提高、废片减少、成本下降。后半段扩展到 Git 版本控制、文章自动配图排版、Obsidian 手机预览/公众号草稿、飞书 CLI 发布，形成从创作到发布的自动化链路。

## 关键实体置信度

```text
confirmed:
  - Bilibili BV1JWdfBTEcy
  - 标题、UP 主、发布时间、时长来自 Bilibili public metadata
  - Obsidian、Claude Code、Git/GitHub、飞书 CLI、Markdown、本地文件夹、版本控制

likely:
  - ASR 中的 "Cloud Code" 多处应为 Claude Code
  - ASR 中的 "Gate/Gatehub/Gate與Nit" 多处应为 Git/GitHub/git init
  - ASR 中的 "Redmi" 应为 README
  - ASR 中的 "sql" 应为 skill
  - ASR 中的 "NanoBudana" 大概率指 Nano Banana

unclear:
  - "保育 Skill / 宝玉 Skills" 的准确仓库名或工具名，需看画面/简介确认
  - 微信预览插件名称，ASR 为 "DRAT"，需画面确认
  - "HER / 假赔司 / Jarvis" 等词受 ASR 影响，按语义理解为 Jarvis/AI assistant

needs user visual check:
  - 具体 GitHub 仓库地址、插件名、提示词文档地址、API key 配置项
```

重点检查：

```text
工具名 / 项目名 / 仓库名 / URL / 命令 / 版本号 / star 数 / 平台支持 / UI 文案，不能只靠 ASR 判断。
```

## 时间轴 / 分段

- 00:00-01:15：提出目标：从静态 Wiki 变成懂你的、持续进化的本地 AI 工作台。
- 01:15-02:13：下载通用创作 skill，先从一个 PDF/原著直接生成漫画，暴露人物和风格不稳定问题。
- 02:13-03:00：第一步锁定人物形象：角色设定、服饰、武器、性格、参考图，要求 AI 每次创作前先读取。
- 03:07-04:20：第二步剧情分解和文件结构：章节概述、出场人物、场景、关键对话、分镜建议、人物状态和可跳转链接。
- 05:00-06:26：第三/四步 feedback 汇总成风格参考和工作流说明书，成为项目中央大脑。
- 06:27-07:10：第五步把项目要求写入专属 skill，触发后按项目说明书、进度和步骤执行。
- 07:10-08:00：抽象方法：打磨本地 Markdown，让 AI 知道项目职能、权限、进度、文件夹用途和可调用边界。
- 08:00-09:50：用 Git/GitHub 做版本控制和回退安全网，防止 AI 误删或覆盖满意作品。
- 09:50-12:28：文章自动配图、排版、重新创建文件、插图规划和图片生成。
- 12:28-14:53：Obsidian 内预览/发布到公众号草稿箱，以及通过 CLI 把 Obsidian 文件发到飞书。
- 15:00-16:20：总结：真正价值不是插件，而是把模糊需求变成可执行流程，让每次对话训练 AI 更懂项目。

## 视频里直接说了什么

- 真正有价值的不是抓取网页建 Wiki，而是 AI 能筛选、理解、调用、转化多少信息。
- 只靠一次提示词直接生成，会出现人物形象、画风、台词和一致性问题。
- 需要把角色设定、剧情分解、文件结构、人物状态、工作流说明书和风格参考写成本地 Markdown。
- 工作流说明书要成为项目中央大脑，AI 每次进入项目必须先读。
- 反馈要被沉淀为标准画风参考、作品风格指导、喜欢/禁止项。
- 文件越多、AI 写文件越强，越需要 Git/GitHub 版本控制和回退。
- 内容生产链路可以继续接自动配图、排版、预览、公众号草稿和飞书发布。
- 工具只是第一步，核心是把模糊需求变成可执行流程。

## 我的理解 / 推断

- 这套方法的核心不是“Obsidian + 很多插件”，而是“项目本地协议化”：把 AI 需要遵守的规则、资源、状态和反馈变成项目内可读文件。
- 它和 VAKS 的相似处是都在反对一次性聊天，强调可追踪、可复用、可回退的工作上下文。
- 它和 VAKS 的差异是：视频主要服务内容生产和风格一致性，默认更鼓励 AI 自动写文件、自动发布；VAKS 必须额外保留 candidate/reviewed/truth/action basis 边界。
- 对我们最值得借的是“工作流说明书 + 项目专属 skill + feedback 变成下次工作约束”，不是它的自动发布冲动。

## 反漏提取检查

```text
pain point:
  - 本地资料很多，但 AI 不知道项目规则、当前进度、偏好和禁止项。
  - 内容创作每次从零开始，排版、配图、发布重复劳动重。
  - AI 生成物风格不一致，容易误删/覆盖满意结果。

workflow:
  - 原始资料/PDF -> 角色/设定/剧情分解 -> 文件结构/链接/状态 -> 工作流说明书 -> 专属 skill -> 创作 -> 人工反馈 -> 风格参考/禁止项 -> 下一轮创作。
  - 成文后 -> 文章结构化 -> 插图规划 -> 图片生成 -> 新文件插入 -> 手机/公众号预览 -> 发布草稿/飞书同步。

tools / plugins:
  - Obsidian, Claude Code, Markdown, Git/GitHub, terminal/CLI, Feishu CLI, image-generation skill/API, Obsidian publishing/preview plugins.

information structure:
  - 项目文件夹按角色、剧情、漫画、人物状态、风格指南、工作流说明书分层。
  - README/工作流说明书充当项目入口，双链连接必须读取的参考文件。
  - 每个文件夹说明自己的用途、权限和可调用关系。

judgment mechanism:
  - 人工挑选喜欢/禁止的输出，把反馈沉淀成风格参考和禁止项。
  - 用废片率、成本、风格一致性、台词准确性判断系统是否进化。

user experience:
  - 用户从重复提示 AI，变成维护项目说明书和少量触发命令。
  - 发布链路从平台切换/手工上传，变成本地 Markdown 到外部平台的连接。

automation boundary:
  - AI 可以自动读取项目规则、生成文件、排版、配图、发布草稿。
  - 但关键风格判断、满意/禁止项、最终发布和版本回退仍需要人控。

risk:
  - 文件越多，AI 越可能漏读、误读或幻觉。
  - 自动写文件可能误删/覆盖满意版本。
  - 自动发布和外部平台连接有安全、成本和账号权限风险。
  - ASR 对工具名/仓库名/命令识别不可靠。

fit for us:
  - 强支持 VAKS 的 project-local manuals、skill、feedback ledger、dev context、activation tier。
  - 可以借“项目说明书作为 AI 入口”和“反馈沉淀为下次工作约束”的设计。
  - 也支持我们刚补的文件转换入口：资料先变成可读 Markdown，再进入候选蒸馏。

challenge to us:
  - 视频路线比 VAKS 更激进，容易把候选/反馈/自动化输出误当成知识。
  - 如果 VAKS 只重审查不重工作台体验，会显得慢；需要把重检查做成 lazy gate。
```

提取合格线：

```text
如果只写了摘要，但没有写痛点、工作流、工具 / 插件、风险、对我们框架的验证或挑战，这条资料卡不算提取完成。
```

## 可抽取 Candidate Points

- `project_operating_manual_as_ai_entrypoint`: 项目级工作流说明书可以作为 AI 每次进入项目的第一读取物，减少漏读和重复提示。
- `feedback_to_style_constraints`: 人工反馈可以沉淀为风格参考、禁止项和下次创作约束，但不应直接变成事实置信度。
- `local_markdown_as_executable_context`: 本地 Markdown 不只是存资料，也可以描述资源、权限、进度、文件夹职责和可调用关系。
- `version_control_as_ai_file_safety_net`: 当 AI 可以批量改文件时，Git/GitHub 类版本控制是必需安全网。
- `publish_pipeline_requires_gate`: 从本地知识库连接公众号/飞书等发布平台很高效，但最终发布、账号权限和成本必须有人工门槛。

## 借鉴标签

```yaml
borrow_value: strong
P1:
  - project_operating_manual_as_ai_entrypoint
  - feedback_to_constraints_not_truth
  - local_markdown_as_executable_context
P2:
  - version_control_required_for_ai_file_work
  - publishing_pipeline_as_tool_layer
P3:
  - content_creation_preview_workflow
avoid:
  - auto_publish_default
  - feedback_as_truth_confidence
  - asr_as_reviewed_evidence
  - project_style_as_global_default
  - private_account_routes_default
```

## 可借鉴

- 借工作流说明书/README 作为项目中央入口。
- 借“项目专属 skill + 本地资料 + 当前进度”的触发方式。
- 借把喜欢/禁止/废片经验写回项目文件，形成下一轮约束。
- 借 Git 版本控制作为 AI 文件操作的安全网。
- 借本地 Markdown 到外部平台的连接思路，但只放在工具层，不进 truth core。

## 不能直接借鉴

- 不能把视频里的自动发布路径直接接入 VAKS 主线。
- 不能把 AI 总结、ASR、反馈、点赞数、工具输出当成 reviewed knowledge。
- 不能让专属 skill 自动改 `wiki/claims`、`wiki/patterns`、`wiki/decisions`。
- 不能默认读 cookies、账号资料、私有仓库或外部平台权限。

## 风险和不确定

- ASR 将 Claude Code 识别成 Cloud Code、Git/GitHub 识别成 Gate/Gatehub，工具名需画面确认。
- 具体插件/仓库/提示词文档没有从画面确认，当前只能作为候选线索。
- 视频主要是创作工作流案例，不能直接证明这些工具组合适合知识审查或行动依据。
- 自动提交/推送频率建议不能照搬；VAKS 需要区分 scratch、repo、Obsidian、commit/push。

## VAKS 归位

```text
Capture: 原始资料、PDF、文章、素材、项目文件夹进入本地 Markdown。
Understand: AI 读取说明书、角色设定、剧情分解、风格指南后生成候选输出。
Review: 人工挑选喜欢/禁止项，形成下一轮约束；在 VAKS 中只能进入候选/反馈，不可直接审定 truth。
Connect: 双链、README/工作流说明书、文件夹职责说明连接上下文。
Activation / Context Pack: 项目入口文件决定 AI 这次要读哪些资料和规则。
Decision / Action: 发布、推送、外部同步属于行动层，需要门槛。
Use Ledger / Feedback: 废片、喜欢项、禁止项、成本下降是反馈线索，可改进激活和流程。
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

当前等级：

medium，已保留完整转写、时间轴、metadata、ledger，并抽取候选自动化逻辑。

升级到 heavy 的条件：

- 如果要把“项目说明书作为 AI 入口”或“feedback-to-constraint”正式写入 VAKS 主架构，需要进入 review queue。
- 如果要接公众号/飞书/自动发布，需要单独安全评审，不从本视频直接采用。

## 下一步

- 将自动化逻辑保存在候选蒸馏和 VAKS 项目 overlay 中。
- 关键工具名、插件名、仓库名若后续要实际复现，需要人工看画面或拿到视频配套文档确认。

