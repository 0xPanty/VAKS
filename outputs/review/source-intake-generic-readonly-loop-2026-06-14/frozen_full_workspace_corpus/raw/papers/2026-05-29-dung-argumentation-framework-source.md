---
type: source
record_kind: source_card
status: source-captured
title: "On the Acceptability of Arguments and its Fundamental Role in Nonmonotonic Reasoning, Logic Programming and n-Person Games"
source_id: 2026-05-29-dung-argumentation-framework-source
source_uri: "https://cse-robotics.engr.tamu.edu/dshell/cs631/papers/dung95acceptability.pdf"
source_url: "https://cse-robotics.engr.tamu.edu/dshell/cs631/papers/dung95acceptability.pdf"
source_type: paper
author: "Phan Minh Dung"
publisher: "Artificial Intelligence"
published_at: 1995
captured_at: 2026-05-29
captured_by: Codex
version_or_commit: "Dung 1995"
source_status: active
raw_location: "external"
review_priority: normal
review_owner: Codex
formalization_status: candidate-generated
topics:
  - argumentation
  - support-challenge-review
  - evidence-aware-review
  - review-semantics
projects:
  - verified-action-knowledge-system
source_family: dung-argumentation-framework
upstream_sources: []
verification_status: single-source
candidate_relation_suggestions: []
tags:
  - source
  - paper
  - architecture-reference
knowledge_status: raw
processing_tier: light
why_saved: see_body_or_legacy_record
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
---

# Dung 1995 Argumentation Framework Source

## 为什么收录

这篇论文作为 `Evidence-Aware Review / Support-Challenge Review` 的概念来源之一。

当前只吸收它的轻量思想：

```text
一个判断不能只看有没有支持。
还要看它面对挑战、反对、范围限制和风险时，是否仍然站得住。
```

## 当前采用边界

本资料库不实现 formal argumentation semantics。

采用的是人类可读 review 面板：

```text
What supports it?
What challenges it?
Is the challenge fatal, major, minor, out of scope, or unresolved?
Where does this claim apply or not apply?
What risks must be carried forward?
Can this be used for action in this context?
```

## 明确不采用

```text
自动论证裁决
自动判断哪一方获胜
自动 accepted argument 计算
自动 confidence 更新
把 attack 直接等同于 rejection
```

## 需要后续复查

```text
full paper has not been deeply reviewed in this vault yet.
Only the Pro analysis, source metadata, and architecture fit were used for this source record.
Before turning this into a stronger claim or pattern, review the original paper more carefully.
```
