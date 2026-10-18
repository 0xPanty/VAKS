---
type: visual_artifact
status: draft
created: 2026-06-06
project: verified-action-knowledge-system
source_reference: raw/repos/2026-06-06-helloianneo-ian-xiaohei-illustrations-source.md
visual_reference: Ian Xiaohei Illustrations
license_attribution: "Inspired by Ian Xiaohei Illustrations by Ian, MIT License."
truth_boundary: explanatory visual only; not reviewed knowledge; not architecture decision; not action basis
---

# VAKS Xiaohei Architecture Logic Visual

## 产物

```text
products/visuals/vaks-xiaohei-architecture-logic/vaks-architecture-gate.svg
products/visuals/vaks-xiaohei-architecture-logic/vaks-architecture-gate.png
products/visuals/vaks-xiaohei-architecture-logic/vaks-architecture-gate-imagegen-draft.png
```

这是一张 VAKS 架构逻辑的“小黑正文配图式”解释图。

SVG 是可读源文件，PNG 是 Obsidian / 聊天预览用渲染图。`imagegen-draft`
是图像模型直接生成的草稿，更接近 Ian Xiaohei Illustrations 的生图味道，
但少了 `不改 truth` 这个边界标注；正式复用时优先看 SVG/PNG 版本。

它不试图画完整模块树，只画一个核心动作：

```text
来源轻进入
-> 候选理解
-> 复核闸门
-> 已审知识
-> 行动包
-> 反馈回流但不改 truth
```

## 为什么这样画

Ian Xiaohei Illustrations 的规则不适合画严肃、密集、可编辑的架构图。它适合把一个判断或结构压成一张有记忆点的正文配图。

所以这张图选择的隐喻是：

```text
小黑在一台低科技复核闸门机器里操作候选理解和复核闸门。
杂乱来源可以轻入口进入。
一部分候选被拦到待复查。
通过复核的卡片才变成已审知识，并能打包成行动包。
行动后的反馈沿蓝线回流，只改善下一次激活，不直接改 truth。
```

## 边界

这张图是解释层，不是主架构文件。

不要把它当成：

```text
正式流程规范
完整系统架构图
schema / template / decision
reviewed knowledge
action basis
```

它只用于向人解释 VAKS 的核心纪律：

```text
The system can suggest.
Only reviewed evidence can support action.
Feedback improves activation, not truth.
```

## 来源与署名

视觉方法参考：

```text
Ian Xiaohei Illustrations
https://github.com/helloianneo/ian-xiaohei-illustrations
Author: Ian / helloianneo
License: MIT
```

本图没有复刻示例图构图；只借用了该 Skill 的视觉原则：16:9、白底、手绘线稿、少量红橙蓝中文批注、小黑承担核心动作。
