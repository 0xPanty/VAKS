---
type: pattern
status: candidate
created: 2026-05-26
source_libraries:
  - "[[2026-05-26-obsidian-ai-orange-book-source]]"
related_concepts:
  - "[[source-verification-and-trust-model]]"
  - "[[obsidian-ai-integrated-production-system]]"
related_projects:
  - 资料库
adoption_status: candidate
tags:
  - pattern/context-routing
  - pattern/agent-navigation
evidence_count: 4
confidence: high
negative_evidence:
replaces:
superseded_by:
extension_points:
  - vault-index
  - folder-index
  - context-pack-api
---

# 设计模式：CLAUDE.md + index.md Navigation Layer

## 一句话定义

用根级 `CLAUDE.md` 定义操作规则，用各目录 `index.md` 提供局部地图，让 AI 以最少 token 快速理解 vault。

## 解决的问题

资料库变大后，AI 如果每次全量扫描，会慢、贵、容易污染上下文。只有目录没有说明时，AI 不知道每个区域的用途和关键文件。

## 适用场景

- Obsidian vault。
- 多目录知识库。
- 需要新窗口快速恢复上下文。
- 不想一开始上 RAG 的中小型资料库。

## 不适用场景

- 资料极少，目录树足够。
- 资料超大且需要语义召回，必须增加检索层。

## 反例与避坑

- 失败条件：index 不更新。
- 相似反模式：所有说明都塞进一个超长 CLAUDE.md。
- 复杂度风险：每个目录都写复杂规则，维护成本上升。
- 替代方案：根 README + 一个全局 index 起步，逐步拆目录 index。

## 来源证据

- Orange Book 明确提出 `CLAUDE.md + index.md` 完成大部分导航工作。
- Heinrich 文章提出 vault index 让 agent 决定拉取哪些 notes。
- Karpathy 工作流也强调索引文件优先于全量读取。
- 当前资料库已有 handoff 和 knowledge-graph-index，实践上有效。

## 标签与量化

- domain: agent-context
- problem: navigation and context routing
- maturity: emerging
- complexity: low
- problem_fit: 5
- reuse_value: 5
- implementation_cost: 2
- integration_fit: 5
- evidence_strength: 5
- reversibility: 5

## 交叉验证

- 相似来源：Orange Book、Heinrich、Karpathy、当前资料库实践。
- 历史项目影子：用户经常需要新窗口恢复和多项目上下文定位。
- 支持证据：当前 handoff 和 index 已经发挥恢复作用。
- 反例：索引陈旧会误导 AI。

## 最小实现方式

当前资料库新增：

```text
CLAUDE.md 或 VAULT.md：短核心规则
wiki/indexes/vault-index.md：全局节点地图
每个关键目录 index.md：目录用途和重要文件
```

## 项目融合建议

采用。先做轻量版，不写巨型规则。

## 可拓展性

- 可以通过什么接口/适配层接入：Obsidian Bases、脚本生成、Verified Vault API。
- 未来可能被什么替代：context-pack API / graph resolver。
- 替换或升级成本：低。
- 回退方式：直接读 README + handoff。

## 验证指标

- 新窗口能否快速定位资料。
- AI 是否减少无关文件读取。
- index 是否能持续维护。

