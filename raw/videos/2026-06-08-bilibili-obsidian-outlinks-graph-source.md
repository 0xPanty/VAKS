---
type: source
record_kind: source_card
status: source-captured
title: "Obsidian9-教你玩转出链/关系图谱"
source_id: bilibili-BV11R7S68EV1
source_uri: bilibili:BV11R7S68EV1
source_url: https://www.bilibili.com/video/BV11R7S68EV1/
source_type: video
platform: bilibili
platform_id: BV11R7S68EV1
author: "慢慢记BetterNote"
publisher: "慢慢记BetterNote"
published_at: "2026-06-08 11:00:00 +08:00"
updated_at:
duration: 305s
captured_at: "2026-06-08 16:43:04 +08:00"
captured_by: Codex
raw_location: raw/videos/2026-06-08-bilibili-obsidian-outlinks-graph-source.md
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
transcript_location: raw/videos/2026-06-08-bilibili-obsidian-outlinks-graph-source/transcript.txt
segments_location: raw/videos/2026-06-08-bilibili-obsidian-outlinks-graph-source/segments.md
transcript_metadata_location: raw/videos/2026-06-08-bilibili-obsidian-outlinks-graph-source/transcript-meta.json
ledger_location: raw/videos/2026-06-08-bilibili-obsidian-outlinks-graph-source/acquisition-ledger.json
media_retention: deleted
source_status: active
topics:
  - obsidian
  - outlinks
  - backlinks
  - graph-view
  - bidirectional-links
  - activation-surface
projects:
  - verified-action-knowledge-system
source_family: obsidian-linking-graph-activation
upstream_sources: []
verification_status: unverified
candidate_relation_suggestions: []
tags:
  - raw-video
  - bilibili
  - candidate-only
why_saved: see_body_or_legacy_record
---

# 视频资料：Obsidian9-教你玩转出链/关系图谱

## 为什么收录

这条视频是一个基础 Obsidian 教程，讲出链、反链、局部关系图和全局关系图。它对 VAKS 的价值不在“新理论”，而在提醒：连接关系最好有一个可视化和可钻取的激活表面，帮助用户发现相关笔记、上下文和未预期的联系。

它不适合作为 VAKS reviewed relation 或 truth confidence 的来源。图谱、出链、反链只能提示“可能有关”，不能证明“已经支持”。

## 来源卡

- 平台：Bilibili
- 原始链接：https://www.bilibili.com/video/BV11R7S68EV1/
- 标题：Obsidian9-教你玩转出链/关系图谱
- UP 主：慢慢记BetterNote
- 发布时间：2026-06-08 11:00:00 +08:00
- 视频时长：305 秒
- 收录时间：2026-06-08 16:43:04 +08:00
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
transcript_quality: medium-low
media_retention: deleted
scratch_cleanup: downloaded public audio deleted after transcript artifacts were saved
project_visible_artifacts: yes
transcript_location: raw/videos/2026-06-08-bilibili-obsidian-outlinks-graph-source/transcript.txt
segments_location: raw/videos/2026-06-08-bilibili-obsidian-outlinks-graph-source/segments.md
transcript_metadata_location: raw/videos/2026-06-08-bilibili-obsidian-outlinks-graph-source/transcript-meta.json
ledger_location: raw/videos/2026-06-08-bilibili-obsidian-outlinks-graph-source/acquisition-ledger.json
```

说明：

```text
字幕 / ASR 是 raw/source text，不是 reviewed evidence。
AI 摘要是 candidate comprehension，不是 truth。
视频无公开字幕；转写使用公开视频音频 + 本地 CUDA ASR。
ASR 对 Obsidian、出链、关系图谱等词有明显误听；关键实体已用视频标题和描述校正。
```

## 人话摘要

视频讲的是 Obsidian 里怎么用出链和反向链接把笔记连起来，再用局部关系图和全局关系图看这些连接。

示例是做一个“周记”笔记，然后用 `[[...]]` 链接每天的日记。当前笔记链接出去的对象是出链；别的笔记引用当前笔记时，会在反向链接面板里显示。最后用关系图查看当前笔记附近的局部网络，或者查看整个库的全局网络。

## 关键实体置信度

```text
confirmed:
  - Bilibili bvid：BV11R7S68EV1。
  - 标题、UP 主、发布时间、时长：来自 Bilibili public view API。
  - 视频描述明确写有 Graph View、Outlinks、Backlinks、双向链接。
  - 无公开字幕：公开 subtitle API 返回 empty。
  - ASR 使用 faster-whisper small / CUDA / float16；未使用 cookies、私有账号或云 ASR。

likely:
  - ASR 中的 "Cdn" 应为 Obsidian。
  - ASR 中的 "初恋" 应为出链。
  - ASR 中的 "UNC-Tokyo" 应为关系图谱 / Graph View。
  - ASR 中的 "sift 点击" 应为 Shift 点击。
  - ASR 中的 "Ctrl 加拼" 应为 Ctrl+P 打开命令面板。

unclear:
  - 画面中的快捷键是否一定是 Ctrl+P，ASR 不能完全确认。
  - 示例笔记日期中 "2号 / 12号" 有 ASR 不稳定。

needs user visual check:
  - 如果要精确记录快捷键、UI 面板名称、示例日期，需要看对应画面。
```

## 时间轴 / 分段

- 00:00-00:45：介绍 Obsidian 笔记关系图谱：节点代表笔记，随时间增长形成网络结构。
- 00:45-01:20：说明用 `[[笔记名]]` 在不同文档间建立链接。
- 01:20-02:18：用周记和日记示例演示出链：当前笔记指向其他笔记，鼠标悬停 / Shift 点击可预览，点击可跳转。
- 02:18-02:59：打开出链面板，查看当前笔记中的出链数量和对象。
- 02:59-03:26：打开反向链接面板，查看哪些笔记引用了当前笔记，并跳转过去。
- 03:36-04:26：通过命令面板打开局部关系图，查看当前笔记与相邻笔记的关联。
- 04:26-05:00：打开全局关系图，查看所有笔记的网络，并用播放展示笔记增长过程。

## 视频里直接说了什么

- Obsidian 的关系图谱可以把笔记展示成节点网络。
- 用 `[[...]]` 可以在文档之间建立链接。
- 出链表示当前笔记链接出去的笔记。
- 反向链接表示哪些笔记引用了当前笔记。
- 局部关系图可以看当前笔记附近的关系。
- 全局关系图可以看整个 vault 的笔记网络和增长过程。

## 我的理解 / 推断

这条视频的核心不是“图谱很酷”，而是一个基础操作闭环：

```text
写笔记
-> 用链接连接相关笔记
-> 用出链看当前笔记主动指向哪里
-> 用反链看哪些上下文主动引用当前笔记
-> 用局部图看当前上下文
-> 用全局图获得整体感
```

对 VAKS 来说，这个闭环可以放在 Activation / Context Pack / Workbench 层，而不能放在 Review / Truth 层。

## 反漏提取检查

```text
pain point:
  - 笔记分散后，用户不知道哪些笔记有关，也不知道某个主题在别处被如何引用。

workflow:
  - 当前笔记中输入 [[...]] 创建链接。
  - 出链面板显示当前笔记链接出去的对象。
  - 反向链接面板显示哪些笔记链接到当前笔记。
  - 局部关系图查看当前笔记附近网络。
  - 全局关系图查看整个库的结构。

tools / plugins:
  - Obsidian core plugin: Outgoing Links / Backlinks / Graph View。
  - 命令面板 / 快捷键。

information structure:
  - 笔记是节点。
  - `[[...]]` 是链接。
  - 出链和反链分别表示两个方向的导航关系。
  - 局部图和全局图是关系视图，不是证据结构。

judgment mechanism:
  - 视频没有提供知识可靠性判断机制。
  - 连接数量、图谱密度、可视化位置都不是质量判断。

user experience:
  - 优点：容易上手，跳转和发现关联快。
  - 局限：关系容易泛滥，图谱大了会变成视觉噪声。

automation boundary:
  - 视频展示的是手动建链和 Obsidian 自动展示反链/图谱。
  - 自动展示关系不等于自动审查关系。

risk:
  - 用户容易把“连上了”误认为“支持了”。
  - 全局图容易让人沉迷结构感，但不解决证据质量。
  - 反链发现的是引用关系，不是因果、支持或事实关系。

fit for us:
  - 可用于 VAKS 的 Connect / Activation / Context Pack UI 参考。
  - 特别适合作为新手解释“为什么链接有用”的 onboarding 素材。

challenge to us:
  - VAKS 的 reviewed relation 边界必须比 Obsidian 普通链接更硬。
  - 如果未来做图谱 UI，必须显示 relation_state，而不是只画线。
```

## 可抽取 Candidate Points

- VAKS 的关系展示可以区分 outlinks / backlinks，让用户知道“我引用了谁”和“谁引用了我”。
- 局部图适合 context activation，全局图适合整体导航，但都不能作为 truth support。
- Graph View 应该显示层级和状态：raw / candidate / reviewed / decision / action basis。
- 反向链接可以触发 review pressure 或 association activation，但不能直接创建 reviewed relation。

## 可借鉴

- `[[...]]` 风格的显式链接对知识导航很有用。
- 出链 / 反链是新手理解知识连接的低门槛解释。
- 局部图比全局图更适合实际工作，因为它服务当前问题。
- 全局图可以用作 onboarding/demo，而不是日常判断工具。

## 不能直接借鉴

- 不要把普通链接当 reviewed relation。
- 不要把图谱密度当知识质量。
- 不要把反链当证据支持。
- 不要让 VAKS 为了图谱好看而鼓励乱连。
- 不要让普通 capture 阶段承担 reviewed relation 的负担。

## 风险和不确定

- ASR 对核心词有误听，虽然标题和视频描述能校正主要实体。
- 视频是基础教程，没有展示复杂 vault 中图谱噪声、链接治理或误连问题。
- 没有讨论证据、审查、版本、冲突或行动依据。

## VAKS 归位

```text
Capture:
  可以允许轻量显式链接，但只作为 candidate association。

Understand:
  出链 / 反链帮助理解当前笔记上下文。

Review:
  不能直接进入 reviewed relation；需要证据支持和人工/流程审查。

Connect:
  可作为 candidate relation discovery 和 association neighborhood。

Activation / Context Pack:
  局部图可用于 context activation；全局图用于导航和 onboarding。

Decision / Action:
  不可作为 action basis。

Use Ledger / Feedback:
  用户可反馈某条链接是否有用，形成 activation/usefulness signal，而不是 truth update。
```

## 处理等级

```text
medium
```

升级到 heavy 的条件：

- 准备设计 VAKS graph viewer / context-pack viewer。
- 准备把普通 Obsidian 链接和 VAKS reviewed relation 做界面区分。
- 需要对出链、反链、局部图的用户误用风险做专项 review。

## 下一步

- 已进入候选蒸馏。
- 不进入 `wiki/claims`、`wiki/patterns`、`wiki/decisions`。
- 当前建议作为 P3 参考：对 onboarding / activation surface 有用，但不改 VAKS core。
