---
type: source
status: source-captured
title: "知识库搭完不知道怎么用？分享下我的思路"
source_id: xhs-6a25a051000000001700a0df
source_uri: xiaohongshu:6a25a051000000001700a0df
source_url: http://xhslink.com/o/6PgPVcxjWYw
resolved_url: "https://www.xiaohongshu.com/discovery/item/6a25a051000000001700a0df"
source_type: video
platform: xiaohongshu
platform_id: 6a25a051000000001700a0df
author: 沫沫姬姬玩AI
publisher: 沫沫姬姬玩AI
published_at:
updated_at: "2026-06-08 16:11:21 +08:00"
duration: "03:46"
captured_at: "2026-06-08 18:42:14 +08:00"
captured_by: Codex
raw_location: raw/videos/2026-06-08-xhs-knowledge-base-not-use-source.md
processing_mode: immediate
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
transcript_location: raw/videos/2026-06-08-xhs-knowledge-base-not-use-source/transcript.txt
segments_location: raw/videos/2026-06-08-xhs-knowledge-base-not-use-source/segments.md
transcript_metadata_location: raw/videos/2026-06-08-xhs-knowledge-base-not-use-source/transcript-meta.json
ledger_location: raw/videos/2026-06-08-xhs-knowledge-base-not-use-source/acquisition-ledger.json
keyframe_snapshot_location: raw/videos/2026-06-08-xhs-knowledge-base-not-use-source/keyframe-contact-sheet.jpg
media_retention: deleted
source_status: active
topics:
  - ai-knowledge-base
  - agent-first-knowledge-base
  - local-files
  - weekly-review
  - skill-workflow
  - source-intake
projects:
  - verified-action-knowledge-system
source_family: xhs-agent-first-knowledge-base
upstream_sources: []
verification_status: unverified
candidate_relation_suggestions: []
tags:
  - raw-video
  - xiaohongshu
  - candidate-only
---

# 视频资料：知识库搭完不知道怎么用

## 为什么收录

这条视频很贴 VAKS：它不再讨论“怎么搭一个知识库”，而是讨论“搭完后怎么真的用起来”。作者的核心判断是：知识库不能只是资料仓库，必须围绕一个或一类问题，建立过滤、拆解、归档、调用和每周迭代规则；真正的一等使用者应当是 agent，而不是只给人自己看。

对 VAKS 的价值主要在工作流和 agent 使用边界：用 skill 做新内容预处理和周度整理；把知识拆成原则、方法、案例、反模式、工具、洞察；用本地文件保存；agent 通过命令增删改查，避免直接读写原子库造成误操作。它不是 reviewed knowledge，也不是源码证据。

## 来源卡

- 平台：小红书
- 原始短链：http://xhslink.com/o/6PgPVcxjWYw
- 解析到的公开条目：`xiaohongshu:6a25a051000000001700a0df`
- 标题：知识库搭完不知道怎么用？分享下我的思路
- 作者：沫沫姬姬玩AI
- 公开视频时长：03:46
- 公开更新时间：2026-06-08 16:11:21 +08:00
- 收录时间：2026-06-08 18:42:14 +08:00
- 访问边界：public SSR metadata / public video stream；未使用 cookies、私有收藏、会员内容或评论区。

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
They do not create reviewed evidence, project borrowing conclusions, truth
confidence, or action basis.

## 获取与转写

```yaml
subtitle_status: public transcript not found in SSR state
transcript_method: local_asr
asr_engine: faster-whisper
asr_model: small
asr_device: cuda
asr_compute_type: float16
transcript_quality: medium
media_retention: deleted
scratch_cleanup: temporary public mp4 and wav deleted after project-visible artifacts and Obsidian sync
project_visible_artifacts: yes
transcript_location: raw/videos/2026-06-08-xhs-knowledge-base-not-use-source/transcript.txt
segments_location: raw/videos/2026-06-08-xhs-knowledge-base-not-use-source/segments.md
transcript_metadata_location: raw/videos/2026-06-08-xhs-knowledge-base-not-use-source/transcript-meta.json
ledger_location: raw/videos/2026-06-08-xhs-knowledge-base-not-use-source/acquisition-ledger.json
keyframe_snapshot_location: raw/videos/2026-06-08-xhs-knowledge-base-not-use-source/keyframe-contact-sheet.jpg
```

说明：

```text
字幕 / ASR 是 raw/source text，不是 reviewed evidence。
AI 摘要是 candidate comprehension，不是 truth。
本条使用公开视频 + 本地 CUDA ASR；完整逐字稿、时间轴、metadata 和 ledger 已复制到项目路径，不依赖 .codex scratch。
ASR 中有明显错字，工具名、项目名、仓库名、URL、命令、版本号、UI 文案不能只靠 ASR 判断。
```

## 人话摘要

视频说的是：很多人搭完 AI 知识库后不知道怎么用，因为他们把知识库当资料库，只囤内容，不筛选、不规划、不迭代。真正的知识库应该围绕问题建立，并且需要明确使用规则和迭代规则。

作者的做法是：新内容先用 `weekly item` 之类的 skill 预处理，按“下个月还能不能复用”过滤低价值内容；保留下来的内容被拆成原则、方法、案例、反模式、工具和洞察，并打话题标签；每周再用 `weekly review` 结合个人画像重新整理，把自己的思考和案例沉淀进专题。最后，agent 在新会话里读取个人画像，并按专题调用知识来做需求评估、周期复盘、skill 编写等具体工作。

## 关键实体置信度

```text
confirmed:
  - 小红书 item id：6a25a051000000001700a0df。
  - 标题、作者昵称、时长、公开更新时间：来自公开页面 SSR state。
  - 画面字幕确认了核心词：知识库不是资料库、隐私性/沉淀与迁移成本、本地 Agent 调用麻烦、需求评估、定期复盘、编写 Skill、知识库使用对象是 Agent。
  - 本次未使用 cookies、私有收藏、会员内容、评论区或云 ASR。

likely:
  - ASR 的 “谷歌 NotabookLM” 应为 Google NotebookLM。
  - ASR 的 “相当化reg检索” 应为向量化 / RAG 检索。
  - ASR 的 “原字信息” 应为原子信息。
  - ASR 的 “项量化存储” 应为向量化存储。
  - ASR 的 “cloud code” 应为 Claude Code。
  - “原则、方法、案例、反模式、工具、动筛” 中最后一类大概率是洞察。

unclear:
  - 作者提到灵感来自一个 GitHub 项目，但没有在公开描述中给出仓库名；本次未确认具体 repo。
  - `weekly item` / `weekly review` 是作者自建 skill 名还是公开 skill 名，未确认。
  - 作者说后续可能开源，但截至本次公开视频和简单公开搜索，没有确认到对应仓库。

needs user visual check:
  - 如果要确认视频画面中 GitHub 项目名、目录结构、命令名或框架图细节，需要人工看 01:16-02:20 和 03:36-03:46 附近画面。
```

## 时间轴 / 分段

- 00:00-00:23：提出问题：AI 知识库搭完后不知道怎么落地使用、怎么持续沉淀。
- 00:23-00:51：两个坑：把知识库当资料库，只囤积内容；只搭建不规划使用和迭代规则，导致内容混乱。
- 00:51-01:13：对比飞书知识库、Google NotebookLM 等云端知识库：方便但有隐私、沉淀迁移、本地 agent 对接成本问题。
- 01:13-01:31：倾向本地知识库；作者系统来自一个 GitHub 项目，但做了个人场景改造。
- 01:32-02:04：输入源与预处理：课程笔记、复盘、外网文章、个人观点；用 `weekly item` 筛选和拆解，核心标准是下个月还能不能复用。
- 02:04-02:20：现阶段放弃向量化存储，使用本地文件和本地命令支持 agent 增删改查，降低 agent 误操作风险。
- 02:20-02:38：用 `weekly review` 做每周整理，结合个人画像重新判断价值，把思考和案例更新进画像。
- 02:38-03:20：agent 新会话读取画像和专题知识，用于需求评估、周期复盘、编写 skill 等具体任务。
- 03:20-03:46：总结：关键是原子化、过滤、迭代；知识库真正的一等公民应当是 agent；作者后续可能开源框架。

## 视频里直接说了什么

- 知识库不是资料库，不能只囤积文章、课程和材料。
- 真正的知识库应围绕一个或一类问题搭建。
- 不规划使用和迭代规则，会让过期、无用和有用内容混在一起。
- 云端知识库开箱即用，但有隐私、沉淀迁移、本地 agent 对接成本。
- 作者采用本地文件保存，用命令让 agent 增删改查。
- 新内容先用 skill 预处理，按“下个月还能不能复用”过滤。
- 保留内容拆成原则、方法、案例、反模式、工具、洞察，并加话题标签。
- 每周 review 会结合个人画像重新判断内容价值。
- agent 会读取个人画像和专题知识，做需求评估、复盘、skill 编写。
- 知识库真正的一等公民应该是 agent。

## 我的理解 / 推断

这条视频真正有价值的是“agent-first 知识库使用规则”。它把知识库从人类收藏夹改成 agent 可调用的工作资产：先过滤，再原子化，再专题化，再定期整理，再进入个人画像和专题库，最后让 agent 在具体任务里调用。

对 VAKS 来说，它强烈支持已有边界：候选材料不能自动变 truth；agent 不能直接乱写核心库；输入要过滤；沉淀要有 review；本地文件和命令接口比直接开放数据库更可控。

## 反漏提取检查

```text
pain point:
  - AI 知识库搭完后吃灰，原因是只收集资料，没有问题导向、过滤规则、迭代规则和 agent 调用路径。

workflow:
  - 新内容 -> weekly item 预处理 -> 下个月能否复用过滤 -> 原子化拆解 -> 六类分类和标签 -> 本地文件保存 -> weekly review 整理 -> 更新个人画像 / 专题库 -> agent 按任务调用。

tools / plugins:
  - weekly item skill
  - weekly review skill
  - 本地文件
  - 本地命令
  - agent
  - Claude Code / Codex 作为可复刻框架的执行入口

information structure:
  - 原子信息
  - 专题分类
  - 原则 / 方法 / 案例 / 反模式 / 工具 / 洞察
  - 话题标签
  - 个人画像
  - 支持库专题

judgment mechanism:
  - 这条内容下个月还能不能复用。
  - 是否能进入需求评估、复盘、skill 编写等具体任务。

user experience:
  - 本地知识库更可控，agent 读取个人画像和专题库后更贴近个人风格。
  - 云端知识库方便，但本地 agent 对接和迁移成本会更麻烦。

automation boundary:
  - AI 可以预处理、拆解、整理、调用。
  - 规则必须先由人设定；自动化不能变成什么都往里塞。

risk:
  - 只搭建不使用。
  - 只囤积不筛选。
  - 过期、低价值内容污染知识库。
  - agent 直接读写原子库造成误操作。
  - 个人画像和专题库被自动更新后可能带来错误积累。

fit for us:
  - 强化 VAKS 的 candidate filtering、review queue、agent gateway、dev context / profile activation、use ledger 方向。

challenge to us:
  - VAKS 不能只做“给人看的资料库架构”，必须让 agent 能安全调用，并且让日常复用闭环跑起来。
```

## 可抽取 Candidate Points

- 知识库要围绕问题搭建，不能只是收集资料。
- 新内容入口应先问“未来一个月还能不能复用”，过滤掉临时低价值内容。
- 候选知识应原子化，并按原则、方法、案例、反模式、工具、洞察等类型拆解。
- 本地文件 + 命令接口可以作为 agent 调用知识库的可控边界。
- agent 读取个人画像和专题库，比每次无上下文生成更稳定。
- 周期性 review 是让知识库持续活起来的必要机制。
- 知识库的一等使用者可以是 agent，但 agent 写入必须被规则约束。

## 可借鉴

- `P1`: agent-first knowledge base：未来 VAKS 的工作台/接口要服务 agent 安全调用，而不只是人类浏览。
- `P1`: weekly item / weekly review 双 skill：一个做入口过滤，一个做周期整理。
- `P1`: 本地文件 + 命令接口：agent 不直接读写核心库，通过受控命令增删改查。
- `P2`: 六类拆解：原则、方法、案例、反模式、工具、洞察，可作为候选标签/路由启发。
- `P2`: 个人画像 + 专题库作为 activation context，但不能当 truth。

## 不能直接借鉴

- 不要把作者的个人分类直接升级成 VAKS schema。
- 不要让 agent 自动更新个人画像后直接影响 truth confidence。
- 不要把 weekly review 变成无人工边界的自动 promotion。
- 不要把“本地文件”简单等同于安全；仍然需要权限、命令白名单和审计。
- 不要把视频里未确认的 GitHub 项目当作已验证实现。

## 风险和不确定

- ASR 存在错词，关键专有名词已做人工画面校对，但仓库名和框架图细节未确认。
- 视频是个人实践经验，不是完整开源实现或评测。
- 作者提到后续可能开源，当前只能作为 workflow candidate 记录。
- “agent 是一等公民”对 VAKS 是强启发，但也带来写入污染、权限失控、反馈误变 truth 的风险。

## VAKS 归位

```text
Capture:
  新内容先经过入口过滤和 reusable 判断。

Understand:
  用 skill 做初步拆解、标签、候选类型分类。

Review:
  weekly review 是周期性候选整理，不等于 evidence-aware review。

Connect:
  按专题、标签、案例、反模式连接到可调用知识。

Activation / Context Pack:
  个人画像和专题库可作为 agent activation context，但不提高真值。

Decision / Action:
  agent 可在需求评估、复盘、skill 编写时调用候选/专题内容；行动 basis 仍需后续 gate。

Use Ledger / Feedback:
  任务使用效果可以反向推动 review_due 或画像更新，但不能直接改变 truth。
```

## 处理等级

```text
medium
```

升级到 heavy 的条件：

- 找到作者承诺的开源框架或原始 GitHub 项目。
- 用户要把 weekly item / weekly review 变成 VAKS 正式 intake / review workflow。
- 需要设计 agent gateway 的命令接口、权限和审计规则。

## 下一步

进入候选蒸馏层，作为 VAKS `agent-first knowledge base` 和 `weekly filtering/review loop` 的 P1 借鉴材料；不进入 reviewed knowledge，不改主架构文档。
