---
type: qa
status: recorded
created: 2026-05-26
topic:
  - llm_wiki
  - verified-knowledge-system
  - architecture-fusion
related_sources:
  - raw/repos/2026-05-26-llm-wiki-source.md
related_summary:
  - wiki/summaries/2026-05-26-llm-wiki-architecture-review.md
related_decision:
  - wiki/decisions/2026-05-26-llm-wiki-fusion-compatibility.md
confidence: high
---

# 问答记录：llm_wiki 和我们的框架有什么区别

## 问题

我们之前的设计不也是用 AI 提炼吗？和 `llm_wiki` 有什么区别？是否冲突，还是互补？

## 结论

不冲突，是互补。

`llm_wiki` 解决“怎么自动把资料编成 wiki”。  
本资料库解决“编出来的东西哪些可信、哪些值得采用、哪些要避开”。

## 大白话解释

`llm_wiki` 更像：

```text
原始资料 -> AI 整理 -> 生成一个好用的 wiki
```

本资料库更像：

```text
原始资料 -> AI 编译 -> 拆成可验证知识节点 -> 判断能不能相信、能不能采用
```

区别不在是否使用 AI，而在 AI 提炼后的结果被系统当成什么。

## 对比

| 维度 | llm_wiki | 本资料库 |
|---|---|---|
| 核心目标 | 自动生成和维护 Wiki | 建可信知识系统 |
| 知识单位 | source / entity / concept / query / synthesis | source / claim / pattern / anti-pattern / decision / risk |
| AI 角色 | Wiki 维护员 | 知识编译器 + 初筛员 |
| 重点 | 整理、搜索、图谱、调用 | 可信度、证据、反例、风险、采纳 |
| 图谱意义 | 页面之间有什么关系 | 关系背后的 claim 是否被多源验证 |
| Review | 冲突、缺页、重复时让人看 | 重要结论进入设计前必须验证 |
| 终局 | 自动生长的个人 Wiki App | Agent 和项目可调用的 verified knowledge graph |

## 融合方式

合理分工：

```text
raw/sources
  可参考 llm_wiki 的导入、watch、cache、queue。

wiki/
  可参考 llm_wiki 的 source / concept / entity / synthesis / index / overview。

claims / patterns / anti-patterns
  必须用本资料库的 verified schema 加严。

decisions/
  仍由本资料库的采纳逻辑控制。

API / context pack
  可参考 llm_wiki 的 local API，但输出必须带 evidence / confidence / risk / negative_evidence。
```

## 风险

- 直接迁移会把本资料库的可信判断层压扁成普通 wiki。
- 直接照搬图谱分数会放大低质量来源。
- 过早 fork 做完整 App，会让还没稳定的 Markdown 契约被 UI 锁死。
- 向量搜索、Louvain、图谱 UI 都属于增强层，不是真值层。

## 当前采用判断

- 直接替代：否。
- 作为辅助工具：可以。
- fork 打磨：中期可行。
- 立即吸收设计：是。

最小吸收点：

- `purpose.md`
- `schema.md`
- two-step ingest
- `index.md / log.md / overview.md`
- `sources[]` 溯源
- review queue
- graph health
- local API / context pack 方向

最终判断：

```text
用它的发动机。
保留我们的真值判断规则。
```
