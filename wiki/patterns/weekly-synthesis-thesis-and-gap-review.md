---
type: pattern
status: active
created: 2026-05-27
updated: 2026-05-27
source_libraries:
  - cyrilXBT automated Obsidian vault article
related_concepts:
  - "[[think-gather-synthesize-gap-analysis]]"
  - "[[compiled-truth-plus-append-only-timeline]]"
  - "[[2026-05-27-automated-vault-feedback-loop-review]]"
related_projects:
  - verified-knowledge-system
adoption_status: adopt-candidate
tags:
  - pattern/synthesis
  - weekly-review
  - gaps
  - contradictions
evidence_count: 2
confidence: medium
negative_evidence:
replaces:
superseded_by:
relations:
  - target: "[[think-gather-synthesize-gap-analysis]]"
    type: refines
    strength: 4
    confidence: medium
    evidence:
      - "[[weekly-synthesis-thesis-and-gap-review]]"
    rationale: "Weekly synthesis operationalizes thesis, contradiction, gap, and action review."
    created: 2026-05-27
    last_verified: 2026-05-27
extension_points:
  - feedback adapters
  - review workflows
---

# 设计模式：Weekly Synthesis Thesis and Gap Review

## 一句话定义

每周把最近资料和已有知识综合一次，产出 emerging thesis、contradictions、knowledge gaps、one action。

## 解决的问题

Daily brief 负责轻量回响，但真正形成思考复利需要低频深加工。

Weekly synthesis 的价值是把碎片变成：

```text
正在形成的观点
正在冲突的证据
明显缺失的视角
本周最值得做的一件事
```

## 适用场景

- 每周有新资料、新项目、新判断。
- 需要观察自己的思考方向。
- 需要把 unreviewed captures 升级为 claims/patterns。

## 不适用场景

- 资料太少，可以两周一次。
- 没有来源标注，综合会变成空泛观点。
- 需要正式 decision 时，weekly synthesis 只能生成 candidate。

## 反例与避坑

- 失败条件：把 emerging thesis 当 final decision。
- 相似反模式：自动综合直接改 truth layer。
- 复杂度风险：每周报告太长没人读。
- 替代方案：只做 contradiction/gap report。

## 来源证据

用户粘贴文章提出 weekly synthesis prompt：emerging thesis、contradictions、knowledge gaps、one action。

gbrain 的 think/gap/dream cycle 也支持周期性综合与 gap tracking。

## 标签与量化

- domain: synthesis
- problem: fragment-to-thesis conversion
- maturity: emerging
- complexity: medium
- problem_fit: 5
- reuse_value: 5
- implementation_cost: 3
- integration_fit: 5
- evidence_strength: 4
- reversibility: 5

## 最小实现方式

输出到：

```text
outputs/review/weekly-synthesis-YYYY-WW.md
```

结构：

```yaml
emerging_thesis:
contradictions:
knowledge_gaps:
one_action:
candidate_nodes:
```

只有 review 后才能创建 formal claim/pattern/decision。

## 项目融合建议

进入 `IMPLEMENTATION_BLUEPRINT.md` 的 feedback v0.2。

它比 daily brief 更适合作为 claim/pattern/decision 的候选生成器。

## 可拓展性

- 可以通过什么接口/适配层接入：review workflow、feedback adapter。
- 未来可能被什么替代：monthly strategy review、project-specific review。
- 替换或升级成本：低。
- 回退方式：人工复盘。

## 验证指标

- 是否能产生候选 claim/pattern/decision。
- 是否能发现 contradictions。
- 是否能记录 gaps 和 missing perspectives。
- one action 是否有来源和风险边界。
