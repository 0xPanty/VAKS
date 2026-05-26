---
type: pattern
status: candidate
created: 2026-05-26
source_libraries:
  - nashsu/llm_wiki
related_concepts:
  - second-brain-knowledge-graph
  - evidence-backed-design-validation
  - source-verification-and-trust-model
related_projects:
  - verified-vault
adoption_status: adapt
tags:
  - knowledge-graph
  - scoring
  - cross-validation
  - high-signal
evidence_count: 4
confidence: high
negative_evidence:
  - algorithmic-graph-scoring-without-source-quality
replaces:
superseded_by:
extension_points:
  - relation scoring script
  - context pack ranking
  - health report metrics
---

# 设计模式：四信号关系图谱评分

## 一句话定义

不要只靠一个 `[[双链]]` 判断知识点关系，而是用多种信号给关系打分：直接链接、共同来源、共同邻居、类型亲和。

## 解决的问题

用户要求“某个点有相似思路或优秀点的影子，我们就交叉验证，确定这条路可行”。四信号评分给这个要求一个可计算框架，避免只凭感觉说“有关联”。

## 适用场景

- 资料库中已有足够 pattern、claim、source、anti-pattern。
- 需要找高信号方向。
- 需要给 Agent 返回更可靠的 context pack。
- 需要知道哪些库在验证同一条设计路线。

## 不适用场景

- 资料很少，直接人工阅读更快。
- 元数据不稳定，`sources[]`、`type`、双链都没维护好。
- 链接主要由 AI 胡乱生成，没有人工 review。

## 反例与避坑

- 失败条件：source metadata 错误会让 source overlap 分数虚高。
- 相似反模式：为了图谱好看乱加链接。
- 复杂度风险：一开始就调复杂算法，忽略资料质量。
- 替代方案：先用手工标签 + 简单 sources overlap。

## 来源证据

`nashsu/llm_wiki` 的 `src/lib/graph-relevance.ts` 中实现了四类分数：

- direct link: 3.0
- source overlap: 4.0
- Adamic-Adar common neighbor: 1.5
- type affinity: 1.0

其中 source overlap 权重大于 direct link，这对我们很重要：同一来源支持的设计关系，比随手写的链接更接近“可验证证据”。

## 标签与量化

- domain: knowledge_graph
- problem: relation_validation
- maturity: emerging
- complexity: medium
- problem_fit: 5
- reuse_value: 5
- implementation_cost: 3
- integration_fit: 5
- evidence_strength: 5
- reversibility: 4

## 交叉验证

- 相似来源：Karpathy 的 backlinks / concepts，Heinrich 的 wiki links，Orange Book 的双链关系层。
- 历史项目影子：用户要求“标签量化 + 交叉验证 + 统一设计前采纳”。
- 支持证据：该 repo 有实际代码，不只是文章说法。
- 反例：图谱分数不能替代人工判断和真实项目验证。

## 最小实现方式

先不做可视化。写一个脚本扫描 `wiki/**/*.md`：

1. 读取 frontmatter 的 `type` 和 `sources`。
2. 解析 `[[wikilinks]]`。
3. 计算节点关系分数。
4. 输出 `outputs/health/relation-scores-YYYY-MM-DD.md`。

## 项目融合建议

作为“高信号指标”的第一版评分标准。后续所有库分析都可以把相似模式连接到同一 pattern，再用关系分数看哪个方向被多源验证。

## 可拓展性

- 可以通过什么接口/适配层接入：health script、Agent API、context pack resolver。
- 未来可能被什么替代：图数据库、embedding + graph hybrid ranking。
- 替换或升级成本：中低。
- 回退方式：保留原始 Markdown，删除评分输出即可。

## 验证指标

- 高分关系是否能帮助我们更快发现可融合设计。
- 低分但人工认为重要的关系是否暴露算法盲区。
- 高分方向落地后是否更少踩坑。
