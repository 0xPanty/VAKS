---
type: concept
status: active
created: 2026-05-26
aliases:
  - Obsidian AI 一体化生产系统
  - 知识生产闭环
  - 开发与短剧生产系统
related:
  - "[[second-brain-knowledge-graph]]"
  - "[[staged-design-harvest-and-synthesis]]"
  - "[[evolvable-design-system]]"
---

# Obsidian + AI 一体化生产系统

## 定义

Yanhua 的 Obsidian + AI 系列和 Karpathy 的 LLM Knowledge Bases 思路不冲突，应该被理解为同一套系统的不同层。

它们不是四套方案，而是一条完整生产链：

```text
信息摄取
  -> 知识编译
  -> AI 上下文激活
  -> 工作流执行
  -> 成品输出
  -> 复盘和健康检查
```

## 四篇内容的分工

### 1. Podwise 文章：信息摄取层

定位：

```text
音频/播客/视频 -> 转录 -> 结构化 Markdown -> raw/
```

价值：

- 把碎片化音频内容变成可检索、可编译的原始资料。
- 适合 AI 短剧、项目调研、行业播客、访谈内容摄取。
- 注意：Podwise 摘要不能替代原始转录，原文和时间戳仍要保留。

状态：

- 目前只看到标题级定位和 Karpathy 文章里的引用说明，尚未完整读取全文。

### 2. Karpathy / LLM Knowledge Bases 文章：知识编译治理层

定位：

```text
raw/ 原始资料 -> LLM 编译 -> wiki/ 知识条目 -> outputs/ 问答和健康检查
```

价值：

- 把资料库从收藏夹变成知识编译系统。
- 强调分层、增量、可追溯、健康检查。
- 这是当前资料库的底层治理框架。

已提炼：

- `raw / wiki / outputs` 三层结构。
- LLM 作为知识编译器。
- 问答落文件。
- 健康检查。
- 小规模阶段先用索引，不急着上 RAG。

### 3. Obsidian + Claude Code 上下文文章：上下文激活层

定位：

```text
Obsidian vault -> AI 可读取的长期上下文 -> 更贴近用户历史和项目的回答
```

价值：

- 笔记库不只是存储，而是 AI 的上下文底座。
- 让 AI 在回答时能看到历史项目、概念、决策、踩坑、设计点。
- 对用户的“第二大脑知识图谱”方向非常关键。

状态：

- 目前只看到标题级定位和 Karpathy 文章里的引用说明，尚未完整读取全文。

### 4. 超级大脑文章：工作流执行层

定位：

```text
Obsidian + Claude Code / Claudian + CLAUDE.md + Skills -> 内容生产流水线
```

价值：

- 把笔记库从思考系统推进到可执行流水线。
- `CLAUDE.md` 固化身份、偏好、质量标准、工作流和 Skills 使用规则。
- Skills 让 AI 不只是“会想”，而是能执行具体动作，如网页转 Markdown、配图、发布。
- 内容生产可以从原始素材走到多平台成品。

已知来源提到的核心结构：

```text
Obsidian = 容器
Claude Code / Claudian = 智能
Skills = 双手
CLAUDE.md = 操作手册和协作规则
```

## 是否冲突

不冲突。

它们回答的是不同问题：

```text
资料怎么进来？       -> Podwise / Web Clipper / URL to Markdown
资料怎么变知识？     -> LLM 编译 raw 到 wiki
知识怎么给 AI 用？   -> Vault 作为上下文
AI 怎么真的干活？    -> Claude Code / Claudian / Skills / 工作流
成品怎么沉淀？       -> products + outputs + health
```

## 需要防的冲突

### 内容工厂和知识库混在一起

风险：

- 成品文章、短剧脚本、X、小红书、公众号内容和 wiki 概念混在一起，会污染知识库。

处理：

- `wiki/` 放自用知识。
- `products/` 放面向读者或平台的成品。

### 上下文全量塞给 AI

风险：

- AI 读太多会产生上下文污染，判断变差。

处理：

- 先读索引，再读相关原文。
- 用 `wiki/indexes/` 做入口，不要无脑全量喂。

### Podwise 摘要替代原始材料

风险：

- 自动摘要可能漏细节、漏语气、漏上下文。

处理：

- 原始转录放 `raw/`。
- 摘要和概念提炼放 `wiki/`。

### 自动化权限过激

风险：

- 一键发布、yolo 权限、自动改文件在早期可能误操作。

处理：

- 前期人工确认。
- 稳定后再逐步自动化。
- 关键发布动作需要确认和回退记录。

## 对用户当前资料库的落地形态

```text
raw/
  articles/
  podcasts/
  x/
  papers/
  repos/

wiki/
  indexes/
  concepts/
  summaries/
  patterns/
  decisions/

outputs/
  qa/
  health/
  reviews/

products/
  x/
  公众号/
  小红书/
  ai-drama/
```

## 当前判断

这四篇内容可以融合成一个系统，但融合方式不是揉成一个大模板，而是分层协作：

- Podwise 负责摄取。
- Karpathy 思路负责编译治理。
- Obsidian + Claude Code 上下文负责长期记忆和调用。
- 超级大脑文章负责执行流水线和内容生产。

最终目标是服务用户的开发项目和 AI 短剧生产，而不是单纯模仿作者的内容工厂。

## 待补

- 完整读取《Obsidian + Claude Code：你的笔记库就是你最强大的 AI 上下文》。
- 完整读取《我用 Podwise 把播客变成了可检索的知识库》。
- 如果全文可获得，再分别写入 `wiki/summaries/`，并提取具体可验证设计点。

