---
type: pattern
status: candidate
created: 2026-05-26
source_libraries:
  - "[[2026-05-26-obsidian-ai-orange-book-source]]"
related_concepts:
  - "[[second-brain-knowledge-graph]]"
related_projects:
  - 资料库
adoption_status: candidate
tags:
  - pattern/vault-organization
  - pattern/metadata
evidence_count: 3
confidence: high
negative_evidence:
replaces:
superseded_by:
extension_points:
  - bases
  - graph-view
  - verified-vault-api
---

# 设计模式：Lifecycle Folders / Topic Tags / Relationship Links

## 一句话定义

文件夹管生命周期，标签管主题，双链管具体关系，三者分工协作而不是互相替代。

## 解决的问题

如果用文件夹做主题分类，一条笔记经常属于多个主题，放哪都不对。如果只用标签，缺少具体语义关系。如果只用双链，缺少全局筛选维度。

## 适用场景

- Obsidian vault。
- 多项目、多主题、多产出并行。
- 需要 AI 和人共同导航资料。

## 不适用场景

- 极小型资料库，目录和搜索足够。
- 已经有严格数据库模型的系统。

## 反例与避坑

- 失败条件：标签失控、链接泛滥、目录深层嵌套。
- 相似反模式：主题文件夹层层嵌套。
- 复杂度风险：同一概念既当标签又当目录又当链接，语义混乱。
- 替代方案：先定义三者职责。

## 来源证据

- Orange Book 明确提出：文件夹管生命周期，标签管主题，双链管关系。
- Heinrich 文章强调链接织进句子，关系网络才是知识。
- 我们当前资料库已经按 raw/wiki/outputs/products 分生命周期，并用 links 连接 concepts/patterns/claims。

## 标签与量化

- domain: vault-architecture
- problem: organization semantics
- maturity: proven
- complexity: low
- problem_fit: 5
- reuse_value: 5
- implementation_cost: 2
- integration_fit: 5
- evidence_strength: 4
- reversibility: 4

## 交叉验证

- 相似来源：Orange Book、Heinrich、Obsidian 双链使用模式。
- 历史项目影子：用户需要多项目开发和 AI短剧素材同时管理。
- 支持证据：当前目录已经体现生命周期和节点类型。
- 反例：标签体系如果不克制，会回到混乱。

## 最小实现方式

当前资料库采用：

```text
folders = lifecycle / node type
tags = topics / domains / status
links = semantic relationship
properties = structured query fields
```

## 项目融合建议

采用。并补一条：Properties/Bases 管结构化筛选。

## 可拓展性

- 可以通过什么接口/适配层接入：Obsidian Tags、Properties、Bases、Graph View、API。
- 未来可能被什么替代：图数据库或 ontology。
- 替换或升级成本：中。
- 回退方式：保留 Markdown links 和 frontmatter。

## 验证指标

- 是否减少“这个资料放哪”的犹豫。
- 是否能通过 tags/Bases 找到跨主题资料。
- 是否能通过 links 找到直接关联。

