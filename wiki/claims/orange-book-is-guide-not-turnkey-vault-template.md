---
type: claim
status: cross-checked
claim: "obsidian-ai-orange-book is a high-quality guide and architecture sample, not a turnkey vault template."
created: 2026-05-26
topics:
  - obsidian-ai-orange-book
  - vault-template
  - architecture-sample
related_projects:
  - 资料库
sources:
  - "[[2026-05-26-obsidian-ai-orange-book-source]]"
supporting_sources:
  - "GitHub repo file tree"
  - "PDF extracted architecture chapters"
conflicting_sources:
evidence_level: primary
verification_status: cross-checked
confidence: 5
impact: 4
last_verified: 2026-05-26
next_review:
tags:
  - claim/high-signal
  - template/evaluation
---

# 主张：Orange Book is guide, not turnkey vault template

## 主张

`alchaincyf/obsidian-ai-orange-book` 是高质量指南和架构样本，但不是可直接 fork 后作为完整 vault 使用的模板仓库。

## 为什么重要

用户问它是否比较全。准确回答是：方法论和章节覆盖比较全；仓库结构本身不全。不能把它当成完整模板照搬，但可以提炼其中的结构原则。

## 支持证据

- 仓库根目录只有 README、PDF、assets、screenshots。
- 没有实际 `CLAUDE.md`、`SCHEMA.md`、`.claude/skills/`、`.base`、示例 notes/wiki。
- PDF 中确实包含三种 vault 模板、SCHEMA.md 示例、CLAUDE.md 示例和工作流。

## 反例 / 冲突证据

- 如果用户只需要一本操作手册，它确实比较完整。
- 如果用户要的是直接运行的 vault starter，它不完整。

## 标签与量化

- evidence_level: primary
- verification_status: cross-checked
- confidence: 5
- impact: 4
- relevance: 5

## 验证方式

本地浅克隆仓库并查看文件树；抽取 PDF 文本查看实际内容。

## 当前结论

作为结构样本采用，作为模板仓库不采用。

## 复查计划

如果作者后续发布可复制 vault starter，再复查。

