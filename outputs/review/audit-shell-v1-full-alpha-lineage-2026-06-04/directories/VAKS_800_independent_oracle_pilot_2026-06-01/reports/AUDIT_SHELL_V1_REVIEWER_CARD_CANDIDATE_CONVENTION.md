# Audit Shell V1 Reviewer-Card Candidate Convention

Status: sandbox candidate convention. No main-vault writeback, no `SCHEMA.md` change, no operation-convention promotion.

## Executive Verdict

Pro's latest convergence verdict supports the current line, with one more narrowing:

```text
default core = shell_core + Chinese reviewer-card rendering
recurrence / grouping = conditional side arm
authority lint + categorical feedback strip = background guardrails
```

This means the next useful alpha is not more automatic fixture expansion. The next useful alpha is human-facing clarity:

```text
Chinese reviewer-facing shell card
```

It is not a new truth layer, not a schema change, and not a separate architecture. It is the Chinese front face of audit shell v1.

## Role Split

| component | role | candidate decision |
| --- | --- | --- |
| hard-trigger shell | default core | keep |
| required unresolved gate | default core | keep |
| anchor health strip | default core | keep |
| sparse provenance / pointer triad | default core drill-down | keep, but humanize front face |
| resolved folding / unresolved-first surface | default core | keep |
| Chinese reviewer-facing shell card | required view-layer alpha | add next |
| versioned fingerprint grouping | conditional side arm | keep out of default core |
| representative / delta recurrence digest | conditional side arm | keep out of default core |
| authority lint | background guardrail | keep, not default card content |
| categorical feedback strip | wording discipline / guardrail | keep, not value engine |

## What The Reviewer-Card Does

The reviewer-card helps a human quickly answer:

- 这条记录现在是什么状态？
- 为什么轻量显示，或为什么必须加厚？
- 有没有锚点问题？
- 是否需要复核？
- 能否跳回 source / record / evidence？
- 能不能作为行动依据？
- 有没有容易被误读成 truth authority 的东西？

It does not decide truth.

It does not prove independence.

It does not turn grouping, feedback, dashboard, tests, or source count into evidence support.

## Default Core Shape

`shell_core` remains the only default-core candidate:

- ordinary records stay light.
- hard triggers become thick.
- unresolved / review_due / blocking / regressed items stay visible.
- resolved items fold by default.
- anchor health is visible.
- sparse source / record / evidence pointers are preserved.

Chinese reviewer-card rendering becomes part of the default core's view expression:

```text
状态：普通 / 需复核 / 阻塞 / 已解决 / 回归
一句话摘要：...
风险原因：...
锚点状态：可回源 / 缺失 / 过期 / 漂移 / 版本不明
处理建议：轻量保存 / 打开 full audit / 补锚点 / 暂不可行动
边界提醒：必要时显示，且不得冒充 truth authority
```

## Trigger Wording

Do not expose raw machine labels as the primary reviewer text.

| internal signal | reviewer-facing wording |
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

## Pointer Display

The machine pointer may remain in the full artifact, but the reviewer-card should not show a single long `pointer_triad` line.

Preferred display:

```text
来源：raw_sources/...
记录：records/...
证据：evidence/...
原文片段：...
```

For broken anchors:

```text
锚点状态：缺失，不能直接回源
影响：暂不能作为行动依据
建议：补锚点或重新定位来源
```

## Recurrence Side Arm

Recurrence / grouping remains conditional. It is not part of the default core.

Allowed only when all are true:

- ordinary
- open-only
- valid anchor
- action meaning stable
- no review_due
- no conflict / challenge / regression / action-basis / known omission / anchor problem

Break fold immediately when any serious condition appears.

Never let folded recurrence replace the member's own summary.

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

## Guardrails

Authority lint and categorical feedback strip remain useful, but they are background guardrails, not the default card's value story.

Use only when relevant:

```text
边界提醒：dashboard 只是诊断信息，不能当事实证据。
边界提醒：测试通过不是 truth proof。
边界提醒：lineage 说明来路，不证明独立性。
边界提醒：group/count 只代表重复路由，不代表支持强度。
反馈：只影响激活、适用性或复核队列，不改变 truth。
```

Never:

```text
truth_confidence +0.17
feedback confidence 83%
source count proves independence
group count proves support
dashboard green proves truth
test pass proves correctness
```

## Placement

This candidate convention should stay in the sandbox until limited human validation exists.

It may be summarized in a handoff as a candidate result, but it should not be promoted into:

- `SCHEMA.md`
- main operation convention
- truth core
- reviewed relation rules

If a main-vault note is later authorized, use candidate wording:

```text
Candidate convention, not adopted operation rule.
```

## Next Work

Recommended next step:

1. implement a Chinese reviewer-card renderer/spec for `shell_core`.
2. keep recurrence as a side-arm study only.
3. run an 8-12 case Chinese usability preflight.
4. only then decide whether to run human timing / dual-review / click-back.

Do not add broad automatic patches unless a specific failure appears.
