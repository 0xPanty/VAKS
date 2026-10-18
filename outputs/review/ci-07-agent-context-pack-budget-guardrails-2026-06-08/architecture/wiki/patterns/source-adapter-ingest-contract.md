---
type: pattern
status: sandbox-candidate
created: 2026-05-27
updated: 2026-06-08
tags:
  - pattern/ingest
  - pattern/source-adapter
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
adoption_status: sandbox-test
evidence_count: 2
negative_evidence: []
relations:
  - target: "[[source-verification-and-trust-model]]"
    type: implements
    strength: 4
    confidence: high
    evidence:
      - "[[2026-05-27-llm-wiki-compiler-implementation-extraction]]"
    rationale: "Source adapters preserve raw material provenance before the verified layer evaluates it."
    created: 2026-05-27
    last_verified: 2026-05-27
---

# 设计模式：Source Adapter Ingest Contract

## 一句话定义

所有来源进入系统前都先通过 adapter 归一化为 source record，保留 origin、类型、截断状态和导入时间。

## 解决的问题

来源会越来越多：网页、PDF、repo、图片、视频字幕、聊天会话、项目产出、field test。如果没有统一 adapter contract，后面无法验证、去重、重编译或追踪质量。

## 来源证据

`llm-wiki-compiler` 的源码支持：

- web Readability + Turndown。
- file / txt / md。
- PDF dynamic import。
- image / transcript。
- Claude/Codex/Cursor session adapters。
- source writer empty slug guard。
- filename collision hash suffix。
- session 导入拒绝空会话。

CI-09 sandbox anchor snapshots:

- `outputs/review/ci-09-source-adapter-ingest-contract-2026-06-08/evidence/llm-wiki-compiler/source-adapter-core-anchor-snapshot.md`
- `outputs/review/ci-09-source-adapter-ingest-contract-2026-06-08/evidence/llm-wiki-compiler/source-adapter-types-anchor-snapshot.md`
- `outputs/review/ci-09-source-adapter-ingest-contract-2026-06-08/evidence/llm-wiki-compiler/source-writer-session-anchor-snapshot.md`

Checked source anchors:

- `src/ingest/shared.ts:11-15` common ingest result shape.
- `src/ingest/shared.ts:140-176` truncation and empty-content checks.
- `src/commands/ingest.ts:190-205` source type detection.
- `src/commands/ingest.ts:207-229` source frontmatter builder.
- `src/commands/ingest.ts:231-275` adapter dispatch and structured ingest result.
- `src/ingest/web.ts:14-63` web adapter extraction and failure handling.
- `src/ingest/pdf.ts:18-57` PDF title and text extraction.
- `src/ingest/file.ts:12-40` file adapter support and rejection rules.
- `src/ingest/image.ts:82-114` image adapter provider requirement and title/content output.
- `src/ingest/transcript.ts:58-73` YouTube transcript handling.
- `src/ingest/transcript.ts:141-156` transcript type handling and rejection.
- `src/utils/source-writer.ts:1-95` empty-slug guard, collision suffix, and idempotent same-source overwrite.
- `src/adapters/types.ts:19-52` normalized session and stateless session adapter contract.
- `src/commands/ingest-session.ts:27-54` session frontmatter and shared writer.
- `src/commands/ingest-session.ts:95-133` zero-success batch import failure.

## VAKS Boundary

Source adapters normalize and preserve source identity. They do not review the source.

Adapter output may create:

- source record
- raw source artifact
- candidate extraction input
- lint / hygiene warning
- review queue pressure

Adapter output must not create:

- reviewed claim
- truth confidence
- verification status upgrade
- reviewed relation
- promotion approval
- action basis
- project adoption verdict

The contract must stay light. It should describe what entered the system, what was extracted, where it was written, whether it was truncated, and what gaps or failures are known. It should not freeze a universal heavy schema for every source type.

## 我们的 adapter contract

```yaml
adapter:
  name:
  source_type:
  input_identity:
  output_source_path:
  title:
  content_hash:
  captured_at:
  captured_by:
  extraction_tool:
  extraction_model:
  truncated:
  original_char_count:
  source_quality:
  adapter_status: ok | partial | failed | blocked
  known_gaps: []
  warnings: []
```

## 扩展方向

```text
web
pdf
repo snapshot
video transcript
image/OCR
chat/session
manual note
product output
field-test result
```

## Minimal VAKS Contract

Required for adapter-created source records:

```yaml
adapter:
  name:
  source_type:
  input_identity:
  output_source_path:
  captured_at:
  captured_by:
  adapter_status: ok | partial | failed | blocked

source_boundary:
  knowledge_status: raw
  action_basis_allowed: false
  truth_mutation_allowed: false
  promotion_gate: review_required
```

Optional when available:

```yaml
content_hash:
title:
source_uri:
source_snapshot:
version_or_commit:
truncated:
original_char_count:
extraction_tool:
extraction_model:
source_quality:
known_gaps: []
warnings: []
```

## 项目融合建议

v0.2 不批量改旧 source records。先在新 adapter-created source records 上使用轻量字段。

v0.3 再做自动 ingest，但仍必须输出 source record / candidate，不得直接写 reviewed truth。

## 验证指标

- 同一 source 重复导入不会生成重复文件。
- 不同 source 同名不会互相覆盖。
- 空内容、空会话、无标题 source 会失败或进入 review。
- source record 能追踪 adapter 和 origin。
- adapter 输出不会直接提高 truth confidence 或 verification status。
- adapter 输出不会直接创建 reviewed relation、promotion approval 或 action basis。
- adapter 字段不会强迫所有 light source 都填写 heavy extraction schema。
