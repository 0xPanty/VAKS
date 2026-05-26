---
type: summary
status: captured
created: 2026-05-26
source: "[[2026-01-thinking-os-with-ai-vault-source]]"
source_status: single-source
evidence_level: anecdotal
confidence: 3
related_patterns:
  - "[[agentic-vault-orientation-index]]"
  - "[[purpose-specific-vault-philosophy]]"
  - "[[composable-claim-notes]]"
related_claims:
  - "[[vault-index-guides-context-loading]]"
  - "[[each-vault-needs-purpose-specific-philosophy]]"
---

# 摘要：Operating system for thinking with AI

## 核心结论

这篇文章把 Obsidian vault 描述成一种“AI 思考操作系统”：AI 不是单纯帮人写作，而是在 Markdown vault 中导航、提取概念、连接已有理解、按需注入上下文，并逐步形成用户思考方式的活体表示。

## 和我们已有方向的碰撞

高信号重合：

- 和 `raw -> wiki -> outputs` 的知识编译模型一致。
- 和“第二大脑知识图谱”一致：笔记价值来自关系，而不是单点内容。
- 和“索引优先，不全量塞上下文”一致：vault index 帮 agent 决定读哪些 notes。
- 和“每个系统需要自己的规则”一致：每个 vault 要有自己的 philosophy 和 CLAUDE.md。
- 和“可拓展系统”一致：Markdown 是底座，工具只是窗口。

## 新增可提炼设计点

1. Vault index 是上下文路由器。
2. Topic pages / MOCs 不只是目录，还可以保存 agent 的导航 breadcrumb。
3. 笔记标题用 claim 风格，让链接自然成为句子的一部分。
4. 笔记要可组合：从任何入口进入都能独立理解。
5. 每个 vault 的 philosophy 应按目的定制，工作 vault、研究 vault、创意 vault 不应套同一套规则。

## 风险和反例

- CLAUDE.md 过长可能变成规则垃圾堆。
- 让 agent 自动写 breadcrumb 可能污染 topic page。
- “每条笔记都是 skill”是类比，不能机械化理解为每条笔记都要做成执行脚本。
- 一月的工具配置细节可能过时，需要用官方文档复核。

## 当前判断

高信号，值得进入我们的设计采样池。

但这篇是单来源经验分享，应该作为 `candidate`，不是最终事实。可采纳的是架构思想，不是直接照搬目录和 hooks。

