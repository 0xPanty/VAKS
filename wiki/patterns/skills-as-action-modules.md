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
  - "[[evolvable-design-system]]"
related_projects:
  - 资料库
  - AI短剧
adoption_status: candidate
tags:
  - pattern/skills
  - pattern/action-modules
evidence_count: 4
confidence: medium
negative_evidence:
replaces:
superseded_by:
extension_points:
---

# 设计模式：Skills as Action Modules

## 一句话定义

把常见动作封装成可复用 Skills，让 AI 不只是读和总结资料，还能执行具体生产任务。

## 解决的问题

普通笔记库只能存知识，AI 聊天只能给建议。Skills 把“知道怎么做”变成“可以重复执行的动作模块”。

## 适用场景

- 网页转 Markdown。
- 图片生成/压缩。
- 平台格式转换。
- 内容发布。
- AI 短剧中的角色卡生成、分镜生成、提示词生成、素材归档。

## 不适用场景

- 不稳定、需要频繁人工判断的任务。
- 涉及账号、支付、删除、覆盖等高风险动作。
- 没有明确输入/输出规范的动作。

## 反例与避坑

- 失败条件：Skill 没有权限边界、输入输出、测试样例。
- 相似反模式：所有任务都靠一个巨大 prompt。
- 复杂度风险：Skills 数量增长后难以维护。
- 替代方案：先模板化，再脚本化，最后才自动化。

## 来源证据

- Yanhua 文章描述 16 个 Skills 分为发布、图像生成、内容转换、工具四类。
- cyrilXBT JARVIS 文章把 inbox processing、weekly connections、brief generation、content writing 写成四个 Claude Code skills，验证 skills 可以表达重复工作流。
- Claude Code 官方文档支持用户级和项目级 `.claude/skills/skill-name/SKILL.md`。
- Claudian README 支持 Slash Commands & Skills，并支持 vault-level scopes。

## 标签与量化

- domain: agent-workflow
- problem: repeatable action execution
- maturity: emerging
- complexity: medium
- problem_fit: 5
- reuse_value: 5
- implementation_cost: 3
- integration_fit: 4
- evidence_strength: 4
- reversibility: 4

## 交叉验证

- 相似来源：Heinrich “notes as skills” 类比、Yanhua `.claude/skills/` 实践、Claude Code 官方 Skills 文档。
- 历史项目影子：用户频繁让 AI 执行 repo 分析、handoff、资料落盘。
- 支持证据：当前资料库已经有 templates，可进一步升级成 Skills。
- 反例：Skill sprawl 和权限过大。

## 最小实现方式

先做 2 个低风险 Skills：

```text
source-to-summary
design-point-extractor
```

只读输入、写入受控目录，不碰发布和删除。

## 项目融合建议

采用，但从低风险、可审查、可回退的 Skills 开始。

## 可拓展性

- 可以通过什么接口/适配层接入：`.claude/skills/`、Codex skills、模板脚本。
- 未来可能被什么替代：专用插件或 MCP。
- 替换或升级成本：中。
- 回退方式：保留 Skills 的 Markdown 说明和手动流程。

## 验证指标

- 是否减少重复操作。
- 输出是否稳定符合模板。
- 是否能明确记录来源和验证状态。
