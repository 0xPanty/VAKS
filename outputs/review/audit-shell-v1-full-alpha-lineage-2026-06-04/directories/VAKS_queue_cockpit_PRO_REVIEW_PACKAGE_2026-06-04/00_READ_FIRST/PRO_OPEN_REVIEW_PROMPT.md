# Pro Open Review Prompt

```text
你是 Pro reviewer。请对 VAKS audit shell v1 的最新版方向做开放式复核和扩展调研。

注意：现在方案已经从“card-first audit shell”推进为：

queue-first risk-tiered operator cockpit

它仍然是：

- operator-only sandbox candidate convention
- 不是普通用户 UI
- 不是 truth layer
- 不是 schema 改动
- 不是 formal adoption

请先读：

1. 00_READ_FIRST/README_FOR_PRO.md
2. 01_CANDIDATE/2026-06-04-audit-shell-v1-pro-review-integration-queue-cockpit.md
3. 02_PROTOTYPE/QUEUE_FIRST_COCKPIT_PROTOTYPE.md
4. 02_PROTOTYPE/QUEUE_COCKPIT_SUMMARY.json
5. 02_PROTOTYPE/COCKPIT_QUEUE_ROWS.csv
6. 04_PILOTS/OPERATOR_TRIAGE_PILOT_PROTOCOL.md
7. 04_PILOTS/SEMANTIC_CLICKBACK_PROTOCOL.md
8. 04_PILOTS/SOURCE_FAMILY_INDEPENDENCE_TRAP_PROTOCOL.md
9. 03_PRESSURE_TEST/PRESSURE_TEST_REPORT.md
10. 01_CANDIDATE/2026-06-04-audit-shell-v1-candidate-operation-convention.md

背景：

上一轮强压测试扫了 282 个真实主库文件：

ordinary: 113
for_review: 139
blocking: 11
regressed: 2
resolved_folded: 17
false-lite: 0
over-heavy: 0
direct full audit: 152

根据你的上一轮开放式复核，当前路线已调整为 queue-first cockpit：

blocking_now: 11
regressed_reopen: 2
review_now: 30
deferred_review_unless_promoted: 109
ordinary_light: 113
folded_history: 17

第一屏主 unresolved queue 从 152 条厚路径收缩为 43 条：

blocking_now + regressed_reopen + review_now = 43

请你开放式评审，不要被当前设计限制住。你可以：

1. 判断 queue-first cockpit 是否比 card-first audit shell 更合理。
2. 判断完整 shell_core 是否应该继续保留。
3. 判断 deferred_review_unless_promoted 是否解决了 for_review 队列过重的问题，还是会引入新的漏审风险。
4. 检查是否仍有 false-lite、over-heavy、wrong actionability、authority misunderstanding 风险。
5. 检查 anchor-strength strip 是否足够，是否应替代前脸完整 landing taxonomy。
6. 检查 selector-grade pointer / semantic click-back 的测试协议是否足够。
7. 检查 source-family / independence trap 是否足够防止 count、lineage、repeated mention 被误当独立支持。
8. 对比成熟系统：Sentry、PagerDuty、Splunk、GRADE、assurance case、W3C Web Annotation / PROV、Cochrane、incident management、issue triage、人机协作 review workflow 等。
9. 如果你认为当前 cockpit lane 设计不好，请提出替代 lane。
10. 如果你认为 pilot 协议不够，请提出更好的小测试。
11. 如果你认为可以推进，请说明推进条件。
12. 如果你认为必须继续 sandbox 或重做设计，请明确说明原因。

请不要只是检查我列出的点。请尽量调研、发散、提出更好的可能性。

请明确区分：

- formal adoption
- main-vault candidate convention
- operator-only sandbox candidate
- queue-first prototype
- continue sandbox
- reject / redesign

建议输出结构：

1. Overall verdict
2. Whether queue-first cockpit is the right abstraction
3. What is genuinely improved vs card-first
4. Main risks and failure modes
5. Missing tests or evidence
6. Keep / change / remove list
7. Better design possibilities
8. Pilot protocol critique
9. Recommended next step
10. If you were designing this from scratch, what would you do differently?

请说人话，结论要清楚。不要为了保留方案放过风险，也不要为了安全把有价值能力先砍掉。
```

