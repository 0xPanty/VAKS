---
type: pattern
status: candidate
created: 2026-05-27
updated: 2026-05-27
tags:
  - pattern/compiler
  - pattern/incremental
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
adoption_status: adopt-soon
evidence_count: 2
negative_evidence: []
relations:
  - target: "[[2026-05-27-llm-wiki-compiler-implementation-extraction]]"
    type: derived_from
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-26-llm-wiki-compiler-source]]"
    rationale: "Source hashing, source state, affected-source tracking, and frozen slugs are directly reusable for an incremental verified compiler."
    created: 2026-05-27
    last_verified: 2026-05-27
---

# 设计模式：Incremental Source State Compiler

## 一句话定义

用 source hash 和 source state 判断哪些资料需要重新编译，同时追踪共享概念，避免改一个 source 时丢掉其他 source 的贡献。

## 解决的问题

知识库变大后，不能每次都全量重跑 LLM。更危险的是：多个 source 支持同一个结论时，只重编译其中一个 source，会把其他证据从生成结果里“静默抹掉”。

## 适用场景

- raw source 增量入库。
- summary/claim/pattern 重新生成候选。
- source 删除、改名、替换。
- 多 source 支持同一个 claim/pattern。

## 来源证据

`llm-wiki-compiler` 的实现包括：

- `src/compiler/hasher.ts`：SHA-256 hash，分类 new/changed/unchanged/deleted。
- `src/compiler/source-state.ts`：candidate 携带 source state，approve 后再落 state。
- `src/compiler/deps.ts`：概念到 source 的反向索引、affected sources、frozen slugs。
- `src/compiler/prompt-budget.ts`：共享 concept 的 combined source 内容预算。

## 最小实现方式

本资料库可先建立：

```yaml
source_state:
  file:
  hash:
  produced_nodes:
    - node:
      type:
  compiled_at:
  last_candidate:
```

再建立反向索引：

```yaml
node_to_sources:
  claim-or-pattern:
    - source-a
    - source-b
```

## 项目融合建议

v0.2 不必先写完整编译器，但 `outputs/review/candidates/` 里应该保存 source hash 和 produced node。v0.3 再做自动检测 changed sources。

## 验证指标

- 修改一个 source 后，只生成受影响候选。
- 删除一个 source 后，不静默删除已被其他 source 支持的结论。
- 候选批准后才更新 source state。
- 重复运行不会生成重复候选。
