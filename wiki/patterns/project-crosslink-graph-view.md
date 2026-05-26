---
type: pattern
status: draft
created: 2026-05-27
updated: 2026-05-27
source_libraries:
  - user-discussion
sources:
  - "[[SCHEMA]]"
  - "[[ARCHITECTURE_PRINCIPLES]]"
  - "[[semantic-relation-edge-schema]]"
related_concepts:
  - "[[semantic-relation-edge-schema]]"
  - "[[obsidian-bases-linked-workbench-views]]"
related_projects:
  - verified-action-knowledge-system
adoption_status: adopt-candidate
verification_status: single-source
evidence_level: synthetic
evidence_count: 1
confidence: medium
negative_evidence:
  - "A dense visual graph can look impressive while hiding weak or unverified relations."
replaces:
superseded_by:
extension_points:
  - viewer / Obsidian workbench
  - context pack modes
  - relation / health layer
last_verified: 2026-05-27
next_review: 2026-06-03
epistemic_type: take
gaps:
  - "No actual graph viewer implementation yet."
  - "Project node schema is not fully specified yet."
evidence_timeline:
  - date: 2026-05-27
    source: "user discussion"
    observation: "User asked whether multiple projects and their shared parts can be shown as a relation graph."
    effect: refines
    confidence: medium
relations:
  - target: "[[semantic-relation-edge-schema]]"
    type: implements
    strength: 4
    confidence: medium
    evidence:
      - "[[project-crosslink-graph-view]]"
    rationale: "Project graph views should render typed relations rather than inventing visual-only links."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[obsidian-bases-linked-workbench-views]]"
    type: refines
    strength: 3
    confidence: medium
    evidence:
      - "[[project-crosslink-graph-view]]"
    rationale: "The view can use Obsidian/Bases/viewer surfaces while keeping Markdown relations as truth."
    created: 2026-05-27
    last_verified: 2026-05-27
tags:
  - pattern/viewer
  - project-graph
  - relation-graph
---

# Project Crosslink Graph View

## AI-readable preamble

This pattern is a visualization/workbench idea, not a new truth layer.

It displays how projects share claims, patterns, anti-patterns, decisions, implementation notes, and sources. The visual graph must be generated from reviewed `relations`, not from unverified link density alone.

Current status: useful viewer/workbench candidate.

## 一句话定义

把多个项目之间共享的关键知识点、模式、反模式、决策和实现记录展示成关系图。

## 解决的问题

用户可能同时做多个项目，例如 Misa、Hermes、资料库、AI 短剧、内容系统、VPS 自动化。

这些项目经常共享同一套底层东西：

```text
agent 权限边界
review gate
context pack
feedback timeline
source-to-publish pipeline
anti-pattern
implementation note
```

如果只按项目文件夹看，很容易看不出哪些能力应该抽象成通用模块，哪些坑会跨项目复现。

## 图应该展示什么

```text
project -> uses pattern
project -> avoids anti-pattern
project -> based_on decision
project -> field-tests claim
project -> produces implementation-note
project -> shares source/context pack with another project
```

## 不是什么

不是普通 Obsidian 漂亮大网图。

它不应该只靠：

```text
双链数量
tag 相同
vector 相似
文件名相近
```

这些可以当候选线索，但不能直接成为正式关系边。

## 最小实现方式

先不做独立 App。

```text
1. 在 project / decision / pattern / implementation-note 中补 related_projects 和 relations。
2. 用 Obsidian graph 或 Bases 做第一版视图。
3. 未来 viewer/API 从 YAML relations 生成 project graph。
```

## 项目融合建议

放在 viewer / Obsidian workbench layer。

优先级低于：

```text
REVIEW_QUEUE.md
CONTEXT_PACK.md
LINT_RULES.md
AGENT_ACCESS.md
```

但它是未来 dashboard/viewer 的重要需求。

## 验证指标

- 是否能看到多个项目共享的 pattern。
- 是否能发现一个 decision 影响哪些项目。
- 是否能发现跨项目反模式。
- 是否能从图上点回证据、关系理由和来源。
- 是否明确区分 candidate relation 和 reviewed relation。
