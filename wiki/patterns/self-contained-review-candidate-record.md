---
type: pattern
status: pattern-candidate
created: 2026-05-27
updated: 2026-05-27
tags:
  - pattern/review
  - pattern/candidate
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
adoption_status: adopt-now
evidence_count: 2
negative_evidence:
  - "[[direct-compile-to-truth-layer-without-review]]"
relations:
  - target: "[[review-gated-compile-queue]]"
    type: implements
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-27-llm-wiki-compiler-implementation-extraction]]"
    rationale: "A review queue needs self-contained candidate records so review and approval refer to the same artifact."
    created: 2026-05-27
    last_verified: 2026-05-27
---

# 设计模式：Self-Contained Review Candidate Record

## 一句话定义

候选不是一段聊天建议，而是一个完整、可审计、可归档、批准时可原样写入的记录。

## 解决的问题

如果 review 看的内容和最终写入的内容不是同一个 artifact，就会出现“复核通过的是 A，落库的是 B”的漂移。

## 来源证据

`llm-wiki-compiler` 的 candidate 包含：

```text
id
title
slug
summary
sources
body
generatedAt
sourceStates
schemaViolations
provenanceViolations
```

approve 时不再调用 LLM，而是在 lock 内重读 candidate，并把 candidate body 原样写入 wiki。

## 我们的候选结构

```yaml
type: review-candidate
status: pending-review
created:
updated:
id:
proposed_node_type:
proposed_title:
proposed_path:
proposed_by:
sources:
source_states: []
body_hash:
schema_violations: []
provenance_violations: []
relation_violations: []
decision_readiness_violations: []
actionability_violations: []
reviewer:
review_result:
reviewed_at:
archive_reason:
relations: []
```

## 最小实现方式

先用 Markdown candidate：

```text
outputs/review/candidates/YYYY-MM-DD-slug.candidate.md
```

批准动作：

```text
candidate -> copy body to wiki/... -> update index -> archive candidate
```

## 项目融合建议

立即采用。它是我们从“人工整理”走向“可运行 compiler”的第一块。

## 验证指标

- 候选有完整 body。
- 候选有 sources 和 violations。
- approve 不重新调用 LLM。
- reject 不删除审计记录，只归档。
