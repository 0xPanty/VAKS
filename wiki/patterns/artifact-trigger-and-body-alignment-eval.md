---
type: pattern
status: active
created: 2026-05-27
updated: 2026-05-27
source_libraries:
  - OpenKB
related_concepts:
  - "[[knowledge-to-agent-skill-factory]]"
  - "[[wiki-foundation-generator-surface-separation]]"
related_projects:
  - verified-knowledge-system
adoption_status: adopt-candidate
tags:
  - pattern/eval
  - agent-skill
  - output-quality
evidence_count: 1
confidence: high
negative_evidence:
replaces:
superseded_by:
relations:
  - target: "[[knowledge-to-agent-skill-factory]]"
    type: refines
    strength: 5
    confidence: high
    evidence:
      - "[[artifact-trigger-and-body-alignment-eval]]"
    rationale: "A generated skill is not reliable until its activation trigger and body coverage are evaluated separately."
    created: 2026-05-27
    last_verified: 2026-05-27
extension_points:
  - output adapters
  - feedback adapters
  - lint rule packs
---

# 设计模式：Artifact Trigger and Body Alignment Eval

## 一句话定义

对生成的 agent skill/output artifact 分开评估两件事：什么时候应该触发，以及触发后内容是否真的够用。

## 解决的问题

一个 skill 可能有两种失败：

- 描述太宽，什么问题都触发。
- 描述很准，但正文空泛，触发后帮不上忙。

OpenKB 的 evaluator 把这两件事分开：

```text
trigger accuracy = description-only grader
body alignment = SKILL.md body + references coverage grader
```

这对我们很重要，因为未来的 Misa/Codex skill 如果触发错，会比普通文档错得更隐蔽。

## 适用场景

- 从 verified nodes 生成 skill。
- 从知识库生成 prompt pack、agent memory pack、workflow pack。
- 需要决定某个 artifact 是否可以交给 agent 自动加载。

## 不适用场景

- 一次性输出，不会被 agent 自动触发。
- 只有人类阅读的报告。
- 没有足够样本生成 should-trigger / should-not questions。

## 反例与避坑

- 失败条件：只检查文件格式，不检查触发边界。
- 相似反模式：skill description 写成主题标签。
- 复杂度风险：LLM eval 自身也会错，不能作为唯一采纳依据。
- 替代方案：人工 review + small fixed eval set。

## 来源证据

OpenKB `skill/evaluator.py` 明确设计两类指标：trigger accuracy 和 body alignment。它生成 should-trigger / should-not prompts，再用 description-only grader 判断触发，用 body+references grader 判断内容是否支持。

`skill/validator.py` 则提供确定性结构检查：SKILL.md frontmatter、name/description、文件大小、references link、foreign wikilinks、stdlib-only scripts 等。

## 标签与量化

- domain: output quality
- problem: generated skill reliability
- maturity: emerging
- complexity: medium
- problem_fit: 5
- reuse_value: 5
- implementation_cost: 3
- integration_fit: 5
- evidence_strength: 4
- reversibility: 5

## 交叉验证

- 相似来源：OpenKB skill eval、Codex skill trigger model、agent access tiers。
- 历史项目影子：Misa 以后可能需要加载领域 skill；误触发会污染行动。
- 支持证据：OpenKB 把 validate 和 eval 都放进 Skill Factory。
- 反例：LLM-generated eval set 需要人工抽查。

## 最小实现方式

给每个 skill candidate 保存：

```yaml
eval:
  should_trigger: []
  should_not_trigger: []
  trigger_pass_rate:
  body_alignment_rate:
  misses: []
  reviewer_notes:
```

第一阶段可以人工写 5 个 should-trigger 和 5 个 should-not。

## 项目融合建议

吸收为 `knowledge-to-agent-skill-factory` 的质量门。

在 `CONTEXT_PACK.md` 和 `AGENT_ACCESS.md` 之后再做，不要抢在 review queue 前面。

## 可拓展性

- 可以通过什么接口/适配层接入：output adapter、feedback adapter、lint rule pack。
- 未来可能被什么替代：真实使用日志、agent telemetry、human acceptance tests。
- 替换或升级成本：低。
- 回退方式：skill 标记为 draft，只通过 manual context pack 使用。

## 验证指标

- false positive trigger 是否下降。
- false negative trigger 是否下降。
- skill body 是否能回答 should-trigger questions。
- eval miss 是否能产生 revision。
