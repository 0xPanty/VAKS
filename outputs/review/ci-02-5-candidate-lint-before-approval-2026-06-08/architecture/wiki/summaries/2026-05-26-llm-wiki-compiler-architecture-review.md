---
type: summary
status: reviewed
created: 2026-05-26
updated: 2026-05-26
title: llm-wiki-compiler 架构压榨
library_name: atomicstrata/llm-wiki-compiler
repo_url: "https://github.com/atomicstrata/llm-wiki-compiler"
sources:
  - "[[2026-05-26-llm-wiki-compiler-source]]"
  - "[[2026-04-04-karpathy-llm-wiki-pattern]]"
verification_status: primary-source
evidence_level: primary
confidence: high
last_verified: 2026-05-26
next_review: 2026-06-02
extracted_patterns:
  - review-gated-compile-queue
  - claim-level-provenance-source-ranges
  - context-pack-evidence-envelope
  - static-wiki-health-lint-before-auto-rewrite
negative_evidence:
  - direct-compile-to-truth-layer-without-review
relations:
  - target: "[[SCHEMA]]"
    type: refines
    strength: 4
    confidence: high
    evidence:
      - "[[2026-05-26-llm-wiki-compiler-source]]"
    rationale: "The repo validates SCHEMA v0.1's review-first and context-pack boundaries at implementation level."
    created: 2026-05-26
    last_verified: 2026-05-26
  - target: "[[review-gated-compile-queue]]"
    type: derived_from
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-26-llm-wiki-compiler-source]]"
    rationale: "The strongest reusable architecture is candidate-first compile with approval gates."
    created: 2026-05-26
    last_verified: 2026-05-26
tags:
  - summary/repo-review
  - verified-knowledge-system
  - llm-wiki
---

# 库分析：atomicstrata/llm-wiki-compiler

## 一句话结论

这是目前最接近我们 v0.2 的实现级参考：它把 Karpathy 的 LLM Wiki 从“好想法”推进到“可审查的知识编译器”。我们应该把它的完整操作能力纳入最终实现，但不能让它的默认 wiki 类型替代本资料库的 verified schema。

## 它真正解决的问题

普通 LLM Wiki 的风险是：LLM 一边读 raw，一边直接写 wiki，于是“提炼结果”很容易被误当成“已验证知识”。

`llm-wiki-compiler` 的关键补强是把链路拆成：

```text
sources/ -> compile -> candidate -> review -> wiki/ -> context pack / query / lint
```

也就是说，LLM 先编译候选，程序先暴露结构和证据问题，人再决定是否入库。

## 最值得压榨的设计

1. 候选优先写入  
   `compile --review` 不改 `wiki/`，只写 `.llmwiki/candidates/`。这和我们的 `outputs/review/` 思路完全同向。

2. 候选必须自包含  
   candidate 里保存完整 body、slug、sources、generatedAt、sourceStates、schemaViolations、provenanceViolations。批准时不再调用 LLM，只复制候选正文。

3. 批准前暴露错误  
   schema lint 和 provenance lint 在候选生成时就运行，reviewer 在 `review show` 阶段能看到问题，而不是等污染正式 wiki 后再发现。

4. Claim-level provenance  
   它把 citation 从“这个段落来自某 source”推进到“这条 claim 指向 source 的某几行”。这是 verified knowledge system 必须要的粒度。

5. Context pack 不是 answer  
   `get_context_pack` / `llmwiki context` 输出证据包：primary pages、chunks、citations、neighbors、warnings、gaps、suggestedActions。它明确是 prepare evidence，不是替 agent 生成最终回答。

6. Source windows 默认关闭  
   原文片段需要 `includeSources` 显式开启，而且只能从 `sources/` 读。这一点适合 Misa/gbrain：默认只拿 verified wiki 和证据索引，必要时才请求 raw snippet。

7. Static lint first  
   lint 是无 LLM 的规则检查：断链、孤儿页、空页、低置信、矛盾、未引用段落、citation 越界、schema cross-link 不足。程序负责校验，不负责擅自改写。

8. 锁与延迟状态  
   approve/reject 使用 lock；同一 source 产出多个 candidate 时，只有最后一个 sibling 通过才更新 source state。这个细节说明它认真处理了“半批准状态污染”。

9. 搜索只是召回  
   chunk embedding、BM25 rerank、graph neighbor、debug 输出都是为了找到候选上下文，不承担真值裁决。

10. Session ingest 可作为 raw source  
   Claude/Codex/Cursor session 可以作为 source 导入，并拒绝空会话。这对我们未来把重要对话沉淀为 raw material 有借鉴价值。

## 对我们系统的翻译

我们不用照搬 `.llmwiki/`，可以翻译成：

```text
raw/...                         # source records and snapshots
outputs/review/candidates/...   # AI/Misa/Codex proposed nodes
wiki/...                        # reviewed formal nodes
SCHEMA.md                       # truth-layer contract
outputs/health/...              # lint and health reports
context-pack.json               # read-only evidence envelope for agents
```

候选节点最小字段：

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

批准规则：

```text
候选 -> schema lint -> provenance lint -> Codex review -> user final authority -> 正式 wiki node
```

## 不是不采用，而是不能让它定义真值层

- 它的 `concept/entity/comparison/overview` 可以作为普通 wiki 页或兼容层，但不能替代核心类型：`source/summary/claim/pattern/anti-pattern/decision/qa/implementation-note`。
- 它的 `confidence: 0-1` 可以保留为实现字段，但不能替代 `verification_status`、`evidence_level`、`last_verified`、`next_review`、反例和 relation strength。
- watch / auto compile 可以作为后续能力，但正式 truth layer 写入必须经过 review gate。
- MCP server、viewer、chunk embedding store 是最终实现范围的一部分，只是不能抢在 schema/review/lint 前面成为核心。
- 外部 agent 可以读、可以生成候选，但不能绕过 review 直接写正式 `wiki/` 或改 `SCHEMA.md`。

## 与 Misa/gbrain 的关系

Misa/gbrain 可以读取 context pack，而不是直接读整个 vault 或改 vault。

推荐边界：

```text
Misa/gbrain: Level 1 read-only context consumer
Misa output: Level 2 candidate suggestion
Codex: Level 3 reviewed write
User: final authority
```

这正好补上我们之前说的“给 agent 一个 API”：不是给它数据库写权限，而是给它一个 verified context pack resolver。

## 当前采纳判断

- 结论：完整纳入实现目标，不直接让它替代核心契约。
- 立刻吸收：review queue、candidate schema/provenance violations、claim source ranges、context pack envelope、static lint。
- 中期实现：MCP server / read-only API、viewer、session ingest、chunk retrieval、export bundle。
- 明确拒绝：用 generic concept schema 替换我们的 SCHEMA，或让 auto compile 直接写 truth layer。

## 下一步建议

1. 在 `outputs/review/` 下增加 candidate 示例。
2. 为 `SCHEMA.md` v0.2 预留 `provenance_spans` 或 `evidence[].spans`。
3. 先写一个 Markdown lint 清单：字段缺失、断链、source 缺失、relation 缺证据、decision 缺风险和回退。
4. 再设计最小 context pack JSON，供 Misa/Hermes read-only 调用。
