# Chinese Reviewer-Card Patch Spec

Status: next alpha patch candidate. View-layer only. No truth-core change.

## Purpose

The reviewer-card is the Chinese front face of audit shell v1.

It answers:

- 这条记录现在是什么状态？
- 为什么轻量显示或为什么必须加厚？
- 有没有证据锚点问题？
- 能不能作为行动依据？
- 是否需要复核？
- 能否跳回 source / record / evidence？

It does not answer:

- 这条结论是不是真的？
- source count 是否代表独立性？
- grouping count 是否代表支持强度？
- feedback 是否提高 truth confidence？

## Required Shape

Use Chinese reviewer-facing wording. Do not expose raw machine labels as the main text.

Recommended front card:

```text
状态：普通 / 需复核 / 阻塞 / 已解决 / 回归
一句话摘要：...
风险原因：...
锚点状态：可回源 / 缺失 / 过期 / 漂移 / 版本不明
处理建议：轻量保存 / 打开 full audit / 补锚点 / 暂不可行动
边界提醒：feedback 不改 truth；grouping 不代表支持强度；dashboard 不是事实证据
```

## Mapping

| internal signal | Chinese reviewer wording |
| --- | --- |
| `ordinary` | 普通记录 |
| `for_review` | 需要复核 |
| `blocking` | 阻塞，暂不可作为行动依据 |
| `regressed` | 已回归，需要重新复核 |
| `resolved_folded` | 已解决，默认折叠，可回看 |
| `missing_anchor` | 锚点缺失，不能回源，必须复核 |
| `stale_pointer` | 锚点可能过期，需要复核来源版本 |
| `selector_drift` | 锚点漂移，当前定位可能不准 |
| `action_basis` | 涉及行动依据，必须打开 full audit |
| `explicit_challenge` | 有明确挑战，必须复核 |
| `conflict` | 存在冲突，必须复核 |
| `known_omission` | 有已知遗漏，不能直接行动 |
| `review_due` | 需要复核 |
| `unresolved_gate` | 进入未解决队列 |
| `dashboard_as_truth` | dashboard 只是诊断，不是事实证据 |
| `test_as_truth` | 测试通过只是诊断，不是事实证据 |
| `lineage_as_independence` | lineage 说明来路，不证明独立性 |
| `group_count_as_support` | group/count 只代表重复路由，不代表支持强度 |
| `feedback_truth_change` | feedback 只影响激活/适用性，不改变 truth |

## Pointer Display

Do not show one long `pointer_triad` line to reviewers.

Use:

```text
来源：raw_sources/...
记录：records/...
证据：evidence/...
原文片段：...
```

For broken anchors:

```text
锚点状态：缺失，不能直接回源
影响：不能作为行动依据
建议：补锚点或重新定位来源
```

## Recurrence Display

Do not let recurrence folding replace the member's own summary.

Bad:

```text
folded member exemplar=SCIFACT-141 count=10
```

Better:

```text
摘要：这条记录自己的真实摘要
重复路由：属于 recurrence group，count=10
边界：count 只用于降噪，不代表支持强度
```

Rules:

- recurrence remains side-arm only.
- show member's own summary.
- show group count only with a no-support-strength boundary.
- break fold on serious, regression, conflict, challenge, anchor problem, known omission, review_due, or action-basis.

## Authority Boundary Display

Bad:

```text
authority_boundary: dashboard_as_truth is diagnostic only
```

Better:

```text
边界提醒：dashboard 只是诊断信息，不能当事实证据。
```

## Feedback Display

Use categorical wording only:

```text
反馈：适用性问题 / 激活有用 / 范围不合 / 重复反馈
影响：只影响激活、适用性或复核队列，不改变 truth
```

Never:

```text
truth_confidence +0.17
feedback confidence 83%
```

## Test Plan

After this patch exists, run only a limited usability preflight:

- 8-12 Chinese reviewer cards.
- no A/B engineering fixture unless hidden and simplified.
- ask reviewer only:
  - 是否看懂状态？
  - 是否看懂为什么复核？
  - 是否能判断要不要打开 full audit？
  - 是否能看出锚点是否可回源？
  - 是否有 count/source/feedback 被误读成 truth 的风险？

Do not call this human timing or independent human oracle.
