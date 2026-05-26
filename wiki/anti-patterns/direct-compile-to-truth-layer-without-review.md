---
type: anti-pattern
status: active
created: 2026-05-26
updated: 2026-05-26
tags:
  - anti-pattern/llm-ingest
  - anti-pattern/truth-layer
  - verified-knowledge-system
sources:
  - "[[2026-05-26-llm-wiki-compiler-source]]"
  - "[[2026-05-26-llm-wiki-compiler-architecture-review]]"
  - "[[automatic-agentic-vault-rewrite-before-schema-stability]]"
verification_status: cross-checked
evidence_level: synthetic
confidence: high
last_verified: 2026-05-26
next_review: 2026-06-02
epistemic_type: take
holder: Codex
valid_from: 2026-05-26
valid_until:
gaps: []
evidence_timeline:
  - date: 2026-05-26
    event: "Karpathy pattern supports LLM-maintained wiki, but llm-wiki-compiler shows why review mode is needed before formal write."
domain: verified-knowledge-system
failure_mode: "LLM output becomes formal truth without review."
severity: 5
likelihood: 4
complexity_cost: 4
cross_validated_with:
  - "[[automatic-agentic-vault-rewrite-before-schema-stability]]"
  - "[[review-gated-compile-queue]]"
related_projects:
  - verified-knowledge-system
replacement: "[[review-gated-compile-queue]]"
decision: avoid
relations:
  - target: "[[review-gated-compile-queue]]"
    type: alternative_to
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-26-llm-wiki-compiler-source]]"
    rationale: "Review-gated compile preserves AI speed while preventing direct truth-layer mutation."
    created: 2026-05-26
    last_verified: 2026-05-26
---

# 反模式 / 踩坑：Direct Compile To Truth Layer Without Review

## 问题描述

LLM 读取 raw source 后，直接把 summary/claim/pattern/decision 写进正式 `wiki/`，并让后续 agent 把这些内容当作 verified truth。

## 为什么不可行

这会混淆三件事：

- LLM 提炼了什么。
- 证据实际支持什么。
- 资料库正式采纳了什么。

普通 LLM Wiki 可以接受“先编译，再慢慢修”。但 verified knowledge system 不行，因为正式节点会参与后续决策、context pack 和 agent 推理。

## 失败条件

- claim 没有 source 或 source span。
- pattern 没有不适用场景和反例。
- decision 没有风险、回退和替代方案。
- 低 confidence 或 contradicted 内容进入 active 状态。
- 外部 agent 能直接改 `SCHEMA.md`、`wiki/` 或 `templates/`。

## 标签与量化

- domain: verified_knowledge_system
- failure_mode: trust_layer_pollution
- severity: 5
- likelihood: 4
- complexity_cost: 4
- evidence_strength: 4
- reversibility: 2

## 交叉验证

- Karpathy LLM Wiki 验证了 raw/wiki/schema 的操作模式，但没有单独解决 verified truth layer。
- `llm-wiki-compiler` 引入 `compile --review`，说明工程实现层也需要写入前审查。
- obsidian-second-brain 的自动 rewrite 在 schema 未稳定前也被记录为反模式。

## 应该避开什么

- 不要让 Misa/gbrain 直接写正式 `wiki/`。
- 不要让 query/save 自动生成的答案直接进入 claim/decision。
- 不要用向量检索结果自动补 relation。
- 不要把 `confidence` 当作唯一 gate。

## 替代方案

采用 [[review-gated-compile-queue]]：

```text
LLM output -> review candidate -> lint -> review -> formal node
```

## 后续是否需要复测

需要。等我们实现第一版 candidate queue 和 lint 后，复测这个反模式是否还会通过人工流程漏进正式库。
