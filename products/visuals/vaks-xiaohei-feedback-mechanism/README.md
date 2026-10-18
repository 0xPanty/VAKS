---
type: visual_artifact
status: draft
created_at: 2026-06-06
project: verified-action-knowledge-system
visual_reference: Ian Xiaohei Illustrations
source_reference: raw/repos/2026-06-06-helloianneo-ian-xiaohei-illustrations-source.md
image: products/visuals/vaks-xiaohei-feedback-mechanism/vaks-feedback-use-ledger.png
related_files:
  - FEEDBACK.md
  - README.md
  - SECOND_BRAIN_MODEL.md
truth_boundary: explanatory visual only; not reviewed knowledge; not architecture decision; not action basis; not feedback schema
tags:
  - visual
  - feedback
  - use-ledger
  - activation
  - review-due
  - candidate-only
---

# VAKS Feedback Mechanism Visual

## 用途

这张图用小黑风格解释 VAKS 的反馈机制：

```text
反馈不是 truth 旋钮。
反馈是使用小票，先进入 Use Ledger。
它可以改善下次激活、范围匹配和上下文选择。
负反馈和明确纠错会制造 review_due / 复查压力。
它不能直接改 truth confidence、verification_status 或 reviewed relation。
```

## 图中对应关系

| Visual element | VAKS meaning | Boundary |
|---|---|---|
| `有用 / 跑偏 / 缺证据 / 明确纠错` 小票 | 使用后的反馈事件 | Feedback record, not truth evidence. |
| `Use Ledger` 分拣台 | 记录知识如何被使用、哪里有用、哪里跑偏 | Ledger can guide future activation and review pressure. |
| 蓝色路径 `下次先读` | 改善 usefulness、scope fit、activation ranking | Activation is not belief. |
| 红色路径 `review_due` | 负反馈或明确纠错触发复查压力 | Review input, not automatic correction. |
| 锁住的 `truth` 保险柜 | reviewed knowledge / truth confidence | Feedback cannot directly rewrite it. |

## 本地依据

这张图只压缩了本地 VAKS 文件中的反馈边界：

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

## 使用边界

这是一张解释图，适合用于：

```text
给人讲 VAKS 的反馈机制
文章正文配图
架构讨论时降低理解成本
```

不适合用于：

```text
替代 FEEDBACK.md
替代 schema / review protocol
作为 reviewed knowledge
作为 action basis
作为反馈字段规范
```

## Attribution

Visual style references `Ian Xiaohei Illustrations` by Ian / helloianneo.

The source repository was captured separately at:

```text
raw/repos/2026-06-06-helloianneo-ian-xiaohei-illustrations-source.md
```
