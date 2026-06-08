---
type: pattern
status: candidate
created: 2026-05-26
updated: 2026-05-26
tags:
  - pattern/provenance
  - pattern/evidence
  - verified-knowledge-system
sources:
  - "[[2026-05-26-llm-wiki-compiler-source]]"
  - "[[2026-05-26-llm-wiki-compiler-architecture-review]]"
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
  - "Need to choose exact YAML field name: evidence[].spans or provenance_spans."
  - "Need to decide how line anchors survive source file rewrites."
evidence_timeline:
  - date: 2026-05-26
    event: "llm-wiki-compiler source review found claim-level citation parsing and lint rules."
source_libraries:
  - atomicstrata/llm-wiki-compiler
related_concepts:
  - "[[source-verification-and-trust-model]]"
related_projects:
  - verified-knowledge-system
adoption_status: adopt
evidence_count: 2
negative_evidence: []
relations:
  - target: "[[SCHEMA]]"
    type: refines
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-26-llm-wiki-compiler-source]]"
    rationale: "SCHEMA v0.1 requires sources and evidence; source ranges make the evidence auditable."
    created: 2026-05-26
    last_verified: 2026-05-26
---

# 设计模式：Claim-Level Provenance Source Ranges

## 一句话定义

重要 claim 不只链接 source 文件，还要尽量指向 source 的具体段落或行范围。

## 解决的问题

`sources: [...]` 只能说明“这篇资料大概支持我”。它不能说明某个具体 claim 是从哪一句、哪段代码、哪段原文来的。

行级 provenance 让复核者可以快速判断：

- 这条 claim 有没有依据。
- 是否被 LLM 过度推断。
- 原文是否被截断、误读或断章取义。
- source 改动后，claim 是否需要复查。

## 适用场景

- `claim` 节点。
- pattern 的“来源证据”段。
- anti-pattern 的失败证据。
- decision 的依据和反例。
- context pack 给 agent 的 citation payload。

## 不适用场景

- 非文本素材还没有稳定 transcript/OCR 时。
- source 文件经常被重排、清洗、改行号时。
- 只做粗略 source capture，还未进入 claim 阶段时。

## 来源证据

`llm-wiki-compiler` 支持 `file.md:42-58` 和 `file.md#L42-L58` 两种 claim citation，并用 lint 检查 malformed citation、line 0、反向 range、越界 range、source 文件缺失。

## 最小实现方式

在本资料库中优先采用 YAML，而不是把所有证据塞进正文标记：

```yaml
evidence:
  - source: "[[2026-05-26-llm-wiki-compiler-source]]"
    source_path: "raw/repos/2026-05-26-llm-wiki-compiler-source.md"
    spans:
      - locator: "README.md"
        start_line:
        end_line:
    supports: "Claim text or field this evidence supports."
    confidence: high
```

如果来源来自 GitHub、论文或源码快照，可以加：

```yaml
source_commit:
source_snapshot:
```

## 项目融合建议

把它作为 `claim` 和 `decision` 的 v0.2 字段候选。短期不要求每个 summary 都做到行级 provenance，但正式 claim 和 decision 应逐步补。

## 验证指标

- 每个 adopted claim 是否至少有一个可追踪 source。
- 高风险 claim 是否有 source span。
- lint 是否能发现 source path 缺失或 span 越界。
- context pack 是否能带出 citation，而不是只带正文摘要。
