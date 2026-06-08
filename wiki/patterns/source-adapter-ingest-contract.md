---
type: pattern
status: candidate
created: 2026-05-27
updated: 2026-05-27
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
adoption_status: adopt-soon
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

## 我们的 adapter contract

```yaml
adapter:
  name:
  source_type:
  input:
  output_source_path:
  title:
  content_hash:
  captured_at:
  captured_by:
  truncated:
  original_char_count:
  source_quality:
  known_gaps: []
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

## 项目融合建议

v0.2 先把现有 raw source records 补齐 adapter 字段。v0.3 再做自动 ingest。

## 验证指标

- 同一 source 重复导入不会生成重复文件。
- 不同 source 同名不会互相覆盖。
- 空内容、空会话、无标题 source 会失败或进入 review。
- source record 能追踪 adapter 和 origin。
