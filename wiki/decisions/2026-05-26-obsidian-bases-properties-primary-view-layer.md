---
type: decision
status: active
created: 2026-05-26
decision_scope:
  - obsidian-database-layer
  - verified-vault
  - view-layer
source_urls:
  - https://obsidian.md/help/bases
  - https://obsidian.md/help/bases/syntax
  - https://obsidian.md/help/properties
  - https://obsidian.md/changelog/2025-05-21-desktop-v1.9.0/
  - https://obsidian.md/changelog/2025-08-18-desktop-v1.9.10/
related_outputs:
  - outputs/qa/2026-05-26-obsidian-bases-properties-layer-check.md
confidence: high
---

# 决策：Properties + Bases 作为主力视图层

## 当前决策

采用 Obsidian 原生 Properties + Bases 作为本资料库第一阶段主力视图层和轻数据库层。

不把 Bases 当成验证层、知识编译器、RAG、图数据库或最终真相来源。

## 它在架构里的位置

```text
raw/
  -> wiki/
  -> claims / patterns / anti-patterns / decisions
  -> Obsidian Properties + Bases 负责展示、筛选、排序、复查
  -> future API / context pack
```

Bases 的职责是让结构化节点可管理：

- 哪些 source 还没验证。
- 哪些 claim 置信度低。
- 哪些 pattern 有多源支持。
- 哪些 anti-pattern 需要复查。
- 哪些 decision 已采用、暂停或废弃。

## 为什么采用

- 官方核心插件，生命周期比普通社区插件更稳。
- 数据仍在 Markdown + YAML Properties 中，Git 友好、可迁移。
- `.base` 文件本身也是 YAML，可读、可 diff、可让 AI 理解。
- 对多项目资料、来源、主张、模式、决策的表格化管理很合适。
- 上手成本低，不需要一开始写 Dataview 查询。

## 保留 Dataview / Datacore 的位置

Dataview：

- 适合复杂查询、内联表达式、DataviewJS、已有社区模板。
- 不作为第一阶段默认入口。

Datacore：

- 适合未来交互式高性能 dashboard。
- 当前仍偏 power user / JS/TS，不作为核心依赖。

## 第一批建议 Bases

- `sources.base`：来源质量、采集时间、验证状态、下次复查。
- `claims.base`：主张、证据等级、置信度、反例、来源数量。
- `patterns.base`：可复用模式、适配层、采用状态、风险。
- `anti-patterns.base`：失败条件、替代方案、避免规则。
- `decisions.base`：决策状态、影响范围、回退方式、复查日期。

## 风险边界

- Properties 不适合塞长文本、嵌套对象和复杂 Markdown。
- Bases 视图能帮助管理 metadata，但不会自动提升知识可信度。
- 社区插件可以补能力，但第一阶段不要依赖过多插件组合。
- 任何从 Bases 看到的结论，都必须能回溯到 source / claim / pattern / decision 文件。

## 采纳状态

当前状态：采用为第一阶段主力视图层。

实施时机：等核心 frontmatter 字段稳定后，再创建 `.base` 文件；不要在字段频繁变化时提前做太多视图。

