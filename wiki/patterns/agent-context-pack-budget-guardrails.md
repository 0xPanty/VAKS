---
type: pattern
status: pattern-candidate
created: 2026-05-27
updated: 2026-05-27
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
adoption_status: adopt-soon
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

## 项目融合建议

v0.2 先写 `context-pack.v0.json` 示例。v0.3 再做 API/MCP。

## 验证指标

- context pack 输出永远是有效 JSON。
- 召回原因可解释。
- 低可信和冲突节点不会被静默包装成“可用证据”。
- raw snippets 默认不出现。
