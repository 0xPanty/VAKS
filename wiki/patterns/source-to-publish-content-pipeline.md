---
type: pattern
status: candidate
created: 2026-05-26
updated: 2026-05-27
source_libraries:
  - "[[2026-05-obsidian-claude-ai-superbrain-content-factory-source]]"
  - "[[2026-05-27-jarvis-obsidian-claude-code-source]]"
related_concepts:
  - "[[obsidian-ai-integrated-production-system]]"
  - "[[staged-design-harvest-and-synthesis]]"
related_projects:
  - 资料库
  - AI短剧
adoption_status: candidate
tags:
  - pattern/content-pipeline
  - pattern/ai-production
evidence_count: 3
confidence: medium
negative_evidence:
replaces:
superseded_by:
extension_points:
---

# 设计模式：Source-to-Publish Content Pipeline

## 一句话定义

把信息源摄取、AI 初稿、人工编辑、自动配图、多平台发布和复盘串成一条可重复执行的生产流水线。

## 解决的问题

内容生产往往卡在多个分散环节：素材收集、理解、写稿、配图、格式适配、发布、复盘。这个模式把它们变成可操作的 workflow。

## 适用场景

- X/公众号/小红书多平台内容。
- AI 短剧素材到脚本/分镜/发布的流程。
- 播客、网页、推文、论文转内容。
- 需要稳定复用风格和质量标准的创作系统。

## 不适用场景

- 需要高度人工原创且暂时无固定流程的创作。
- 对平台自动化风险极高的账号。
- 素材质量低、没有可信度治理的内容库。

## 反例与避坑

- 失败条件：只追求速度，不保留人工编辑 gate。
- 相似反模式：自动把 raw 直接发布为成品。
- 复杂度风险：每个平台一套 Skill，维护成本上升。
- 替代方案：先做半自动 pipeline，发布前人工确认。

## 来源证据

- Yanhua 文章给出 Podwise -> Claude 初稿 -> 自动配图 -> X Article 发布的实践案例。
- cyrilXBT JARVIS 文章给出 capture -> connection -> brief -> draft -> published metrics 的内容流水线。
- Karpathy 工作流和我们当前资料库结构支持 raw/wiki/outputs/products 分层。

## 标签与量化

- domain: content-production / ai-drama
- problem: end-to-end production
- maturity: emerging
- complexity: medium
- problem_fit: 5
- reuse_value: 5
- implementation_cost: 3
- integration_fit: 5
- evidence_strength: 3
- reversibility: 4

## 交叉验证

- 相似来源：Yanhua 超级大脑文章、Karpathy raw/wiki/outputs 分层。
- 历史项目影子：用户要做 AI 短剧，并且已有多项目开发需求。
- 支持证据：当前资料库已区分 raw/wiki/outputs/products。
- 反例：全自动发布容易出质量和账号风险。

## 最小实现方式

先建立半自动版本：

```text
raw source
  -> wiki summary/concepts
  -> draft
  -> human edit
  -> product output
  -> outputs/qa or review
```

发布动作先人工执行或人工确认。

## 项目融合建议

作为 AI 短剧和内容创作的核心候选模式。

## 可拓展性

- 可以通过什么接口/适配层接入：Skills、scripts、templates、Obsidian Bases。
- 未来可能被什么替代：专用内容管理系统或自动发布平台。
- 替换或升级成本：中。
- 回退方式：保留 Markdown drafts 和人工发布流程。

## 验证指标

- 单条素材到成品的耗时。
- 人工修改比例。
- 发布后数据表现。
- 是否能追溯到原始资料和决策。
