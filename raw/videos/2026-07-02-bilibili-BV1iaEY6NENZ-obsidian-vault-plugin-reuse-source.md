---
type: source
record_kind: source_card
status: source-captured
title: Obsidian新建Vault，插件又得重新安装？用这两个方法轻松解决
source_id: bilibili-BV1iaEY6NENZ
source_uri: bilibili:BV1iaEY6NENZ
source_url: https://www.bilibili.com/video/BV1iaEY6NENZ/
source_type: video
source_identity:
  schema_version: 1
  source_id: bilibili-BV1iaEY6NENZ
  kind: video
  canonical_locator: https://www.bilibili.com/video/BV1iaEY6NENZ/
  identity_profile:
    platform: bilibili
    bvid: BV1iaEY6NENZ
    aid: 116729594255397
    cid: 39028395745
  aliases:
    - kind: provider_object_id
      value: BV1iaEY6NENZ
latest_observed_capture_ref: raw/videos/2026-07-02-bilibili-BV1iaEY6NENZ-obsidian-vault-plugin-reuse-source/source-metadata.json
platform: bilibili
platform_id: BV1iaEY6NENZ
author: Next蔡蔡
publisher: Next蔡蔡
published_at: 2026-06-11 12:31:54 +0800
updated_at:
duration: 276s
captured_at: 2026-07-02
captured_by: Codex
raw_location: raw/videos/2026-07-02-bilibili-BV1iaEY6NENZ-obsidian-vault-plugin-reuse-source/
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
why_saved: Obsidian 多 vault 共享插件与配置的轻量工作流参考。
access_boundary: public_no_cookies
transcript_method: local_asr
transcript_location: raw/videos/2026-07-02-bilibili-BV1iaEY6NENZ-obsidian-vault-plugin-reuse-source/transcript.txt
segments_location: raw/videos/2026-07-02-bilibili-BV1iaEY6NENZ-obsidian-vault-plugin-reuse-source/segments.md
transcript_metadata_location: raw/videos/2026-07-02-bilibili-BV1iaEY6NENZ-obsidian-vault-plugin-reuse-source/transcript-meta.json
ledger_location: raw/videos/2026-07-02-bilibili-BV1iaEY6NENZ-obsidian-vault-plugin-reuse-source/acquisition-ledger.json
media_retention: deleted
source_status: captured
topics:
  - obsidian
  - vault-configuration
  - plugin-management
  - symlink
projects:
  - VAKS
source_family: obsidian-workflow
upstream_sources: []
verification_status: unverified
candidate_relation_suggestions: []
tags:
  - video-source
  - bilibili
  - obsidian
---

# 视频资料：Obsidian新建Vault，插件又得重新安装？用这两个方法轻松解决

## 为什么收录

这个视频给出一个很小但实用的 Obsidian 多库配置复用问题：新建 vault 后插件、主题、快捷键等配置默认不共享。它对 VAKS 的价值不在 truth core，而在工程/操作层的轻量工作流参考：如何把“笔记内容”和“工具配置”分开管理。

## 来源卡

- 平台：Bilibili
- 原始链接：https://www.bilibili.com/video/BV1iaEY6NENZ/
- 标题：Obsidian新建Vault，插件又得重新安装？用这两个方法轻松解决
- 作者 / UP 主：Next蔡蔡
- 发布时间：2026-06-11 12:31:54 +0800
- 视频时长：276 秒
- 收录时间：2026-07-02
- 访问边界：public_no_cookies

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
subtitle_status: no_public_subtitle_found
transcript_method: local_asr
asr_engine: faster-whisper
asr_model: small
asr_device: cuda
transcript_quality: medium
media_retention: deleted
scratch_cleanup: media_deleted_by_helper
project_visible_artifacts: yes
transcript_metadata_location: raw/videos/2026-07-02-bilibili-BV1iaEY6NENZ-obsidian-vault-plugin-reuse-source/transcript-meta.json
ledger_location: raw/videos/2026-07-02-bilibili-BV1iaEY6NENZ-obsidian-vault-plugin-reuse-source/acquisition-ledger.json
```

说明：公开视频 API 可访问，未发现公开字幕；随后使用公开视频音频做本地 ASR。未使用 cookie，未使用云 API。ASR 对专名有明显误识别，例如 vault、Symlink、Claude/Cursor 等需要以视频页面描述或人工画面核验为准。

## 保留文本产物

- transcript: `raw/videos/2026-07-02-bilibili-BV1iaEY6NENZ-obsidian-vault-plugin-reuse-source/transcript.txt`
- timestamp segments: `raw/videos/2026-07-02-bilibili-BV1iaEY6NENZ-obsidian-vault-plugin-reuse-source/segments.md`
- segment JSON: `raw/videos/2026-07-02-bilibili-BV1iaEY6NENZ-obsidian-vault-plugin-reuse-source/segments.json`
- transcript metadata: `raw/videos/2026-07-02-bilibili-BV1iaEY6NENZ-obsidian-vault-plugin-reuse-source/transcript-meta.json`
- acquisition ledger: `raw/videos/2026-07-02-bilibili-BV1iaEY6NENZ-obsidian-vault-plugin-reuse-source/acquisition-ledger.json`
- source metadata: `raw/videos/2026-07-02-bilibili-BV1iaEY6NENZ-obsidian-vault-plugin-reuse-source/source-metadata.json`

## Key Entity Confidence

| entity | confidence | basis | note |
|---|---|---|---|
| Obsidian | confirmed | title / description / ASR | 视频主题明确。 |
| vault | confirmed | title / description | ASR 多处误作 Vote。 |
| `.obsidian/plugins` | confirmed | page description / ASR | 页面描述明确写出方法一。 |
| Symlink | confirmed | page description / ASR | 页面描述明确写出方法二；ASR 误作 SimLink。 |
| Junction on Windows | likely | ASR | 页面描述未展开命令，需画面核验具体命令。 |
| Claude Code / Cursor style coding tools | likely | ASR | ASR 有误识别，若用于操作说明需核验画面。 |

## Candidate Routing

- 候选蒸馏：`outputs/review/2026-07-02-bilibili-BV1iaEY6NENZ-obsidian-vault-plugin-reuse-candidate-distillation.md`
- 建议用途：VAKS 工具配置层 / 操作手册参考。
- 不建议用途：不作为 reviewed knowledge、action basis、Obsidian 配置迁移标准。
