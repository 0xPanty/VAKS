---
type: pattern
status: candidate
created: 2026-05-26
source_libraries:
  - nashsu/llm_wiki
related_concepts:
  - purpose-specific-vault-philosophy
  - obsidian-ai-integrated-production-system
  - staged-design-harvest-and-synthesis
related_projects:
  - verified-vault
  - ai-short-drama
adoption_status: adopt-lite
tags:
  - purpose
  - vault-philosophy
  - agent-orientation
evidence_count: 3
confidence: high
negative_evidence:
  - overgrown-always-on-instructions
replaces:
superseded_by:
extension_points:
  - purpose templates per vault
  - project-specific purpose overrides
---

# 设计模式：purpose.md 作为知识库使命层

## 一句话定义

把“这个资料库为什么存在、要回答什么问题、边界在哪里”写进独立的 `purpose.md`，和负责结构规则的 `schema.md` / `CLAUDE.md` 分开。

## 解决的问题

只靠目录结构和 CLAUDE.md，Agent 知道“怎么做”，但不一定知道“为什么这么做”。`purpose.md` 给知识库一个方向盘：同样一篇资料，用于开发项目、AI短剧、内容工厂时，提炼重点是不一样的。

## 适用场景

- 多用途 vault。
- 不同项目需要不同提炼标准。
- Agent 每次启动需要快速理解当前资料库目标。
- 后续希望做 API / context pack，需要把检索结果按目标过滤。

## 不适用场景

- 只有几十条临时资料的小收藏夹。
- 目标还完全没想清楚，写了也只是空话。

## 反例与避坑

- 失败条件：`purpose.md` 写成口号，没有可执行问题和边界。
- 相似反模式：把所有规则都塞进 CLAUDE.md，最后 2000 行没人敢改。
- 复杂度风险：每个子项目都新建目的文件会失控。
- 替代方案：小型阶段可以先在 README 的“当前目标”里维护。

## 来源证据

- `nashsu/llm_wiki` 在 README 中明确把 `purpose.md` 作为新增层，区别于 schema。
- Heinrich 的 thinking vault 强调每个 vault 需要自己的 philosophy。
- 我们已有 `purpose-specific-vault-philosophy` 概念节点。

## 标签与量化

- domain: knowledge_base
- problem: agent_orientation
- maturity: emerging
- complexity: low
- problem_fit: 5
- reuse_value: 5
- implementation_cost: 1
- integration_fit: 5
- evidence_strength: 4
- reversibility: 5

## 交叉验证

- 相似来源：Heinrich vault philosophy、Yanhua CLAUDE.md 身份定义。
- 历史项目影子：用户要求不同阶段的开发理解被保留，并在全貌视角下综合。
- 支持证据：`llm_wiki` 把 `purpose.md` 读入 ingest/query 上下文。
- 反例：目的层如果不更新，会让 Agent 延续旧方向。

## 最小实现方式

在 vault 根目录增加 `purpose.md`，字段包括：

- 当前资料库目标
- 核心问题
- 主要产出
- 不做什么
- 当前阶段优先级
- 复查日期

## 项目融合建议

立刻采用轻量版本。先给当前 `资料库` 写一个总 `purpose.md`，后面再按开发资料、AI短剧资料、内容生产资料拆分。

## 可拓展性

- 可以通过什么接口/适配层接入：Agent 启动读取、context pack、API metadata。
- 未来可能被什么替代：多 vault profile / project config。
- 替换或升级成本：低。
- 回退方式：删掉或改回 README 目标段。

## 验证指标

- Agent 总结资料时是否更稳定地围绕项目目标。
- 同一来源在不同目的下是否能产出不同但合理的摘要。
- 后续健康检查能否发现 purpose 与实际内容偏离。
