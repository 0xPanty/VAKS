---
type: source
record_kind: source_card
status: source-captured
title: "alchaincyf/obsidian-ai-orange-book"
source_url: "https://github.com/alchaincyf/obsidian-ai-orange-book"
source_type: repo
author: alchaincyf
publisher: GitHub
published_at: 2026-04-11
captured_at: 2026-05-26
captured_by: git-clone-and-pdf-extract
repo_commit: f659934
topics:
  - obsidian
  - claude-code
  - ai-second-brain
  - vault-architecture
  - llm-wiki
projects:
  - 资料库
  - AI短剧
evidence_level: secondary
source_integrity:
  capture_confidence: 4
source_status: cross-checked
verified_by:
  - "GitHub repo README"
  - "PDF text extraction"
  - "kepano/obsidian-skills GitHub"
last_verified: 2026-05-26
next_review:
related_claims:
  - "[[orange-book-is-guide-not-turnkey-vault-template]]"
related_concepts:
  - "[[obsidian-ai-integrated-production-system]]"
  - "[[source-verification-and-trust-model]]"
tags:
  - source/repo
  - obsidian-ai
  - structure-sample
knowledge_status: raw
processing_tier: light
source_id: "https://github.com/alchaincyf/obsidian-ai-orange-book"
why_saved: see_body_or_legacy_record
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
legacy_raw_metadata:
  source_quality: 4
  freshness: 5
  relevance: 5
  cross_source_count: 3
---
# 来源记录：alchaincyf/obsidian-ai-orange-book

## 为什么收录

用户提供该 GitHub 仓库，并说明自己已经 fork，希望判断它的设计思路，以及是否比较完整。

该仓库是一本 Obsidian + Claude Code 橙皮书指南，定位为从零搭建 AI 驱动个人知识管理系统。它不是一个可直接复制的完整 vault 模板仓库，但 PDF 中包含较完整的架构方法、三种目录模板、CLAUDE.md 示例、SCHEMA.md 示例、工作流和进阶建议。

## 仓库事实

- 仓库：`alchaincyf/obsidian-ai-orange-book`
- 本地检查提交：`f659934 docs: add hero animation to README`
- 根目录文件：`README.md`、`README_en.md`、中文 PDF、英文 PDF、`assets/`、`screenshots/`
- 没有实际 `.obsidian/`、`.claude/skills/`、`CLAUDE.md`、`SCHEMA.md`、`.base` 或示例 vault 目录。
- GitHub 页面显示约 956 stars、90 forks、6 commits（2026-05-26 检查）。

## 核心内容

README 将本书定位为“AI 时代的知识管理方法论 + 落地工具”，覆盖：

- 信息坟场问题。
- 为什么选 Obsidian。
- Claude Code 接入。
- Vault 架构。
- Karpathy LLM Wiki 模式。
- 7 个真实工作流。
- 插件生态。
- Git、Skills、本地 AI、多 Vault。

## 已验证内容

- `kepano/obsidian-skills` 当前确实存在，并说明其 Agent Skills 可用于 Obsidian，覆盖 Obsidian Markdown、Bases、JSON Canvas、CLI、Defuddle。
- `obsidian-ai-orange-book` README 中列出的书籍结构和核心洞察与 PDF 抽取内容一致。
- 该书的 `CLAUDE.md + index.md`、`raw -> wiki -> output`、`SCHEMA.md` 等方向与我们前面从 Karpathy / Heinrich / Yanhua 提炼出的方向高度一致。

## 未验证内容

- 书中提到的某些项目 stars、收购、社区数据属于易变信息，需要单独核验。
- “40 万字以内不需要向量数据库”的边界是经验判断，不应当当成硬定律。
- 书中对 `Markdown 是唯一格式` 的建议对纯知识 vault 合理，但对 AI 短剧这种媒体资产密集场景过于严格。

## 可复用点

- `CLAUDE.md + index.md` 作为导航层。
- `SCHEMA.md` 作为 AI 维护 wiki 的宪法。
- 文件夹管生命周期，标签管主题，双链管关系。
- frontmatter 至少包含 title、tags、created、type、summary。
- 区分人的输入和 AI 的产出。
- 先简单，后升级：极简型、PARA 型、Karpathy Wiki 型。
- 用 Git 管理 vault，方便审查 AI 修改和回退。
- 自定义 Skills 要明确触发条件、操作范围、输出格式，并先小范围测试。

## 风险和缺口

- 它是指南型仓库，不是完整模板型仓库。
- 缺少可直接落地的示例 vault、Bases、CLAUDE.md、SCHEMA.md 和 Skills 实体文件。
- 对来源验证、claim 级置信度、负面证据、反模式、gbrain/API 接入没有我们当前体系细。
- 默认结构偏知识管理/内容生产，对开发项目 + AI 短剧还需要改造。

## 当前判断

高信号结构样本。适合作为“前沿完整指南”参考，不适合作为直接照搬的最终架构。

