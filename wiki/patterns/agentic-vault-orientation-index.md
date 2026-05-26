---
type: pattern
status: candidate
created: 2026-05-26
source_libraries:
  - "[[2026-01-thinking-os-with-ai-vault-source]]"
related_concepts:
  - "[[obsidian-ai-integrated-production-system]]"
  - "[[source-verification-and-trust-model]]"
related_projects:
  - 资料库
adoption_status: candidate
tags:
  - pattern/context-routing
  - pattern/agent-orientation
evidence_count: 2
confidence: medium
negative_evidence:
replaces:
superseded_by:
extension_points:
---

# 设计模式：Agentic Vault Orientation Index

## 一句话定义

用一个轻量 vault index 帮 AI 先理解资料库结构，再按需读取相关笔记，而不是全量扫描 vault。

## 解决的问题

当资料库变大后，AI 不可能每次读完所有文件。没有索引时，AI 容易漏掉相关资料，或者把无关上下文塞满窗口。

## 适用场景

- Obsidian vault。
- 多项目资料库。
- AI 需要跨 notes 查找上下文。
- 笔记数量开始增长，但还没到必须上 RAG 的阶段。

## 不适用场景

- 资料极少，直接读目录即可。
- 资料强结构化且已有数据库查询层。
- 需要语义召回大规模内容时，可能需要 RAG 或全文搜索辅助。

## 反例与避坑

- 失败条件：index 不维护，变成过期地图。
- 相似反模式：每次把整个 vault 交给 AI。
- 复杂度风险：为 index 写太多格式规则，反而难维护。
- 替代方案：小规模用目录树，中规模用 index，大规模再考虑检索系统。

## 来源证据

- 本文提出 vault index：每条 note 一句描述，让 agent 快速决定读什么。
- Karpathy 工作流也强调先维护索引文件，再让 LLM 读索引定位相关内容。
- Claude Code 官方 memory 文档显示：短索引/入口文件更适合作为启动上下文，详细 topic 文件按需读取。

## 标签与量化

- domain: knowledge-base / agent-context
- problem: context selection
- maturity: emerging
- complexity: low
- problem_fit: 5
- reuse_value: 5
- implementation_cost: 2
- integration_fit: 5
- evidence_strength: 4
- reversibility: 5

## 交叉验证

- 相似来源：Karpathy LLM Knowledge Bases、Claude Code memory docs。
- 历史项目影子：用户长期多项目开发，需要新窗口恢复和上下文定位。
- 支持证据：当前资料库已建立 `wiki/indexes/knowledge-graph-index.md`。
- 反例：index 若不更新，会误导 agent。

## 最小实现方式

维护一个 `wiki/indexes/vault-index.md`：

- 每个核心目录一句说明。
- 每个重要 concept / pattern / claim 一句摘要。
- 标记 source_status / confidence / next_review。

## 项目融合建议

应该采用，但保持轻量。

## 可拓展性

- 可以通过什么接口/适配层接入：Obsidian Bases、Markdown index、后续脚本生成。
- 未来可能被什么替代：RAG、全文检索、图数据库。
- 替换或升级成本：低。
- 回退方式：直接用目录树和手动搜索。

## 验证指标

- 新窗口能否通过 index 在 3 分钟内定位关键资料。
- AI 是否减少无关文件读取。
- 重要节点是否都能从 index 找到入口。

