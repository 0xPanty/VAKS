---
type: pattern
status: draft
created: 2026-05-26
source_libraries:
  - rafafields/Obsidian-Base-Hub
related_concepts:
  - obsidian-bases-properties-primary-view-layer
related_projects:
  - verified-knowledge-system
adoption_status: adapt
tags:
  - obsidian
  - bases
  - workbench
  - view-layer
evidence_count: 1
confidence: medium
negative_evidence:
  - inconsistent-property-names-in-bases-template
replaces:
superseded_by:
extension_points:
  - source-review-base
  - claim-verification-base
  - decision-review-base
---

# 设计模式：Obsidian Bases linked workbench views

## 一句话定义

用 `.base` 文件把同一类 Markdown 节点筛出来，再把相关视图嵌入根页面，形成轻量复查工作台。

## 解决的问题

Markdown 文件多了以后，人很难知道哪些 source 待摘要、哪些 claim 缺验证、哪些 pattern 等待采用、哪些 decision 需要复查。Bases 可以把这些状态变成可扫视的表格/卡片。

## 适用场景

- schema 字段已经稳定。
- 需要人工复查、筛选、排序、批量补字段。
- Obsidian 是主要阅读和整理入口。

## 不适用场景

- schema 尚未稳定时。
- 需要自动推理、交叉验证或真值判断时。
- 大规模检索和上下文包生成。

## 反例与避坑

- 失败条件：Base 视图反过来决定 schema。
- 相似反模式：把 Bases 当数据库 truth layer。
- 复杂度风险：每个项目/节点复制一个 `.base` 文件，后续字段改动要到处同步。
- 替代方案：先用 Markdown index，等字段稳定后再做少量全局 Base。

## 来源证据

- Obsidian-Base-Hub 的 Project / Area 根页面嵌入 Team、Tasks、Meetings 三个 Base view。
- People / Locations / Daily 示例展示 linked views 和日期过滤。
- Base 文件用 `file.inFolder()`、`contains(link())`、`file.hasLink(this.file.path)`、`date(...).format(...) == this.file.name` 实现低代码视图。

## 标签与量化

- domain: obsidian-view-layer
- problem: review-workbench
- maturity: emerging
- complexity: low
- problem_fit: 4
- reuse_value: 4
- implementation_cost: 2
- integration_fit: 5
- evidence_strength: 3
- reversibility: 5

## 交叉验证

- 相似来源：Obsidian Bases + Properties 作为主力视图层。
- 历史项目影子：用户需要“文件为准，对话为辅”，但还要能快速看到状态。
- 支持证据：`.base` 是本地文件，和 Markdown/Git 兼容。
- 反例：该库字段命名出现 `projects/proyectos`、`role/rol`、`scheduled/agendado` 混用，说明 schema-first 必须先于 view-first。

## 最小实现方式

等 `SCHEMA.md` 稳定后创建：

```text
wiki/bases/sources.base
wiki/bases/claims.base
wiki/bases/patterns.base
wiki/bases/decisions.base
wiki/bases/review-queue.base
```

第一版只做筛选和排序，不做复杂公式。

## 项目融合建议

正向，但属于视图层。先完成 schema 和模板，再让 Bases 提升人工操作效率。

## 验证指标

- 低置信 claim 能被一眼筛出。
- conflicted / needs-review 节点不会被淹没。
- 新 source 能从 inbox/source queue 进入 summary/claim 流程。
- 修改 schema 时只需要更新少量全局 Base。

