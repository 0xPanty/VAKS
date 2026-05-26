---
type: pattern
status: pattern-candidate
created: 2026-05-26
updated: 2026-05-26
tags:
  - pattern/review
  - pattern/llm-ingest
  - verified-knowledge-system
sources:
  - "[[2026-05-26-llm-wiki-compiler-source]]"
  - "[[2026-05-26-llm-wiki-compiler-architecture-review]]"
  - "[[2026-04-04-karpathy-llm-wiki-pattern]]"
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
  - "Need a local candidate file example for this vault."
  - "Need a lint implementation before this becomes active."
evidence_timeline:
  - date: 2026-05-26
    event: "llm-wiki-compiler source review found compile --review and candidate approve/reject implementation."
source_libraries:
  - atomicstrata/llm-wiki-compiler
related_concepts:
  - "[[async-review-queue-for-ai-ingest]]"
  - "[[provenance-safe-source-lifecycle]]"
related_projects:
  - verified-knowledge-system
adoption_status: adopt-soon
evidence_count: 3
negative_evidence:
  - "[[direct-compile-to-truth-layer-without-review]]"
relations:
  - target: "[[direct-compile-to-truth-layer-without-review]]"
    type: replaces
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-26-llm-wiki-compiler-source]]"
    rationale: "The review queue prevents generated content from becoming formal truth before review."
    created: 2026-05-26
    last_verified: 2026-05-26
  - target: "[[SCHEMA]]"
    type: implements
    strength: 4
    confidence: high
    evidence:
      - "[[2026-05-26-llm-wiki-compiler-architecture-review]]"
    rationale: "SCHEMA v0.1 already defines AI assisted writing and program validation; this pattern makes that operational."
    created: 2026-05-26
    last_verified: 2026-05-26
---

# 设计模式：Review-Gated Compile Queue

## 一句话定义

LLM 只能把新知识编译成候选文件；候选通过 schema/provenance 检查和人工/AI 复核后，才能进入正式 `wiki/` 节点。

## 解决的问题

它解决“LLM 自动整理 = 自动变成事实”的风险。

对 verified knowledge system 来说，最危险的不是 LLM 提炼错一次，而是错的提炼直接进入 truth layer，后续 agent 又把它当成可信上下文继续推理。

## 适用场景

- raw source 进入 summary。
- summary 提炼 claim。
- claim 综合为 pattern / anti-pattern。
- pattern 被提议进入 decision。
- Misa/gbrain 或外部 agent 产生候选建议。

## 不适用场景

- 保存原始素材：raw source 应尽量原样保留，不需要 review queue 才能落盘。
- 纯临时问答：可以放 `outputs/qa/`，但进入 wiki 前仍要 review。
- 已明确人工直接编辑的小范围修正：可以直接改，但仍应过 lint。

## 反例与避坑

- 失败条件：候选目录变成另一个没人看的垃圾箱。
- 相似反模式：[[direct-compile-to-truth-layer-without-review]]
- 复杂度风险：一开始就做完整状态机、锁、MCP、viewer。
- 替代方案：先用 `outputs/review/candidates/` 的 Markdown/YAML 文件，人工 approve。

## 来源证据

`llm-wiki-compiler` 已实现候选 JSON、approve/reject/list/show、候选内 schema/provenance violations、approve 时不再调用 LLM、锁内重读候选、多候选 source state 延迟提交。

## 最小实现方式

v0.1 可以很轻：

```text
outputs/review/candidates/
  2026-05-26-some-claim.candidate.md
```

候选字段：

```yaml
type: review-candidate
status: pending-review
created:
proposed_node_type:
proposed_path:
proposed_by:
sources:
verification_status:
evidence_level:
confidence:
schema_violations: []
provenance_violations: []
reviewer:
review_result:
relations: []
```

批准动作：

```text
candidate -> lint -> review -> copy body into wiki/... -> update index -> archive candidate
```

## 项目融合建议

立即采用为 v0.2 第一优先级。它正好连接用户当前工作方式：资料主要由 Codex 入库，Misa/gbrain 只读正式知识，候选可由 Codex 把关。

## 验证指标

- 正式 `wiki/` 中是否没有未 review 的 AI 候选。
- 候选是否记录 sources、evidence_level、verification_status、relations。
- review 后是否能追踪批准/拒绝原因。
- lint 是否能在批准前发现缺字段、断链、citation 错误。
