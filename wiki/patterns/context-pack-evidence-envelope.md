---
type: pattern
status: pattern-candidate
created: 2026-05-26
updated: 2026-05-26
tags:
  - pattern/context-pack
  - pattern/agent-api
  - verified-knowledge-system
sources:
  - "[[2026-05-26-llm-wiki-compiler-source]]"
  - "[[2026-05-26-llm-wiki-compiler-architecture-review]]"
  - "[[verified-vault-api-for-agent-brain]]"
verification_status: primary-source
evidence_level: primary
confidence: high
last_verified: 2026-05-26
next_review: 2026-06-02
epistemic_type: take
holder: Codex
valid_from: 2026-05-26
valid_until:
gaps:
  - "Need a minimal context pack JSON schema for this vault."
  - "Need to decide whether Misa receives source windows by default. Current answer: no."
evidence_timeline:
  - date: 2026-05-26
    event: "llm-wiki-compiler source review found get_context_pack and context v1 envelope."
source_libraries:
  - atomicstrata/llm-wiki-compiler
related_concepts:
  - "[[verified-vault-api-for-agent-brain]]"
  - "[[local-verified-vault-api]]"
related_projects:
  - verified-knowledge-system
  - misa-hermes
adoption_status: adopt-soon
evidence_count: 3
negative_evidence: []
relations:
  - target: "[[verified-vault-api-for-agent-brain]]"
    type: implements
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-26-llm-wiki-compiler-source]]"
    rationale: "Context pack is the safest API shape for giving agents evidence without write access."
    created: 2026-05-26
    last_verified: 2026-05-26
---

# 设计模式：Context Pack Evidence Envelope

## 一句话定义

给 agent 的不是整库权限，也不是最终答案，而是一个结构化、只读、可预算、带 citation/warnings/gaps 的证据包。

## 解决的问题

Agent 直接读整个 vault 会过载，直接查向量库又可能把候选召回当真。context pack 把两者中间的层做清楚：

```text
agent prompt -> retrieve candidates -> package evidence -> agent reasons with boundaries
```

它服务的是“准备上下文”，不是“裁决真相”。

## 适用场景

- Misa/gbrain 需要回答“我知道什么关于 X”。
- Hermes/agent 在 VPS 上需要读取资料库，但不能改资料库。
- Codex 需要为某个设计决策加载最相关 source/claim/pattern/decision。
- 未来 API/MCP resolver。

## 不适用场景

- 需要更新正式 wiki 节点时。
- 需要自动冲突裁决时。
- 没有足够 verified node，只有 raw source 时。

## 来源证据

`llm-wiki-compiler` 的 context pack v1 包含 `prompt`、`budget`、`project`、`primary`、`neighbors`、`warnings`、`gaps`、`suggestedActions`。MCP 的 `get_context_pack` 明确用于打包 evidence，`query_wiki` 才用于生成 answer。

## 最小实现方式

本资料库的 context pack v0.1 可以先定义为：

```yaml
version: 1
query:
budget:
generated_at:
verification_boundary:
primary_nodes: []
supporting_sources: []
relations: []
warnings: []
gaps: []
suggested_actions: []
source_windows: []
```

默认规则：

- `source_windows` 默认空。
- raw snippets 只有显式 `include_sources=true` 才返回。
- pack 必须包含 warnings/gaps，不能只返回“看起来相关”的内容。
- pack 不写回 wiki。

## 项目融合建议

这是我们给 Misa/gbrain 的 API 形状：Misa 读 context pack，产出候选建议；Codex/用户决定是否入库。

## 验证指标

- agent 是否能在不读全库的情况下拿到足够上下文。
- pack 是否显示低置信、冲突、待复查、缺证据。
- source windows 是否默认关闭。
- pack 是否能解释为什么某个节点被召回。
