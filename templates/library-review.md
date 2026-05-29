---
type: library_review
status: draft
library_name:
repo_url:
source_url:
checked_commit:
commit_time:
source_status: active | legacy | deprecated | unknown
reviewed_at:
domain:
related_projects:
current_branch:
extracted_patterns:
fusion_decision: watch
confidence: medium
evidence_count:
cross_validated_with:
negative_evidence:
extension_potential:
relations: []
---

# 库分析：

## 它解决什么问题


## 核心设计


## Source / Code Anchors

记录看过的文件、函数、模板、配置或 artifact。不要只写 README 感想。

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
|  |  |  |  |

## 当前支线价值

当前支线：

```text

```

它对当前支线：

```text
supports / contradicts / refines / risk_of / derived_from / no-clear-value
```

具体价值：

-

风险：

-

## 全貌架构价值

必须过一遍，不因当前支线而跳过。

| Architecture Zone | Value / Finding | Adopt? |
|---|---|---|
| Karpathy spine |  |  |
| Dusk workbench |  |  |
| source ingest |  |  |
| review queue |  |  |
| schema / reviewed knowledge |  |  |
| memory / dev context |  |  |
| feedback |  |  |
| retrieval / cache |  |  |
| API / MCP / agent access |  |  |
| viewer / workbench |  |  |
| publishing |  |  |
| risk / anti-pattern |  |  |

## 值得提炼的模式


## 标签与量化

- domain:
- problem:
- pattern:
- maturity: experimental / emerging / proven
- complexity: low / medium / high
- problem_fit: 1-5
- reuse_value: 1-5
- implementation_cost: 1-5
- integration_fit: 1-5
- evidence_strength: 1-5
- reversibility: 1-5

## 交叉验证

- 相似设计来源：
- 用户历史项目里的相似问题/影子：
- 支持证据：
- 反例或失败边界：
- 最小验证方式：

## Knowledge Calibration / Point Collision

先把资料蒸馏成少量 candidate points，再和本地 reviewed knowledge 做双向校准。不要让整篇 repo / article 直接撞库。

| Candidate Point | Local Reviewed Knowledge | Calibration Output | Review Question |
|---|---|---|---|
|  |  | candidate_relation / contradiction_candidate / scope_mismatch / stale_assumption_candidate / missing_evidence / review_due |  |

边界：

- 相似不是支持。
- 冲突不是自动推翻。
- 重复出现不是自动真理。
- 校准输出是 review input，不是 reviewed relation。

## Support / Challenge Review

对值得吸收的 claim / pattern / decision，检查它在支持、反对、范围限制和风险下是否还站得住。

- What supports it:
- What challenges it:
- Challenge severity: fatal / major / minor / out_of_scope / unresolved
- Scope limits:
- Known risks:
- Review again when:
- Action readiness: ready / not_ready / risky / needs_review

边界：

- provenance 不是 support。
- 有引用不等于有证据。
- 支持变多不自动提高 confidence。

## 关系边 / 关联强度

```yaml
relations:
  - target: "[[node-name]]"
    type: supports | contradicts | refines | risk_of | derived_from
    relation_state: candidate | reviewed | rejected | stale
    strength: 1-5
    confidence: low | medium | high
    evidence:
      - "[[source-or-claim]]"
    rationale: "One sentence explaining why this edge exists."
    created:
    last_verified:
```

## 对当前项目的适配点


## 可拓展性

- 是否适合作为插件/适配层：
- 是否会绑定核心结构：
- 未来替换成本：
- 可迁移路径：

## 复杂度和风险


## 不可行点 / 避坑

- 可能失败的条件：
- 已知反例：
- 相似踩坑：
- 应该避开的实现方式：
- 更稳的替代方案：

## 融合判断

- 结论：adopt / adapt / watch / reject
- 理由：
- 验证方式：

## 直接判断

- Direct use:
- Fork:
- Design-only:
- Reject:
- Current branch value:
- Whole architecture value:
- Risk:
- Next action:

## 后续行动
