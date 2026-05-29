---
type: source
status: source-captured
title: "A Truth Maintenance System"
source_id: 2026-05-29-truth-maintenance-system-source
source_uri: "https://www.sciencedirect.com/science/article/pii/0004370279900080"
source_url: "https://www.sciencedirect.com/science/article/pii/0004370279900080"
source_type: paper
author: "Jon Doyle"
publisher: "Artificial Intelligence"
published_at: 1979-11
captured_at: 2026-05-29
captured_by: Codex
version_or_commit: "Artificial Intelligence 12(3), 1979"
source_status: active
raw_location: "external"
processing_mode: immediate
processing_level: light
review_priority: normal
review_owner: Codex
formalization_status: candidate-generated
topics:
  - truth-maintenance
  - reason-maintenance
  - knowledge-calibration
  - point-collision
projects:
  - verified-action-knowledge-system
source_family: truth-maintenance-system
upstream_sources: []
verification_status: single-source
candidate_relation_suggestions: []
tags:
  - source
  - paper
  - architecture-reference
---

# A Truth Maintenance System

## 为什么收录

这篇论文作为 `Knowledge Calibration / Point Collision` 的概念祖先。

当前只吸收它的控制思想：

```text
不要只记录结论。
要记录为什么相信这个结论。
新证据进入时，要知道哪些旧判断被支持、被挑战、被细化、暴露风险或需要复查。
行动依据要能解释来源、理由和风险。
```

## 当前采用边界

本资料库不照搬老式自动 truth-maintenance 系统。

采用的是轻量版：

```text
external material
-> candidate points
-> calibration against local reviewed knowledge
-> review input
-> reviewed relation / reviewed node only after review
```

## 明确不采用

```text
自动判真
自动冲突解决
自动提升 confidence
自动改写 reviewed knowledge
把本地旧知识当永远裁判
把外部新资料当自动胜出证据
```

## 需要后续复查

```text
full paper has not been deeply reviewed in this vault yet.
Only bibliographic metadata, the Pro analysis, and current architecture fit were used for this source record.
Before turning this into a stronger claim or pattern, review the original paper more carefully.
```
