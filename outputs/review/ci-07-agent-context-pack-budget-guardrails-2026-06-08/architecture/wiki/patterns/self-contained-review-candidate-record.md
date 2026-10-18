---
type: pattern
status: active
created: 2026-05-27
updated: 2026-06-08
tags:
  - pattern/review
  - pattern/adopted
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
adoption_status: adopted
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
candidate_body_location:
body_hash:
body_hash_algorithm:
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

采用为 promotion 前的对象完整性门槛。

它不是新架构模块，也不是新的 truth layer。它补的是候选进入评审前的
artifact discipline：评审时看的候选正文、证据包、边界和审批事实必须固定在
同一个记录里。

## 落地位置

```text
source / summary
-> candidate point
-> self-contained review candidate record
-> Evidence Packet / Evidence Sufficiency Gate
-> reviewed claim / pattern / anti-pattern / decision
```

普通 light capture 不需要这个门槛。只有 promotion、formal writeback、
strong reviewed relation、action basis，或 reviewer 明确要求时才需要。

## 不替换什么

- 不替换 Evidence Packet。
- 不替换 Evidence Sufficiency Gate。
- 不替换 `REVIEW_QUEUE.md` 的 promotion 规则。
- 不改变 Source node 的 provenance / support 分离。
- 不允许自动晋升。

## 验证指标

- 候选有完整 body。
- 候选有 sources 和 violations。
- approve 不重新调用 LLM。
- reject 不删除审计记录，只归档。
- body 改动后 body_hash 改变，并触发重新评审。
- 候选正文放在 Markdown 正文段落或外部引用里，不塞进 frontmatter/YAML。
- body_hash 采用固定规则：hash `candidate_body_location` 指向的正文内容，不含标题，CRLF 统一为 LF，首尾空白 trim，UTF-8 SHA256。
