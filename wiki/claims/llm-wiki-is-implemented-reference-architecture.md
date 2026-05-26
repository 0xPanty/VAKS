---
type: claim
status: verified
claim: nashsu/llm_wiki is an implemented reference architecture, not merely an Obsidian template.
created: 2026-05-26
topics:
  - llm-wiki
  - reference-architecture
  - knowledge-base
related_projects:
  - verified-vault
sources:
  - raw/repos/2026-05-26-llm-wiki-source.md
supporting_sources:
  - https://github.com/nashsu/llm_wiki
conflicting_sources:
evidence_level: primary
verification_status: code-inspected
confidence: 4
impact: 5
last_verified: 2026-05-26
next_review: 2026-06-26
tags:
  - implemented
  - source-inspected
  - high-signal
---

# 主张 / 结论：llm_wiki 是实现级参考架构

## 主张

`nashsu/llm_wiki` 不是一套纯 Obsidian 架构模板，也不是单篇方法论文章，而是 Karpathy LLM Wiki 模式的实现级参考架构。

## 为什么重要

我们之前看的资料更多是设计思路或指南。这个 repo 给出了实际工程做法，可以拿来验证我们的方向，也能拆出可落地的最小实现。

## 支持证据

- `package.json` 显示完整前端应用和图谱依赖。
- `src-tauri/src/api_server.rs` 实现本地 API、限流、安全路径、文件读取、搜索、图谱、source rescan。
- `src/lib/graph-relevance.ts` 实现四信号关系评分。
- `src/lib/graph-insights.ts` 实现知识缺口和意外连接检测。
- README 描述完整桌面应用、ingest、review、graph、API。

## 反例 / 冲突证据

- 没有运行 app 做端到端体验验证。
- Chat API 在 Rust API server 中尚未实现，不能把它当成完整 agent chat 后端。
- 作为直接可复制的 Obsidian vault 模板，它并不合适。

## 标签与量化

- evidence_level: primary
- verification_status: code-inspected
- confidence: 4
- impact: 5
- relevance: 5

## 验证方式

后续可以运行 app，导入小型资料集，检查：

- ingest 质量
- graph 关系是否合理
- API 返回是否适合 Agent context pack
- review 队列是否真的能减少低质量写入

## 当前结论

作为方向验证和设计提炼，高价值。作为直接照搬对象，暂不采用。

## 复查计划

当我们的 vault 节点超过 50 个后，再复查是否需要引入脚本版四信号评分或本地 API。
