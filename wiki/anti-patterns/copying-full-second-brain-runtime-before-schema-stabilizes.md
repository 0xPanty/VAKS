---
type: anti-pattern
status: draft
created: 2026-05-26
source_libraries:
  - garrytan/gbrain
related_patterns:
  - markdown-system-of-record-derived-indexes
  - schema-packs-as-living-contract
related_projects:
  - verified-knowledge-system
tags:
  - overengineering
  - runtime
  - schema-first
confidence: high
evidence_count: 1
---

# 反模式：Schema 未稳就复制完整第二大脑 runtime

## 一句话定义

在资料库核心 schema、晋级流程、验证门槛还没稳定前，直接 fork 或重写 gbrain 级别的 DB/MCP/minions/scheduler/OAuth/runtime。

## 为什么危险

这会把当前任务从“设计 verified knowledge system”变成“维护一个完整产品栈”。系统看起来更强，但真实问题没有变简单：source、claim、pattern、decision 仍然没有统一契约。

## 失败条件

- 先上 DB/index/API，后补 schema。
- AI 自动抽取大量 facts/takes，但没有人工审查和采纳门槛。
- 图谱和检索分数被误当 truth。
- 维护成本超过知识增益。

## gbrain 给的警示

gbrain 的实现很成熟，但它包含产品级能力：CLI、MCP、OAuth、company brain、minions、cycle locks、query cache、multi-source、schema packs、vector index、reranker、scheduler。对当前阶段来说，这些大多是未来扩展层，不是第一步。

## 更稳的替代方案

1. 先做 `SCHEMA.md`。
2. 手工跑通 source -> summary -> claim/pattern/anti-pattern -> decision。
3. 加 health check。
4. 再做半自动 AI compile。
5. 最后才考虑 local API / retrieval / runtime。

## 回退方式

如果某个外部系统实现过重，只保留：

- file shape
- invariant
- relation type
- validation gate
- failure mode

不保留 runtime。

