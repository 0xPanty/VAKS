---
type: pro-review-brief
status: ready-for-pro
created: 2026-06-04
updated: 2026-06-04
project: verified-action-knowledge-system
subject: audit-shell-v1-candidate-operation-convention
review_target:
  - "outputs/review/2026-06-04-audit-shell-v1-candidate-operation-convention.md"
  - "C:\\Users\\Administrator\\Documents\\VAKS_audit_shell_pressure_test_2026-06-04\\PRESSURE_TEST_REPORT.md"
  - "C:\\Users\\Administrator\\Documents\\VAKS_audit_shell_pressure_test_2026-06-04\\PRESSURE_TEST_RESULTS.csv"
  - "C:\\Users\\Administrator\\Documents\\VAKS_audit_shell_pressure_test_2026-06-04\\NON_REDUCTIVE_OPERATOR_SURFACE_DESIGN.md"
review_mode: adversarial-design-review
---

# Pro Review Brief: Audit Shell v1 Candidate Operation Convention

## 给 Pro 的任务

请复核 audit shell v1 是否可以继续作为 VAKS 的后台 operator convention 候选。

重点：不要先把方案砍小。请先判断完整 `shell_core` 在真实资料库流量里是否有保留价值，再指出应该怎么设计、哪里会误导、哪里会太重。

## 背景

这不是用户前台 card，不是 truth layer，不是 schema 改动。

它是 Codex / Pro / reviewer 的后台资料库管家 surface，用来把材料分流成：

```text
ordinary
for_review
blocking
resolved_folded
regressed
```

## 最新测试

强压 sandbox：

```text
C:\Users\Administrator\Documents\VAKS_audit_shell_pressure_test_2026-06-04
```

真实主库样本：

```text
282 files
ordinary: 113
for_review: 139
blocking: 11
regressed: 2
resolved_folded: 17
false-lite: 0
over-heavy: 0
direct full audit: 152
```

覆盖维度：

```text
raw/articles
raw/videos
raw/repos
raw/papers
wiki/claims
wiki/patterns
wiki/anti-patterns
wiki/concepts
wiki/decisions
wiki/summaries
wiki/projects
outputs/review
outputs/feedback
outputs/qa
00_handoff
templates
```

压力诱饵：

```text
ASR / video
flat transcript
segments
repo zip snapshot
package zip
old handoff
old package manifest
draft pattern
accepted claim
dashboard / test / lint
source count / lineage / repeated mention
feedback truth bait
template mistaken as record
derived QA / summary
review_due / stale next_review
```

## 请重点复核

1. 是否同意：当前结果已经支持“不要先降性能，保留完整 shell_core 做设计”。
2. 是否发现 false-lite 漏洞：哪些材料被错误轻放。
3. 是否发现 over-heavy 问题：哪些普通材料被过度加厚。
4. 视频/ASR 拆分是否正确：

```text
video source card = ordinary provenance
ASR/acquisition json = ordinary diagnostic metadata
segments.md = for_review
transcript.txt = blocking before evidence/action use
```

5. landing class 是否足够：

```text
source_record_landing
claim_landing
claim_relevant_context_landing
evidence_landing
transcript_segment_landing
transcript_landing
diagnostic_landing
handoff_landing
template_landing
binary_snapshot_landing
```

6. feedback / dashboard / test / lint / count / lineage 的非 authority 边界是否表达清楚。
7. 旧 handoff 和旧 package manifest 用 `resolved_folded` / `regressed` 是否合理。
8. 下一步应该做中文 operator front-face prototype，还是继续扩大压力测试。

## 请输出

请按这个格式给结论：

```text
Verdict:
- keep_full_shell_core / reduce_scope / continue_sandbox / reject

Main concerns:
- ...

False-lite cases:
- ...

Over-heavy cases:
- ...

Design requirements:
- ...

Next step:
- ...
```

## Pro 可直接复制的提示词

```text
你是 Pro reviewer。请复核 VAKS audit shell v1 candidate operation convention。

请先读：
1. C:\Users\Administrator\Documents\资料库\outputs\review\2026-06-04-audit-shell-v1-candidate-operation-convention.md
2. C:\Users\Administrator\Documents\VAKS_audit_shell_pressure_test_2026-06-04\PRESSURE_TEST_REPORT.md
3. C:\Users\Administrator\Documents\VAKS_audit_shell_pressure_test_2026-06-04\PRESSURE_TEST_SUMMARY.json
4. C:\Users\Administrator\Documents\VAKS_audit_shell_pressure_test_2026-06-04\PRESSURE_TEST_RESULTS.csv
5. C:\Users\Administrator\Documents\VAKS_audit_shell_pressure_test_2026-06-04\NON_REDUCTIVE_OPERATOR_SURFACE_DESIGN.md
6. C:\Users\Administrator\Documents\VAKS_audit_shell_pressure_test_2026-06-04\OPERATOR_FRONT_FACE_EXAMPLES.md

请不要先把方案砍小。请先判断完整 shell_core 是否应该保留，再指出哪里会误导、哪里会太重、哪里漏拦。

重点检查：
- false-lite
- over-heavy
- ASR / video boundary
- landing class
- feedback not truth
- dashboard/test/lint/count/lineage not authority
- old handoff/package stale handling
- whether this should proceed to operator front-face prototype

请输出：
Verdict:
- keep_full_shell_core / reduce_scope / continue_sandbox / reject

Main concerns:
False-lite cases:
Over-heavy cases:
Design requirements:
Next step:
```

