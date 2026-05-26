---
type: concept
status: active
created: 2026-05-26
aliases:
  - 负面证据
  - 踩坑记录
  - 反模式
  - avoid list
related:
  - "[[evidence-backed-design-validation]]"
  - "[[positive-design-fusion]]"
  - "[[staged-design-harvest-and-synthesis]]"
---

# 负面证据与避坑机制

## 定义

资料库不仅记录优秀设计点，也要记录不可行路线、踩坑、反例和反模式。

负面证据的价值是帮助后续统一设计时避开错误路线，避免重复踩坑，避免把看起来高级但不适合当前系统的东西硬塞进来。

## 记录对象

- 明确不可行的设计。
- 成本过高但收益不明确的设计。
- 在多个项目或库中被证明容易失败的模式。
- 和当前系统边界冲突的方案。
- 只能在特定规模或特定组织条件下成立的方案。
- 用户历史项目中已经踩过的坑。

## 标签维度

每个负面设计点至少尽量标记：

- `domain`：所属领域。
- `failure_mode`：失败模式。
- `severity`：严重度，1 到 5。
- `likelihood`：发生概率，1 到 5。
- `complexity_cost`：复杂度代价，1 到 5。
- `avoid_reason`：为什么应该避开。
- `trigger_condition`：什么条件下会失败。
- `cross_validated_with`：哪些库、论文、项目或历史经验也证明了类似问题。
- `replacement`：更稳的替代方案。
- `status`：`avoid` / `watch` / `limited-use` / `retest-later`。

## 交叉验证

负面结论也要交叉验证，不能只凭一次失败就永久否定。

更可靠的负面证据通常来自：

- 多个优秀库都没有采用，或明确避开。
- 成熟项目 issue / postmortem / migration note 中反复出现。
- 用户历史项目中出现过相似失败。
- 小实验显示收益不成立或成本过高。
- 需要的前置条件当前不具备。

## 使用方式

后续统一设计时，不只看 `candidate` 和 `adopt`，也要查 `avoid` 和 `limited-use`。

每个落地方案都应该回答：

- 有没有相关反模式？
- 这条路线以前为什么失败？
- 当前条件是否已经改变？
- 是否存在更轻的替代方案？
- 如果仍然采用，如何限制范围和回退？

## 原则

科学采纳不是只收集正面证据，而是同时维护正面证据、负面证据、边界条件和验证结果。

