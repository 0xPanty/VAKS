---
type: pattern
status: sandbox-candidate
created: 2026-05-27
updated: 2026-06-08
tags:
  - pattern/context-pack
  - pattern/agent
  - pattern/budget
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
adoption_status: sandbox-test
evidence_count: 2
negative_evidence: []
relations:
  - target: "[[context-pack-evidence-envelope]]"
    type: refines
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-27-llm-wiki-compiler-implementation-extraction]]"
    rationale: "Context packs need budget, warning, gap, and source-window safety contracts before agents can rely on them."
    created: 2026-05-27
    last_verified: 2026-05-27
---

# 设计模式：Agent Context Pack Budget Guardrails

## 一句话定义

Agent context pack 必须有预算、裁剪顺序、warnings/gaps，以及 raw source window 的安全边界。

## 解决的问题

没有预算的 context pack 会爆上下文；没有 warnings/gaps 的 context pack 会让 agent 误以为资料完整；没有 source window 防护则会泄露 raw 文件或越界读取。

## 来源证据

`llm-wiki-compiler` 的 context 实现包括：

- `src/context/types.ts`：稳定 v1 envelope。
- `src/context/budget.ts`：token 估算和 deterministic trimming。
- `src/context/provenance.ts`：source window 上限、line window 上限、path confinement。
- `src/context/retrieval.ts`：semantic retrieval 失败时降级并返回稳定 warning。
- `src/context/ranking.ts`：lexical / exact / semantic / graph-neighbor reasons。

CI-07 sandbox anchor snapshots:

- `outputs/review/ci-07-agent-context-pack-budget-guardrails-2026-06-08/evidence/llm-wiki-compiler/context-budget-anchor-snapshot.md`
- `outputs/review/ci-07-agent-context-pack-budget-guardrails-2026-06-08/evidence/llm-wiki-compiler/source-window-budget-anchor-snapshot.md`
- `outputs/review/ci-07-agent-context-pack-budget-guardrails-2026-06-08/evidence/llm-wiki-compiler/retrieval-warning-anchor-snapshot.md`

Checked source anchors:

- `src/context/budget.ts:1-24` token estimation, deterministic trimming, JSON validity.
- `src/context/budget.ts:31-43` trimmed section names and token estimator.
- `src/context/budget.ts:56-69` budget envelope defaults.
- `src/context/budget.ts:77-103` deterministic trim result.
- `src/context/budget.ts:116-173` section trimming implementation.
- `src/context/build.ts:449-505` budget finalization and structured truncation fields.
- `src/context/provenance.ts:101-137` per-pack source-window budget.
- `src/context/provenance.ts:139-149` path-guarded source window reads.
- `src/context/provenance.ts:152-198` source root confinement and traversal rejection.
- `src/context/provenance.ts:222-246` clamped line windows.
- `src/context/build.ts:513-565` project warnings before budget trimming.
- `src/context/retrieval.ts:38-70` stable semantic retrieval warning codes.
- `src/context/retrieval.ts:72-108` best-effort retrieval with warnings.
- `src/context/retrieval.ts:115-147` missing/malformed/empty store fallback.
- `src/context/retrieval.ts:149-175` provider failure classification.
- `src/context/types.ts:44-55` budget envelope.
- `src/context/types.ts:150-161` top-level pack includes budget, warnings, and gaps.

## VAKS Boundary

Budget guardrails are context-pack safety, not truth logic.

Budget trimming may remove lower-priority context, but it must not hide:

- warnings
- gaps
- missing evidence
- source-window unavailability
- evidence insufficiency
- action-risk notes
- unresolved contradictions

If trimming removes source windows, chunks, or primary entries needed for an action-facing claim, the pack cannot be marked action-ready until the missing support is restored or the scope is narrowed.

Budget fields are warnings about context loss. They are not proof, review, approval, retrieval quality, or evidence sufficiency.

## 可直接采用的规则

```text
trim order:
1. neighbors
2. source windows
3. chunks
4. primary nodes
```

```text
source windows:
- 默认关闭
- include_sources 才开启
- 只允许 raw/source 目录
- 拒绝绝对路径
- 拒绝 ..
- 拒绝 symlink escape
- 单个窗口限制行数
- 整包限制窗口数量
```

## 我们的升级

增加 verified/action 字段：

```yaml
verification:
  verification_status:
  evidence_level:
  confidence:
  negative_evidence:
  last_verified:
  next_review:
actionability:
  decision_status:
  recommended_action:
  risk:
  rollback:
  success_metric:
warnings: []
gaps: []
```

CI-07 sandbox additions:

```yaml
budget:
  requested_tokens:
  estimated_tokens:
  truncated: true | false
  trimmed_sections:
    - neighbors
    - sourceWindows
    - chunks
    - primary
budget_guardrails:
  deterministic_trim_order:
    - neighbors
    - sourceWindows
    - chunks
    - primary
  preserve_warnings: true
  preserve_gaps: true
  source_windows_default: off
  source_windows_opt_in: include_sources
  action_ready_blocked_when_key_support_trimmed: true
```

## 项目融合建议

v0.2 先写 `context-pack.v0.json` 示例。v0.3 再做 API/MCP。

## 验证指标

- context pack 输出永远是有效 JSON。
- 召回原因可解释。
- 低可信和冲突节点不会被静默包装成“可用证据”。
- raw snippets 默认不出现。
- budget.truncated / trimmed_sections 是否暴露裁剪。
- warnings/gaps 是否不会因预算裁剪而消失。
- 关键 source window / chunk / primary 被裁掉时，action_readiness 是否被挡住。
- semantic retrieval 失败是否返回稳定 warning，而不是静默当作完整检索。
