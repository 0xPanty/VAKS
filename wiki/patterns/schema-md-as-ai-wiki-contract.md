---
type: pattern
status: candidate
created: 2026-05-26
source_libraries:
  - "[[2026-05-26-obsidian-ai-orange-book-source]]"
related_concepts:
  - "[[source-verification-and-trust-model]]"
  - "[[evidence-backed-design-validation]]"
related_projects:
  - 资料库
adoption_status: candidate
tags:
  - pattern/schema
  - pattern/wiki-contract
evidence_count: 3
confidence: high
negative_evidence:
replaces:
superseded_by:
extension_points:
  - source-schema
  - claim-schema
  - pattern-schema
  - anti-pattern-schema
---

# 设计模式：SCHEMA.md as AI Wiki Contract

## 一句话定义

用 `SCHEMA.md` 明确定义 wiki 条目的命名、字段、标签、链接和文章结构，让 AI 按稳定规则维护知识库。

## 解决的问题

通用 AI 每次整理资料的格式可能不同，导致 tags 混乱、命名不一致、链接规则不稳定。`SCHEMA.md` 把隐性规范显性化。

## 适用场景

- AI 维护 `wiki/`。
- 需要 concepts/entities/topics/claims/patterns 等不同节点类型。
- 多次增量编译，必须保持格式一致。

## 不适用场景

- 还没开始积累资料，过早写复杂 schema。
- 原始资料区 raw，不应被强行 schema 化。

## 反例与避坑

- 失败条件：schema 太复杂，AI 每次都要读大量规则。
- 相似反模式：没有 schema，只靠口头约定。
- 复杂度风险：schema 过细导致写入摩擦。
- 替代方案：先从短 schema 起步，按错误案例扩展。

## 来源证据

- Orange Book 明确用 `SCHEMA.md` 定义命名、frontmatter、标签、wikilink、文章结构、全局索引。
- 我们当前已有模板体系，但还没有统一 schema 文件。
- Claude/agent 工作流通常更依赖显性规则而非隐性习惯。

## 标签与量化

- domain: knowledge-governance
- problem: consistency
- maturity: emerging
- complexity: medium
- problem_fit: 5
- reuse_value: 5
- implementation_cost: 3
- integration_fit: 5
- evidence_strength: 4
- reversibility: 5

## 交叉验证

- 相似来源：Orange Book、Yanhua CLAUDE.md 工作流、当前模板体系。
- 历史项目影子：用户要求来源验证、标签量化、反模式记录。
- 支持证据：当前资料库已有 source/claim/pattern/anti-pattern 模板。
- 反例：过度 schema 会降低采集速度。

## 最小实现方式

建立 `SCHEMA.md`，先只定义：

- 节点类型。
- 必填 metadata。
- 命名规范。
- 链接规则。
- 可信度字段。
- index 更新规则。

## 项目融合建议

采用，但我们要比 Orange Book 更强：加入 source verification、confidence、negative evidence、review fields。

## 可拓展性

- 可以通过什么接口/适配层接入：Obsidian Bases、模板、Skills、Verified Vault API。
- 未来可能被什么替代：JSON Schema / schema validator。
- 替换或升级成本：中。
- 回退方式：保留 Markdown 模板。

## 验证指标

- 新增节点格式是否稳定。
- AI 是否减少命名和标签漂移。
- Bases/API 是否能稳定读取字段。

