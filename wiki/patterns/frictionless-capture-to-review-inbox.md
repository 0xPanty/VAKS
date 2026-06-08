---
type: pattern
status: active
created: 2026-05-27
updated: 2026-05-27
source_libraries:
  - cyrilXBT automated Obsidian vault article
related_concepts:
  - "[[source-adapter-ingest-contract]]"
  - "[[url-source-ingest-normalization]]"
related_projects:
  - verified-knowledge-system
adoption_status: adopt
tags:
  - pattern/capture
  - inbox
  - review-queue
evidence_count: 1
confidence: medium
negative_evidence:
replaces:
superseded_by:
relations:
  - target: "[[source-adapter-ingest-contract]]"
    type: refines
    strength: 4
    confidence: medium
    evidence:
      - "[[frictionless-capture-to-review-inbox]]"
    rationale: "Low-friction capture improves source coverage, but must land in review rather than truth."
    created: 2026-05-27
    last_verified: 2026-05-27
extension_points:
  - source adapters
  - review workflows
---

# 设计模式：Frictionless Capture to Review Inbox

## 一句话定义

把 Readwise、Telegram、voice note、clipper 等低摩擦入口统一导入 raw/inbox/review，而不是要求用户手动整理。

## 解决的问题

如果 capture 需要超过几秒，人会放弃。长期资料库最大的断点不是 schema，而是资料根本没进来。

## 适用场景

- 快速想法。
- 文章/highlight。
- 推文/bookmark。
- 语音转录。
- 移动端临时输入。

## 不适用场景

- 高风险事实。
- 需要立即成为 decision 的内容。
- 来源不明、可能污染系统的自动内容。

## 反例与避坑

- 失败条件：capture 直接写 formal wiki。
- 相似反模式：自动入库即自动采纳。
- 复杂度风险：入口太多导致 inbox 垃圾堆。
- 替代方案：先只支持手动 raw/source record。

## 来源证据

用户粘贴的 automated Obsidian vault 文章强调 capture friction 是知识系统失败原因之一，并提出 Readwise、Airr、Whisper、Telegram bot、N8N 自动写入 vault。

## 标签与量化

- domain: source ingest
- problem: capture friction
- maturity: emerging
- complexity: medium
- problem_fit: 4
- reuse_value: 4
- implementation_cost: 3
- integration_fit: 4
- evidence_strength: 3
- reversibility: 5

## 最小实现方式

v0.1：

```text
inbox/
outputs/review/inbox/
```

所有自动 capture 只写候选文件：

```yaml
capture_source:
captured_at:
raw_text:
processing_status: unreviewed
```

## 项目融合建议

可以进 `IMPLEMENTATION_BLUEPRINT.md`，但排在 review queue 之后。先有收口，再放开入口。

## 可拓展性

- 可以通过什么接口/适配层接入：source adapter、review workflow。
- 未来可能被什么替代：browser clipper、mobile app、webhook。
- 替换或升级成本：低。
- 回退方式：手动写 raw/source。

## 验证指标

- capture 是否低摩擦。
- inbox 是否有处理状态。
- 未 review 内容是否不会进入 verified graph。
