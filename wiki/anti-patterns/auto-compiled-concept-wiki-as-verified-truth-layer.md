---
type: anti-pattern
status: active
created: 2026-05-27
updated: 2026-05-27
domain: verified-knowledge-system
failure_mode: "Treating auto-compiled generic concept pages as verified truth."
severity: 5
likelihood: 4
complexity_cost: 4
cross_validated_with:
  - "[[direct-compile-to-truth-layer-without-review]]"
  - "[[generic-concept-schema-as-truth-layer]]"
related_projects:
  - verified-knowledge-system
replacement:
  - review-gated candidate compile
  - source/summary/claim/pattern/anti-pattern/decision flow
relations:
  - target: "[[2026-05-27-openkb-architecture-review]]"
    type: derived_from
    strength: 4
    confidence: high
    evidence:
      - "[[auto-compiled-concept-wiki-as-verified-truth-layer]]"
    rationale: "OpenKB's concept auto-update model is useful for generic wiki compilation but unsafe as this vault's verified truth layer."
    created: 2026-05-27
    last_verified: 2026-05-27
decision: avoid
---

# 反模式 / 踩坑：把自动编译 Concept Wiki 当 Verified Truth Layer

## 问题描述

OpenKB 这类系统会把新 source 自动编译成 summary 和 concept，并直接更新 `wiki/concepts/`。

这对普通 LLM Wiki 是好功能；对本资料库，如果直接采用，会变成反模式。

原因是本资料库不是概念百科，而是：

```text
source -> summary -> claim -> pattern / anti-pattern -> decision -> context pack
```

concept page 可以帮助理解主题，但不能直接等于 verified claim、adopted pattern 或 action-ready decision。

## 为什么不可行

自动 concept rewrite 有几个风险：

- LLM 把新资料揉进旧页面，证据边界变模糊。
- 多个来源的冲突被写成流畅综合，负面证据消失。
- 没有 claim 粒度验证。
- 没有 decision risk / rollback / actionability。
- 后续 agent 看到 polished concept，容易误以为已验证。

## 失败条件

- `openkb add` 或类似 compile 直接写 formal wiki。
- `concepts/` 被当成决策依据。
- 没有 review queue。
- 没有 verification_status/evidence_level/confidence。
- 没有 negative evidence 和 gaps。

## 标签与量化

- domain: verified knowledge
- failure_mode: unreviewed synthesis as truth
- severity: 5
- likelihood: 4
- complexity_cost: 4
- evidence_strength: 4
- reversibility: 3

## 交叉验证

- 相似失败来源：[[direct-compile-to-truth-layer-without-review]]、[[generic-concept-schema-as-truth-layer]]
- 历史项目证据：当前资料库已经确认搜索/编译只产生候选，review 才产生 truth。
- 支持证据：OpenKB 源码的 compile path 直接写 summaries/concepts/index/log。
- 是否可能只是局部失败：是。对于普通个人 wiki，它不是失败；对于 verified action knowledge，它是失败。

## 应该避开什么

不要做：

```text
raw source
-> OpenKB-style concept update
-> formal truth
```

不要把这些东西当最终结论：

```text
generic concept
LLM summary
semantic lint report
query answer
skill body
```

## 替代方案

正确路径：

```text
raw source
-> compiler candidate
-> candidate summary / claim / pattern / anti-pattern
-> lint
-> review
-> verified node
-> decision / action basis
```

OpenKB 可以作为 compiler adapter，而不是 truth authority。

## 后续是否需要复测

需要。等 `REVIEW_QUEUE.md` 和 `IMPLEMENTATION_BLUEPRINT.md` 写完后，可以复测 OpenKB 是否能作为候选 compiler backend。
