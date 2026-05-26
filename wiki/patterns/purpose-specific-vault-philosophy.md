---
type: pattern
status: candidate
created: 2026-05-26
source_libraries:
  - "[[2026-01-thinking-os-with-ai-vault-source]]"
related_concepts:
  - "[[evolvable-design-system]]"
  - "[[positive-design-fusion]]"
related_projects:
  - 资料库
adoption_status: candidate
tags:
  - pattern/vault-philosophy
  - pattern/system-instructions
evidence_count: 2
confidence: medium
negative_evidence:
replaces:
superseded_by:
extension_points:
---

# 设计模式：Purpose-Specific Vault Philosophy

## 一句话定义

每个 vault 都应该根据自己的用途定义不同的组织原则、质量标准和 AI 协作规则，而不是套用同一套通用 PKM 模板。

## 解决的问题

工作 vault、研究 vault、创意 vault、内容生产 vault 的目标不同。如果共用一套目录和规则，AI 会按错误标准整理资料。

## 适用场景

- 多用途资料库。
- 开发项目和 AI 短剧并行。
- 需要 AI 按不同业务目标操作不同资料区域。

## 不适用场景

- 只有单一用途的小型 vault。
- 用户还没有形成稳定目标，过早制定 philosophy 可能变成空规则。

## 反例与避坑

- 失败条件：哲学写成口号，没有具体操作规则。
- 相似反模式：所有 vault 都照搬同一套 PARA/Zettelkasten/内容工厂模板。
- 复杂度风险：规则太多，agent 遵循下降。
- 替代方案：先写 10 条核心原则，后续按错误案例迭代。

## 来源证据

- 本文明确主张 every vault needs its own philosophy。
- Claude Code 官方文档支持用 CLAUDE.md 存项目特定规则和工作流。

## 标签与量化

- domain: knowledge-base / agent-instructions
- problem: purpose alignment
- maturity: emerging
- complexity: medium
- problem_fit: 5
- reuse_value: 5
- implementation_cost: 2
- integration_fit: 5
- evidence_strength: 3
- reversibility: 5

## 交叉验证

- 相似来源：Yanhua 超级大脑文章强调 CLAUDE.md 编码身份、偏好、workflow。
- 历史项目影子：用户多个项目、Misa/Hermes、cybernetic、AI短剧需求不同。
- 支持证据：当前资料库已开始区分开发、短剧、来源、设计采样。
- 反例：过度规训会降低灵活性。

## 最小实现方式

在资料库根目录写一个短版 `CLAUDE.md` 或 `AGENTS.md` 风格说明：

- 这个 vault 的目标。
- 文件分层。
- 资料可信度规则。
- AI 写入规则。
- 什么情况下只读，什么情况下落盘。

## 项目融合建议

应该采用，但先轻量，不写 2000 行。

## 可拓展性

- 可以通过什么接口/适配层接入：根目录说明文件 + 子目录局部规则。
- 未来可能被什么替代：更细的 rules/skills/automation。
- 替换或升级成本：低。
- 回退方式：保留基础 README + handoff。

## 验证指标

- 新窗口是否能按资料库目的工作。
- AI 是否减少误分类和过度设计。
- 用户是否需要反复纠正规则。

