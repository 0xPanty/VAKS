---
type: review-synthesis
status: candidate-updated
created: 2026-06-04
updated: 2026-06-04
project: verified-action-knowledge-system
subject: audit-shell-v1-pro-review-integration
sources:
  - "outputs/review/2026-06-04-audit-shell-v1-candidate-operation-convention.md"
  - "outputs/review/2026-06-04-audit-shell-v1-pro-review-brief.md"
  - "C:\\Users\\Administrator\\Documents\\VAKS_audit_shell_queue_cockpit_prototype_2026-06-04\\README.md"
  - "C:\\Users\\Administrator\\Documents\\VAKS_audit_shell_queue_cockpit_prototype_2026-06-04\\QUEUE_FIRST_COCKPIT_PROTOTYPE.md"
  - "C:\\Users\\Administrator\\Documents\\VAKS_audit_shell_queue_cockpit_prototype_2026-06-04\\PRO_REVIEW_INTEGRATION.md"
evidence_level: pro-review-synthesis
verification_status: candidate-updated
confidence: medium-high
---

# Audit Shell v1 Pro Review Integration: Queue-First Cockpit

## 大白话结论

Pro 没有否定 audit shell v1。

Pro 的核心意见是：

```text
不要把它继续做成一堆 audit card。
要把它升级成后台 queue-first operator cockpit。
```

也就是说：

```text
底层 shell_core 保留。
前脸展示收缩。
主交互单位从 card 改成 queue。
deep audit 只在行动、冲突、质疑、缺锚点、回归时打开。
```

## 当前状态

这仍然是候选，不是正式 adoption：

```text
operator-only sandbox candidate convention
queue-first prototype ready
not schema change
not truth-layer change
not user-facing UI
not formal main-vault rule
```

## Pro 明确支持保留

- `ordinary`
- `for_review`
- `blocking`
- `resolved_folded`
- `regressed`
- landing class discipline
- source / record / evidence / transcript / handoff jump-back
- video / ASR / transcript / metadata split
- feedback 不改 truth
- dashboard / test / lint / count / lineage 不当 authority
- recurrence / grouping 默认关闭

## Pro 要求改变

### 1. Card 不做主单位

card 只能是 renderer / pane。

主单位应该是：

```text
unresolved-first queue
issue shell row
deep packet
```

### 2. Landing class 前脸收缩

完整 landing taxonomy 保留在机器层。

人类前脸改成四档 anchor-strength strip：

```text
1. 精确证据落点
2. 精确文本落点但尚未审证
3. 仅 source / claim / context 落点
4. 仅 diagnostic / history / binary / weak 落点
```

### 3. `for_review` 拆 lane

不要把所有 `for_review` 都挤进主 unresolved 队列。

拆成：

```text
review_now
deferred_review_unless_promoted
```

只有被引用、晋级、挑战、用于行动或涉及冲突时，deferred 才升级。

### 4. Pointer 要往 selector-grade 走

只有 URL / path / file 不够。

下一步 click-back 要测：

```text
exact quote
position/range
timestamp segment
code/data position
dead-end
wrong semantic landing
```

## 已落地的 sandbox prototype

路径：

```text
C:\Users\Administrator\Documents\VAKS_audit_shell_queue_cockpit_prototype_2026-06-04
```

关键文件：

- `QUEUE_FIRST_COCKPIT_PROTOTYPE.md`
- `COCKPIT_QUEUE_ROWS.csv`
- `QUEUE_COCKPIT_SUMMARY.json`
- `OPERATOR_TRIAGE_PILOT_SAMPLE_80.csv`
- `OPERATOR_TRIAGE_PILOT_PROTOCOL.md`
- `SEMANTIC_CLICKBACK_PILOT_SAMPLE_60.csv`
- `SEMANTIC_CLICKBACK_PROTOCOL.md`
- `SOURCE_FAMILY_INDEPENDENCE_TRAP_SAMPLE.csv`
- `SOURCE_FAMILY_INDEPENDENCE_TRAP_PROTOCOL.md`
- `PRO_REVIEW_INTEGRATION.md`

## Prototype 结果

基于 282 条强压样本重新映射：

```text
blocking_now: 11
regressed_reopen: 2
review_now: 30
deferred_review_unless_promoted: 109
ordinary_light: 113
folded_history: 17
```

这把第一屏主 unresolved 队列从原来的 152 条厚路径，收缩成：

```text
11 + 2 + 30 = 43 条
```

这就是 Pro 要的方向：

```text
能力不砍，但前脸减负。
```

## 下一步

不要继续盲目扩大自动化扫描。

下一步跑三个小而关键的 operator-only pilot：

1. `80` 条 operator triage 双评。
2. `60` 条 semantic click-back。
3. `60` 条 source-family / independence trap。

通过后再考虑 paired benchmark：

```text
SciFact
AVeriTeC
AmbiFC
FEVER
本地主库案例
```

## 当前建议

```text
继续推进。
保持候选状态。
保留完整 shell_core。
改为 queue-first cockpit。
先跑 operator pilot，不要正式 adoption。
```

