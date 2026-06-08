---
type: pattern
status: active
created: 2026-05-27
updated: 2026-05-27
source_libraries:
  - cyrilXBT automated Obsidian vault article
related_concepts:
  - "[[2026-05-27-automated-vault-feedback-loop-review]]"
  - "[[context-pack-evidence-envelope]]"
related_projects:
  - verified-knowledge-system
adoption_status: adopt
tags:
  - pattern/feedback
  - daily-brief
  - knowledge-return
evidence_count: 1
confidence: medium
negative_evidence:
  - "[[automated-brief-as-truth-without-review]]"
replaces:
superseded_by:
relations:
  - target: "[[context-pack-evidence-envelope]]"
    type: refines
    strength: 4
    confidence: medium
    evidence:
      - "[[daily-brief-as-knowledge-return-loop]]"
    rationale: "Daily briefs are recurring context packs that return connections and questions to the user."
    created: 2026-05-27
    last_verified: 2026-05-27
extension_points:
  - context pack modes
  - feedback adapters
  - output adapters
---

# 设计模式：Daily Brief as Knowledge Return Loop

## 一句话定义

每天自动生成一个简短 brief，把最近资料和旧知识之间的连接、模式和问题推回给用户。

## 解决的问题

知识库只进不出，就会变成死档案。

Daily brief 的目标不是总结所有内容，而是让系统每天“回响”一次：

```text
connections
pattern
question
```

## 适用场景

- 每天有新 capture。
- 用户希望持续看到跨资料连接。
- 需要形成长期思考复利。

## 不适用场景

- 没有 review queue，brief 会变成幻觉扩音器。
- 新资料太少，不需要每天跑。
- 高风险决策，不能靠 daily brief 直接行动。

## 反例与避坑

- 失败条件：brief 直接修改 claim/decision。
- 相似反模式：[[automated-brief-as-truth-without-review]]
- 复杂度风险：每天生成大量低质量文本，反而增加噪音。
- 替代方案：手动 weekly synthesis。

## 来源证据

用户粘贴文章提出 weekday 6am daily brief，内容包含 recent connections、weekly pattern、one question。

## 标签与量化

- domain: feedback
- problem: no reason to return
- maturity: emerging
- complexity: low
- problem_fit: 5
- reuse_value: 4
- implementation_cost: 2
- integration_fit: 5
- evidence_strength: 3
- reversibility: 5

## 最小实现方式

先不自动排程，手动命令/提示即可：

```text
read latest inbox/review candidates
read recent verified nodes
produce:
  3 connections
  1 pattern
  1 question
write to outputs/review/daily-brief-YYYY-MM-DD.md
```

## 项目融合建议

进入 `CONTEXT_PACK.md`：作为 `mode: daily_brief`。

进入 `LINT_RULES.md`：brief 必须标注哪些来自 verified nodes，哪些只是 unreviewed captures。

## 可拓展性

- 可以通过什么接口/适配层接入：context pack mode、feedback adapter、output adapter。
- 未来可能被什么替代：dashboard、email、IM digest。
- 替换或升级成本：低。
- 回退方式：手动读 index + recent nodes。

## 验证指标

- brief 是否引用来源。
- brief 是否区分 verified/unverified。
- brief 是否产生可用 review/action candidate。
- brief 是否减少用户忘记重要资料的概率。
