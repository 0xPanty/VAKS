---
type: pattern
status: candidate
created: 2026-05-27
updated: 2026-05-27
tags:
  - pattern/export
  - pattern/interoperability
  - verified-knowledge-system
sources:
  - "[[2026-05-26-llm-wiki-compiler-source]]"
  - "[[2026-05-27-llm-wiki-compiler-implementation-extraction]]"
verification_status: primary-source
evidence_level: primary
confidence: medium
last_verified: 2026-05-27
next_review: 2026-06-10
source_libraries:
  - atomicstrata/llm-wiki-compiler
adoption_status: watch
evidence_count: 2
negative_evidence: []
relations:
  - target: "[[2026-05-27-quality-bar-extensible-verified-action-knowledge-system]]"
    type: supports
    strength: 3
    confidence: medium
    evidence:
      - "[[2026-05-27-llm-wiki-compiler-implementation-extraction]]"
    rationale: "Export surfaces make the knowledge system usable by downstream tools without binding to one runtime."
    created: 2026-05-27
    last_verified: 2026-05-27
---

# 设计模式：Exportable Knowledge Artifact Surface

## 一句话定义

知识系统应该能导出多种机器可读 artifact，让模型、图谱工具、前端 viewer、产品生成器都能复用。

## 解决的问题

如果知识只能在一个 app 里读，就会被运行时锁死。导出层让主记录仍然是 Markdown，但下游可以吃 JSON、GraphML、llms.txt、context pack。

## 来源证据

`llm-wiki-compiler` 支持：

- `llms.txt`
- `llms-full.txt`
- JSON
- JSON-LD
- GraphML
- Marp

导出时过滤 orphaned / untitled pages，并把 page metadata、sources、tags、links、body 标准化。

## 我们的导出层

```text
llms.txt              # model-readable index
json/jsonl            # agent and scripts
graphml               # graph analysis tools
context-pack bundles  # agent runtime
decision-pack bundles # action basis
product packs         # content production
feedback packs        # field-test and action results
```

## 项目融合建议

暂时 watch，不急着实现。等 formal node schema 稳定后再做导出，否则会输出不稳定字段。

## 验证指标

- 导出不包含 pending candidate。
- 导出不包含 rejected/deprecated 节点，除非显式 include。
- 导出保留 provenance、verification、relations、actionability。
