---
type: source
record_kind: source_card
status: source-captured
title: "cBrain 公开知识体系脑图"
source_id: cbrain-share-mindmap-2c5da0409d489407
source_uri: cbrain:share-mindmap:2c5da0409d489407
source_url: https://cbrain.site/cbrain/share/mindmap?nodeid=2c5da0409d489407
source_type: interactive-web-mindmap
author: unknown
publisher: cBrain
published_at:
updated_at:
captured_at: "2026-06-08 16:21:53 +08:00"
captured_by: Codex
version_or_commit:
source_integrity:
  source_hash: 9edbc386f9fa354dbe93cd77103f89dd6e2b5f9eabd5f56aff21dd77e9165fb5
  snapshot_hash: e2b453bece44f9ff54cb7d873df2556f898bdccd43701d2b9d8ea2130423d41b
  ingest_state: captured
adapter_ingest:
  adapter_name: public-web-plus-spa-api
  adapter_version: manual-2026-06-08
  capture_method: public share HTML plus public /prod-api/cbrain/map/{nodeid}/3 JSON
  extraction_trace:
    - fetched public share page
    - inspected public frontend chunk for anonymous API path
    - fetched public API JSON without cookies or authentication
  known_limits:
    - interactive SPA UI state and images were not fully rendered or archived
    - author identity and publication date were not independently verified
    - node notes are raw public export text and may include personal opinions or stale links
source_status: active
raw_location: raw/articles/2026-06-08-cbrain-knowledge-system-mindmap-source.md
snapshot_location: raw/articles/2026-06-08-cbrain-knowledge-system-mindmap-source/cbrain-map-type3.json
html_snapshot_location: raw/articles/2026-06-08-cbrain-knowledge-system-mindmap-source/share-page.html
ledger_location: raw/articles/2026-06-08-cbrain-knowledge-system-mindmap-source/acquisition-ledger.json
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
topics:
  - cbrain
  - personal-knowledge-system
  - mindmap
  - knowledge-graph-ui
  - node-note-model
  - public-knowledge-sharing
projects:
  - verified-action-knowledge-system
source_family: productized-personal-knowledge-system
upstream_sources: []
verification_status: unverified
candidate_relation_suggestions: []
tags:
  - raw-article
  - web-source
  - public-mindmap
  - candidate-only
why_saved: see_body_or_legacy_record
---

# 来源记录：cBrain 公开知识体系脑图

## 为什么收录

这是一个公开可访问的 cBrain 个人知识体系分享页。它不是论文、不是代码仓库，也不是 VAKS 的证据来源；它的价值在于展示一个个人知识系统如何把知识节点、节点笔记、脑图导航、统计和多种可视化做成公开产品界面。

对 VAKS 来说，这个来源适合作为外层展示、activation surface、节点工作台和知识体系产品化的参考来源，不适合作为 truth / evidence / review 机制的来源。

## 来源信息

- 发布方：cBrain
- 原始链接：https://cbrain.site/cbrain/share/mindmap?nodeid=2c5da0409d489407
- 根节点：`c知识体系`
- 节点 ID：`2c5da0409d489407`
- 采集方式：公开 HTML 分享页 + 公开 SPA API JSON。
- 认证边界：未使用 cookies、私有账号、浏览器登录态或会员内容。
- HTML 快照：`raw/articles/2026-06-08-cbrain-knowledge-system-mindmap-source/share-page.html`
- API 快照：`raw/articles/2026-06-08-cbrain-knowledge-system-mindmap-source/cbrain-map-type3.json`
- 采集 ledger：`raw/articles/2026-06-08-cbrain-knowledge-system-mindmap-source/acquisition-ledger.json`

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

这个 source card 只记录来源、采集方式、快照位置和初步可看点。它不创建 reviewed knowledge，不创建 reviewed relation，不给 VAKS 做采用决策，也不能作为行动依据。

## 采集摘要

公开分享页是一个 SPA。前端 chunk 显示 `/cbrain/share/mindmap` 允许匿名访问，脑图组件通过：

```text
GET /prod-api/cbrain/map/{nodeId}/{type}
```

读取脑图数据。本次对节点 `2c5da0409d489407` 使用 `type=3` 抓取公开 JSON 快照。

快照中的粗略结构：

- `mapInfo`: 243 条脑图节点记录。
- `nodeInfo`: 274 条节点详情记录。
- 有笔记内容的节点：273 条。
- 节点笔记总字符数：约 320701。
- 顶层分支包括：`0 底层智慧`、`1 人文艺术`、`2 科学知识`、`3 信息技术`、`4 实践体系`、`5 资源管理`。

## 初步看点

- 将一个个人知识体系做成公开分享页，而不是只放在本地 vault。
- 同一套节点数据可以切换为脑图、旭日图、树状图、矩阵树图和关系图。
- 节点结构与节点详情分离：`mapInfo` 更像导航层，`nodeInfo` 更像节点笔记层。
- 每个节点可钻取、返回、搜索、查看节点信息和统计。
- 节点包含 `kq`、颜色、链接和笔记等字段，可作为 UI 状态和导航线索。

## 明显疑点

- `kq` 的含义和计算方式未独立确认，不能当作质量、置信度或证据强度。
- 公开脑图是个人知识组织结果，不等于可迁移的通用知识 schema。
- 公开 API 暴露的是展示层数据，不说明后端存储、审查、版本、证据或权限机制。
- 节点笔记包含大量个人判断、学习记录和外链，不能直接进入 reviewed knowledge。
- 作者身份、节点更新时间、完整版本历史未从独立来源确认。

## 可抽取 Candidate Points

- VAKS 可借鉴“同一知识底座，多种可视化视图”的外层工作台。
- VAKS 可借鉴“节点导航层”和“节点笔记层”分离，但不能让展示层替代 evidence / review。
- VAKS 可借鉴公开分享页作为 activation / onboarding 入口。
- VAKS 不应借鉴 `kq` 作为真值、置信度或行动依据。

## 当前处理等级

```text
medium
```

升级到 heavy 的条件：

- 准备实现 VAKS 图谱/节点工作台 UI。
- 需要对 cBrain 的后端、开源代码、数据结构或使用方法做独立复核。
- 需要与其他知识图谱/Obsidian 发布系统做横向比较。

## 下一步

- 当前只进入 candidate distillation。
- 不进入 `wiki/claims`、`wiki/patterns`、`wiki/decisions`。
- 如果未来做 VAKS 产品化界面，可重新打开这个 source 做 UI / activation review。
