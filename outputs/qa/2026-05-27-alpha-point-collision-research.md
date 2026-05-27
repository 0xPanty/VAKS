---
type: qa
status: archived
created: 2026-05-27
updated: 2026-05-27
question: "Alpha point collision cross-validation 是否可行，外部有没有类似思路，如何落地 v0.1？"
answer_summary: "可行。外部相近领域包括 truth discovery、data fusion、claim verification、truth maintenance、agentic memory、literature-based discovery。我们的差异是把这些简化为 Markdown vault 内的 provenance-first + point collision + review-gated promotion。"
sources:
  - "https://arxiv.org/abs/2502.12110"
  - "https://github.com/agiresearch/A-mem"
  - "https://research.google/pubs/data-fusion-resolving-conflicts-from-multiple-sources/"
  - "https://arxiv.org/abs/1503.00310"
  - "https://research.google/pubs/knowledge-vault-a-web-scale-approach-to-probabilistic-knowledge-fusion/"
  - "https://arxiv.org/abs/1803.05355"
  - "https://www.sciencedirect.com/science/article/abs/pii/0004370279900080"
  - "https://arxiv.org/abs/1409.6428"
related_claims:
  - "[[accumulated-source-cross-validation]]"
related_patterns:
  - "[[accumulated-source-cross-validation]]"
  - "[[review-gated-compile-queue]]"
  - "[[claim-level-provenance-source-ranges]]"
related_decisions:
  - "[[2026-05-27-traceability-first-graduated-verification]]"
verification_status: single-source
evidence_level: synthetic
confidence: high
last_verified: 2026-05-27
next_review: 2026-06-03
relations:
  - target: "[[accumulated-source-cross-validation]]"
    type: supports
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-27-alpha-point-collision-research]]"
    rationale: "External research supports point-level cross-source collision as a lightweight validation route."
    created: 2026-05-27
    last_verified: 2026-05-27
tags:
  - qa
  - alpha
  - point-collision
  - cross-validation
---

# Alpha Point Collision Research

## TL;DR

这个 alpha 思路可行，而且有外部近亲。

但它不能做成“自动验证系统”。正确版本是：

```text
provenance-first
+ candidate point extraction
+ point collision signals
+ review-gated promotion
```

也就是：每条 source 先进来，保留 provenance；从 source 里抽出 point；新 point 和旧 point 撞击，产生 supports / contradicts / refines / replaces；这些信号先进入 review，不能自动变 truth。

## 外部相似思路

### A-MEM / agentic memory

A-MEM 会在新增 memory 时生成带结构属性的 note，然后分析历史 memory，建立相似链接，并允许旧 memory 的表示随新 memory 演化。

相似点：

```text
new memory -> structured note -> historical similarity links -> memory evolution
```

差异：

```text
A-MEM 主要解决 agent memory organization。
我们的机制解决 source-backed point validation 和 promotion。
```

### Truth discovery / data fusion

Truth discovery 研究多个来源互相冲突时如何找更可信的值，并估计来源可信度。

相似点：

```text
多来源
冲突值
来源可靠性
候选事实可信度
```

关键警告：

```text
简单多数投票不可靠。
同源复制必须识别。
来源在不同领域可靠性不同。
```

### FEVER / claim verification

FEVER 把 claim 标成：

```text
Supported
Refuted
NotEnoughInfo
```

并要求 evidence sentence。

这正好支持我们把 point collision 的 review 结果限制为：

```text
supports
contradicts
not-enough-info
refines
replaces
```

### Knowledge Vault

Knowledge Vault 是重型版本：自动融合文本、表格、页面结构和已有知识库，计算概率。

我们不照搬概率推理，只借鉴：

```text
多来源融合
事实级别概率/置信信号
抽取结果不能等于 truth
```

### Truth maintenance systems

TMS 的核心是记录 belief 的理由，并在新发现矛盾时修正 belief。

相似点：

```text
belief 有理由
理由可解释
矛盾触发 revision
```

我们的 Markdown 版本是：

```text
point / claim 有 provenance
collision edge 有 rationale
contradiction 触发 review
```

### Literature-based discovery

Swanson ABC 模型说明：分散文献中已有的 A-B、B-C 关系，可以组合出新的 A-C 假设。

这支持“库越厚，连接越多”的方向。

但它也提醒：连接只能生成 hypothesis，不能自动生成 truth。

## 可行性判断

可行，前提是 v0.1 不做重型算法。

正确路线：

```text
先让 Codex 抽 point
再用关键词/BM25/手工检索找相似旧 point
生成 collision candidate
人工或 Codex review 后确认关系
只把 reviewed collision 用作 promotion signal
```

不正确路线：

```text
用 embedding similarity 自动涨 confidence
把重复出现当 cross-checked
把 AI summary 当独立 source
自动合并冲突
自动晋级 decision
```

## v0.1 成功标准

拿 10 条真实 source 试跑，应该能得到：

```text
10 个 source records
20-50 个 candidate points
若干 supports / contradicts / refines collision signals
至少 1 个 point cluster 可晋级 claim 或 pattern
至少 1 个 conflict 被识别而不是被覆盖
```

如果做不到，说明 point 抽取粒度、source ranges 或 similarity 检索方式需要调整。
