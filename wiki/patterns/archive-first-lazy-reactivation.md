---
type: pattern
status: draft
created: 2026-05-27
updated: 2026-05-27
source_libraries:
  - byarbrough/obsidian-para
related_concepts:
  - "[[MEMORY_TIER]]"
  - "[[DEV_CONTEXT]]"
related_projects:
  - verified-action-knowledge-system
adoption_status: adapt
verification_status: single-source
evidence_level: secondary
evidence_count: 1
confidence: medium
negative_evidence:
  - "Archive-first migration can hide useful items if search and reactivation routes are weak."
replaces:
superseded_by:
extension_points:
  - memory-tier
  - feedback-event
  - query-run
last_verified: 2026-05-27
next_review: 2026-06-03
epistemic_type: take
gaps:
  - "Needs a real trial on existing cold/raw materials."
evidence_timeline:
  - date: 2026-05-27
    source: "[[2026-05-27-obsidian-para-source]]"
    observation: "The migration advice puts old material into Archive first and moves it out only when used."
    effect: supports
    confidence: medium
relations:
  - target: "[[MEMORY_TIER]]"
    type: refines
    strength: 5
    confidence: medium
    evidence:
      - "[[2026-05-27-obsidian-para-source]]"
    rationale: "Archive-first migration provides a practical cold-by-default and reheat-on-use rule."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[conversation-derived-feedback-routing]]"
    type: refines
    strength: 3
    confidence: medium
    evidence:
      - "[[2026-05-27-obsidian-para-source]]"
    rationale: "A source can be reactivated by actual use signals rather than pre-sorting."
    created: 2026-05-27
    last_verified: 2026-05-27
tags:
  - pattern
  - memory-tier
  - archive
  - reactivation
---

# Archive-First Lazy Reactivation

## AI-readable preamble

Do not pre-sort all old material.

Default old material to cold/archive, then reactivate it when a real project, query, or feedback event uses it.

This lowers maintenance cost and lets actual use reveal value.

## 一句话定义

旧资料先冷存；只有被真实问题、项目或反馈重新调用时，才在具体 scope 下升温。

## 解决的问题

全库冷热分层如果一开始就做重，会变成整理工程。

更现实的办法是：

```text
archive first
reactivate by use
write back only when reusable value appears
```

这样可以避免：

```text
把大量旧资料手工分类
把暂时不用的资料误标 hot
让整理成本压过使用价值
```

## 适用场景

- 初次迁移大量旧资料。
- raw/source 积累过多但尚未审查。
- 项目开发时需要从历史资料中找可复用材料。
- query-run 或 feedback-event 发现旧资料重新相关。

## 不适用场景

- 当前正在执行的高风险项目材料。
- 必须定期复核的 decision / compliance / safety 资料。
- 已知会频繁使用的核心操作手册。

## 反例与避坑

- 失败条件：archive 没有 search/index，导致冷资料永远找不回来。
- 相似反模式：把 cold 当成 useless。
- 复杂度风险：如果每次 reactivation 都要求搬文件，会增加摩擦。
- 替代方案：先用 `memory_tier` metadata 和 dev context pack，少搬物理路径。

## 来源证据

- `[[2026-05-27-obsidian-para-source]]`：PARA 迁移建议是旧资料先入 Archive；每次实际用到旧 note/file，再移动到合适位置。

## 标签与量化

- domain: knowledge-lifecycle
- problem: vault-migration
- maturity: emerging
- complexity: low
- problem_fit: 5
- reuse_value: 5
- implementation_cost: 1
- integration_fit: 5
- evidence_strength: 3
- reversibility: 5

## 交叉验证

- 相似来源：待与更多 Second Brain / PARA / AI context systems 交叉验证。
- 历史项目影子：当前资料库已有 `raw/` 和 `outputs/`，天然承载 cold/archive。
- 支持证据：`FEEDBACK.md` 已允许反馈生成 route / missing-point / activation 信号。
- 反例：没有索引和 query-run 时，archive-first 可能变成遗忘。

## 最小实现方式

1. 不对旧资料做全量物理移动。
2. 默认旧 raw/source/query-run 为 cold。
3. 当某项目使用它时，在 dev context pack 的 `Cold References` 或 `Support` 中记录。
4. 如果它被复用或形成稳定模式，再写回：

```yaml
memory_tier: warm
activation_status: active
scope_key:
activation_reason:
last_activated:
```

5. 如果它成为当前任务必须读的文件，再在具体 scope 下标记 hot。

## 项目融合建议

加入 `MEMORY_TIER.md`：

```text
Do not classify every old note upfront.
Cold is the default for old material.
Use creates scoped activation.
Reuse creates warm status.
Current task creates scoped hot status.
```

加入 `DEV_CONTEXT.md` Exit：

```text
After a project ends, scan Core/Support for reusable patterns.
Reusable items cool to warm.
One-off evidence returns to cold.
```

## 可拓展性

- 可以通过什么接口/适配层接入：query-run, feedback-event, dev-context-pack, Obsidian Bases.
- 未来可能被什么替代：automatic activation scoring, but only after query-run evidence exists.
- 替换或升级成本：低。
- 回退方式：manual archive search.

## 验证指标

- 旧资料迁移时间降低。
- 被 reactivated 的 cold material 都有 scope 和 reason。
- 项目结束后有明确 cool-down 记录。
- warm 层不是靠主观整理，而是靠复用痕迹形成。
