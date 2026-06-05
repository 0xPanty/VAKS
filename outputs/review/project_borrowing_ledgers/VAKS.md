---
type: project_lens_derived_view
status: pilot_derived_view
project_id: VAKS
project_name: Verified Action Knowledge System / 资料库
created_at: 2026-06-05
truth_boundary: derived project lens view only; not reviewed knowledge; not ADR; not action basis; not source of truth
source_overlay: outputs/review/project_lens_overlays/VAKS.md
---

# VAKS Project Lens Derived View

## 当前口径：Project Lens 派生视图

根据 Pro 调研结果，这份文件不再作为主 authoring surface。

```text
主记录 = outputs/review/project_lens_overlays/VAKS.md
本文件 = 从 Project Lens sidecar 派生出来的项目汇总视图
```

人话：

```text
知识点本体像书。
Project Lens sidecar 像透明纸。
本文件只是把透明纸上的 VAKS 当前视角汇总出来，方便人看。
```

## Pro 后的降重规则

```text
Project Borrowing Ledger 不应写成轻量 ADR。
Project Lens 才是项目侧联标记层。
Ledger / View 只做聚合、索引、周度汇总或恢复入口。
```

## 边界

这份文件汇总 VAKS 对 candidate patterns / candidate points 的项目临时视角。

它不是：

- source card；
- reviewed knowledge；
- architecture decision；
- action basis；
- truth confidence；
- 自动 promotion；
- 永久项目状态；
- 正式开发区目录要求；
- 主记录文件。

当前候选主记录字段在 Project Lens sidecar 中：

```text
kp_ref: direct pointer back to candidate/core knowledge point
stance: watch | partial | avoid | park
target_hint: structured locator with healthy/conceptual/not_checked/etc.
outcome_ref: empty | landed_snapshot | boundary_snapshot
```

High-intensity sandbox update:

```text
The source of truth for current Project Lens details is the sidecar, not this table.
The sidecar now includes kp_ref and conceptual target status.
This derived table is intentionally lossy and may omit snapshot/anchor details.
```

重要边界：

```text
landed 不是普通 stance；真用上后才生成 landed_snapshot。
踩坑 / rejected 不是普通结论；沉淀后才生成 boundary_snapshot。
```

真正进入主架构、reviewed relation 或 action basis，必须另走 review / decision，并在 action-facing use 时触发 v0.2.13。

旧字段兼容解释：

```text
adapt     ~= partial
prototype ~= partial with prototype gate
reject    ~= avoid
```

## Derived Summary

| Knowledge Point | Stance | Target Hint | One-Line Reason | Gate |
|---|---|---|---|---|
| `source-structure-first-rag` | partial | `workflow:source-intake`; `doc:SOURCE_INTAKE.md` | 保留 source structure 有助于 VAKS raw/source/candidate/review 边界。 | design-review |
| `retrieval-is-activation-not-truth` | partial | `doc:MEMORY_TIER.md#Activation Tier`; `workflow:context-pack-preparation` | 检索能激活上下文，不能制造 reviewed truth。 | design-review |
| `file-first-agent-workbench` | watch | `module:future-agent-workbench`; `workflow:dev-context-inspection` | 文件可见性能降低黑盒，但 agent 写入必须隔离。 | prototype |
| `adaptive-retrieval-depth` | watch | `module:activation-tier`; `workflow:context-pack-budgeting` | 快慢检索有价值，但当前不需要重 runtime。 | prototype |
| `memory-granularity-and-quarantine` | watch | `doc:MEMORY_TIER.md`; `workflow:feedback-ledger` | 多粒度记忆有用，但不能直接改 reviewed truth。 | design-review |
| `graph-and-ontology-as-candidate-context` | watch | `module:relation-review`; `workflow:context-neighborhood-activation` | 图/本体可组织候选上下文，不能创建 reviewed relation。 | design-review |
| `visual-workbench-for-retrieval-diagnostics` | partial | `module:future-reviewer-workbench`; `workflow:retrieval-diagnostics` | 可视化适合诊断失败，不是 confidence。 | prototype |
| `skills-and-prompts-as-visible-files` | watch | `module:future-agent-workbench`; `workflow:skill-registry` | 可见 prompt/skill 降低黑盒，但编辑权需要 quarantine。 | design-review |
| `search-to-analysis-before-answer` | watch | `workflow:context-pack-drafting`; `workflow:evidence-envelope-preparation` | 先分析再回答可改良 drafting，但不能加重普通查询。 | design-review |
| `simple-first-retrieval-baseline` | watch | `workflow:ordinary-query`; `module:retrieval-baseline` | 简单基线能降复杂度，但不能否定复杂检索的适用场景。 | prototype |

## 明确不借

- 不借任何把 retrieval score / rerank / dashboard / feedback heat 当 truth confidence 的做法。
- 不借任何把 AI summary 直接写成 reviewed knowledge 的做法。
- 不借任何把 source family 多报告当独立支持数的做法。
- 不借 terminal tool 只靠简单 blacklist 的安全边界。
- 不借“single source of truth”把 raw / insight / decision 全揉在一起的 framing。

## 当前结论

这个文件证明：同一个 candidate pattern / knowledge point 可以保持通用，而 VAKS 的 Project Lens sidecar 可以单独存在，不污染知识点本体。

当前 Pro 调研已经支持方向：

```text
accept_direction
best name: Project Lens
storage: project-scoped sidecar overlay
ledger role: derived view, not primary authoring surface
```
