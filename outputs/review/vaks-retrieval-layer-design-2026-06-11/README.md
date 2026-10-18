---
record_kind: design_workspace
status: candidate
knowledge_status: candidate
project_id: VAKS
created_at: 2026-06-11
created_by: Codex
workspace_scope: retrieval_layer_design
truth_boundary: candidate workspace only; not reviewed knowledge; not decision; not action basis
action_basis_allowed: false
truth_mutation_allowed: false
---

# VAKS Retrieval Layer Design Workspace

## 说人话

这个目录专门放 VAKS 检索层设计。

目标不是马上决定技术栈，而是先把市面上主流和前沿的检索/向量方案吸收一轮，再设计一套适合 VAKS 的定制检索层：

```text
既要找得快、找得全、找得准
也不能把 raw / candidate / reviewed / overlay / feedback 混成一个假权威排行榜
```

## 当前判断

VAKS 现在强的是检索治理：

```text
先分桶
先看知识状态
先看 retrieval_policy
先看能不能进 context pack 或 action basis
再做相关度排序
```

VAKS 现在弱的是检索工程：

```text
语义召回不够强
chunk / anchor 还不够细
hybrid retrieval 还没有成型
query intent router 还没有工程化
counterevidence / risk retrieval 还没有系统化
```

## 这个工作区的边界

这里的所有内容都是 candidate design material。

它不能直接创建：

```text
reviewed knowledge
reviewed relation
truth confidence
architecture decision
action basis
mainline dependency
```

## 文件地图

```text
task_plan.md
  这个工作区的阶段计划。

findings.md
  已吸收资料、初步判断、设计发现。

progress.md
  会话进度和验证记录。

frontier-source-ledger.md
  待吸收和已吸收的主流/前沿检索方案台账。

design-questions.md
  VAKS 检索层必须回答的问题。

retrieval-layer-north-star.md
  初始设计北极星：效率和边界怎么同时保留。
```

## 预期路线

```text
Phase 1:
  固定工作区和边界。

Phase 2:
  吸收主流/前沿检索资料：
  vector index / vector DB / hybrid search / rerank / graph retrieval / chunking / evaluation。

Phase 3:
  建比较矩阵：
  召回效率、准确度、过滤能力、边界风险、可本地化、可重建性、VAKS 适配度。

Phase 4:
  设计 VAKS 定制检索层：
  bucket first -> hybrid recall -> rerank -> anchor queue -> context pack -> evidence/action gate。

Phase 5:
  做小型 pilot：
  用 VAKS 真实 markdown chunk 测 recall、anchor correctness、越权风险。
```

