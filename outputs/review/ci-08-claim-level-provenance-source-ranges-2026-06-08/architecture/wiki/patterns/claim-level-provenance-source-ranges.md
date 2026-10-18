---
type: pattern
status: sandbox-candidate
created: 2026-05-26
updated: 2026-06-08
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
  - "Use strict source ranges only for claim, decision, reviewed relation, promotion, and action-facing evidence; keep ordinary raw/source capture light."
  - "Line anchors can drift after source rewrites, so source_snapshot or source_commit is required when stability matters."
evidence_timeline:
  - date: 2026-05-26
    event: "llm-wiki-compiler source review found claim-level citation parsing and lint rules."
  - date: 2026-06-08
    event: "CI-08 sandbox tested source ranges as provenance and review handles, not automatic support or truth."
source_libraries:
  - atomicstrata/llm-wiki-compiler
related_concepts:
  - "[[source-verification-and-trust-model]]"
related_projects:
  - verified-knowledge-system
adoption_status: sandbox-test
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

CI-08 sandbox anchor snapshots:

- `outputs/review/ci-08-claim-level-provenance-source-ranges-2026-06-08/evidence/llm-wiki-compiler/claim-citation-parser-anchor-snapshot.md`
- `outputs/review/ci-08-claim-level-provenance-source-ranges-2026-06-08/evidence/llm-wiki-compiler/citation-lint-anchor-snapshot.md`
- `outputs/review/ci-08-claim-level-provenance-source-ranges-2026-06-08/evidence/llm-wiki-compiler/citation-render-and-context-anchor-snapshot.md`

Checked source anchors:

- `src/utils/markdown.ts:18-25` defines claim citation markers and `:start-end` / `#Lstart-Lend` line syntax.
- `src/utils/markdown.ts:117-190` extracts claim citations, multi-source citations, and source span entries.
- `src/utils/markdown.ts:195-230` detects malformed citation entries and builds provenance inspection.
- `src/linter/rules.ts:348-446` parses both line range syntaxes.
- `src/linter/rules.ts:450-536` checks missing sources and out-of-bounds line ranges.
- `src/linter/rules.ts:556-584` checks malformed claim citations before approval.
- `src/viewer/citation-rule.ts:1-16` defines citation chip rule shape and accepted line range formats.
- `src/viewer/citation-rule.ts:88-115` maps parsed citations into render metadata.
- `src/viewer/citation-rule.ts:162-190` renders citation chips with source line metadata.
- `src/context/provenance.ts:67-91` flattens citation spans into context citation records.
- `src/context/provenance.ts:116-149` materializes source windows only when explicitly requested.
- `src/context/provenance.ts:170-198` rejects absolute paths, parent traversal, and source-root escapes.
- `src/context/provenance.ts:222-246` reads clamped 1-indexed line windows.

## VAKS Boundary

Source ranges are provenance and review handles. They help a reviewer find the relevant source span quickly.

They do not by themselves create:

- evidence support
- truth confidence
- verification status
- reviewed relation
- action readiness
- promotion approval

To count as support, a ranged evidence item must also name the `target_claim`, state `span_supports_target`, state `evidence_role`, and include a warrant / scope note explaining why that span supports or challenges the exact target.

Blocked interpretations:

- URL-only reference as support.
- summary-only reference as support.
- `background_context` as support.
- malformed, missing-source, or out-of-bounds source range as support.
- valid source range automatically raising truth confidence.
- valid source range automatically creating reviewed relation or action-ready basis.

## 最小实现方式

在本资料库中优先采用 YAML，而不是把所有证据塞进正文标记：

```yaml
evidence:
  - source: "[[2026-05-26-llm-wiki-compiler-source]]"
    source_path: "raw/repos/2026-05-26-llm-wiki-compiler-source.md"
    source_snapshot:
    source_commit:
    source_range: "README.md:42-58"
    target_claim:
    quote_or_excerpt:
    evidence_support:
      span_supports_target: supported | partial | unsupported | unclear
      evidence_role: direct_support | inferential_support | background_context | counterexample
      warrant:
      scope:
      reviewer_note:
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
- source range 是否没有被当成 truth confidence、verification status、reviewed relation、promotion approval 或 action readiness。
- URL-only、summary-only、background_context、malformed range、missing source、out-of-bounds range 是否被阻止作为 support。
- valid range 是否仍要求 target-specific warrant / scope，不能靠行号本身冒充 evidence support。
