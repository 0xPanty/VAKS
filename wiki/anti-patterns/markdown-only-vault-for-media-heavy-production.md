---
type: anti_pattern
status: limited-use
created: 2026-05-26
domain: vault-architecture
failure_mode: over-strict markdown-only rule for media-heavy workflows
severity: 3
likelihood: 4
complexity_cost: 3
cross_validated_with:
  - "[[2026-05-26-obsidian-ai-orange-book-source]]"
  - "AI短剧 production requirements"
related_projects:
  - 资料库
  - AI短剧
replacement: "Keep source metadata and extracted text in Markdown, store heavy media in attachments/assets with clear source records."
decision: limited-use
---

# 反模式 / 踩坑：媒体密集生产中机械执行 Markdown-only

## 问题描述

Orange Book 建议 vault 里只放 Markdown，PDF、音频、视频等原始文件放在 vault 外。这对纯知识管理很干净，但对 AI 短剧和内容生产可能过于严格。

## 为什么不可行

AI短剧需要图片、音频、视频、分镜参考、角色图、素材源文件。如果完全把媒体排除在 vault 外，资料库会失去资产管理能力。

## 失败条件

- 只保留 Markdown 摘要，不保留媒体资产路径。
- 生成内容和素材来源断链。
- AI 只看到文本，看不到视觉/声音资产上下文。

## 标签与量化

- domain: vault-architecture
- failure_mode: media provenance loss
- severity: 3
- likelihood: 4
- complexity_cost: 3
- evidence_strength: 3
- reversibility: 4

## 交叉验证

- 相似失败来源：内容生产和短剧工作流天然需要附件资产。
- 历史项目证据：用户明确要做 AI短剧。
- 支持证据：当前资料库已有 `products/`，后续会有素材和成品。
- 是否可能只是局部失败：是。纯研究 vault 可以严格 Markdown-only。

## 应该避开什么

- 不要把“vault 只存 Markdown”当绝对规则。
- 不要让附件没有 metadata。

## 替代方案

```text
Markdown 记录：
  source metadata
  extracted text
  transcript
  prompt
  license
  usage rights
  generated asset path

媒体文件：
  attachments/
  assets/
  products/
```

## 后续是否需要复测

等开始 AI 短剧素材库时，设计 media asset template 和 license/copyright fields。

