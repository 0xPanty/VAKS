---
type: qa
question: "Grok 关于 Obsidian Bases + Properties 是 2026 最优数据库层的判断是否可信？"
asked_at: 2026-05-26
source_urls:
  - https://obsidian.md/help/bases
  - https://obsidian.md/help/bases/syntax
  - https://obsidian.md/help/properties
  - https://obsidian.md/changelog/2025-05-21-desktop-v1.9.0/
  - https://obsidian.md/changelog/2025-08-18-desktop-v1.9.10/
  - https://github.com/blacksmithgu/obsidian-dataview
  - https://github.com/blacksmithgu/datacore
related:
  - wiki/decisions/2026-05-26-obsidian-bases-properties-primary-view-layer.md
  - wiki/decisions/2026-05-26-architecture-layering-v0-1.md
confidence: high
---

# Q&A：Obsidian Bases + Properties 核验

## 结论

Grok 的大方向基本对，但表达有明显营销化。

对本资料库来说，最合理采用方式是：

```text
Obsidian Properties + Bases
  = 主力视图层 / 轻数据库层 / dashboard 层
  != verified truth layer
```

也就是说，它很适合帮我们看、筛、排、改 metadata；但它不负责判断资料真假，也不替代 `claims / patterns / anti-patterns / decisions` 的验证规则。

## 哪些说法成立

- Bases 是 Obsidian 官方核心插件，不是普通社区插件。
- Bases 数据仍然落在本地 Markdown 文件和 YAML Properties 里。
- `.base` 文件用 YAML 描述 filters、formulas、properties、summaries、views。
- 官方支持表格、列表、卡片、地图等 view；社区插件可以继续扩展 view 类型。
- Properties 是机器可读的 metadata 层，适合给 Source、Claim、Pattern、Decision 等节点打结构化标签。
- Dataview 仍然是成熟的大生态插件；GitHub 页面显示约 9k stars。
- Datacore 确实是 Dataview 作者方向上的新一代尝试，强调性能和交互式视图，但文档也明确说当前偏 power user 和 JS/TS 用户。

## 哪些说法要降温

- “2025 年 5 月正式推出”不够精确：Bases 在 2025-05-21 的 1.9.0 Desktop early access 中引入；公开版 1.9.10 在 2025-08-18 发布。
- “Dataview 很多都可以退休”只适合普通表格/筛选场景。复杂计算、内联表达式、DataviewJS、旧模板生态仍然有价值。
- “看板、画廊、地图全都无脑成熟”要拆开看：卡片 view 可做 gallery-like 视图，地图 view 官方存在；Kanban 更像插件/社区扩展方向，不应作为第一阶段核心依赖。
- “生态爆炸”可以作为趋势观察，但不能作为 verified 架构依据。我们只依赖官方核心能力和可读 Markdown/YAML。

## 对我们怎么用

第一阶段：

- 用 Properties 作为所有节点的共享 metadata。
- 用 Bases 做可视化管理页面，比如 Sources、Claims、Patterns、Anti-patterns、Decisions、Outputs。
- 用 Bases 筛选 `verification_status`、`confidence`、`evidence_level`、`next_review`、`source_quality`。

第二阶段：

- 如果 Bases 表达不了复杂派生关系，再用 Dataview。
- 如果需要高度自定义、交互式、性能敏感的 dashboard，再观察 Datacore。

## 反模式

不要因为 Obsidian 插件生态很强，就把插件堆成系统核心。

本资料库的核心仍然是：

```text
raw source
  -> compiled wiki
  -> evidence-backed claim
  -> pattern / anti-pattern
  -> decision
  -> context pack
```

Bases 只是让这些节点更好管理，不是让未验证资料自动变可信。

## 量化标签

- domain: obsidian_database_layer
- layer: view_and_metadata_layer
- maturity: high
- official_support: 5
- data_portability: 5
- usability: 5
- implementation_cost: 1
- verified_truth_value: 1
- integration_fit: 5
- overengineering_risk: 2
- dependency_risk: 2

