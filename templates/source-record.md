---
type: source
status: source-captured
title:
source_id:
source_uri:
source_url:
source_type: article
author:
publisher:
published_at:
updated_at:
captured_at:
captured_by:
version_or_commit:
source_status: unknown
raw_location:
processing_mode: inbox
processing_level: light
review_priority: normal
review_owner: Codex
formalization_status: raw-only
topics:
projects:
source_family:
upstream_sources: []
verification_status: unverified
relations: []
tags:
---

# 来源记录：

## 为什么收录


## 来源信息

- 作者：
- 发布方：
- 发布时间：
- 更新时间：
- 原始链接：
- 原始位置：
- 版本 / commit / DOI：
- source_status: active / legacy / deprecated / unknown
- 采集方式：

## Medium / Heavy Optional Provenance

```yaml
extraction:
  extracted_at:
  extracted_by:
  model:
  tool:
  source_ranges: []

provenance:
  model: PROV-lite
  activities:
    - type: captured
      at:
      by:
    - type: extracted
      at:
      by:
      tool:
      model:
  agents:
    - id:
      type: human | model | tool
```

说明：

```text
provenance 只记录来源和处理轨迹，不代表这个 source 支持了某个 claim。
claim 是否成立，仍然要进入 candidate / calibration / review。
review、promotion、context-pack use 不放在 Source 主字段里。
```

## 时间线 / 上下文

- 作者/组织背景：
- 当时版本或阶段：
- 后续更新：
- 是否 legacy / deprecated：
- 为什么这个时间点重要：

## 初步看点



## 明显疑点


## 可抽取 Candidate Points


## 当前处理等级

```text
light / medium / heavy
```

升级到 heavy 的条件：

-


## 可选验证字段

```yaml
source_quality:
freshness:
relevance:
confidence:
cross_source_count:
last_verified:
next_review:
```

## 关系边 / 关联强度

```yaml
relations:
  - target: "[[claim-or-pattern]]"
    type: derived_from | supports | contradicts | refines | risk_of
    relation_state: candidate | reviewed | rejected | stale
    strength: 1-5
    confidence: low | medium | high
    evidence:
      - "[[this-source]]"
    rationale: "One sentence explaining what this source contributes."
    created:
    last_verified:
```


## 下一步
