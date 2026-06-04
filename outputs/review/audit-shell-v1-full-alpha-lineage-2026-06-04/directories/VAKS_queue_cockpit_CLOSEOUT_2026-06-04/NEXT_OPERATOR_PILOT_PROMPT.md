# Next Operator Pilot Prompt

```text
请继续 VAKS audit shell v1 的下一阶段：queue-first operator cockpit pilot。

不要重新做架构复核。
不要继续泛泛让 Pro 评审方向。
不要把它写成正式主库规则。
不要改 SCHEMA.md。
不要打开 recurrence / grouping 默认。

当前路线已经收尾为：

operator-only sandbox candidate convention
queue-first risk-tiered operator cockpit

源目录：

C:\Users\Administrator\Documents\VAKS_audit_shell_queue_cockpit_prototype_2026-06-04

先读：

1. README.md
2. QUEUE_FIRST_COCKPIT_PROTOTYPE.md
3. QUEUE_COCKPIT_SUMMARY.json
4. OPERATOR_TRIAGE_PILOT_PROTOCOL.md
5. SEMANTIC_CLICKBACK_PROTOCOL.md
6. SOURCE_FAMILY_INDEPENDENCE_TRAP_PROTOCOL.md
7. PRO_REVIEW_INTEGRATION.md

要执行三个 pilot：

1. Operator triage pilot
   输入：OPERATOR_TRIAGE_PILOT_SAMPLE_80.csv
   目标：判断 operator 是否能更快、更稳地做对第一步动作。

2. Semantic click-back pilot
   输入：SEMANTIC_CLICKBACK_PILOT_SAMPLE_60.csv
   目标：判断 source / claim / context / transcript / diagnostic / handoff / binary landing 有没有语义点错。

3. Source-family independence trap
   输入：SOURCE_FAMILY_INDEPENDENCE_TRAP_SAMPLE.csv
   目标：判断 count / lineage / repeated mention / derived summary 有没有被误当独立支持。

输出目录：

C:\Users\Administrator\Documents\VAKS_queue_cockpit_OPERATOR_PILOT_YYYY-MM-DD

至少产出：

- OPERATOR_TRIAGE_PILOT_REPORT.md
- OPERATOR_TRIAGE_PILOT_RESULTS.csv
- SEMANTIC_CLICKBACK_PILOT_REPORT.md
- SEMANTIC_CLICKBACK_PILOT_RESULTS.csv
- SOURCE_FAMILY_TRAP_REPORT.md
- SOURCE_FAMILY_TRAP_RESULTS.csv
- PILOT_SUMMARY.json
- NEXT_STEP_VERDICT.md

判断门槛：

- serious false-lite = 0
- high-risk wrong actionability = 0
- serious miss = 0
- severe authority misunderstanding = 0
- dead-end click = 0
- wrong semantic landing = 0 for weak/evidence distinction
- independence misread = 0

最终只给三种结论之一：

1. ready_for_candidate_operation_convention_writeback
2. continue_sandbox_with_specific_fixes
3. redesign_required

请说人话，不要堆术语。重点不是设计好不好听，而是 operator 能不能更快、更稳地做对动作。
```

