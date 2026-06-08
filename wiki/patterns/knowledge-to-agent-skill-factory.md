---
type: pattern
status: active
created: 2026-05-27
updated: 2026-05-27
source_libraries:
  - OpenKB
related_concepts:
  - "[[2026-05-27-openkb-architecture-review]]"
  - "[[wiki-foundation-generator-surface-separation]]"
related_projects:
  - verified-knowledge-system
adoption_status: adopt
tags:
  - pattern/output-adapter
  - agent-skill
  - skill-factory
  - action-basis
evidence_count: 1
confidence: high
negative_evidence:
replaces:
superseded_by:
relations:
  - target: "[[wiki-foundation-generator-surface-separation]]"
    type: implements
    strength: 4
    confidence: high
    evidence:
      - "[[knowledge-to-agent-skill-factory]]"
    rationale: "Skill Factory is a concrete generator surface built on top of compiled wiki knowledge."
    created: 2026-05-27
    last_verified: 2026-05-27
extension_points:
  - output adapters
  - context pack modes
  - agent access tiers
  - feedback adapters
---

# 设计模式：Knowledge-to-Agent Skill Factory

## 一句话定义

把已验证知识编译成可安装、可触发、可评估、可回滚的 agent skill，而不是每次都临时塞 context。

## 解决的问题

context pack 适合一次任务，但有些知识会反复被 agent 使用：

- 某个专家方法论。
- 某个项目操作规范。
- 某类决策规则。
- 某套风格/写作/研究流程。

如果每次都重新检索和解释，成本高、触发不稳定、质量不可复盘。

Skill Factory 的价值是把知识变成一个可分发能力包：

```text
verified knowledge
-> skill candidate
-> SKILL.md + references
-> validate
-> eval trigger/body coverage
-> iteration history / rollback
```

## 适用场景

- Misa/Codex/Hermes 需要长期复用某套知识。
- 资料库中某个主题已经足够稳定。
- 用户想把知识交给多个 agent 使用。
- 某个决策流程需要明确 trigger conditions 和 not-for boundaries。

## 不适用场景

- 知识还没有验证，只是 raw summary。
- 主题太宽，skill 会变成泛泛指南。
- 没有 trigger evaluation，容易过度触发。
- 下游 agent 不支持 skill/plugin。

## 反例与避坑

- 失败条件：从 unverified concept 直接生成 skill。
- 相似反模式：把漂亮的 skill 文案当成可信知识。
- 复杂度风险：维护 marketplace、eval、rollback 会变成新产品线。
- 替代方案：先做 context pack mode，再做 skill candidate。

## 来源证据

OpenKB 的 Skill Factory 包含：

- `openkb skill new`
- `output/skills/<name>/SKILL.md`
- `references/`
- `marketplace.json`
- `skill validate`
- `skill eval`
- `skill history`
- `skill rollback`

源码中的 evaluator 明确区分 trigger accuracy 和 body alignment，这是非常有价值的质量门。

## 标签与量化

- domain: output adapter
- problem: reusable agent capability
- maturity: emerging
- complexity: high
- problem_fit: 5
- reuse_value: 5
- implementation_cost: 4
- integration_fit: 4
- evidence_strength: 4
- reversibility: 4

## 交叉验证

- 相似来源：OpenKB Skill Factory、Codex skills、Claude skills、Misa/Hermes skill/memory 需求。
- 历史项目影子：用户希望 Misa 能读取资料库，但不直接改 truth layer。
- 支持证据：OpenKB 已把 wiki -> skill 做成 CLI 流程。
- 反例：如果生成 skill 没有 eval，很容易变成另一个不可信 prompt 文件。

## 最小实现方式

先不做完整 Skill Factory，先定义 skill candidate：

```text
outputs/review/skills/<skill-name>.md
```

字段：

```yaml
source_nodes:
trigger_description:
not_for:
decision_rules:
references:
known_gaps:
validation_status:
eval_prompts:
```

通过 review 后再导出为真实 `SKILL.md`。

## 项目融合建议

中期吸收，不进入第一阶段最小闭环。

优先顺序：

```text
context pack contract
-> agent access rules
-> reviewed skill candidate
-> skill validate/eval
-> installable skill output
```

## 可拓展性

- 可以通过什么接口/适配层接入：output adapter、context pack mode、agent access tier。
- 未来可能被什么替代：MCP tool package、Codex skill、Claude skill、Hermes plugin。
- 替换或升级成本：中高，但 references 和 decision rules 可保留。
- 回退方式：回退成 Markdown context pack。

## 验证指标

- skill 是否只由 verified nodes 生成。
- trigger description 是否不过宽。
- body 是否真的覆盖 trigger claims。
- eval miss 是否能反馈到 skill revision。
- skill 输出是否保留来源和 known gaps。
