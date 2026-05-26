---
type: pattern
status: candidate
created: 2026-05-26
source_libraries:
  - SIXIANGGUO/cc-note-ops
related_concepts:
  - obsidian-ai-integrated-production-system
  - skills-as-action-modules
  - source-to-publish-content-pipeline
related_projects:
  - verified-vault
  - content-production
adoption_status: adapt
tags:
  - obsidian
  - operation-layer
  - content-workbench
  - safe-ai-actions
evidence_count: 3
confidence: high
negative_evidence:
  - full-app-overengineering-before-clean-markdown-vault
---

# 设计模式：当前笔记操作台

## 一句话定义

在 Obsidian 中围绕“当前打开的源笔记”提供一组安全 AI 操作按钮，让 AI 可以生成内容、整理结构、补标签双链或修改原文。

## 它在我们架构里的位置

它不属于资料库核心层，也不属于知识图谱层。

它属于操作层：

```text
raw / wiki / claims / patterns
  -> 当前笔记操作台
  -> AI 执行动作
  -> outputs / products / reviewed edits
```

## 主要用途

1. 降低 AI 操作门槛。
   - 不需要每次复制路径、写 prompt、切终端。
   - 常用动作变成固定按钮。

2. 防止改错文件。
   - 锁定源笔记。
   - 排除运行结果和备份目录。
   - 适合作为以后 Agent 操作 vault 的安全边界。

3. 区分“生成输出”和“修改原文”。
   - 输出类任务只写新文件。
   - 修改类任务必须先备份。
   - 这对我们的资料库很重要，因为 verified knowledge 不能被随便覆盖。

4. 区分“表达型任务”和“结构化任务”。
   - 公众号、小红书、润色可以读取文风。
   - 摘要、标签、双链、路标不读文风，保持结构化和客观。

## 对我们有什么价值

它解决的不是“知识怎么组织”，而是“知识怎么被操作”。

适合未来用于：

- 把一篇 raw/source 快速生成摘要路标。
- 把一篇资料转成小红书/公众号/短视频脚本草稿。
- 对某篇笔记补标签、双链、frontmatter。
- 把当前笔记送进 review 或 health 检查。
- 给 AI 短剧素材做一键拆解：角色、冲突、场景、镜头、台词。

## 不适合做什么

- 不适合当第二大脑核心。
- 不适合替代 source verification。
- 不适合自动修改高价值知识节点。
- 不适合在没有 diff/review 的情况下批量改文件。

## 来源证据

`SIXIANGGUO/cc-note-ops` 源码确认了三点：

- 当前笔记锁定：`main.js` 记录 `sourceNotePath`，并排除 `控制中心/运行结果/` 和 `控制中心/备份/`。
- 输出/修改分离：`data.json` 用 `kind: output` / `kind: modify` 区分任务，`note-action.sh` 修改前先备份。
- 表达/结构分离：`usesProfile: true/false` 控制是否读取文风模板。

## 标签与量化

- domain: obsidian_ai_ops
- problem: safe_note_action
- maturity: emerging
- complexity: low
- problem_fit: 4
- reuse_value: 4
- implementation_cost: 2
- integration_fit: 4
- evidence_strength: 4
- reversibility: 5

## 融合建议

可加入我们的架构，但只能作为操作层。

短期不需要照搬插件；可以先吸收三条规则：

- 当前任务必须绑定 source note。
- 输出任务和修改任务必须分离。
- 表达型任务可以读文风，结构化任务不读文风。

## 验证指标

- 是否减少复制路径和重复 prompt。
- 是否避免 AI 改错文件。
- 是否让内容生产更快进入 outputs/products。
- 是否仍能保持资料库核心节点的可信度。
