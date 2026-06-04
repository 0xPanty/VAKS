---
type: integration-validation
status: passed-candidate-framework-run
created: 2026-06-04
project: verified-action-knowledge-system
subject: audit-shell-v1-main-framework-integration-validation
scope: operator-only-candidate-convention
verification_status: main-framework-consistency-pass
evidence_level: local-main-vault-artifact-check
confidence: high-for-candidate-merge
---

# Audit Shell v1 主框架集成验证

## 大白话结论

拿完整主框架跑了一遍，结果是：

```text
输出和测试结果一致。
没有发现和主框架硬冲突。
这是强正向、高价值改动。
可以保留在主库作为 operator-only candidate convention。
```

但它仍然不是：

```text
formal adoption
schema guidance
truth-layer guidance
user-facing UI
operator-usability validated
product-grade click-back validated
```

## 这次怎么跑的

这次验证不是重新设计，而是用主库当前入口做集成检查：

```text
AGENTS / REVIEW_QUEUE / SOURCE_INTAKE / FEEDBACK / MEMORY_TIER
-> candidate convention
-> full alpha lineage
-> pressure test / queue cockpit summary
-> handoff / index recovery path
```

检查目标：

```text
测试数字有没有变
主库入口能不能找到完整 alpha
是否和 schema / truth layer / feedback / source intake 边界冲突
是否有旧 Pro / not_go_yet 口径残留误导
```

## 结果一致性

Full ingest simulation：

```text
sample_count: 46
ordinary: 24
for_review: 16
blocking: 2
resolved_folded: 3
regressed: 1
```

Pressure test：

```text
sample_count: 282
ordinary: 113
for_review: 139
blocking: 11
regressed: 2
resolved_folded: 17
false_lite: 0
over_heavy: 0
immediate_full_audit: 152
```

Queue-first cockpit：

```text
queue_rows: 282
blocking_now: 11
regressed_reopen: 2
review_now: 30
deferred_review_unless_promoted: 109
ordinary_light: 113
folded_history: 17
first_screen_unresolved: 43
operator / clickback / independence pilot rows: 80 / 60 / 60
```

说人话：

```text
原来 152 条会直接厚审计的东西，
现在第一屏 unresolved 只剩 43 条。

这不是把风险藏起来，
而是把“不立刻打扰但一用就晋级”的 deferred lane 写成硬规则。
```

## 主库资产完整性

完整 alpha lineage 已进入主库：

```text
outputs/review/audit-shell-v1-full-alpha-lineage-2026-06-04/
```

Manifest 结果：

```text
directory: 15
zip: 20
current_record: 7
total_files: 5092
total_bytes: about 87.9 MB
```

关键目录副本和外部原目录一致：

```text
VAKS_full_ingest_sim_2026-06-04: parity true
VAKS_audit_shell_pressure_test_2026-06-04: parity true
VAKS_audit_shell_queue_cockpit_prototype_2026-06-04: parity true
VAKS_queue_cockpit_CLOSEOUT_2026-06-04: parity true
```

## 主框架冲突检查

没有改：

```text
SCHEMA.md
README.md
FUSION_ARCHITECTURE_V0_2_DRAFT.md
SOURCE_INTAKE.md
FEEDBACK.md
MEMORY_TIER.md
```

实际挂入口只改了：

```text
REVIEW_QUEUE.md
00_handoff/2026-05-31-route-lock-confirmation-handoff.md
wiki/indexes/knowledge-graph-index.md
outputs/review/2026-06-04-audit-shell-v1-candidate-operation-convention.md
outputs/review/2026-06-04-audit-shell-v1-final-version-review.md
outputs/review/2026-06-04-audit-shell-v1-queue-cockpit-closeout.md
```

主框架边界是匹配的：

```text
SOURCE_INTAKE: video / ASR 是 source format，不是 truth format。
REVIEW_QUEUE: background / same-origin / summary / count 不能当独立 support。
FEEDBACK: feedback 不直接改 truth。
MEMORY_TIER: activation tier 不是 truth tier。
AGENTS: dashboard / retrieval / metadata / brief / feedback 不是 reviewed knowledge。
```

## 已发现并修掉的冲突

发现两个恢复口径冲突：

1. 候选正文末尾还保留“请 Pro 复核”的旧状态。
2. 旧 handoff 里还保留 6 月 1 日阶段的 main-doc writeback hold。

已修：

```text
候选正文改成 Final Pro Gate：无合入阻塞。
handoff 标明 6 月 1 日 hold 已被 6 月 4 日最终候选合入 supersede。
```

复扫结果：

```text
没有 pending-pro-review 残留。
没有 No major issue found 这种容易被误读成正式批准的宽口径。
没有当前口径要求继续找 Pro 做设计复核。
```

## 价值判断

这是强正向、高价值改动。

原因很简单：

1. 普通资料没有被拖成重审计。
2. 高风险资料没有被轻放。
3. 视频 / ASR / transcript / binary / summary 的边界被守住。
4. feedback / dashboard / test / lint / count / lineage 没有被当 truth authority。
5. 旧 handoff / package manifest 的 stale 风险有处理路径。
6. queue-first 把 operator 第一屏压力从 152 条降到 43 条。
7. 完整 alpha lineage 已入主库，后续窗口可以恢复，不靠聊天记忆。

## 剩余风险

剩余风险不是“能不能合入候选”，而是 formal adoption 前必须跑：

```text
80-row operator triage
60-row selector-grade semantic click-back
60-row source-family independence trap
```

尤其要继续验证：

```text
deferred lane 会不会实际 false-lite
exact evidence anchor click-back 是否够稳
source family / repeated mention 会不会被误当独立支持
真人 operator 是否真的更快、更准
```

## 最终判断

```text
main-framework integration: pass
result parity with tests: pass
hard conflict with framework: none after wording fix
value: strongly positive
recommendation: keep in main vault as operator-only candidate convention
next step: run 80/60/60 pilot
```
