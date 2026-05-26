---
type: pattern
status: active
created: 2026-05-27
updated: 2026-05-27
source_libraries:
  - OpenKB
  - llm-wiki-compiler
  - Karpathy LLM Wiki
related_concepts:
  - "[[2026-05-27-openkb-architecture-review]]"
  - "[[2026-05-27-quality-bar-extensible-verified-action-knowledge-system]]"
related_projects:
  - verified-knowledge-system
adoption_status: adopt
tags:
  - pattern/architecture
  - output-adapter
  - context-pack
evidence_count: 3
confidence: high
negative_evidence:
  - "[[auto-compiled-concept-wiki-as-verified-truth-layer]]"
replaces:
superseded_by:
relations:
  - target: "[[2026-05-27-openkb-as-module-reference]]"
    type: supports
    strength: 5
    confidence: high
    evidence:
      - "[[wiki-foundation-generator-surface-separation]]"
    rationale: "OpenKB strongly demonstrates that compiled knowledge should be separated from query/chat/skill outputs."
    created: 2026-05-27
    last_verified: 2026-05-27
extension_points:
  - context pack modes
  - output adapters
  - agent access tiers
---

# 设计模式：Wiki Foundation 与 Generator Surface 分离

## 一句话定义

把知识底座和输出生成器分开：wiki/verified graph 负责积累和验证，query/chat/skill/report 只负责把底座变成当前任务需要的输出。

## 解决的问题

如果知识库和输出层混在一起，会出现两个问题：

- 每次 query 都重新发明知识，不能积累。
- 输出生成器为了好用，反过来污染 truth layer。

分层后：

```text
foundation stores reusable knowledge
generator produces task-specific output
```

## 适用场景

- 资料库要同时服务问答、写作、agent context、skill、项目决策。
- 知识要长期维护，但输出形态会不断变化。
- 需要支持多个 agent 或多个产品表面。

## 不适用场景

- 只有一次性问答，不需要沉淀。
- 资料规模很小，不值得维护 generator。
- 没有 review/lint，导致 generator 输出被误写回 truth layer。

## 反例与避坑

- 失败条件：generator 可以直接改 formal wiki。
- 相似反模式：[[auto-compiled-concept-wiki-as-verified-truth-layer]]
- 复杂度风险：过早做太多 output adapters。
- 替代方案：先做 context pack，再做 skill/report/podcast 等生成器。

## 来源证据

- OpenKB README 明确分成 wiki foundation 与 generators。
- OpenKB 源码中 query/chat/skill/lint 都在 wiki 之上工作。
- `llm-wiki-compiler` 也有 context/export/MCP/viewer 等派生表面。

## 标签与量化

- domain: knowledge architecture
- problem: output surfaces should not own truth
- maturity: emerging
- complexity: medium
- problem_fit: 5
- reuse_value: 5
- implementation_cost: 3
- integration_fit: 5
- evidence_strength: 4
- reversibility: 5

## 交叉验证

- 相似来源：Karpathy LLM Wiki、OpenKB、llm-wiki-compiler。
- 历史项目影子：Misa/gbrain/context pack 需要从可信底座读取，而不是各自维护记忆副本。
- 支持证据：多个项目都把 wiki/compiled knowledge 作为 substrate。
- 反例：纯 RAG 每次 query 重新召回，知识不自然复利。

## 最小实现方式

v0.1：

```text
wiki/ verified nodes
-> manual context pack markdown/json
-> outputs/qa or outputs/review
```

v0.2：

```text
context_pack builder
query mode
decision mode
implementation mode
skill candidate mode
```

## 项目融合建议

采用为核心架构原则。

但本资料库中的 foundation 不是 OpenKB 的 generic concepts，而是：

```text
source / summary / claim / pattern / anti-pattern / decision
```

## 可拓展性

- 可以通过什么接口/适配层接入：context pack modes、output adapters、agent access tiers。
- 未来可能被什么替代：更强的 API/MCP/viewer，但不替代 foundation。
- 替换或升级成本：低，前提是 output layer 不写 truth。
- 回退方式：直接读 Markdown verified nodes。

## 验证指标

- 同一批 verified nodes 能否生成不同输出：answer、decision、implementation pack、skill。
- 输出错了能否不污染 truth layer。
- 新 generator 是否能只依赖 context pack contract 接入。
