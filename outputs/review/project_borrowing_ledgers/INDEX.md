---
type: project_lens_derived_view_index
status: pilot_derived_view
created_at: 2026-06-05
truth_boundary: derived project lens views only; not ADR; not action basis; not source of truth
---

# Project Lens Derived Views

Pro 调研后，本目录不再被理解为主 authoring surface。

主记录应放在：

```text
outputs/review/project_lens_overlays/
```

本目录只保留派生视图 / 汇总页 / 恢复入口。

Project Lens Derived View 回答：

```text
这个项目当前从什么视角看相关 candidate pattern / knowledge point？
可能借什么？
可能借到哪里？
为什么先这样看？
下一步需要过什么 gate？
```

它不是 source card，不复制外部资料内容。

它也不是 ADR，不直接形成架构决策。

## Main Sidecar Fields

```text
project
kp_id
stance: watch | partial | avoid | park
borrow_scope
target_hint
reason_1liner
```

`landed` 和踩坑结果不作为普通 live tag。它们应该通过 `outcome_ref` 指向：

```text
landed_snapshot
boundary_snapshot
```

## Boundaries

```text
Project Lens tag is not reviewed knowledge.
Project Lens tag is not architecture decision.
Project Lens tag is not action basis.
Ledger view is not source of truth.
```

真正进入 promotion / decision / action basis 时，才触发 v0.2.13 warrant gate。

## Views

- [[VAKS]]
