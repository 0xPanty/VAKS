---
type: source
status: source-captured
title: "如何基于 Obsidian 和 Claude 打造 AI 时代超级大脑？"
source_url:
source_type: article
author: Yanhua
publisher:
published_at:
captured_at: 2026-05-26
captured_by: user-paste
topics:
  - obsidian
  - claude-code
  - claudian
  - skills
  - content-factory
  - ai-production-pipeline
projects:
  - 资料库
  - AI短剧
evidence_level: anecdotal
source_status: single-source
source_quality: 4
freshness: 4
relevance: 5
confidence: 4
cross_source_count: 2
verified_by:
  - "Claudian GitHub README"
  - "Claude Code official docs for skills and permissions"
last_verified: 2026-05-26
next_review:
related_claims:
  - "[[purpose-specific-vaults-change-the-system-goal]]"
  - "[[skills-turn-knowledge-vaults-into-action-systems]]"
related_concepts:
  - "[[obsidian-ai-integrated-production-system]]"
  - "[[purpose-specific-vault-philosophy]]"
  - "[[evidence-backed-design-validation]]"
tags:
  - source/obsidian-ai
  - source/content-factory
  - status/single-source
---

# 来源记录：Obsidian + Claude 超级大脑内容工厂

## 为什么收录

这篇是 Yanhua 基于 Heinrich “thinking OS” 文章做出的实践转化：从深度思考 vault，转向程序员 + 多平台内容创作者需要的内容生产流水线。

它对当前资料库特别重要，因为它验证了一个高信号方向：

```text
同一个底层模式：Markdown vault + AI agent + instructions + skills
可以根据目的变成不同系统：
thinking vault / work vault / research vault / content factory / AI短剧生产台
```

## 核心内容

作者认为 Heinrich 的 thinking vault 不完全适合自己，因为自己的需求不是单纯深度思考，而是多平台内容创作。因此他把 Obsidian + Claude Code + Claudian + Skills + CLAUDE.md 组合成一条内容生产流水线。

核心三层：

```text
Obsidian = 容器，承载知识、Markdown、目录结构
Claude Code + Claudian = 智能，负责读、想、做
Skills = 双手，执行图片生成、发布、格式转换等任务
CLAUDE.md = 操作手册，编码身份、偏好、规则、工作流
```

## 来源信息

- 作者：Yanhua
- 发布方：未提供
- 发布时间：未提供
- 原始链接：未提供
- 采集方式：用户粘贴全文 + 截图

## 标签与量化

- source_type: article
- evidence_level: anecdotal
- source_status: single-source
- source_quality: 4
- freshness: 4
- relevance: 5
- confidence: 4
- cross_source_count: 2

## 已验证内容

- Claudian GitHub README 描述其可把 Claude Code、Codex、Opencode 等 agent 嵌入 Obsidian vault，并支持读写、搜索、bash、多步工作流、Skills、BRAT 安装等能力。
- Claude Code 官方文档确认 Skills 可放在项目级 `.claude/skills/`，并通过 `SKILL.md` 让 agent 在合适场景加载能力。
- Claude Code 官方权限文档确认有 permission modes 和 bypass/accept edits 等机制，因此文章的 yolo/自动批准方向在机制上成立，但风险需要单独管理。

## 未验证内容

- 作者自定义 16 个 Skills 的具体实现质量。
- X/公众号/小红书发布 Skills 的稳定性、平台合规性和账号风险。
- “30 分钟从播客到带图长文发布”的效率是否可普遍复现。
- 图像生成和自动配图质量是否稳定。

## 冲突或疑点

- `yolo` 权限适合成熟用户和受控 vault，不适合新系统默认开启。
- 浏览器自动发布受平台 UI、登录状态、风控影响，应该视为脆弱自动化。
- 内容工厂容易牺牲质量，需要保留人工编辑/判断 gate。
- `.claude/skills/` 变多后需要版本、权限、测试和回退管理。

## 可复用点

- 把 Heinrich 的 thinking OS 转化成 purpose-specific content factory，强力支持“每个 vault 需要自己的 philosophy”。
- Skills 不只是知识注入，也可以是行动模块。
- CLAUDE.md 的价值是把身份、读者、偏好、工作流、错误教训文字化。
- 从播客/网页/X 到文章/配图/发布的流水线，可迁移到 AI 短剧生产。
- 人的角色从“写所有内容”转向“判断、编辑、策展和质量把关”。

## 下一步

- 如果拿到原文链接，补充 `source_url` 和发布时间。
- 将 “内容生产流水线” 映射到 AI 短剧：素材摄取、世界观编译、剧本生成、分镜、图像/视频、发布复盘。
- 对发布自动化、yolo 权限和 skill sprawl 建立反模式与验证 gate。

