---
type: library_review
status: draft
library_name: rafafields/Obsidian-Base-Hub
repo_url: https://github.com/rafafields/Obsidian-Base-Hub
source_url: raw/repos/2026-05-26-obsidian-base-hub-source.md
reviewed_at: 2026-05-26
domain:
  - obsidian
  - bases
  - view-layer
related_projects:
  - verified-knowledge-system
extracted_patterns:
  - obsidian-bases-linked-workbench-views
fusion_decision: adapt
confidence: medium
evidence_count: 1
cross_validated_with:
  - Obsidian Bases + Properties layer decision
negative_evidence:
  - inconsistent-property-names-in-bases-template
extension_potential: medium
---

# 库分析：Obsidian Base Hub

## 它解决什么问题

它解决的是 Obsidian 里“如何像 Notion 一样用数据库视图管理个人项目/任务/会议/人物”。它不是知识验证架构，也不是 AI/RAG/agent 第二大脑。

## 核心设计

```text
folder = 数据集边界
frontmatter properties = 字段
.base = 表格/卡片/筛选/分组视图
root note = 嵌入相关 base 视图的上下文页面
template = 新条目的默认字段
```

## 值得提炼的模式

最有价值的不是它的项目管理分类，而是它的工作台形态：

- Project/Area 根页面嵌入 Team、Tasks、Meetings。
- People 页面嵌入 linked meetings。
- Location 页面嵌入 linked people / linked meetings。
- Daily note 嵌入当天 meetings。
- Base 视图里的 `+ New` 变成结构化入口。

这可以迁移到我们的资料库：

```text
Source dashboard
  -> 待摘要 / 待验证 / 已废弃

Claim dashboard
  -> unverified / single-source / cross-checked / conflicted

Pattern dashboard
  -> watch / adapt / adopted / rejected

Decision dashboard
  -> active / superseded / needs-review
```

## 标签与量化

- domain: obsidian-view-layer
- problem: workbench-navigation
- maturity: emerging
- complexity: low
- problem_fit: 3
- reuse_value: 4
- implementation_cost: 2
- integration_fit: 4
- evidence_strength: 3
- reversibility: 5

## 交叉验证

- 相似设计来源：Obsidian Bases + Properties 主视图层判断。
- 用户历史项目影子：用户希望资料库不是聊天结论，而是可长期查看和复查的文件系统。
- 支持证据：库中实际 `.base` 文件展示了 filters、order、sort、groupBy、embedded views。
- 反例或失败边界：字段命名混乱会让 Base 视图失效或分裂。
- 最小验证方式：等 `SCHEMA.md` 出来后，为 5 类节点各建一个最小 `.base`，只读筛选，不引入复杂自动化。

## 对当前项目的适配点

它补的是“人工复查工作台”，不是“知识可信度内核”。

适配后的形态应该是：

```text
SCHEMA.md 决定字段
templates 决定写入形状
.base 决定查看和复查效率
```

Base 文件不能反过来决定 schema。

## 复杂度和风险

- 直接照搬目录会污染我们已有 raw/wiki/outputs/products 分层。
- 每个项目复制 `.base` 文件会产生维护重复。
- 字段中英文/西语混用是明确风险。
- emoji 状态页面适合个人任务，不适合 verified claim 的长期 schema。

## 融合判断

- 结论：adapt。
- 理由：作为视图工作台有用，作为核心架构不够。
- 验证方式：先不做 `.base`，等 `SCHEMA.md` 和模板稳定后再生成 source/claim/pattern/decision 的 Bases。

## 后续行动

1. 在 `SCHEMA.md` 之后设计 Bases 视图。
2. 只保留 4-6 个全局 `.base`，避免每个节点复制一个 Base。
3. 视图字段必须完全来自 schema 枚举。
4. 第一批视图只做人工复查：待处理 source、低置信 claim、conflicted claim、watch patterns、needs-review decisions。

