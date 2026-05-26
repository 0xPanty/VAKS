---
type: qa
status: captured
asked_at: 2026-05-26
question: "不可行、踩坑、特别不适合的点是否也要打标签、交叉验证，并用于后续统一设计？"
related:
  - "[[negative-evidence-and-avoidance]]"
  - "[[evidence-backed-design-validation]]"
  - "[[staged-design-harvest-and-synthesis]]"
---

# 负面证据与科学采纳

## TL;DR

是。不可行路线、踩坑、反模式和特别不适合当前系统的设计，也要进入资料库。它们和优秀设计点一样，需要标签、量化、交叉验证、失败条件和替代方案。

## 用户要求

当前处于开发阶段。后续会持续看优秀库、提炼设计点，但不能只记录正面设计。

同样重要的是：

- 哪些路线不可行。
- 哪些设计看起来高级但实际会增加负担。
- 哪些坑在历史项目或其他优秀库里已经出现过。
- 哪些方案只适合特定规模，不适合当前阶段。
- 哪些方案需要暂缓，等条件变化后再复测。

## 执行方式

后续记录负面证据时，要尽量包含：

- `domain`：所属领域。
- `failure_mode`：失败模式。
- `severity`：严重度。
- `likelihood`：发生概率。
- `complexity_cost`：复杂度代价。
- `trigger_condition`：什么条件下会失败。
- `cross_validated_with`：相似失败来源。
- `replacement`：替代方案。
- `decision`：avoid / watch / limited-use / retest-later。

## 后续统一设计时的要求

统一设计前，不能只看候选优秀模式，也要主动查询：

- 相关反模式。
- 历史踩坑。
- 已知失败边界。
- 替代方案。
- 回退方式。

## 原则

科学合理的应用采纳 = 正面证据 + 负面证据 + 交叉验证 + 最小实验 + 统一设计。

最终目标不是堆叠优秀点，而是形成一套经过验证、知道边界、可落地、可回退的自己的系统。

