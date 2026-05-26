---
type: concept
status: active
created: 2026-05-26
aliases:
  - 可拓展设计
  - 可演化系统
  - extensibility
  - evolvable architecture
related:
  - "[[staged-design-harvest-and-synthesis]]"
  - "[[evidence-backed-design-validation]]"
  - "[[negative-evidence-and-avoidance]]"
  - "[[positive-design-fusion]]"
---

# 可拓展与可演化设计

## 定义

资料库和未来项目设计不能被做成一次性的最终答案，而要被做成可持续演化的系统。

以后如果出现新的、更强的思路、库、论文、框架或产品模式，应该能够继续进入采集、验证、综合和落地流程，而不是推翻原有结构。

## 核心目标

- 能持续吸收新设计。
- 能替换旧方案。
- 能保留历史判断。
- 能比较新旧路线。
- 能小范围试验。
- 能在失败时回退。

## 设计原则

- `modular`：模块化。每个设计点尽量独立记录，避免和其他判断混在一起。
- `versioned`：版本化。重要模式、决策和架构方案要保留时间、状态和变更记录。
- `replaceable`：可替换。不要把某个工具或库绑定成唯一答案。
- `adapter-first`：优先通过适配层接入新思路，避免直接侵入核心结构。
- `migration-aware`：迁移可见。采用新方案前要知道旧方案如何迁移、如何回退。
- `evidence-updatable`：证据可更新。新的证据可以提高或降低某个设计点的可信度。

## 新思路进入流程

```text
新思路/新库/新论文
  -> raw 原始资料
  -> library-review 或 development-insight
  -> design-pattern / anti-pattern
  -> evidence-backed validation
  -> 和旧路线比较
  -> 小实验或观察
  -> decision-record
  -> 统一设计时再落地
```

## 需要避免

- 把当前方案写死成唯一正确答案。
- 每来一个新想法就推翻旧结构。
- 把工具能力和系统能力混在一起。
- 没有迁移路径就大规模采用。
- 忽略旧决策的上下文，反复重新争论。

## 判断问题

以后遇到更强的新思路时，要问：

- 它比当前方案强在哪里？
- 它是否解决当前没有解决的问题？
- 它是否只是更复杂，而不是真更强？
- 它能不能先作为插件、适配层或局部实验接入？
- 它会替换哪些旧设计？
- 旧设计是否需要废弃、保留、降级或迁移？
- 如果新方案失败，怎么回退？

## 原则

真正可拓展的系统，不是无限加东西，而是允许新证据改变设计，同时保留边界、版本、验证和回退。

