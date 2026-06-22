---
type: candidate_distillation
record_kind: candidate_distillation
status: draft
title: "Agent-first 知识库：过滤、原子化、周期迭代"
created_at: "2026-06-08"
created_by: Codex
processing_tier: medium
knowledge_status: candidate
overlay_state: none
review_pressure: none
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
derived_from:
  - raw/videos/2026-06-08-xhs-knowledge-base-not-use-source.md
  - raw/videos/2026-06-08-xhs-knowledge-base-not-use-source/transcript.txt
  - raw/videos/2026-06-08-xhs-knowledge-base-not-use-source/segments.md
projects:
  - verified-action-knowledge-system
topics:
  - agent-first-knowledge-base
  - source-intake
  - weekly-review
  - local-file-boundary
  - personal-profile-activation
borrow_value: strong
borrow_order: P1
evidence_strength: medium_for_workflow_low_for_implementation
tags:
  - candidate-only
  - source-distillation
  - xiaohongshu
  - design-only
provisional: true
---

# 候选蒸馏：Agent-first 知识库

## 一句话

这条视频对 VAKS 是 `P1 / strong`，但只限于工作流和产品逻辑：它把“知识库怎么真正用起来”说清楚了，尤其是 **agent 才是知识库的一等使用者**、**新内容先过滤**、**知识要原子化**、**每周 review 迭代**、**agent 通过本地命令受控调用知识库**。

它不是源码证据，也不是 reviewed knowledge。

## 我们 VAKS 已经有的部分

VAKS 已有的主线是：

```text
Capture -> Understand -> Review -> Connect -> Act and Learn
```

也已经有这些边界：

```text
raw != candidate != reviewed != action basis
activation != truth
feedback != truth mutation
agent write must be quarantined
```

这条视频不是推翻这些设计，而是给出一个更好懂、更能落地的使用闭环：

```text
问题导向
-> 入口过滤
-> 原子化拆解
-> 专题归档
-> 周期 review
-> 更新画像 / 支持库
-> agent 在具体任务里调用
```

## Candidate Points

### 1. 知识库不是资料库

只把文章、课程、笔记收进去，最多是资料库。真正的知识库要围绕一个或一类问题搭建，并有明确的使用场景。

对 VAKS 的映射：

```text
source capture 是入口
candidate comprehension 是理解
review / activation / action 才是让知识活起来的路径
```

### 2. 入口过滤标准可以很朴素

视频里的过滤标准是：

```text
这条内容下个月我还能不能复用？
```

这对 VAKS 很有用。它可以成为 light / medium source intake 的低成本 triage 问题，帮助筛掉临时热闹、低复用、无项目关系的材料。

### 3. 原子化不是为了拆碎，而是为了让 agent 调用

作者把内容拆成原则、方法、案例、反模式、工具、洞察，并打话题标签。重点不是分类本身，而是 agent 可以按任务取用：需求评估、周期复盘、skill 编写等。

VAKS 可以吸收为：

```text
candidate point atomization
type/routing labels
agent context-pack preparation
```

但不能把这六类直接升级成正式 schema。

### 4. 本地文件 + 命令接口是一个好边界

视频里最像 VAKS 的点是：数据保存在本地文件，agent 通过命令增删改查，而不是直接读取和改写原子库。这个和 VAKS 的 agent quarantine 很贴。

可借鉴为：

```text
agent gateway command layer
read-only / append-only / candidate-only write commands
auditable operations
no direct reviewed truth mutation
```

### 5. Weekly item / weekly review 是很好的双 skill 模式

可以抽象成两个 lazy gate：

```text
weekly item:
  新内容入口预处理、过滤、拆解、打标签。

weekly review:
  周期性整理、结合画像重新判断价值、移动到专题、制造 review pressure。
```

这比“全自动入库”安全，也比“每条都重审”轻。

### 6. 个人画像是 activation，不是 truth

作者让 agent 每次新会话读取个人画像，明确身份、习惯、目标，然后调用专题库。这个很适合 VAKS 的 Activation / Dev Context，但必须防止画像变成真值层。

VAKS 应吸收：

```text
profile as activation context
project/person scope fit
use feedback updates profile cautiously
```

不要吸收：

```text
profile directly changes claim confidence
agent auto-writes reviewed facts
```

## Borrow Gradient

```yaml
borrow_value: strong
borrow_order: P1
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "task is specifically about agent gateway, source intake workflow, weekly review loop, or profile/context activation"
  support_when: "designing VAKS workbench, inbox, review queue, dev context, or agent-facing commands"
  risk_when: "agent gains write access, profile updates affect truth, or weekly automation starts promoting knowledge"
  cold_references:
    - raw/videos/2026-06-08-xhs-knowledge-base-not-use-source.md
    - raw/videos/2026-06-08-xhs-knowledge-base-not-use-source/transcript.txt
    - raw/videos/2026-06-08-xhs-knowledge-base-not-use-source/segments.md
```

## 对 VAKS 的具体借鉴

| VAKS 区域 | 可借鉴点 | 不要越界 |
|---|---|---|
| Capture | 用“下个月还能不能复用”做轻量入口过滤 | 不要默认全量保存 |
| Understand | 用 skill 做原子化拆解、候选类型、话题标签 | AI 拆解不是 truth |
| Review | weekly review 作为周期性候选整理和 review pressure | 不等于 evidence-aware promotion |
| Connect | 按专题、案例、反模式、工具连接到 agent 任务 | 自动连接不是 reviewed relation |
| Activation | 个人画像 / 项目画像作为 agent context | 画像不是真值层 |
| Context Pack | agent 按任务读取专题和画像 | context pack 不能隐藏证据边界 |
| Decision / Action | 需求评估、复盘、skill 编写可调用候选知识 | action basis 仍需 gate |
| Use Ledger / Feedback | 使用效果反推 review_due 或画像调整 | feedback 不直接改 truth confidence |
| Agent Gateway | 本地命令接口、受控增删改查、避免直接改原子库 | agent 不直接写 reviewed knowledge |

## 不要借鉴

- 不要把视频里的个人分类体系硬塞进 VAKS schema。
- 不要把 weekly review 做成定时自动 promotion。
- 不要让 agent 自动更新个人画像并影响 truth confidence。
- 不要因为“本地文件”就放松权限和审计。
- 不要把未确认的 GitHub 项目当作可复用源码。

## 值得形成的内部术语候选

```text
agent-first knowledge base:
  知识库不仅给人浏览，更要让 agent 能安全调用。

weekly item gate:
  新内容入口过滤和候选拆解。

weekly review gate:
  周期性整理、画像校准、专题归档、review pressure 生成。

profile activation:
  画像进入上下文激活层，不进入 truth 层。

command-mediated agent access:
  agent 通过命令接口操作候选层，不直接改 reviewed truth。
```

## Knowledge Calibration / Point Collision

| Candidate Point | Local Boundary | Calibration Output | Review Question |
|---|---|---|---|
| agent 是知识库一等用户 | Agent memory quarantine: agent writes cannot directly mutate reviewed truth | supports with risk | VAKS agent gateway 是否需要优先定义命令白名单？ |
| 新内容先按复用性过滤 | SOURCE_INTAKE light/medium/heavy | refines | light intake 是否要加“下个月是否可复用”的轻量问题？ |
| weekly review 周期整理 | Review queue and feedback boundaries | candidate_relation | 周期整理产生的是 review_due 还是 candidate overlay？ |
| 个人画像供 agent 读取 | Activation Tier is not truth | supports | profile 更新是否需要 Use Ledger trace？ |
| 本地命令比直接库读写更安全 | action_basis_allowed false by default | supports | 命令接口如何限制 append-only/candidate-only？ |

## 融合判断

```text
fusion_decision: adapt
borrow_value: strong
borrow_order: P1
direct_use: no
schema_change: no
workflow_value: high
architecture_value: medium
implementation_evidence: low
current_branch_value: high_for_agent_gateway_and_intake
action_readiness: not_ready
```

## 最小吸收建议

先不改主架构，只把这条作为候选借鉴保留。未来如果做 VAKS 的 inbox / agent gateway，可以把它转成三个很小的实验：

```text
1. weekly item: 新来源只做复用性过滤 + candidate atomization。
2. weekly review: 周期整理只产生 review_due / candidate routing，不做 promotion。
3. command-mediated access: agent 只通过白名单命令读候选、写候选、追加 Use Ledger。
```

这条可以成为后续 `Agent Gateway` 和 `Source Intake UX` 的 P1 参考，但不能直接变成 reviewed decision。
