---
type: pilot-results
status: superseded-by-high-intensity-graduation
created: 2026-06-04
project: verified-action-knowledge-system
subject: audit-shell-v1-formal-graduation-pilot
scope: operator-only-operation-convention
verdict: continue_sandbox_with_specific_fixes
superseded_by:
  - "outputs/review/2026-06-04-audit-shell-v1-high-intensity-graduation-report.md"
  - "outputs/review/2026-06-04-audit-shell-v1-formal-graduation-verdict.md"
---

# Audit Shell v1 Formal Pilot Results

## Supersession Note

This initial 80/60/60 pilot passed its hard gates but held formal adoption for narrow evidence gaps.

Those gaps were later closed by:

```text
outputs/review/2026-06-04-audit-shell-v1-high-intensity-graduation-report.md
outputs/review/2026-06-04-audit-shell-v1-formal-graduation-verdict.md
```

Current status:

```text
ready_for_formal_operator_only_operation_convention
```

## 一句话结论

三组 pilot 的硬安全门槛全部通过：没有 false-lite、没有高风险轻放、没有漏掉 blocking/regressed、没有把 source/claim/context/diagnostic/history/binary landing 说成 evidence support，也没有把 count/lineage/repeated mention/derived summary 当独立支持。

但本轮不建议直接升级为 formal operation convention。原因不是架构失败，而是 formal graduation 还差两个最小证据：双 operator 或双 pass 计时可用性，以及包含 `1_precise_evidence_anchor` / `evidence_landing` 的 selector-grade evidence click-back 样本。

## 执行边界

- 执行身份：single Codex operator。
- 输入：只使用 prototype 里的 80 / 60 / 60 三个 CSV。
- 本轮未改 `SCHEMA.md`、truth layer、handoff、AGENTS 或 video intake 文件。
- 本轮没有真人第二 operator，因此 `time_to_first_action_seconds` 记录为 `not_measured_single_codex_operator`。
- click-back 样本没有 `1_precise_evidence_anchor` 行，因此不能声称 product-grade evidence click-back 已验证。

## Pilot 1: 80-row Operator Triage

| 指标 | 结果 |
|---|---:|
| rows | 80 |
| wrong_actionability | 0 |
| wrong_actionability_on_high_risk | 0 |
| serious_miss | 0 |
| severe_authority_misunderstanding | 0 |
| serious_false_lite | 0 |
| deferred_used_as_action_basis_without_receipt | 0 |
| ordinary_rows_kept_light | 20 |

测出来的东西：queue-first row 能把第一动作稳定压到 `light_save / defer_review / review_now / block_and_fix_anchor / reopen_regressed / fold_history` 六类。20 条 ordinary 都保持轻量；21 条 deferred 没有进入 action-basis，且全部标记为“若引用、行动、规则依据、challenge、冲突或弱锚点影响回答，必须先 promotion receipt”。

没有测出来的东西：真实真人操作秒数。本轮能证明第一动作清楚、硬风险没漏，不能证明真人中位时间已经比 direct full audit 快 25-30%。

## Pilot 2: 60-row Semantic Click-Back

| 指标 | 结果 |
|---|---:|
| rows | 60 |
| path_exists | 60 |
| first_correct_click | 60 |
| wrong_semantic_landing | 0 |
| dead_end_click | 0 |
| claimed_evidence_support_without_selector_grade | 0 |
| precise_evidence_anchor_rows | 0 |

测出来的东西：60 个路径全部能点回真实文件；source record、claim/context、summary/QA、diagnostic、review output、handoff、template、transcript segment、flat transcript 都没有被错叫成 evidence support。4 条 transcript segment 只被判为 precise text / timestamp context，不当 reviewed evidence。

没有测出来的东西：product-grade evidence landing。因为样本里没有 `1_precise_evidence_anchor`，本轮只能证明“弱 landing 没有被夸大”，不能证明“精确证据锚点点击已稳定”。

## Pilot 3: 60-row Source-Family Independence Trap

| 指标 | 结果 |
|---|---:|
| rows | 60 |
| path_exists | 60 |
| independence_misread | 0 |
| action_basis_from_count_or_lineage | 0 |
| independent_support_yes | 0 |

测出来的东西：derived QA / summary、review output、source record、binary/package lineage、同族材料重复出现，都只被当成 route/context/provenance/diagnostic。没有一条被当成独立支持，也没有一条被拿去做 action-basis。

## Gate Table

| Gate | Result |
|---|---|
| serious false-lite = 0 | pass |
| high-risk wrong actionability = 0 | pass |
| serious miss = 0 | pass |
| severe authority misunderstanding = 0 | pass |
| dead-end click = 0 | pass |
| weak/source/claim/context/diagnostic/history/binary landing not called evidence | pass |
| independence misread = 0 | pass |
| action basis from count/lineage = 0 | pass |
| two-operator/timed usability | not measured |
| product-grade exact evidence click-back | not measured: no exact evidence-anchor rows |

## Operator 使用是否更顺

更顺，限于“第一屏分流”和“第一动作清楚”这个层面：80 行里没有动作歧义导致的轻放或漏挡；ordinary 没被拖进厚审计；deferred 没污染 action-basis；blocking/regressed/review_now 都进了需要处理的路径。

还不能说“真人使用已验证更快”：没有第二 operator，也没有 direct full audit 对照秒表。

## 升级判断

本轮建议：`continue_sandbox_with_specific_fixes`。

不要 redesign。不要重开架构复核。继续保留 main-vault operator-only candidate convention。最小差距只有两项：

1. 同一 80 行跑双 operator 或双 pass 计时，记录 queue-first row 相比 direct full audit 的 median first-action 时间。
2. 补一组 `1_precise_evidence_anchor` / `evidence_landing` 的 exact selector-grade 样本，重跑 semantic click-back。

## 输出文件

- `outputs/review/2026-06-04-audit-shell-v1-formal-pilot-results.csv`
- `outputs/review/2026-06-04-audit-shell-v1-formal-pilot-summary.json`
- `outputs/review/2026-06-04-audit-shell-v1-formal-adoption-recommendation.md`
