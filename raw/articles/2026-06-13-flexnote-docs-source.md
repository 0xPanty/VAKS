---
type: source
record_kind: source_card
status: source-captured
title: FlexNote documentation
source_id: web-flexnote-docs-2026-06-13
source_uri: https://wiki.myflexnote.com/docs/intro
source_url: https://wiki.myflexnote.com/docs/intro
source_type: documentation_site
author: unknown
publisher: FlexNote
published_at:
updated_at:
captured_at: 2026-06-13
captured_by: Codex
version_or_commit: docs-as-of-2026-06-13
source_integrity:
  source_hash:
  snapshot_hash: 0F13DFC82AA0B6183CEB6B5645434D4374015D4E121F6F80EB33E02C2FE5B78D
  ingest_state: new
adapter_ingest:
  adapter_name: manual-web-docs-review
  adapter_version: 2026-06-13
  capture_method: public documentation pages opened through web browser tool
  extraction_trace:
    - raw/articles/2026-06-13-flexnote-docs-source/inspected-pages.md
  known_limits:
    - documentation inspected, app not run
    - no source code or storage schema inspected
    - website pages may change after capture
source_status: active
raw_location: raw/articles/2026-06-13-flexnote-docs-source/inspected-pages.md
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
why_saved: User requested distillation of the FlexNote documentation and whether its thinking can be extracted for VAKS.
topics:
  - visual-note-taking
  - infinite-canvas
  - card-system
  - tag-database
  - pdf-video-annotation
  - local-first
  - third-party-sync
projects:
  - VAKS
source_family:
  - visual-pkm
  - local-first-note-app
upstream_sources: []
verification_status: documentation-inspected-not-run
evidence_granularity: excerpt_or_passage
candidate_relation_suggestions:
  - target: "[[scope-dashboard-live-context-surface]]"
    relation_type: refines
    relation_state: candidate
    why_suggested: "FlexNote's whiteboard model is a concrete visual workbench pattern for arranging cards, source excerpts, tasks, and relationships."
    source_anchor: "https://wiki.myflexnote.com/docs/tutorial-basics/whiteboard"
  - target: "[[source-adapter-ingest-contract]]"
    relation_type: refines
    relation_state: candidate
    why_suggested: "FlexNote's PDF/video highlights become cards with source and location metadata, resembling a source-anchor extraction surface."
    source_anchor: "https://wiki.myflexnote.com/docs/tutorial-basics/Highlight"
  - target: "[[derived-relatedness-as-truth-signal]]"
    relation_type: risk_of
    relation_state: candidate
    why_suggested: "Visual arrows, backlinks, tags, and boards can look like knowledge relations, but they are organization/activation signals unless reviewed."
    source_anchor: "https://wiki.myflexnote.com/docs/tutorial-basics/reference"
tags:
  - source-card
  - flexnote
  - documentation-site
  - visual-pkm
  - card-system
  - whiteboard
  - tag-database
  - annotation-to-card
  - candidate-only
---

# 来源记录：FlexNote documentation

## 为什么收录

用户要求蒸馏 `https://wiki.myflexnote.com/docs/intro`，并判断它的思路能不能提炼出来给 VAKS 借鉴。

本记录只保存来源身份、检查范围和候选关系建议。它不是 reviewed knowledge，不是架构决策，也不能作为 action basis。

## 来源信息

- 原始链接：https://wiki.myflexnote.com/docs/intro
- 中文链接：https://wiki.myflexnote.com/zh/docs/intro
- 发布方：FlexNote
- 捕获时间：2026-06-13
- 捕获方式：公开文档页面浏览与相邻教程页检查
- 保留锚点：`raw/articles/2026-06-13-flexnote-docs-source/inspected-pages.md`
- source_status: active

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

Source records provide provenance and findability. They must not carry truth scores, project decisions, reviewed relations, or action basis.

## 时间线 / 上下文

- 文档页版权标识为 2025 FlexNote。
- 本次检查时间为 2026-06-13。
- 文档显示产品支持 Windows/macOS，移动端尚未支持；云同步和 PDF 导出存在 beta/未来计划表述。
- 本次没有运行 app，也没有检查实现源码。

## 初步看点

- FlexNote 的核心不是 AI，而是视觉化知识组织。
- 它把所有内容抽象成可复用卡片：笔记、PDF、视频、网页、图片、音频、附件、标注、脑图节点。
- 它把无限白板作为多视角工作台，让同一张卡片能进入不同上下文。
- 它把标签升级成数据库：字段、过滤、关系、表格/看板/列表视图。
- 它把 PDF/video/web 的材料片段转成卡片，并保留来源和位置线索。
- 它是 local-first，加第三方云同步，而不是自家云强绑定。

## 明显疑点

- 文档级材料不能证明 app 的实现质量。
- 标注自动生成卡片不等于生成可靠知识。
- 视觉箭头和双向链接容易被误认为 reviewed relation。
- tag database 字段容易被误认为 VAKS schema。
- 第三方同步和导入导出需要额外 source integrity / conflict handling，文档说明不足以作为行动依据。

## 可抽取 Candidate Points

1. 卡片作为统一信息原子，比“页面/文件夹”更适合承载多源材料和多视角复用。
2. 白板作为 project workbench / context pack viewer 很有价值，但它只能展示和组织，不定义 truth。
3. 标签数据库可作为 review queue、source queue、project dashboard 的 UI 参考，但不替代 VAKS schema。
4. PDF/video highlights 自动生成 cards 的思路，可转译成 VAKS source anchor / evidence packet 的候选输入。
5. `@` link、backlink、visual arrow 都可以做 activation / navigation，不可直接变成 reviewed relation。
6. Journal 可以作为 daily capture / use ledger / project log 入口，但不直接改 reviewed knowledge。

## 当前处理等级

```text
medium documentation-site intake
```

升级到 heavy 的条件：

- FlexNote 被用于设计 VAKS visual workbench、PDF/video source adapter、review dashboard 或 desktop client。
- 后续找到官方 repo、schema、implementation docs 或真实运行证据。
- 其中某个候选点准备进入 pattern / anti-pattern / decision。

## 下一步

- 读取 candidate distillation 进行方向判断。
- 项目可借与不可借范围写在 project overlay。
- 不从 source card 直接创建 reviewed relation 或 architecture decision。
