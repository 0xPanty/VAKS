---
type: summary
status: captured
created: 2026-05-26
source: "[[2026-05-26-obsidian-ai-orange-book-source]]"
source_status: cross-checked
evidence_level: secondary
confidence: 4
related_patterns:
  - "[[claude-md-index-md-navigation-layer]]"
  - "[[schema-md-as-ai-wiki-contract]]"
  - "[[lifecycle-folders-topic-tags-relationship-links]]"
related_claims:
  - "[[orange-book-is-guide-not-turnkey-vault-template]]"
---

# 架构评审：obsidian-ai-orange-book

## TL;DR

这个仓库比较全，但它全在“书和方法论”层，不是“完整可复制 vault 模板”层。

它对我们最有价值的地方是：系统性验证了我们已经确定的几条主线：

- Markdown vault 是 AI agent 友好的知识底座。
- `CLAUDE.md + index.md` 可以完成大部分上下文导航。
- `raw -> wiki -> output` 是合理的信息编译链。
- `SCHEMA.md` 可以把通用 AI 约束成稳定的 wiki 管理员。
- 文件夹、标签、双链要分工，而不是互相替代。
- Git 是 AI 写入资料库后的审查和回退层。

## 它比较全的地方

### 1. 从问题到工具选择完整

它不是只给目录模板，而是从“信息坟场”问题讲到为什么 Obsidian + Markdown 适合 AI agent 操作。

### 2. 有架构原则

§05 提出六条 vault 设计原则：

- Markdown 作为主要处理格式。
- 术语统一。
- 扁平优先。
- 每条笔记有 summary。
- frontmatter 五字段。
- 区分人的输入和 AI 的产出。

### 3. 有三种目录模板

- 极简型：`daily / notes / projects / archive / CLAUDE.md`
- PARA 型：`1-Projects / 2-Areas / 3-Resources / 4-Archive / daily / CLAUDE.md`
- Karpathy Wiki 型：`raw / wiki / output / SCHEMA.md / CLAUDE.md`

### 4. 有 SCHEMA.md 示例

它把 wiki 分成：

- concepts
- entities
- topics

并规定命名、frontmatter、标签、wikilink、文章结构、全局索引。

### 5. 有工作流和边界

§07 给了日记、读书笔记、调研、写作、项目管理、旧笔记整理、自动 backlinks 等工作流。

§09 补了 Git、Skills、本地 AI、多 Vault。

## 它不够完整的地方

### 1. 仓库不是模板仓库

根目录只有 README、PDF、assets、screenshots。没有实际可复制的：

- `CLAUDE.md`
- `SCHEMA.md`
- `.claude/skills/`
- `.base`
- 示例 notes
- 示例 wiki
- 示例 index

### 2. 对可信度治理不够

它有 `sources` 字段，但没有系统区分：

- source quality
- evidence level
- verification status
- confidence
- conflicting sources
- negative evidence
- next review

这一块我们当前体系更强。

### 3. 对开发项目和 AI 短剧不够定制

它更偏个人知识管理、内容创作和通用研究。对用户的多项目开发、优秀库设计采样、AI 短剧生产，需要二次改造。

### 4. 对 API / gbrain 接入没有展开

它讲 index-first 和 AI 直读，但没有到“Verified Vault API / context pack / agent gbrain 边界”这一层。

## 当前结论

它不是我们的终局模板，但它是一个高质量结构样本。

建议吸收：

- `CLAUDE.md + index.md` 导航层。
- `SCHEMA.md` 作为 wiki contract。
- 生命周期目录 + 主题标签 + 关系双链的三分法。
- Git 审查层。
- Skills 小范围测试原则。

建议不要照搬：

- 纯 Markdown 作为唯一 vault 内容格式。
- 只用 `type: fleeting/literature/permanent` 管所有资料。
- 不带可信度字段的简单 frontmatter。
- 过早相信 RAG 规模边界。

