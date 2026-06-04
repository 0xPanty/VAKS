# Chinese Forbidden Wording Lint

Status: sandbox lint convention for Chinese operator-facing renderer text. No
main-vault writeback, no `SCHEMA.md` change, and no operation-convention
promotion.

## Scope

This lint applies to normal Chinese operator-facing wording:

- Chinese reviewer/operator cards
- future Chinese review surface copy
- default renderer wording shown to Codex / Pro / reviewer agents

Adversarial packets may intentionally quote banned wording only when the text
is explicitly labeled as a trap. Those examples must not be treated as accepted
renderer wording.

## Banned Wording

The following wording must fail forbidden-wording lint:

```text
已验证
已证实
已确认正确
可信度 87%
truth_confidence +0.17
scope-fit 0.72
风险 0.18
5 个来源支持，因此更可靠
多个 URL，因此独立性更强
lineage 完整，因此独立
重复出现 7 次，因此支持更强
dashboard 绿色，因此成立
测试通过，因此正确
lint 通过，因此安全
feedback 提高了 truth confidence
可直接行动
无锚点但大意一致
grouped summary 证明该关系已被接受
high confidence
enough confidence
safe to proceed
ready for action
verified enough
可直接采用
可直接上线
足够可靠
多源交叉证实
reviewer approved so OK
green enough
looked aligned
summary matches source so fine
```

The machine-readable rules live in:

```text
forbidden_wording_zh.json
```

They include exact phrases and regex patterns for numeric confidence, source
count, URL count, lineage, recurrence count, dashboard/test/lint, feedback,
grouped-summary authority leakage, high/enough confidence as readiness, direct
adoption wording, multi-source cross-verification wording, reviewer approval as
OK, and summary/source alignment as safety.

## Safe Replacements

Use these instead:

```text
当前状态：普通记录 / 需要复核 / 阻塞 / 已解决折叠 / 已回归
锚点异常，暂不能回源，必须复核
已记录来源 / 记录 / 证据入口；独立性需另证
同类重复 N 次，仅表示归并与路由
dashboard / tests / lint 仅作诊断
feedback 只影响适用性或复核队列，不改变 truth
如需行动依据，请打开 full audit
```

## Why This Matters

Status, grouping, diagnostics, and feedback serve triage, not truth.

- Sentry issue status is triage state, not proof strength.
- GitHub resolved / unresolved is review workflow state, not code truth.
- ClaimReview metadata describes claim review compactly; it does not turn
  review metadata into the claim's truth proof.

The same rule applies to VAKS: shell/card/grouping/lint/feedback/dashboard/test
surfaces must not be written as conclusion strength or readiness.

## Latest Lint Result

The generated 24-case Chinese operator packet was checked with these rules:

```text
review_packet_risk_tiered_24/forbidden_wording_lint_zh.json
```

Latest status:

```text
pass
findings: 0
```
