---
type: pattern
status: candidate
created: 2026-05-27
updated: 2026-05-27
tags:
  - pattern/health
  - pattern/next-action
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
adoption_status: adopt
evidence_count: 2
negative_evidence: []
relations:
  - target: "[[vault-health-check-as-maintenance-contract]]"
    type: refines
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-27-llm-wiki-compiler-implementation-extraction]]"
    rationale: "Health checks should not just list problems; they should classify project state and recommend next actions."
    created: 2026-05-27
    last_verified: 2026-05-27
---

# 设计模式：Project State Next Action Contract

## 一句话定义

系统应该能读取当前资料库状态，并给出下一步建议，而不是只输出静态错误列表。

## 解决的问题

一人企业知识系统最怕“知道一堆问题，但不知道下一步干什么”。状态机可以把当前状态转成明确动作。

## 来源证据

`llm-wiki-compiler` 的 `src/project/state.ts` 和 `src/project/recommendations.ts` 会收集：

- sources 是否存在。
- wiki 是否存在。
- concept/query 数量。
- pending candidates。
- index 是否缺失。
- lint cache 是否过期或损坏。
- project 是否 unreadable。

然后分类为：

```text
fresh
sources-only
review-pending
lint-attention
wiki-ready
empty-wiki
broken-project
```

## 我们的状态机升级

```text
fresh
sources-only
candidate-pending
lint-attention
verified-ready
decision-ready
action-ready
feedback-needed
schema-attention
agent-access-attention
```

## 项目融合建议

先做 `outputs/health/next-action.md`，不需要 API。每次大批量入库后生成一次。

## 验证指标

- health report 有 state。
- state 有 recommended action。
- action 不是裸 shell 命令，而是带 placeholder 的安全动作。
- pending review / stale lint / missing evidence 能变成明确下一步。
