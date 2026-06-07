---
type: pattern
status: active
created: 2026-05-26
updated: 2026-06-08
tags:
  - pattern/review
  - pattern/llm-ingest
  - pattern/adopted
  - verified-knowledge-system
sources:
  - "[[2026-05-26-llm-wiki-compiler-source]]"
  - "[[2026-05-26-llm-wiki-compiler-architecture-review]]"
  - "[[2026-05-27-llm-wiki-compiler-implementation-extraction]]"
  - "[[2026-04-04-karpathy-llm-wiki-pattern]]"
  - "outputs/review/promotion-funnel-pilot-2026-06-08/PROMOTION_EVIDENCE_PACKETS.md#EP-02"
verification_status: primary-source
evidence_level: primary
confidence: high
last_verified: 2026-06-08
next_review: 2026-07-08
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
adoption_status: adopted
evidence_count: 3
negative_evidence:
  - "[[direct-compile-to-truth-layer-without-review]]"
relations:
  - target: "[[direct-compile-to-truth-layer-without-review]]"
    type: contradicts
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-26-llm-wiki-compiler-source]]"
    rationale: "The review queue blocks the anti-pattern where generated content becomes formal knowledge before review."
    created: 2026-05-26
    last_verified: 2026-06-08
  - target: "[[SCHEMA]]"
    type: refines
    strength: 4
    confidence: high
    evidence:
      - "[[2026-05-26-llm-wiki-compiler-architecture-review]]"
    rationale: "SCHEMA already defines AI assisted writing and program validation; this pattern narrows that boundary for compile/writeback."
    created: 2026-05-26
    last_verified: 2026-06-08
---

# 设计模式：Review-Gated Compile Queue

## 一句话定义

LLM / compile / agent 只能把拟写入正式 `wiki/` 的内容先编译成 review candidate；候选经过固定正文、来源锚点、lint / evidence review 和审批后，才能进入正式知识节点。

## 解决的问题

它解决“LLM 自动整理 = 自动变成事实”的风险。

对 verified knowledge system 来说，最危险的不是 LLM 提炼错一次，而是错的提炼直接进入 truth layer，后续 agent 又把它当成可信上下文继续推理。

2026-06-08 正式收口：

```text
AI / compile generated formal node
-> review candidate
-> fixed candidate body + source anchors + lint / evidence checks
-> approval of that exact body
-> wiki writeback / archive receipt
```

这不是新架构层，只是把原有 `candidate != truth` 和 `review before wiki`
原则在 compile/writeback 场景下变成硬闸门。

## 适用场景

- raw source 进入 summary。
- summary 提炼 claim。
- claim 综合为 pattern / anti-pattern。
- pattern 被提议进入 decision。
- Misa/gbrain 或外部 agent 产生候选建议。
- query / brief / proactive synthesis 的结果准备进入正式 `wiki/`。

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

关键源码锚点：

```text
raw/repos/_snapshots/llm-wiki-compiler-main-2026-05-26.zip
llm-wiki-compiler-main/src/compiler/index.ts:560-619
llm-wiki-compiler-main/src/compiler/candidates.ts:34-103
llm-wiki-compiler-main/src/commands/review-approve.ts:35-64
llm-wiki-compiler-main/src/commands/review-show.ts:11-40
llm-wiki-compiler-main/src/commands/review-reject.ts:21-41
```

本地 promotion pilot 的 EP-02 复核结论是：

```text
supported
sufficient for pattern promotion under VAKS scope
```

## 最小实现方式

v0.1 可以很轻：

```text
outputs/review/candidates/
  2026-05-26-some-claim.candidate.md
```

候选字段：

```yaml
record_type: review-candidate
status: pending
knowledge_status: candidate
created:
candidate_id:
promotion_target:
proposed_path:
proposed_by:
candidate_body_location:
body_hash:
body_hash_algorithm:
evidence_packet_ref:
source_anchor_refs: []
schema_violations: []
provenance_violations: []
approval_integrity:
  approved_by:
  approved_at:
  checked_specific_evidence:
  checked_body_hash:
```

批准动作：

```text
candidate
-> lint / evidence review
-> approve exact body
-> copy fixed body into wiki/...
-> update index
-> archive candidate / write receipt
```

## 项目融合建议

已采用为 VAKS 的 compile/writeback 闸门。

它正好连接当前工作方式：资料主要由 Codex 处理，Misa/gbrain 或其他 agent
只能读取正式知识或提交候选，正式 `wiki/` 写入由 review gate 把关。

## 不替代什么

- 不替代 Evidence Packet。
- 不替代 Evidence Sufficiency Gate。
- 不替代 Self-Contained Review Candidate Record。
- 不替代 source hash registry / idempotent ingest。
- 不允许 `query --save`、watch auto-compile、MCP write 或 Obsidian sync 绕过 review。
- 不改变 truth confidence，不自动晋升，不创建 reviewed relation。

## 验证指标

- 正式 `wiki/` 中是否没有未 review 的 AI 候选。
- 候选是否记录 proposed path、fixed body、source anchors、evidence packet ref 和 lint findings。
- review 后是否能追踪批准/拒绝原因。
- lint 是否能在批准前发现缺字段、断链、citation 错误。
- approve 是否写入固定候选正文，而不是重新生成正文。
- reject 是否归档候选且不改正式 `wiki/`。
