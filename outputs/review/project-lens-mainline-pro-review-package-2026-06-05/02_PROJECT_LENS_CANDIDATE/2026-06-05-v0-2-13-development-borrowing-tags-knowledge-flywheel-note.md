---
type: candidate_design_note
status: candidate-only
created_at: 2026-06-05
project: verified-action-knowledge-system
scope: project-lens-overlay-and-knowledge-flywheel
truth_boundary: candidate design note only; not reviewed knowledge; not schema; not template; not architecture decision
write_scope: outputs/review only
---

# Project Lens / Knowledge Flywheel Candidate Note

## 说人话结论

Pro 调研后的当前候选结论是：

```text
外部资料先被 AI 蒸馏成通用、独立、原子化的知识点。
当前项目开发时，不改动知识点本体，只通过 Project Lens sidecar 贴一层项目视角。
Project Lens 标出：当前项目可能能借什么、不能借什么、可能借到哪里、为什么先这么看。
项目结束后，大多数 lens 归档或删除；真正用上或踩坑的少数点才生成 landed_snapshot / boundary_snapshot。
```

这不是新文件夹，不是新 schema，不是新 template，不是正式决策区。

它更像：

```text
通用知识点上的项目透镜 / 透明蒙版 / sidecar overlay。
```

Pro verdict:

```text
accept_direction
```

## Why This Is Strong

这套思路强在它把三件事拆开：

```text
通用知识内容 / 可复用原子知识点
动态项目视角 / Project Lens
沉淀经验 / 项目结束后的成功模式和失败边界
```

如果三者混在一起，知识库会污染：

```text
某项目的临时判断会写脏通用知识点
某阶段的看法会被误读成长期 truth
某次踩坑会丢失上下文，未来无法预警
```

拆开后：

```text
知识点保持干净
项目透镜临时可撤
经验快照可以复用
正式架构只留下真正落地的东西
```

## Core Flow

```text
外部资料
-> AI 蒸馏成通用候选知识点
-> 当前项目通过 Project Lens sidecar 贴项目视角
-> 开发中验证 / 采用 / 避开 / 踩坑
-> 项目结束对少数真实结果做快照
-> 成功经验回流成架构模式 / 经验指南
-> 失败经验回流成负向知识 / 项目边界
-> 下个项目优先复用这些经验和边界
```

## Layer Meaning

### 1. 通用知识点

作用：

```text
把资料蒸馏成以后还能复用的“标准件”。
```

特点：

```text
独立
原子化
可回源
不属于单个项目
不写当前项目临时判断
```

### 2. Project Lens Overlay

作用：

```text
开发当前项目时，用 sidecar overlay 标记哪些通用知识点可能能借、不能借、可能借到哪里。
```

特点：

```text
轻量
临时
可撤
项目局部
不污染知识点本体
不等于正式采用
不写进原知识点 YAML / 正文
```

### 3. 项目经验快照

作用：

```text
项目结束后，保留这次项目实际采用了什么、避开了什么、踩过什么坑。
```

特点：

```text
是项目经验，不是把项目判断写回通用知识点
可以成为未来项目的预警和复用材料
```

## Stance / Outcome Semantics

旧候选标签 `watch / borrow / avoid / landed / parked` 不再作为定稿。

Pro 建议拆成两层：

```text
stance: watch | partial | avoid | park
outcome_ref: empty | landed_snapshot | boundary_snapshot
```

含义：

```text
stance = 项目开发中的当前姿态
outcome_ref = 真有结果后，指向 landed 或 boundary 快照
```

`landed` 不再是普通标签。真的采用 / 实装 / 吸收以后，才生成 landed_snapshot。

`avoid / rejected / 踩坑` 如果要成为长期资产，也不是永久挂在知识点上的标签，而是生成 boundary_snapshot。

stance 不是 truth confidence。

stance 只是：

```text
当前项目开发视角。
```

## Minimal Project Lens Fields

最小形态不是新模板，而是项目侧联文件里的稀疏记录。

建议真正必填：

```text
project:
kp_id:
kp_ref:
stance: watch | partial | avoid | park
borrow_scope:
target_hint:
reason_1liner:
```

按需字段：

```text
non_borrow_scope:
gate_hint:
review_origin:
outcome_ref:
updated_at:
anchor_health:
```

`target_hint` 建议用结构化可定位格式，但只表示可能作用位置，不表示已经决定修改：

```yaml
target_hint:
  - type: doc | repo_symbol | repo_line | module | workflow | pr | unknown
    value: "<locator>"
    status: active | healthy | conceptual | not_checked | drifted | unanchored
    anchor_version: "<optional version/date/commit/check note>"
```

优先用 `path + heading/symbol/module`；行号只是辅助，因为会漂移。保留 `target_hint` 这个弱名字，不改成 `code_anchor`。

高强度沙盒后的补充：

```text
kp_ref 值得保留：它让 Lens entry 能直接回到 candidate pattern / core KP 文件。
conceptual 值得保留：它区分“概念性 workflow/module hint”和“还没检查的文件锚点”。
```

## Lifecycle

### During Research

```text
AI 从资料中蒸馏候选知识点。
知识点进入候选通用知识层。
```

### During Development

```text
AI 或人提出 Project Lens 建议。
人确认或修改 stance / scope / target_hint / reason_1liner。
Lens 只回答：这个项目当前可能能不能借，怎么借，不能借什么。
```

### Before Landing

如果 lens 要变成正式架构、决策或 action basis：

```text
触发 v0.2.13 late-stage action-facing review。
不能只看 lens，必须说明 evidence 为什么支撑 claim。
```

### After Project

项目结束后：

```text
ordinary lens tags -> 归档或移除
true landed outcome -> landed_snapshot -> 架构模式 / 经验指南 / best practice
true failure / non-fit outcome -> boundary_snapshot -> 负向知识 / 项目边界 / 雷区
```

Lens 可以消失，但项目经验和边界快照留下。

## Positive Feedback: Architecture Patternization

落地成功的知识点不是普通资料点。

它经过了：

```text
调研
适配
开发
验证
修正
落地
复盘
```

它可以回流成：

```text
架构模式
经验指南
best practice
可复用套路
```

这就是“架构模式化”。

## Negative Feedback: Knowledge Boundaries

avoid / rejected / not borrowed 的点同样可能是资产，但资产不是 live tag 本身。

它们回答：

```text
什么在什么场景下不适合
为什么不适合
踩过什么坑
下次看到类似方案要警惕什么
```

这形成：

```text
负向知识库
项目边界
雷区
自动预警材料
```

这类知识可能比正向经验更节省未来时间。

最小 boundary_snapshot 应该记录可触发内容：

```text
trap_title
bad_move_or_non_fit
failure_context
trigger_conditions
why_it_failed
boundary_of_applicability
similar_keywords
warning_1liner
safer_alternative_or_escalation
evidence_refs
```

## Relationship To v0.2.13

Project Lens 和 v0.2.13 不冲突。

关系是：

```text
Project Lens = 帮当前项目筛选、聚类、提示可借鉴点
v0.2.13 = 当某个点准备变成正式行动 / 决策 / promotion 时，检查理由够不够
```

Lens 本身不是 action basis。

当 lens 要变正式，才问：

```text
claim 是什么？
anchored evidence 是什么？
为什么 evidence 支撑 claim？
scope / assumptions 是什么？
还有什么 challenges / gaps / open risk？
```

## What This Is Not

```text
不是新 folder requirement
不是 schema
不是 template
不是 ADR
不是 reviewed knowledge
不是 action basis
不是永久 truth 状态
不是把所有 intake 变重
不是把项目字段写进原知识点 YAML
```

## Current VAKS Mapping

当前名字这样降重理解：

```text
Candidate Pattern Bank
  = 高阶、重复出现、问题中心明确的候选模式
  = 不是所有通用原子知识点的复制

Project Lens Overlay
  = 当前项目贴在知识点旁边的 sidecar 视角
  = 主 authoring surface

Project Borrowing Ledger
  = Project Lens 的派生视图 / 汇总页
  = 不是主记录
```

当前试点文件：

```text
outputs/review/project_lens_overlays/VAKS.md
outputs/review/project_borrowing_ledgers/VAKS.md
```

这仍然不是正式开发区目录。

## Pro Research Result

Pro 已返回：

```text
Verdict: accept_direction
Best name: Project Lens
Storage: project-scoped sidecar overlay
Lifecycle: stance during project, outcome_ref only after real outcome
Ledger role: derived view, not main authoring surface
```

## Current Recommendation

```yaml
direction: accept_direction
main_candidate_name: Project Lens
storage: project_scoped_sidecar_overlay
mainline_change_now: no
schema_change_now: no
template_change_now: no
formal_workspace_directory_now: no
candidate_sidecar_pilot: outputs/review/project_lens_overlays/VAKS.md
next_step: run small real use examples before any mainline or template promotion
```
