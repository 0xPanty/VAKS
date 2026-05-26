---
type: anti_pattern
status: watch
created: 2026-05-26
domain: agent-instructions
failure_mode: always-on instruction bloat
severity: 4
likelihood: 4
complexity_cost: 4
cross_validated_with:
  - "Claude Code memory docs recommend concise instructions and on-demand topic files"
related_projects:
  - 资料库
replacement: "核心规则保持短，详细知识放索引、topic pages、skills 或按需读取文件"
decision: limited-use
---

# 反模式 / 踩坑：过度膨胀的常驻指令

## 问题描述

文章提到作者的 CLAUDE.md 约 2000 行，并持续把哲学、规则、经验写进去。这个方向有价值，但如果不分层，常驻指令会变成规则垃圾堆。

## 为什么不可行

过长的常驻指令会增加上下文负担，也可能降低规则遵循稳定性。很多细节更适合放在 topic pages、skills、templates 或索引里，按需读取。

## 失败条件

- 把所有经验都塞进 CLAUDE.md。
- 规则互相冲突。
- 没有分层：核心原则、执行流程、参考资料混在一起。
- AI 每次启动读太多与当前任务无关的内容。

## 标签与量化

- domain: agent-instructions
- failure_mode: instruction bloat
- severity: 4
- likelihood: 4
- complexity_cost: 4
- evidence_strength: 3
- reversibility: 4

## 交叉验证

- 相似失败来源：Claude Code 官方 memory 文档提到更短的指令通常更容易遵循，详细 topic 文件应按需读取。
- 历史项目证据：长上下文容易带来上下文污染和恢复偏航。
- 支持证据：当前资料库已采用 handoff + indexes + templates + concepts 分层，而不是一个巨型说明文件。
- 是否可能只是局部失败：是。成熟用户可以维护长 CLAUDE.md，但不适合作为第一阶段默认方案。

## 应该避开什么

- 不要把资料库所有哲学、模板、规则都塞进一个文件。
- 不要把“作者 2000 行 CLAUDE.md”当作目标。

## 替代方案

```text
README / CLAUDE.md：短核心规则
wiki/indexes/：入口和地图
wiki/concepts/：稳定概念
templates/：可复用结构
outputs/qa/：问答沉淀
```

## 后续是否需要复测

当资料库有 50+ 核心节点后，测试是否需要拆分或新增子目录规则。

