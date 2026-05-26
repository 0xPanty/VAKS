---
type: concept
status: active
created: 2026-05-26
aliases:
  - 设计点量化验证
  - 交叉验证
  - 可行性验证
related:
  - "[[staged-design-harvest-and-synthesis]]"
  - "[[library-design-extraction]]"
  - "[[positive-design-fusion]]"
---

# 设计点量化与交叉验证

## 定义

以后记录优秀库、框架、论文、产品或项目经验时，不能只写“这个设计很好”。每个设计点都要被打标签、量化、关联相似证据，并通过交叉验证判断它是否是一条可行路线。

目标是让借鉴变成可验证的工程判断，而不是灵感拼贴。

## 基本流程

```text
发现设计点
  -> 打标签
  -> 量化评分
  -> 寻找相似设计或历史影子
  -> 记录支持证据和反例
  -> 判断可行性
  -> 设计最小验证
  -> 再决定是否进入落地候选
```

## 标签维度

每个设计点至少尽量标记这些维度：

- `domain`：属于哪个领域，如 agent、knowledge-base、workflow、runtime、ui、storage、retrieval。
- `problem`：解决什么问题。
- `pattern`：设计模式，如 plugin-architecture、event-sourcing、incremental-compile、typed-schema。
- `maturity`：成熟度，`experimental` / `emerging` / `proven`。
- `complexity`：复杂度，`low` / `medium` / `high`。
- `fit`：对当前项目适配度，1 到 5。
- `evidence_count`：有多少独立来源支持。
- `risk`：主要风险。
- `validation`：如何验证。

## 量化评分

建议使用 1 到 5 分：

- `problem_fit`：它解决的问题和用户当前目标是否匹配。
- `reuse_value`：未来复用价值有多高。
- `implementation_cost`：实现成本，分数越高代表成本越高。
- `integration_fit`：和现有系统衔接是否自然。
- `evidence_strength`：是否被多个优秀来源或历史项目交叉证明。
- `reversibility`：如果判断错了，是否容易撤回。

最终不要只看总分，要看结构：

- 高收益 + 低成本 + 多来源验证：优先候选。
- 高收益 + 高成本：进入观察或做最小验证。
- 单来源但很有启发：记录，不急着采用。
- 多来源都出现但和当前问题不匹配：保留为概念，不进入落地。

## 交叉验证规则

一个设计点更可信，通常需要满足至少一种：

- 在多个优秀库中独立出现。
- 在用户历史项目中有类似影子或痛点对应。
- 被论文、成熟产品或真实生产系统验证过。
- 能用小实验验证核心收益。
- 有明确失败边界和反例。

## 输出要求

每条重要设计点都应回答：

- 它来自哪里？
- 哪些库或资料出现了相似思想？
- 它和用户历史项目哪个问题对应？
- 它的收益可以怎么测？
- 它的失败条件是什么？
- 当前状态是 `capture`、`candidate`、`validate`、`adopt`、`reject` 还是 `watch`？

## 关键原则

只有能被追溯、交叉验证、最小验证的设计点，才允许进入落地候选。

