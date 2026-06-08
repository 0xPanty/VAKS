---
type: pattern
status: candidate
created: 2026-05-27
updated: 2026-05-27
tags:
  - pattern/agent-access
  - pattern/mcp
  - verified-knowledge-system
sources:
  - "[[2026-05-26-llm-wiki-compiler-source]]"
  - "[[2026-05-27-llm-wiki-compiler-implementation-extraction]]"
verification_status: primary-source
evidence_level: primary
confidence: high
last_verified: 2026-05-27
next_review: 2026-06-03
source_libraries:
  - atomicstrata/llm-wiki-compiler
adoption_status: adopt
evidence_count: 2
negative_evidence: []
relations:
  - target: "[[verified-vault-api-for-agent-brain]]"
    type: refines
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-27-llm-wiki-compiler-implementation-extraction]]"
    rationale: "Agent API design needs tool-level access classes rather than one flat permission surface."
    created: 2026-05-27
    last_verified: 2026-05-27
---

# 设计模式：Agent Tool Access Tiering

## 一句话定义

Agent 工具必须按读、建议、编译、写入、最终批准分级，而不是给一个万能 API。

## 解决的问题

MCP/API 一旦暴露 ingest、compile、query、read、lint、status，如果没有权限层，就容易让 agent 把候选输出误写成正式知识。

## 来源证据

`llm-wiki-compiler` 的 MCP 层已经区分：

- `read_page`、`lint_wiki`、`wiki_status`：read-only / no provider required。
- `get_context_pack`：read-only，provider optional。
- `compile_wiki`、`query_wiki`、`search_pages`：需要 LLM provider。
- `ingest_source`：会写 `sources/`。
- MCP resources：只读暴露 index/concept/query/sources/state。

## 我们的访问等级

```text
Level 1 read-only:
  read_node
  search_verified
  get_context_pack
  wiki_status
  lint_report

Level 2 suggest-only:
  propose_candidate
  propose_relation
  propose_action

Level 3 reviewed-write:
  approve_candidate
  archive_candidate
  update_index

Level 4 owner-final:
  change_schema
  adopt_decision
  grant_agent_access
```

## 项目融合建议

Misa/gbrain 默认 Level 1；它可以输出 Level 2 candidate，但不能直接 Level 3。

## 验证指标

- API 文档中每个工具都有 access level。
- 默认 agent key 不能改 `SCHEMA.md`、`templates/`、formal `wiki/`。
- 所有写入都进入 candidate 或 review。
