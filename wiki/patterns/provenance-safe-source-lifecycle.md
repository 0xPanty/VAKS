---
type: pattern
status: candidate
created: 2026-05-26
source_libraries:
  - nashsu/llm_wiki
related_concepts:
  - source-verification-and-trust-model
  - evidence-backed-design-validation
  - evolvable-design-system
related_projects:
  - verified-vault
adoption_status: adapt
tags:
  - provenance
  - source-lifecycle
  - incremental-compile
  - stale-claims
evidence_count: 3
confidence: high
negative_evidence:
  - algorithmic-graph-scoring-without-source-quality
replaces:
superseded_by:
extension_points:
  - source watch
  - stale claim invalidation
  - deletion cleanup
---

# 设计模式：来源安全的资料生命周期

## 一句话定义

每条原始资料从新增、修改、删除到影响哪些摘要、概念、主张，都要能追踪和清理，避免旧资料留下过期结论。

## 解决的问题

资料库长期运行后，最大风险不是“没资料”，而是旧资料被更新、删除或证伪后，wiki 里的结论还在。来源生命周期让知识库可维护，而不是只增不减。

## 适用场景

- 技术库、政策、市场、产品信息会变化。
- 多篇来源共同支持一个 claim。
- 需要撤销某个 source 对知识图谱的影响。

## 不适用场景

- 一次性静态阅读资料。
- 不做长期可靠知识，只做临时搜索。

## 反例与避坑

- 失败条件：文件重命名或 source id 冲突导致误删结论。
- 相似反模式：只 append，不 invalidate。
- 复杂度风险：自动删除生成文件过于激进。
- 替代方案：先标记 stale / deprecated，不自动删除。

## 来源证据

`nashsu/llm_wiki` README 描述 `raw/sources/` auto-watch、新增/编辑/删除进入同一 ingest/delete lifecycle，并用 SHA256 incremental cache 跳过未变化文件。API 也有 `sources/rescan`。

## 标签与量化

- domain: knowledge_maintenance
- problem: stale_knowledge
- maturity: emerging
- complexity: medium
- problem_fit: 5
- reuse_value: 5
- implementation_cost: 3
- integration_fit: 4
- evidence_strength: 5
- reversibility: 3

## 交叉验证

- 相似来源：Karpathy incremental compile。
- 历史项目影子：用户要求以后新思路可以替换旧思路，且要记录不可行和踩坑。
- 支持证据：`llm_wiki` 已把 source rescan 做成 API。
- 反例：自动删除如果没有人工确认，会误伤共享概念。

## 最小实现方式

每个 source 记录一个稳定 id，并在所有 summary / concept / claim 的 `sources` 里引用。删除或更新 source 时：

1. 找出引用它的所有节点。
2. 如果节点只有这个 source 支持，标记 `stale`。
3. 如果节点还有其他 source 支持，降低 evidence_count 并复查 confidence。
4. 不自动删除，先进入 review。

## 项目融合建议

采用轻量版。先做 source id 和 stale 标记，不急着做自动 watch。

## 可拓展性

- 可以通过什么接口/适配层接入：source index、health report、Agent API source rescan。
- 未来可能被什么替代：数据库级 source dependency graph。
- 替换或升级成本：中。
- 回退方式：保留历史 Markdown 和 git diff。

## 验证指标

- 更新 source 后，相关 claim 是否能被定位。
- 删除 source 后，失去证据的结论是否被标记。
- 新证据出现后，旧 claim 的 confidence 是否会变化。
