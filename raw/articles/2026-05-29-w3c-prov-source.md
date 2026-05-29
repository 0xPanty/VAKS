---
type: source
status: source-captured
title: "W3C PROV family of provenance documents"
source_id: 2026-05-29-w3c-prov-source
source_uri: https://www.w3.org/TR/prov-overview/
source_url: https://www.w3.org/TR/prov-overview/
source_type: official-spec
author: W3C Provenance Working Group
publisher: W3C
published_at: 2013-04-30
updated_at:
captured_at: 2026-05-29
captured_by: Codex
extracted_by: Codex
extracted_at: 2026-05-29
extraction_tool: web
extraction_model: Codex
version_or_commit: "PROV-Overview Working Group Note 2013-04-30; PROV-DM Recommendation 2013-04-30"
provenance:
  model: PROV-lite
  activities:
    - type: captured
      at: 2026-05-29
      by: model:Codex
    - type: extracted
      at: 2026-05-29
      by: model:Codex
      tool: web
  agents:
    - id: model:Codex
      type: model
    - id: tool:web
      type: tool
source_status: active
raw_location:
processing_mode: immediate
processing_level: light
review_priority: normal
review_owner: Codex
formalization_status: source-only
topics:
  - provenance
  - traceability
  - source-record
projects:
  - verified-action-knowledge-system
source_family: w3c-prov
upstream_sources: []
verification_status: primary-source-captured
candidate_relation_suggestions: []

---

# 来源记录：W3C PROV

## 为什么收录

Pro 第三个补充建议用 W3C PROV 给 source provenance 一个标准化骨架。

本项目只吸收轻量思想：

```text
source identity:
  资料是什么，从哪里来，什么版本

capture / extraction:
  谁或什么工具采集、提取过

agent:
  用简单 human / model / tool 字符串记录
```

不吸收完整 PROV ontology、RDF/OWL serializations、validator、query protocol 或 provenance graph。

## 来源信息

- 发布方：W3C Provenance Working Group
- PROV-Overview：W3C Working Group Note, 2013-04-30
- PROV-DM：W3C Recommendation, 2013-04-30
- 原始链接：
  - https://www.w3.org/TR/prov-overview/
  - https://www.w3.org/TR/prov-dm/
- 采集方式：官方文档网页核验

## 初步看点

- PROV 的核心描述对象是 entities、activities 和 people/agents involved in producing data or things。
- PROV-DM 是 W3C provenance family 的 conceptual data model。
- 这正好可以给本项目的 source provenance 提供轻量词汇，但不要求 source record 承担 review、promotion 或 context-pack 使用日志。

## 吸收方式

```text
Use PROV-lite, not full PROV.

entity:
  source identity and version

activity:
  capture and extraction in the source record
  review, promotion, and context-pack use in their own records

agent:
  human, model, tool
```

## 边界

```text
PROV-lite records traceability.
It does not decide truth.
It does not raise confidence.
It does not turn a citation into support.
```

## 可抽取 Candidate Points

1. Source provenance should track the material, the handling activity, and the responsible agent.
2. Source trace can borrow PROV's entity/activity/agent skeleton without implementing the full standard.
3. Source records should stay light: review, promotion, and context-pack use belong to reviewed nodes, promotion records, context packs, or the use ledger.
4. Traceability improves reviewability and trust assessment, but it is not itself a truth judgment.

## 下一步

- Keep the source template lightweight.
- Use optional `provenance:` only when a source is important enough for medium/heavy processing.
