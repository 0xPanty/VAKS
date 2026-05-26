---
type: decision
status: active
created: 2026-05-27
updated: 2026-05-27
decision: "目标升级为可拓展的可信知识与行动依据系统，质量标准必须高于已分析参考库。"
related_projects:
  - verified-knowledge-system
based_on:
  - "[[SCHEMA]]"
  - "[[2026-05-27-implementation-includes-llm-wiki-stack]]"
  - "[[2026-05-26-architecture-layering-v0-1]]"
  - "[[2026-05-26-llm-wiki-compiler-architecture-review]]"
patterns:
  - "[[context-pack-evidence-envelope]]"
  - "[[review-gated-compile-queue]]"
  - "[[semantic-relation-edge-schema]]"
  - "[[compiled-truth-plus-append-only-timeline]]"
outcome: adopted
evidence_strength: high
verification_status: active
evidence_level: synthetic
confidence: high
last_verified: 2026-05-27
next_review: 2026-06-03
negative_evidence:
  - "[[direct-compile-to-truth-layer-without-review]]"
relations:
  - target: "[[2026-05-27-implementation-includes-llm-wiki-stack]]"
    type: refines
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-27-quality-bar-extensible-verified-action-knowledge-system]]"
    rationale: "The implementation includes the LLM Wiki stack, but the quality bar is trusted action support, not just wiki compilation."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[SCHEMA]]"
    type: refines
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-27-quality-bar-extensible-verified-action-knowledge-system]]"
    rationale: "SCHEMA must evolve from node fields into an extensible contract for trusted knowledge and action."
    created: 2026-05-27
    last_verified: 2026-05-27
migration_path: "Define extension contracts first, then implement modules behind those contracts."
rollback_path: "If an extension becomes too complex, freeze its contract and fall back to Markdown records and manual review."
tags:
  - decision/quality-bar
  - verified-knowledge-system
  - action-basis
  - extensibility
---

# 决策记录：更高质量的可信知识与行动依据系统

## 决策

目标升级：最终系统不是“一个更安全的 LLM Wiki”，而是一个可拓展的可信知识与行动依据系统。

它必须覆盖我们看过的优秀库能力，并在质量上超过它们：

```text
参考库能力全覆盖
+ verified truth layer
+ action basis layer
+ extensible module contracts
+ review / lint / evidence gates
+ feedback from real actions
```

## 背景

用户明确要求：只要更好，不要把系统框小。可信知识和行动依据是正确方向，但不够大；系统要有更强可拓展能力，质量要比已分析库都好。

因此，“更好”不能只理解为字段更多、权限更严，而要理解为最终效果更强：

```text
不仅知道什么是真的，
还知道什么可以行动，
为什么可以行动，
风险是什么，
缺口是什么，
行动后如何反馈回知识系统。
```

## 质量标准

### 1. 比 Karpathy LLM Wiki 更强

Karpathy 模式强在：

```text
raw -> wiki -> index/log -> query/lint
```

我们必须在此基础上增加：

```text
claim verification
pattern / anti-pattern
decision readiness
context pack for agents
action feedback
```

### 2. 比 llm-wiki-compiler 更强

`llm-wiki-compiler` 强在工程实现：ingest、compile、review、provenance、lint、context pack、MCP、viewer。

我们必须吸收这些能力，但增加：

```text
source / summary / claim / pattern / anti-pattern / decision typed flow
evidence_level + verification_status
relation strength
negative evidence
decision risk / rollback
agent permission tiers
action-oriented context packs
```

### 3. 比 gbrain 更适合当前用户

gbrain 强在 epistemic layer、timeline、compiled truth、gaps。

我们必须吸收这些，但避免过早复制完整 runtime。目标是：

```text
更轻量的 Markdown system-of-record
更明确的 action basis
更容易由 Codex/用户共同维护
```

### 4. 比 obsidian-second-brain 更可信

obsidian-second-brain 强在 agentic vault runtime、progressive context loading、health check。

我们必须吸收这些，但不让 background rewrite 和自动冲突裁决污染真值层。

### 5. 比搜索/RAG 类方案更可靠

BM25、vector、GraphRAG、Zilliz、QMD 都只能做召回层。

我们的质量标准是：

```text
retrieval finds candidates
verified layer decides trust
decision layer decides action
feedback layer updates future confidence
```

## 可拓展能力定义

系统要靠 contract 扩展，不靠一次性堆功能。

必须预留这些扩展点：

```text
source adapters       # web/pdf/repo/video/session/chat/manual notes
node schema packs     # dev / content / product / legal / finance / research
compile strategies    # summary / claim extraction / pattern mining / contradiction scan
lint rule packs       # schema / provenance / relations / decision readiness
retrieval engines     # BM25 / vector / graph / hybrid / external stores
review workflows      # Codex review / user approval / external expert notes
context pack modes    # answer / decision / implementation / content / agent memory
agent access tiers    # read-only / suggest-only / reviewed-write
output adapters       # Obsidian / MCP / API / viewer / products
feedback adapters     # action result / project outcome / user correction / field test
```

## 行动依据层

可信知识只是中间产物，最终要服务行动。

每个可行动结论需要回答：

```yaml
actionability:
  recommended_action:
  decision_status:
  expected_gain:
  risk:
  preconditions:
  blocked_by:
  rollback:
  owner:
  review_by:
  success_metric:
  feedback_source:
```

这不是每个普通 summary 都要写，但进入 decision 或 implementation-note 的节点必须具备。

## 不是怎么变大

不靠这些方式变大：

- 一开始复制完整桌面 App。
- 一开始接重型向量数据库。
- 一开始做全自动 agent。
- 一开始把所有资料都自动变成决策。
- 一开始追求炫酷图谱 UI。

## 应该怎么变大

靠这些方式变大：

- 每层都有清楚 contract。
- 每个模块可以替换。
- 每个输出都有 provenance。
- 每个行动都有风险和回退。
- 每次真实行动能反馈到 confidence 和 decision。
- 每个 agent 只能在自己的权限层工作。

## 最终系统形态

```text
Extensible Verified Action Knowledge System

raw sources
  -> compiler stack
  -> candidate queue
  -> verified knowledge graph
  -> decision / action basis
  -> context pack / API / viewer
  -> agent or human action
  -> feedback timeline
  -> updated confidence / gaps / next review
```

## 验证方式

判断它是否真的比参考库好，不看功能数量，看这几个问题：

1. 同一份 raw source，是否能产出比普通 wiki 更可验证的 claim？
2. 同一批参考库，是否能提炼出 pattern、anti-pattern 和 decision？
3. Agent 拿到 context pack 后，是否知道哪些能行动、哪些不能？
4. 决策出错后，系统是否能记录反馈并降低置信度？
5. 新检索、新 UI、新 API、新 agent 能否作为插件接入，而不改 truth layer？
6. 用户能否从资料入库一路走到行动建议，而不是停在“我知道一些笔记”？

## 当前结论

可信知识和行动依据是核心方向，但系统目标要更大：

```text
不是 Obsidian vault。
不是普通 LLM Wiki。
不是 RAG。
不是单一 agent memory。

是可拓展的可信知识与行动依据系统。
```

所有后续设计都按这个质量标准推进。
