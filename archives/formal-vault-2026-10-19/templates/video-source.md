---
type: source
status: source-captured
title:
source_id:
source_uri:
source_url:
source_type: video
platform:
platform_id:
author:
publisher:
published_at:
updated_at:
duration:
captured_at:
captured_by: Codex
raw_location: raw/videos/
processing_mode: inbox
processing_level: light
processing_tier: light
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
transcript_method: none
transcript_location:
segments_location:
transcript_metadata_location:
ledger_location:
media_retention: not_downloaded
source_status: unknown
topics:
projects:
source_family:
upstream_sources: []
verification_status: unverified
candidate_relation_suggestions: []
tags:
---

# 视频资料：

## 为什么收录


## 来源卡

- 平台：
- 原始链接：
- 标题：
- 作者 / UP 主：
- 发布时间：
- 视频时长：
- 收录时间：
- 访问边界：public / authenticated / private / unknown

## Intake Boundary

```yaml
processing_tier: light | medium | heavy
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
subtitle_status:
transcript_method: public_subtitle | local_asr | user_supplied | none
asr_model:
asr_device:
transcript_quality: high | medium | low | unknown
media_retention: deleted | kept | not_downloaded
scratch_cleanup:
project_visible_artifacts: yes | no
transcript_metadata_location:
ledger_location:
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


## 关键实体置信度

```text
confirmed:
  -

likely:
  -

unclear:
  -

needs user visual check:
  -
```

重点检查：

```text
工具名 / 项目名 / 仓库名 / URL / 命令 / 版本号 / star 数 / 平台支持 / UI 文案，不能只靠 ASR 判断。
```

## 时间轴 / 分段


## 视频里直接说了什么


## 我的理解 / 推断


## 反漏提取检查

```text
pain point:
  -

workflow:
  -

tools / plugins:
  -

information structure:
  -

judgment mechanism:
  -

user experience:
  -

automation boundary:
  -

risk:
  -

fit for us:
  -

challenge to us:
  -
```

提取合格线：

```text
如果只写了摘要，但没有写痛点、工作流、工具 / 插件、风险、对我们框架的验证或挑战，这条资料卡不算提取完成。
```

## 可抽取 Candidate Points

- 

## 可借鉴

- 

## 不能直接借鉴

- 

## 风险和不确定

- 

## VAKS 归位

```text
Capture:
Understand:
Review:
Connect:
Activation / Context Pack:
Decision / Action:
Use Ledger / Feedback:
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

升级到 heavy 的条件：

- 

## 下一步
