---
type: pattern
status: pattern-candidate
created: 2026-05-26
updated: 2026-05-26
tags:
  - pattern/lint
  - pattern/health-check
  - verified-knowledge-system
sources:
  - "[[2026-05-26-llm-wiki-compiler-source]]"
  - "[[2026-05-26-llm-wiki-compiler-architecture-review]]"
  - "[[vault-health-check-as-maintenance-contract]]"
verification_status: primary-source
evidence_level: primary
confidence: high
last_verified: 2026-05-26
next_review: 2026-06-02
epistemic_type: take
holder: Codex
valid_from: 2026-05-26
valid_until:
gaps:
  - "Need to implement first local lint script for SCHEMA.md v0.1."
evidence_timeline:
  - date: 2026-05-26
    event: "llm-wiki-compiler source review found static lint before candidate approval."
source_libraries:
  - atomicstrata/llm-wiki-compiler
related_concepts:
  - "[[vault-health-check-as-maintenance-contract]]"
related_projects:
  - verified-knowledge-system
adoption_status: adopt-soon
evidence_count: 3
negative_evidence:
  - "[[automatic-agentic-vault-rewrite-before-schema-stability]]"
relations:
  - target: "[[automatic-agentic-vault-rewrite-before-schema-stability]]"
    type: alternative_to
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-26-llm-wiki-compiler-source]]"
    rationale: "Static lint surfaces problems without silently rewriting the vault."
    created: 2026-05-26
    last_verified: 2026-05-26
---

# 设计模式：Static Wiki Health Lint Before Auto Rewrite

## 一句话定义

程序先做无 LLM 的结构、链接、证据和状态检查；在 schema 稳定前，不做后台自动改写。

## 解决的问题

自动 rewrite 看起来省事，但会造成隐藏漂移：字段被改、关系被补、冲突被“自动解决”，最后没人知道正式知识层为什么变成现在这样。

static lint 的作用是把问题变成可见报告，而不是替用户做裁决。

## 适用场景

- review candidate 批准前。
- 每次大批量入库后。
- 生成 context pack 前。
- Misa/gbrain 输出候选后。

## 不适用场景

- 需要语义判断的真假裁决。
- 需要人工权衡的 decision。
- source 本身质量低或不完整时。

## 来源证据

`llm-wiki-compiler` 的 lint 规则是静态检查，不需要 API key，也不调用 LLM。它检查断链、孤儿页、缺 summary、重复概念、空页、broken citations、低 confidence、contradicted page、未引用推断段落、schema cross-link minimum 等。

## 最小实现方式

本资料库 v0.1 lint 清单：

- 必填字段缺失：`type/status/created/updated/verification_status/evidence_level/confidence/relations`。
- 未知 `type`。
- 未知 `verification_status` 或 `evidence_level`。
- `sources` 指向不存在节点或缺失 source record。
- `relations[].target` 断链。
- `relations[]` 缺 `type/strength/confidence/evidence/rationale`。
- `claim` 没有来源。
- `pattern` 没有适用/不适用场景。
- `anti-pattern` 没有替代方案。
- `decision` 没有风险、反例或回退。
- `status: active` 但 `verification_status: unverified/conflicted`。
- `next_review` 已过期。

## 项目融合建议

先写 `outputs/health/` 报告，不自动修文件。等 schema 稳定后，再允许 Codex 根据报告逐项修复。

## 验证指标

- lint 能否在候选入库前拦住明显坏节点。
- 报告是否可读、可复查、可追踪。
- 自动化是否没有绕过用户 final authority。
