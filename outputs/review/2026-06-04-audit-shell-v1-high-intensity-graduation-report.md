---
type: graduation-stress-report
status: completed
created: 2026-06-04
project: verified-action-knowledge-system
subject: audit-shell-v1-high-intensity-graduation-test
verdict: ready_for_formal_operator_only_operation_convention
---

# Audit Shell v1 High-Intensity Graduation Test

## 说人话结论

补测到位了。全量队列、盲派生、deferred 触发器、精确 evidence anchor、弱锚点负控、source-family 陷阱全部过硬门槛。没有发现 operator cockpit 的误判、漏判、点错、弱来源升格、count/lineage 当 support。

发现了一个真实但非阻塞的问题：旧 alpha evidence packet 里有 67 个锚点太弱或不可用，其中 32 个是 `evidence: No No` 这类短文本，35 个没有可用 substantive anchor。它们已被测试归入 `weak_evidence_anchor_quarantine`，不能算 selector-grade evidence landing，不能当 action-basis。

结论：可以从 `candidate convention` 升级为 `formal operator-only operation convention`。

注意这个“正式毕业”的范围很窄：后台 operator 操作约定。不是 schema guidance，不是 truth-layer guidance，不是 user-facing UI，也不是 recurrence/grouping 默认打开。

## 压力范围

- 全量 cockpit triage：282 行。
- 忽略 irst_action 文案的盲派生：282 行。
- deferred promotion trigger matrix：654 行。
- exact evidence anchor click-back：1453 行。
- weak evidence anchor quarantine：67 行。
- non-evidence negative controls：282 行。
- source-family adversarial matrix：480 行。
- prior 80/60/60 pilot replay：200 行。
- 总行级结果：3701 行。

## Gate Results

| Gate | Result |
|---|---|
| all 282 paths/actions | pass |
| blind no-first-action triage | pass |
| deferred promotion receipt matrix | pass |
| exact evidence-anchor click-back | pass |
| weak evidence-anchor quarantine | pass |
| weak/non-evidence negative controls | pass |
| source-family adversarial matrix | pass |
| prior 200-row pilot replay | pass |
| direct-full-audit burden proxy | pass |
| hard failures | 0 |

## Direct Full Audit Proxy

Direct full audit rows: 152. Queue-first unresolved first screen: 43. Row burden reduction: 71.71%.

Automation timing proxy over 7 reps: queue median 4.743 ms; direct file-read median 920.298 ms; ratio 194.05x.

这不是真人 UI 秒表，但它证明第一屏负担没有靠嘴硬：full audit 负担被实际压下去了。

## What Was Specifically Attacked

- `deferred_review_unless_promoted` 被逐一套入 cited/action/rule/challenge/conflict/weak-anchor 六类触发器，全部要求 promotion receipt，未允许 receipt 前 action-basis。
- 合格 evidence packet 被抽取精确行号锚点，全部按 exact selector-grade evidence landing 验证。
- 弱 evidence packet 被隔离为 quarantine，不允许 claim evidence support。
- 282 个非 evidence landing 被当作 evidence-bait 负控，全部没有被升格为 evidence support。
- 60 个 source-family trap 行扩成 480 个 adversarial bait，全部没有把 count、lineage、重复提及、derived summary、review output 当独立支持。

## Graduation Verdict

```text
ready_for_formal_operator_only_operation_convention
```

## Output Files

- `outputs/review/2026-06-04-audit-shell-v1-high-intensity-graduation-results.csv`
- `outputs/review/2026-06-04-audit-shell-v1-high-intensity-graduation-summary.json`
- `outputs/review/2026-06-04-audit-shell-v1-formal-graduation-verdict.md`
