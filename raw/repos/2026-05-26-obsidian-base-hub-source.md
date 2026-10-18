---
type: source
record_kind: source_card
status: source-captured
title: rafafields/Obsidian-Base-Hub
source_url: https://github.com/rafafields/Obsidian-Base-Hub
source_type: repo
author: rafafields
publisher: GitHub
published_at:
captured_at: 2026-05-26
captured_by: Codex
topics:
  - obsidian
  - bases
  - project-management
  - view-layer
projects:
  - verified-knowledge-system
evidence_level: primary
source_integrity:
  capture_confidence: 4
source_status: source-captured
verified_by:
  - local-source-read
last_verified: 2026-05-26
next_review:
related_claims:
related_concepts:
  - obsidian-bases-properties-primary-view-layer
tags:
  - repo
  - obsidian-bases
  - view-template
knowledge_status: raw
processing_tier: light
source_id: https://github.com/rafafields/Obsidian-Base-Hub
why_saved: see_body_or_legacy_record
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
legacy_raw_metadata:
  source_quality: 3
  freshness: 4
  relevance: 3
  cross_source_count: 1
---
# 来源记录：rafafields/Obsidian-Base-Hub

## 为什么收录

用户提供 `rafafields/Obsidian-Base-Hub`，要求看看是否有可借鉴之处。该库是 Obsidian 原生 Bases 的完整 vault 模板，和我们之前确定的 “Bases + Properties 是视图层，不是 truth layer” 判断相关。

## 核心内容

这是一个个人项目/任务管理 vault 模板，不是知识验证系统。它用 Obsidian `.base` 文件做 Notion-like 数据库视图，覆盖 Inbox、Projects、Areas、Tasks、Daily、Meetings、People、Locations。

## 来源信息

- 仓库：`https://github.com/rafafields/Obsidian-Base-Hub`
- 当前读取 commit：`ca4c927b42a74c63911aa5aa97d1d0694e6e126b`
- 本地临时目录：`C:\Users\Administrator\AppData\Local\Temp\obsidian_base_hub_probe\Obsidian-Base-Hub`
- 本地源码快照：`raw/repos/_snapshots/Obsidian-Base-Hub-ca4c927b42a74c63911aa5aa97d1d0694e6e126b.zip`
- 采集方式：Git clone 后读取 README、How it works、Changelog、`.base` 文件、templates、示例 notes。

## 已读取重点

- `Readme.md`
- `How it works (with screenshots!).md`
- `Changelog.md`
- `.obsidian/core-plugins.json`
- `.obsidian/types.json`
- `010 - Inbox/DDBB - Inbox.base`
- `020 - Projects/999 - Demo Project/DDBB Demo Project.base`
- `030 - Areas/999 - Demo Area/DDBB Demo Area.base`
- `040 - Tasks/DDBB Tasks.base`
- `050 - Daily/DDBB Daily.base`
- `060 - Meetings/DDBB Meetings.base`
- `070 - People/DDBB People.base`
- `080 - Locations/DDBB Locations.base`
- `999 - Templates/New Task.md`
- `999 - Templates/New Meeting.md`
- `999 - Templates/New People.md`

## 标签与量化

- source_type: repo
- evidence_level: primary
- source_status: source-captured
- source_quality: 3
- freshness: 4
- relevance: 3
- confidence: 4
- cross_source_count: 1

## 已验证内容

- 库里确实包含 Obsidian `.base` 文件和示例 vault，而不是纯 README。
- 它的核心模式是：用文件夹限定数据集，用 properties 作为字段，用 `.base` 视图做筛选/分组/排序，用根页面嵌入局部视图。
- Project / Area 根页面嵌入 Team、Tasks、Meetings 三个 Base 视图。
- Daily note 可嵌入当天会议视图：用 `date(note.scheduled).format("YYYY-MM-DD") == this.file.name` 匹配日记标题。
- Base 视图里的 `+ New` 按钮被当作快速创建入口，减少手动放文件夹和填字段的摩擦。

## 未验证内容

- 没有在 Obsidian GUI 中打开确认所有 `.base` 视图渲染。
- 未验证最新 Obsidian Bases 语法兼容性。
- README 的版本号和 changelog 版本略不一致，未进一步追踪 release。

## 冲突或疑点

- 字段命名有混用：`projects/areas` 与 `proyectos/áreas`，`role/rol`，`scheduled/agendado`，`minutes/minutos`，`guests/invitados` 同时出现。这对我们是反面提醒：schema 字段必须统一。
- 它偏个人项目管理，不是资料验证；不能直接替代 source / claim / pattern / decision。
- 每个 Project / Area 复制一个 `.base` 文件，早期直观，但长期可能产生维护重复。

## 可复用点

- 用 Base 做 lightweight workbench，而不是 truth layer。
- 根页面嵌入局部 Base 视图，形成“一个对象的上下文面板”。
- `+ New` 作为结构化条目入口。
- 用 link properties 连接项目、任务、会议、人物。
- 用状态/优先级页面作为枚举值，方便可视化和过滤。

## 下一步

不采用它的目录结构。等 `SCHEMA.md` 稳定后，借鉴它的 `.base` 工作台模式，为 source review、claim verification、pattern adoption、decision review 建立轻量 Obsidian 视图。

