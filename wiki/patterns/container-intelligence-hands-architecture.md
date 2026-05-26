---
type: pattern
status: candidate
created: 2026-05-26
source_libraries:
  - "[[2026-05-obsidian-claude-ai-superbrain-content-factory-source]]"
related_concepts:
  - "[[obsidian-ai-integrated-production-system]]"
related_projects:
  - 资料库
  - AI短剧
adoption_status: watch
tags:
  - pattern/architecture-model
  - pattern/mental-model
evidence_count: 1
confidence: medium
negative_evidence:
replaces:
superseded_by:
extension_points:
---

# 设计模式：Container / Intelligence / Hands Architecture

## 一句话定义

把 Obsidian 视为容器，Claude Code + Claudian 视为智能，Skills 视为双手，CLAUDE.md 视为操作手册。

## 解决的问题

很多 AI 知识库方案把工具、知识、规则、执行能力混在一起。这个模型用四层分工帮助判断系统边界。

## 适用场景

- 解释 Obsidian + AI 工作台。
- 设计资料库操作边界。
- 规划 AI 短剧生产系统的模块分层。

## 不适用场景

- 需要严格软件架构建模时，这只是类比，不是完整架构。
- 复杂生产系统还需要权限、队列、状态、测试、发布 gate 等层。

## 反例与避坑

- 失败条件：把类比当成完整设计。
- 相似反模式：只有三层图，没有权限和验证机制。
- 复杂度风险：忽略数据治理和回退。
- 替代方案：把它作为沟通模型，再补可信度、验证、权限、复盘层。

## 来源证据

- Yanhua 文章和配图明确将系统分成 Obsidian 容器、Claude Code + Claudian 智能、Skills 双手、CLAUDE.md 操作手册。

## 标签与量化

- domain: architecture
- problem: mental model
- maturity: emerging
- complexity: low
- problem_fit: 4
- reuse_value: 4
- implementation_cost: 1
- integration_fit: 5
- evidence_strength: 2
- reversibility: 5

## 交叉验证

- 相似来源：Heinrich 的 vault/CLAUDE.md/agent/notes-as-skills。
- 历史项目影子：用户需要把资料库、AI、执行能力、发布成品分清。
- 支持证据：当前资料库已经分 raw/wiki/outputs/products/templates。
- 反例：模型缺少安全和质量 gate。

## 最小实现方式

在资料库设计文档里保留这张分层：

```text
Container: Obsidian / Markdown vault
Intelligence: Claude Code / Codex / Claudian
Hands: Skills / scripts / tools
Manual: README / CLAUDE.md / templates / handoff
Governance: source verification / negative evidence / health checks
```

## 项目融合建议

作为解释和沟通模型采用，不作为完整工程架构。

## 可拓展性

- 可以通过什么接口/适配层接入：技能层、工具层、规则层。
- 未来可能被什么替代：更严谨的生产系统架构图。
- 替换或升级成本：低。
- 回退方式：保留 raw/wiki/outputs 基础结构。

## 验证指标

- 是否帮助快速解释系统。
- 是否避免把知识、工具、发布、规则混成一团。

