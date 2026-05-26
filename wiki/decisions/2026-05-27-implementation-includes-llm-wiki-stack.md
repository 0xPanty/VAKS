---
type: decision
status: active
created: 2026-05-27
updated: 2026-05-27
decision: "最终实现包含 Karpathy LLM Wiki / llm-wiki-compiler 的完整操作能力，但由 verified schema 约束。"
related_projects:
  - verified-knowledge-system
based_on:
  - "[[2026-04-04-karpathy-llm-wiki-pattern]]"
  - "[[2026-05-26-llm-wiki-compiler-architecture-review]]"
  - "[[SCHEMA]]"
  - "[[2026-05-27-quality-bar-extensible-verified-action-knowledge-system]]"
patterns:
  - "[[review-gated-compile-queue]]"
  - "[[claim-level-provenance-source-ranges]]"
  - "[[context-pack-evidence-envelope]]"
  - "[[static-wiki-health-lint-before-auto-rewrite]]"
outcome: adopted
evidence_strength: high
verification_status: active
evidence_level: synthetic
confidence: high
last_verified: 2026-05-27
next_review: 2026-06-03
negative_evidence:
  - "[[direct-compile-to-truth-layer-without-review]]"
replaces:
relations:
  - target: "[[2026-05-27-quality-bar-extensible-verified-action-knowledge-system]]"
    type: supports
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-27-implementation-includes-llm-wiki-stack]]"
    rationale: "The LLM Wiki stack is included as implementation capability, while the higher quality target is trusted action support."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[2026-05-26-architecture-layering-v0-1]]"
    type: refines
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-27-implementation-includes-llm-wiki-stack]]"
    rationale: "This decision clarifies that layering means phased inclusion, not shrinking the final implementation."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[2026-05-26-llm-wiki-compiler-architecture-review]]"
    type: refines
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-27-implementation-includes-llm-wiki-stack]]"
    rationale: "The compiler stack is an implementation substrate to include, while SCHEMA remains the contract."
    created: 2026-05-27
    last_verified: 2026-05-27
migration_path: "Start with Markdown candidate queue and lint, then implement ingest/query/lint/index/log/context pack, then API/MCP/viewer."
rollback_path: "If a module becomes too heavy, keep its data contract and disable the runtime feature without changing formal wiki nodes."
tags:
  - decision/implementation-scope
  - llm-wiki
  - verified-knowledge-system
---

# 决策记录：最终实现包含 LLM Wiki Stack

## 决策

我们的目标不是只做 verified knowledge system 的底层契约，也不是只做一个小心翼翼的 Markdown 规范。

最终实现要包含 Karpathy LLM Wiki / llm-wiki-compiler 代表的完整操作能力：

```text
raw ingest
-> wiki compile
-> index / log
-> query
-> lint
-> review queue
-> provenance
-> context pack
-> API / MCP
-> read-only viewer / Obsidian view
```

区别在于：这些能力不直接定义 truth layer。它们运行在 `SCHEMA.md` 和 verified node flow 之下。

## 背景

前一轮表述把“不能直接采用”说得太窄，容易误解成我们只要底层契约、不想做完整实现。

正确理解应该是：

```text
不是不用这些库。
是要把这些库的能力包含进来，但不能让它们的默认 schema 替代我们的 verified schema。
```

## 依据

- Karpathy 模式验证了 `raw/`、`wiki/`、`index.md`、`log.md`、`ingest/query/lint` 是一人企业知识系统的高效操作形态。
- `llm-wiki-compiler` 验证了这些操作可以工程化为 CLI、review queue、context pack、MCP、viewer。
- 本资料库已经确定更强的真值链路：`source -> summary -> claim -> pattern / anti-pattern -> decision -> context pack`。

## 量化判断

- problem_fit: 5
- reuse_value: 5
- implementation_cost: 4
- integration_fit: 5
- evidence_strength: 5
- reversibility: 4

## 交叉验证

- 相似库/产品/论文：Karpathy LLM Wiki、atomicstrata/llm-wiki-compiler、nashsu/llm_wiki、gbrain、obsidian-second-brain。
- 支持证据：多个来源都收敛到 raw/wiki/index/log/context/lint/review。
- 失败边界：如果直接采用 generic concept schema，会削弱 claim/pattern/decision 的验证链路。

## 备选方案

1. 只做 SCHEMA，不做完整运行时。  
   结论：拒绝。最终效果不够，用户要的是可工作的知识系统。

2. 直接 fork llm-wiki-compiler，当成核心。  
   结论：不作为核心契约，但可以作为实现底座候选。

3. 完整吸收其操作能力，同时保留 verified schema。  
   结论：采用。

## 可拓展性与迁移

- 是否绑定特定工具/库：不强绑定，但 `llm-wiki-compiler` 可以作为第一实现参考。
- 后续新方案如何接入：只要能输出符合 `SCHEMA.md` 的候选节点、context pack 和 lint report，就可以替换。
- 迁移路径：先 Markdown-only，再脚本，再 API/MCP，再 viewer。
- 回退路径：任何运行时失败，都回退到 Markdown system-of-record。

## 为什么这样选

用户要的是最终实现效果，不是一个孤立的规范文件。

因此正确架构是：

```text
Karpathy / llm-wiki-compiler = 操作能力和工程发动机
SCHEMA.md / verified flow     = 真值契约和采纳规则
Misa/gbrain                   = read-only context consumer + candidate proposer
Codex/User                    = review and final authority
```

这不是保守缩小，而是做成更强的超集。进一步的质量目标见 [[2026-05-27-quality-bar-extensible-verified-action-knowledge-system]]：系统不仅要能编译知识，还要能形成可信行动依据，并允许未来模块持续替换和扩展。

## 风险

- 实现层太早膨胀，拖慢 verified schema 落地。
- API/MCP/viewer 先行，导致 formal nodes 还没稳定就进入工具维护。
- 候选队列没人 review，变成堆积区。
- LLM compile 结果被误认为决策。

## 避坑与反模式

- 相关反模式：[[direct-compile-to-truth-layer-without-review]]
- 不采用哪些做法：不让 generic concept page 直接替代 claim/pattern/decision。
- 失败边界：agent 可以生成候选，但不能绕过 review 直接写 truth layer。
- 回退方案：保留 raw、wiki、outputs/review、SCHEMA 的 Markdown 主记录。

## 验证方式

第一阶段成功标准：

- 能把 raw source 编译成候选 summary/claim/pattern。
- 候选进入 review queue，而不是直接污染 formal wiki。
- lint 能发现 schema/provenance 问题。
- index/log 能记录操作。
- context pack 能给 Misa/gbrain 只读使用。

第二阶段成功标准：

- query 能优先查 verified wiki，而不是每次重读 raw。
- context pack 能带出 evidence、warnings、gaps。
- API/MCP/viewer 能接入，但不获得 truth-layer 写权限。

## 复盘

2026-05-27：用户明确纠偏，要求最终实现包含这些库和 Karpathy 的所有实现能力。已将架构表述从“暂不做/不直接采用”修正为“阶段化包含/不让其替代核心契约”。
