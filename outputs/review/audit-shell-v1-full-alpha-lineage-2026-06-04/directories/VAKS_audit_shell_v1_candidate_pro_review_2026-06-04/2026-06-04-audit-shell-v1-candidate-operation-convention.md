---
type: review-candidate
status: pending-pro-review
created: 2026-06-04
updated: 2026-06-04
project: verified-action-knowledge-system
proposed_node_type: operation-convention-candidate
proposed_title: "Audit Shell v1 后台 operator 分流约定"
proposed_by: Codex
sources:
  - "C:\\Users\\Administrator\\Documents\\VAKS_audit_shell_pressure_test_2026-06-04\\PRESSURE_TEST_REPORT.md"
  - "C:\\Users\\Administrator\\Documents\\VAKS_audit_shell_pressure_test_2026-06-04\\PRESSURE_TEST_RESULTS.csv"
  - "C:\\Users\\Administrator\\Documents\\VAKS_audit_shell_pressure_test_2026-06-04\\PRESSURE_TEST_SUMMARY.json"
  - "C:\\Users\\Administrator\\Documents\\VAKS_audit_shell_pressure_test_2026-06-04\\NON_REDUCTIVE_OPERATOR_SURFACE_DESIGN.md"
  - "C:\\Users\\Administrator\\Documents\\VAKS_audit_shell_pressure_test_2026-06-04\\OPERATOR_FRONT_FACE_EXAMPLES.md"
evidence_level: sandbox-pressure-test
verification_status: candidate-tested
confidence: medium-high
reviewer: Pro
review_result:
---

# Audit Shell v1 后台 Operator 分流约定候选

## 先说边界

这不是正式主库规则，不改 `SCHEMA.md`，不改 truth layer，不打开 recurrence / grouping 默认。

这是一条候选 operation convention：给 Codex / Pro / reviewer 当后台资料库管家 surface 用，不是给普通用户看的 card。

## 一句话

Audit shell v1 的价值是让后台 operator 在真实资料流量里先分清：

```text
轻量收
需要复核
必须挡住
旧的折叠
过期/回归的重开
```

它不是为了证明资料是真的，而是为了防止 Codex 把 source、ASR、summary、feedback、dashboard、test、lint、count、old handoff 混成可靠知识。

## 候选规则

### 状态机

保留完整 `shell_core`：

```text
ordinary
for_review
blocking
resolved_folded
regressed
```

含义：

| State | 人话 | 操作 |
|---|---|---|
| `ordinary` | 普通资料 | 轻量处理；变成行动依据时再打开 full audit。 |
| `for_review` | 需要复核 | 进 unresolved/review；复核前不当行动依据。 |
| `blocking` | 暂不可行动 | 先修锚点、证据、冲突或 action-basis 问题。 |
| `resolved_folded` | 历史/已处理 | 默认折叠；只有被重新使用时打开。 |
| `regressed` | 回归/旧入口误导 | 重新入队，先核对最新入口。 |

### 前脸 slots

每条 operator 前脸必须覆盖：

```text
状态
一句话摘要
风险原因
锚点状态
处理建议
定向边界提醒
回源入口
```

注意：不要求每条都写成长 card。ordinary 要短，风险提醒只在命中风险时显示。

## 必须挡住或复核的触发器

这些不能轻放：

- 用作行动依据。
- 用作主库规则、schema、operation convention 依据。
- 缺 source URL / source URI / source anchor。
- flat transcript 被拿来当证据。
- repo/package zip 被拿来当 evidence landing。
- `next_review` 已过期且要当当前规则。
- draft / candidate pattern 要被当 adopted rule。
- feedback 被当 truth change。
- dashboard / test / lint / count / lineage 被当 authority。
- 旧 handoff 或旧 package manifest 被当当前入口。
- derived QA / summary 被当 reviewed truth。

## 必须保持轻量的东西

这些不要乱加厚：

- 普通 source card。
- video source card，前提是不直接当证据。
- ASR / acquisition metadata JSON。
- template。
- concept explanation。
- current handoff pointer，前提是不改路线。
- completed review output，前提只是历史查看。

轻量不是相信，轻量只是“不需要现在打开 full audit”。

## 视频 / ASR 规则

强压测试支持这个拆分：

```text
video source card = ordinary provenance
ASR/acquisition json = ordinary diagnostic metadata
segments.md = for_review
transcript.txt = blocking before evidence/action use
```

这条不能砍。视频链路最容易把 source、ASR、summary、candidate、reviewed knowledge 混掉。

## Landing class

候选 operator landing class：

| Landing | 说明 |
|---|---|
| `source_record_landing` | 只落到来源记录，能追溯，不等于证据支持。 |
| `claim_landing` | 落到 claim 文本，不是 evidence landing。 |
| `claim_relevant_context_landing` | 相关上下文，比 claim landing 还弱。 |
| `evidence_landing` | 落到具体证据位置。 |
| `transcript_segment_landing` | 落到时间段 ASR 文本，需要 key entity check。 |
| `transcript_landing` | flat transcript，不能直接行动。 |
| `diagnostic_landing` | 元数据、lint、test、dashboard、manifest，只能辅助。 |
| `handoff_landing` | 恢复入口，不是 schema 或 truth。 |
| `template_landing` | 模板，不是 record facts。 |
| `binary_snapshot_landing` | 有文件，但没有可读证据落点。 |

## 强压结果

本轮 sandbox 强压测试扫了 282 个真实主库文件。

结果：

```text
ordinary: 113
for_review: 139
blocking: 11
regressed: 2
resolved_folded: 17
false-lite: 0
over-heavy: 0
direct full audit: 152
```

说人话：

```text
该轻的能轻。
该挡的能挡。
该复核的没直接放行。
```

## 为什么值得进入候选

它明显帮 Codex 减少三类错误：

1. 把“有文件/有摘要/有 transcript”误当“能当证据”。
2. 把 feedback / dashboard / test / lint / count / lineage 误当 authority。
3. 被旧 handoff / 旧 package manifest 带错恢复入口。

## 反例和不确定性

还没有完成：

- 真人或第二 operator timing。
- Pro/reviewer 独立误解率测试。
- 真实 click-back 成功/失败记录。
- 前脸 UI/文本长度验证。
- `for_review` 大量出现时的队列可用性设计。

所以它不应直接正式 adoption。

## Pro 复核问题

请 Pro 不要先把方案砍小，而是先检查：

1. 这套完整 `shell_core` 是否应该保留。
2. 有没有严重 false-lite 没被强压测试发现。
3. 有没有普通入库会被系统性拖慢。
4. landing class 是否足够防止 claim/context/source/transcript 被误当 evidence。
5. 视频 / ASR 拆分是否正确。
6. feedback、dashboard、test、lint、count、lineage 的非 authority 边界是否足够清楚。
7. 旧 handoff / 旧 package 的 `resolved_folded` / `regressed` 处理是否合理。
8. 下一步应该做 operator front-face prototype，还是还需要继续扩大测试。

## 当前建议

```text
保留完整 shell_core。
不要先降性能。
不要正式 adoption。
先让 Pro 复核候选约定和强压报告。
```

