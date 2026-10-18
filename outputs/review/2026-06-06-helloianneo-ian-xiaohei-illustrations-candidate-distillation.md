---
type: repo_candidate_distillation
status: candidate_only
created_at: 2026-06-06
source_record: raw/repos/2026-06-06-helloianneo-ian-xiaohei-illustrations-source.md
source_url: https://github.com/helloianneo/ian-xiaohei-illustrations/tree/main
checked_commit: 91b560849e8f883922cc2fa8a358a668caa94105
truth_boundary: visual-expression candidate only; not reviewed knowledge; not architecture decision; not action basis
review_priority: low
projects:
  - verified-action-knowledge-system
tags:
  - visual-reference
  - codex-skill
  - xiaohei
  - explanatory-visual
  - candidate-only
---

# Ian Xiaohei Illustrations Candidate Distillation

## 一句话人话结论

这个 repo 不是架构资料，也不是绘图库。它是一个 Codex Skill，用来把中文文章里的一个关键判断、流程、结构、状态或隐喻，画成 16:9 白底手绘正文配图。

对 VAKS 有用的是表达方式：

```text
不要把全系统塞进一张严肃架构图。
先抓一个认知锚点。
用一个怪诞但清爽的物理隐喻画出来。
```

## 对 VAKS 的适配判断

适合：

```text
解释 VAKS 给人看
做文章正文配图
做“为什么反馈不改 truth”这类单点说明
做“轻入口 + 复核闸门 + 行动包”的低认知负担图
```

不适合：

```text
正式系统架构图
完整模块关系图
schema 可编辑图
review / action basis 证据图
```

## 候选提炼

### 1. visual_metaphor_for_vaks_architecture_explanation

候选理解：

```text
VAKS 的主逻辑可以用“复核闸门机器”解释：来源轻进，候选理解，复核拦截，已审知识才支撑行动包。
```

边界：

```text
图是解释层，不是正式 architecture decision。
```

### 2. single_cognitive_anchor_per_illustration

候选理解：

```text
每张 VAKS 解释图只画一个认知动作，比完整模块图更适合小黑风格。
```

边界：

```text
完整工程结构仍应留给 Markdown docs / diagrams / review packets。
```

### 3. attribution_required_for_xiaohei_visual_language

候选理解：

```text
使用小黑视觉语言或派生文档时，应保留 Ian Xiaohei Illustrations 名称或给 Ian attribution。
```

边界：

```text
Attribution 是使用边界，不是 VAKS 知识支持。
```

## 这次试画

产物：

```text
products/visuals/vaks-xiaohei-architecture-logic/vaks-architecture-gate.svg
products/visuals/vaks-xiaohei-architecture-logic/vaks-architecture-gate.png
products/visuals/vaks-xiaohei-architecture-logic/vaks-architecture-gate-imagegen-draft.png
products/visuals/vaks-xiaohei-architecture-logic/README.md
products/visuals/vaks-xiaohei-feedback-mechanism/vaks-feedback-use-ledger.png
products/visuals/vaks-xiaohei-feedback-mechanism/README.md
```

这张图选择的 VAKS 逻辑是：

```text
来源 -> 候选理解 -> 复核闸门 -> 已审知识 -> 行动包
反馈回流 -> 改善激活路径，但不直接改 truth
```

这个选择来自本地 VAKS 当前主线文件：

```text
README.md:
Capture -> Understand -> Review -> Connect -> Act and Learn
The system can suggest.
Only reviewed evidence can support action.
Feedback improves activation, not truth.

FUSION_ARCHITECTURE_V0_2_DRAFT.md:
source -> candidate points -> calibration / point collision -> review -> reviewed node or relation -> context pack / action basis -> action -> feedback / outcome

ARCHITECTURE_PRINCIPLES.md:
Markdown is the system of record.
Review creates truth.
Strict checks are lazy gates.
```

追加反馈机制图选择的 VAKS 逻辑是：

```text
反馈事件 -> Use Ledger -> 改善下次 activation / scope fit / usefulness
负反馈 / 明确纠错 -> review_due / 复查压力
feedback 不能直接改 truth confidence / reviewed relation / verification_status
```

这个选择来自本地 VAKS 当前反馈边界文件：

```text
FEEDBACK.md:
Feedback improves future retrieval and context activation.
Feedback must not directly rewrite truth.
Positive feedback is weak.
Negative feedback creates review pressure.
Explicit correction creates review_due.

README.md:
Feedback improves activation, not truth.

SECOND_BRAIN_MODEL.md:
Use Ledger records how knowledge was used and improves activation without rewriting truth.
```

## 不吸收的部分

- 不安装该 skill 到本机 Codex。
- 不把小黑风格变成 VAKS 默认视觉规范。
- 不把这个图当成完整架构图。
- 不把视觉表达结果写进 `wiki/` 正式知识层。
- 不用示例图复刻构图。

## 结论

```text
watch_as_visual_expression_tool
usable_for_explainer_artifacts
not_architecture_source
```
