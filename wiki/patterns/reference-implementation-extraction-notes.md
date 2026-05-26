---
type: pattern
status: active
created: 2026-05-26
source_libraries:
  - nashsu/llm_wiki
related_concepts:
  - library-design-extraction
  - evidence-backed-design-validation
related_projects:
  - verified-vault
adoption_status: adopt
tags:
  - implementation-notes
  - reference-repo
  - anti-regression
evidence_count: 1
confidence: high
negative_evidence:
  - full-app-overengineering-before-clean-markdown-vault
---

# 设计模式：参考库实现级提取笔记

## 一句话定义

看过优秀库后，不只记录它的架构结论，还要记录“源码里哪些实现不变量防止踩坑”。

## 解决的问题

高层 pattern 容易让后续实现变形：

```text
知道要做 ingest queue
但忘了 active project guard / abort / cleanup / retry
```

这会导致自己写代码时重犯参考库已经解决过的错误。

## 适用场景

- 参考库源码已经读到核心模块。
- 未来可能自己实现类似功能。
- 参考库有成熟的边界处理、缓存、队列、安全、回退或测试设计。

## 不适用场景

- 只看过 README，没有读源码。
- 只是概念启发，不准备复刻实现。
- 参考库代码质量不明，记录反而会污染判断。

## 记录格式

每个实现级记录至少包含：

- 来源仓库和 commit / 日期。
- 本地临时路径是否存在。
- 读过的源码文件。
- 模块解决的问题。
- 可复用的不变量。
- 不照搬的部分。
- 未来本库落地时的最小实现顺序。

## 反例与避坑

- 不把整仓库源码复制进资料库。
- 不把 UI 组件细节当核心架构。
- 不记录“它用了某个库”这种低价值事实，除非这个库承担关键边界。
- 不把参考库算法分数当真值。
- 如果未来要 fork，必须 pin commit，而不是靠临时 zip。

## 来源证据

- `nashsu/llm_wiki` 的 ingest、queue、cache、graph、search、API、source lifecycle、vectorstore 模块。

## 标签与量化

- domain: software_architecture / knowledge_system
- problem: reimplementation_risk
- maturity: emerging
- complexity: low
- problem_fit: 5
- reuse_value: 5
- implementation_cost: 1
- integration_fit: 5
- evidence_strength: 4
- reversibility: 5

## 最小实现方式

先为每个高价值参考库新增一份 `outputs/qa/*implementation-extraction.md`，等同类记录超过 3 份后，再考虑抽成正式 `wiki/implementation-notes/` 类型。

## 项目融合建议

当前不新增复杂目录类型。实现级记录先放在 `outputs/qa/`，核心模式进入 `wiki/patterns/`，索引只链接高价值条目。
