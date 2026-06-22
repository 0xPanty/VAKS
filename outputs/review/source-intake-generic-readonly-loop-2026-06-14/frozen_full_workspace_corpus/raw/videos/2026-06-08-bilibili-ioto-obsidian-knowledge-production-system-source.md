---
type: source
record_kind: source_card
status: source-captured
title: "历时三年，专为Obsidian打造——IOTO知识生产系统的基本使用（IOTO2.0系列 01）"
source_id: bilibili-BV1jLXeBREzN
source_uri: bilibili:BV1jLXeBREzN
source_url: https://www.bilibili.com/video/BV1jLXeBREzN/
source_type: video
platform: bilibili
platform_id: BV1jLXeBREzN
author: "Johnny学"
publisher: "Johnny学"
published_at: "2026-03-30 18:02:28 +08:00"
updated_at:
duration: 847s
captured_at: "2026-06-08 16:51:20 +08:00"
captured_by: Codex
raw_location: raw/videos/2026-06-08-bilibili-ioto-obsidian-knowledge-production-system-source.md
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
transcript_location: raw/videos/2026-06-08-bilibili-ioto-obsidian-knowledge-production-system-source/transcript.txt
segments_location: raw/videos/2026-06-08-bilibili-ioto-obsidian-knowledge-production-system-source/segments.md
transcript_metadata_location: raw/videos/2026-06-08-bilibili-ioto-obsidian-knowledge-production-system-source/transcript-meta.json
ledger_location: raw/videos/2026-06-08-bilibili-ioto-obsidian-knowledge-production-system-source/acquisition-ledger.json
media_retention: deleted
source_status: active
topics:
  - obsidian
  - ioto
  - knowledge-production-system
  - input-output-task-result
  - project-workflow
  - daily-task-list
  - quick-panel
  - folder-structure
projects:
  - verified-action-knowledge-system
source_family: obsidian-ioto-knowledge-production-system
upstream_sources: []
verification_status: unverified
candidate_relation_suggestions: []
tags:
  - raw-video
  - bilibili
  - candidate-only
why_saved: see_body_or_legacy_record
---

# 视频资料：历时三年，专为 Obsidian 打造——IOTO 知识生产系统的基本使用

## 为什么收录

这条视频介绍 IOTO 2.0 系列的第 1 期基础用法：文件夹结构、日期型任务列表、项目创建、快捷面板。

它对 VAKS 的价值不是“证据审查”或“真值判断”，而是一个很实用的工作流逻辑：

```text
外部资料进来
-> 变成给自己看的思考
-> 通过项目任务每天推进
-> 最后沉淀成给别人看的成果
```

这个逻辑可以帮助 VAKS 思考未来的项目工作台、context pack 执行面板、候选理解与外部交付之间的边界。

## 来源卡

- 平台：Bilibili
- 原始链接：https://www.bilibili.com/video/BV1jLXeBREzN/
- 标题：历时三年，专为Obsidian打造——IOTO知识生产系统的基本使用（IOTO2.0系列 01）
- UP 主：Johnny学
- 发布时间：2026-03-30 18:02:28 +08:00
- 视频时长：847 秒
- 收录时间：2026-06-08 16:51:20 +08:00
- 访问边界：public metadata and public audio；未使用 cookies、私有收藏、会员内容或云 ASR
- 视频描述中的官网：pursueideal.com/guides/ioto；本轮未打开官网，未把官网内容作为证据

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
asr_engine: faster-whisper
asr_model: small
asr_device: cuda
asr_compute_type: float16
language: zh
duration_seconds: 846.738875
segment_count: 260
text_chars: 3727
transcript_quality: medium
media_retention: deleted
scratch_cleanup: downloaded public audio deleted after transcript artifacts were saved
project_visible_artifacts: yes
transcript_location: raw/videos/2026-06-08-bilibili-ioto-obsidian-knowledge-production-system-source/transcript.txt
segments_location: raw/videos/2026-06-08-bilibili-ioto-obsidian-knowledge-production-system-source/segments.md
transcript_metadata_location: raw/videos/2026-06-08-bilibili-ioto-obsidian-knowledge-production-system-source/transcript-meta.json
ledger_location: raw/videos/2026-06-08-bilibili-ioto-obsidian-knowledge-production-system-source/acquisition-ledger.json
```

说明：

```text
字幕 / ASR 是 raw/source text，不是 reviewed evidence。
AI 摘要是 candidate comprehension，不是 truth。
视频无公开字幕；转写使用公开视频音频 + 本地 CUDA ASR。
ASR 把 IOTO 多次听成 LTO / L2O；关键实体以 Bilibili 标题和描述校正。
```

## 人话摘要

作者把 IOTO 设计成一个项目化的 Obsidian 知识生产系统。它的核心不是“文件夹好看”，而是把知识工作拆成四类东西：

- 输入：别人给你的资料。
- 输出：你写给自己看的思考，从第一大脑输出到第二大脑。
- 任务：按项目组织的日期型任务列表，用来每天推进。
- 成果：交付给别人看的东西，比如文章、视频、总结、报告。

视频演示的基本流程是：先给某个项目创建今天的任务列表，然后从任务列表里创建输入、输出、成果，并自动带上项目属性和状态。未完成任务可以从昨天滚到今天；创建新项目时可以同步生成对应的成果类型和项目目录。快捷面板负责降低创建摩擦，但作者强调不要做复杂控制面板，越简单越好。

## 关键实体置信度

```text
confirmed:
  - Bilibili bvid：BV1jLXeBREzN。
  - 标题、UP 主、发布时间、时长：来自 Bilibili public view API。
  - 系统名称 IOTO、版本 IOTO 2.0.4、官网 pursueideal.com/guides/ioto：来自 Bilibili 标题和描述。
  - 第 1 期内容包括文件夹结构、日期型任务列表、项目创建、快捷面板：来自 Bilibili 描述。
  - 无公开字幕：公开 subtitle API 返回 empty。
  - ASR 使用 faster-whisper small / CUDA / float16；未使用 cookies、私有账号或云 ASR。

likely:
  - ASR 中的 LTO / L2O 应为 IOTO。
  - ASR 中的 "OB / Obi" 应为 Obsidian。
  - ASR 中的 "OpenCloud" 只是演示示例词，可能不是关键实体。
  - ASR 中的 "任务列表是工作的中书平台" 应为 "中枢平台"。

unclear:
  - 开头提到的既有框架名 ASR 听作 UFCD，未从画面或官网确认。
  - 快捷面板中 6 个按钮的完整 UI 文案没有逐一视觉确认。

needs user visual check:
  - 如果要精确复刻 IOTO 的按钮名称、属性字段、项目目录命名，需要看对应画面或官网文档。
```

## 时间轴 / 分段

- 00:00-00:55：说明 IOTO 经过三年开发和使用验证，进入 2.0 系列，本期讲最基本使用。
- 00:55-03:14：介绍文件夹结构：辅助文件夹、输入、输出、任务、成果；区分输入、输出和成果。
- 03:14-04:08：任务文件夹以项目方式管理任务列表，任务和成果在项目维度一一对应。
- 04:08-06:32：演示用快捷面板创建项目任务列表、成果、输入和输出，并把新建笔记插入当前任务列表。
- 06:32-07:12：新建笔记会自动带项目属性，成果还会带状态属性。
- 07:12-08:10：演示日期型任务列表：昨天未完成的输入和成果任务自动带到今天，并从昨天列表移除。
- 08:10-08:56：通过上一个 / 下一个文件箭头在日期任务列表之间快速回顾。
- 08:56-10:57：演示创建新项目，添加额外成果类型，再在项目任务列表里创建对应成果。
- 10:57-12:01：快捷面板可以调位置、样式、颜色，服务快速创建。
- 12:01-13:01：作者解释设计取向：任务列表是每天工作的中枢平台，不要复杂控制面板，越简单越好。
- 13:01-14:06：提到官网可了解理念和动态交互；说明 IOTO 是付费产品。

## 视频里直接说了什么

- 输入主要存放下载来的资料，也就是别人给你的知识。
- 输出是你的思考，不是给别人看的，而是给自己看的。
- 成果是给别人看的交付物，比如文章、视频、总结。
- 任务文件夹通过项目管理方式管理项目下的任务列表。
- 任务和成果下面的项目是一一对应的。
- 正常第一步是为某个项目创建任务列表，然后在任务列表中规划要做什么。
- 日期型任务列表可以把未完成任务带到今天。
- 快捷面板用于快速创建输入、输出、任务和成果。
- 作者偏好简单工作中枢，而不是复杂控制面板。

## 我的理解 / 推断

这套逻辑的关键是把“知识生产”拆成三个标准不同的层：

```text
输入:
  外部材料，标准是来源清楚、能被找回。

输出:
  自己的中间思考，标准是自己未来能看懂。

成果:
  对外交付物，标准是别人能看懂，并符合外部规范。
```

任务层不是知识层，而是推进层：

```text
项目
-> 今天的任务列表
-> 从任务里创建输入 / 输出 / 成果
-> 自动挂项目属性
-> 未完成项滚到下一天
-> 用相邻日期回顾推进轨迹
```

所以 IOTO 的设计重点不是分类本身，而是让知识从“资料”走到“思考”，再走到“交付”，中间用项目任务把动作压住。

## 反漏提取检查

```text
pain point:
  - Obsidian 资料、思考、任务和交付物混在一起后，用户不知道今天该推进什么，也分不清自己笔记和对外交付。

workflow:
  - 以项目为容器。
  - 先创建日期型任务列表。
  - 从任务列表中创建输入、输出和成果。
  - 新建笔记自动带项目属性，成果带状态属性。
  - 昨天未完成任务滚到今天。
  - 用相邻日期导航回顾项目推进。

tools / plugins:
  - Obsidian vault。
  - IOTO 快捷面板、脚本、模板、项目创建命令。
  - 视频没有开放脚本或模板细节。

information structure:
  - 辅助文件夹存核心文件、脚本、模板、帮助文件。
  - 输入 / 输出 / 任务 / 成果是核心一级结构。
  - 任务和成果按项目对应。
  - 成果类型可配置，例如文章、总结、报告、周报。

judgment mechanism:
  - 视频没有提供证据审查、事实校验、冲突处理或 truth confidence。
  - 它提供的是生产流程和项目推进逻辑，不是知识可靠性机制。

user experience:
  - 快捷面板降低创建摩擦。
  - 日期任务列表让每天工作可回到一个中枢。
  - 简洁模式 / 单色模式 / 面板位置调整用于减少干扰。

automation boundary:
  - 自动创建文件、插入链接、附加属性、迁移未完成任务。
  - 这些自动化只服务 workflow，不产生 reviewed knowledge。

risk:
  - 容易把文件夹结构误认为知识质量。
  - 自动迁移未完成任务可能隐藏真实停滞原因。
  - 付费产品的具体实现不可直接假设可复制。

fit for us:
  - 对 VAKS 的项目工作台、activation surface、context pack 执行面板有 P2 参考价值。
  - 特别有用的是“输出给自己 / 成果给别人”的边界。

challenge to us:
  - VAKS 需要比 IOTO 更硬的 raw / candidate / reviewed / action basis 边界。
  - VAKS 的任务推进不能直接改变 truth，也不能把未完成迁移当成进展。
```

## 可抽取 Candidate Points

- VAKS 可以吸收“输入 / 内部输出 / 外部成果”的边界，用来解释 raw source、candidate comprehension 和 publishable/action output 的差异。
- VAKS 可以把项目工作台设计成“今天的中枢”，只显示当前项目的待处理 source、candidate、review、decision/action items。
- VAKS 的 artifact 创建入口可以自动带项目、source_family、review_state、action_basis_allowed 等元数据，降低人工维护成本。
- 未完成任务可以滚动到新的 context pack / daily workbench，但必须记录为 workflow carry-forward，不是知识审查或事实更新。

## 可借鉴

- 借“输入是别人给你的知识，输出是给自己看的思考，成果是给别人看的交付物”这个解释。
- 借“项目 + 日期任务列表”作为工作推进中枢。
- 借“从任务列表直接创建关联 artifact，并自动补元数据”的交互。
- 借“相邻日期任务列表回顾”的轻量复盘方式。
- 借“快捷面板降低摩擦，但 UI 越简单越好”的设计取向。

## 不能直接借鉴

- 不把 IOTO 的文件夹结构直接搬成 VAKS schema。
- 不把内部输出当 reviewed knowledge。
- 不把成果当 action basis；VAKS 的对外交付仍然需要证据和范围检查。
- 不把未完成任务自动迁移当作真实进展。
- 不借付费产品的脚本、模板、UI 细节，除非后续有公开资料和授权边界。
- 不让复杂控制面板进入 VAKS 核心；最多做薄工作台。

## 风险和不确定

- ASR 对 IOTO 名称有反复误听，关键实体已用公开标题/描述校正。
- 视频是产品教程，未展示底层脚本、模板、权限、失败处理或长期维护成本。
- 视频没有证据审查机制，不能支持 VAKS truth/review 设计。
- 作者提到官网有理念和交互内容；本轮没有抓官网，所以这张卡只蒸馏视频本身。

## VAKS 归位

```text
Capture:
  输入层可对应 raw/source capture，但必须保留 provenance。

Understand:
  输出层可对应 candidate comprehension / personal synthesis，允许粗糙，但不能当真。

Review:
  IOTO 视频没有 review 机制；VAKS 仍需 Evidence Packet / Evidence Support Check。

Connect:
  项目属性和链接可帮助聚合相关 source / candidate / review items。

Activation / Context Pack:
  日期型项目任务列表很适合做 current workbench / context pack execution surface。

Decision / Action:
  成果层可启发 VAKS 的 publishable output / action output，但必须通过 action_basis gate。

Use Ledger / Feedback:
  未完成任务滚动、每日回顾和项目推进记录可以进入 Use Ledger / workflow feedback，不改变 truth。
```

## 处理等级

```text
medium
```

升级到 heavy 的条件：

- 准备设计 VAKS 项目工作台 / daily workbench / context pack execution UI。
- 需要打开 IOTO 官网或更多系列视频，确认其理念、脚本、模板和长期使用机制。
- 需要比较 IOTO、PARA、Johnny 学其他 Obsidian 方法论与 VAKS 的边界差异。

## 下一步

- 已进入候选蒸馏。
- 不进入 `wiki/claims`、`wiki/patterns`、`wiki/decisions`。
- 当前建议作为 P2 参考：对 VAKS 的项目推进和工作台设计有用，但不改 VAKS core truth/review 结构。
