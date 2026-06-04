# Risk-Tiered Reviewer UX Patch Spec

Status: sandbox patch spec. AI/reviewer-operator surface only. No truth-core change, no `SCHEMA.md` change, no operation-convention promotion.

## Purpose

This patch reframes the next step from "Chinese reviewer-card" to:

```text
risk-gated review surface
+ evidence envelope
+ source-first drilldown
```

The immediate implementation is still small: a Chinese AI/reviewer-operator
renderer for `shell_core`, plus a 12-24 case operator preflight and a mandatory
12-case adversarial add-on for anti-self-proof traps.

This is not an ordinary user workflow. The ordinary user should not have to read cards, fill sheets, or inspect review packets during normal vault use. The operator surface helps Codex / Pro / reviewer agents manage escalation consistently in the background. The user should only see short plain-language risk notices when a risk changes the answer or action.

## What This Solves

The patch is meant to answer:

- Can an AI/reviewer operator understand why a record stayed light or became thick?
- Can an AI/reviewer operator see whether the record is actionable, needs review, needs an anchor fix, or must open full audit?
- Can an AI/reviewer operator jump back to source / record / evidence without reading raw machine labels?
- Can the UI avoid implying that count, tests, dashboard, lineage, feedback, or shell output are truth authority?

It is not meant to prove:

- truth
- product readiness
- independent human oracle
- semantic safety
- recurrence maturity
- mainline readiness

## Product-Grade Shell V1 Minimum Shape

The proposed audit shell v1 is not a new card schema. It is a four-layer view
convention that keeps the existing schema untouched:

| layer | role | current action |
| --- | --- | --- |
| truth ledger | Preserve raw source, record, evidence, anchor, selector, lineage, and other reversible traces. | Do not change schema; keep jump-back, hash / quote / offset / state usable. |
| escalation controller | Decide when a record stays light, becomes thick, or enters unresolved. | Use hard triggers; do not mix dashboard, grouping, or feedback into escalation authority. |
| operator review surface | Help Codex / Pro / reviewer agents see why a record is light or thick and what to do next. | `shell_core` + Chinese AI/reviewer-operator rendering. |
| end-user answer surface | Show ordinary users short plain-language risk notices, not audit cards. | Expose one-sentence risk notices only when risk affects an answer or action. |

Card is only one renderer inside the operator surface. It is not the architecture, not a truth layer, and not the ordinary user interface.

## Core Layers Detail

### 1. Truth Ledger

Keeps raw and audit material reversible:

- raw source
- record
- evidence
- source anchor
- quote / selector
- lineage / version where available

This layer is for traceability, not display polish and not truth authority.

### 2. Escalation Controller

Determines what must become thick or unresolved.

Hard triggers:

- action-basis
- promotion
- explicit challenge
- conflict
- regression
- known omission
- missing evidence / insufficient evidence
- missing anchor
- stale pointer
- selector drift
- moved anchor
- action outcome / decision outcome
- reviewer block
- high-severity wrong answer
- independence needed for confidence
- review_due
- blocking state

Rules:

- ordinary valid records may stay light.
- resolved records may fold by default.
- regressed records must reopen.
- anchor trouble must be visible.
- action-basis records must open full audit.
- promotion candidates must open the review surface before being treated as reviewed knowledge.
- conflict / challenge / known omission must not be hidden.
- outcome-driven problems create review pressure, not truth mutation.
- reviewer blocks and high-severity wrong answers force unresolved handling until reviewed.
- when source independence is needed for confidence, source count / lineage / group count cannot substitute for independence review.

### 3. Operator Surface

The current minimum surface is a Chinese AI/reviewer-operator record card.

This surface is for the system caretaker, not for the ordinary vault user.
The ordinary user-facing output should usually collapse this into one sentence:

```text
这条不能作为行动依据，因为锚点缺失。
这个结论有冲突，我先放进复核队列。
这条普通资料我先轻量保存。
```

Longer term, this may become a cockpit:

```text
left: unresolved / regressed / anchor-broken / action-basis queue
center: risk strip + summary + actionability
right: source-first drilldown
```

For this patch, only the center-card renderer and drilldown handles are generated.

### 4. Side Surfaces

Recurrence, digest, and badges stay side surfaces:

- queue/list compression only.
- no member-summary overwrite.
- no count-as-support wording.
- serious / conflict / challenge / regression / anchor problem breaks out.

## Required Chinese Renderer Slots

The front face should stay compact, but the six-line idea is a budget
constraint, not a structural pass/fail metric. Fixed line-count metrics are too
easy for a renderer to self-satisfy. The invariant is the information slots,
not the literal number of lines.

Each operator-facing sample card must expose:

```text
状态：
一句话摘要：
风险原因：
锚点状态：
处理建议：
仅在必要时出现的边界提醒：
```

`边界提醒` should be targeted. Do not repeat a long global warning on every card. Use it only when a record contains sensitive surfaces such as count, lineage, dashboard, test, feedback, recurrence, or authority bait.

The drilldown may sit just behind the front face rather than inside the six-line
budget, but it must remain source-first and easy for the operator to open:

```text
来源：
记录：
证据：
原文片段：
```

## State Wording

| internal state | reviewer wording |
| --- | --- |
| `ordinary` | 普通记录 |
| `for_review` | 需要复核 |
| `blocking` | 阻塞，暂不可作为行动依据 |
| `regressed` | 已回归，重新进入队列 |
| `resolved_folded` | 已解决，默认折叠，可回看 |

## Anchor Wording

| anchor status | reviewer wording |
| --- | --- |
| `valid` | 可回源 |
| `missing` | 锚点缺失，不能直接回源 |
| `stale` | 锚点可能过期，需要复核来源版本 |
| `drift` | 锚点漂移，当前定位可能不准 |
| `moved` | 来源位置移动，需要重新定位 |

## Handling Suggestions

Use one of:

- 轻量保存
- 打开 full audit
- 补锚点
- 重新定位来源
- 暂不可行动
- 默认折叠，可回看

## Forbidden Wording

Never write:

- 已验证
- 已证实
- 已确认正确
- 可信度 87%
- scope-fit 0.72
- 风险 0.18
- 5 个来源支持，因此更可靠
- lineage 完整，因此独立
- 重复出现 7 次，因此支持更强
- dashboard/tests 通过，因此成立
- 无锚点但大意一致
- lint 通过，已安全
- 可直接行动

Allowed replacements:

- 当前状态：普通记录 / 需要复核 / 已解决折叠
- 锚点异常，暂不能回源，必须复核
- 可回源来源数：N；独立性未单独证明
- 已记录来历链路；独立性需另证
- 同类重复 N 次，仅表示归并与路由
- 诊断通过；不代表事实成立
- lint 通过；仅表示未见该类越界
- 如需行动依据，请打开完整审计包

## Operator Preflight Metrics

Do not optimize for line reduction.

Measure:

- `time_to_triage_seconds`
- `serious_miss_y_n`
- `wrong_actionability_y_n`
- `clickback_success_source_record_evidence`
- `authority_misunderstanding_y_n`

Optional qualitative fields:

- why upgraded understood?
- would open full audit?
- anchor problem understood?
- burden 1-5
- notes

## Current Scope

This patch only tests default core:

```text
shell_core + Chinese AI/reviewer-operator rendering
```

It does not test recurrence as a default core.

It does not start user testing, human timing, or dual-review.

## Sparse Pointer Technical Floor

The front face should use a sparse pointer, not a full provenance transcript.

Technical floor:

- keep source / record / evidence handles visible or one click away.
- keep original anchor, selector, quote, version, and hash in the full audit.
- treat pointer display as navigation and auditability, not evidence support.
- do not treat URL-only or path-only provenance as support.
- when a position is missing, stale, drifted, or moved, show anchor health and require review.

This follows the useful part of Web Annotation / PROV-style thinking:

- quote selectors and position selectors are useful, but position can be fragile when resources change.
- provenance bundles can keep the full trace behind a light front-face pointer.
- a front-face sparse pointer can mention the fuller provenance bundle without duplicating it.

Current VAKS interpretation:

```text
front face:
  source / record / evidence / short quote / anchor health

full audit:
  original anchor / selector / quote / offset / version / hash / evidence packet
```

## Alternative Architectures And Absorption Level

| option | judgment | absorption level |
| --- | --- | --- |
| Upgrade "reviewer-card" to "risk-gated review surface + evidence envelope + source-first drilldown". | Better upper-level abstraction. | Directly absorb. |
| Separate ordinary user interface from operator surface. | Required. | Directly absorb. |
| Promote reviewer-card to ordinary user default interface. | Wrong; pushes engineering noise to the user. | Reject. |
| Build a full reviewer cockpit immediately. | Good long-term direction, but beyond the smallest necessary step. | Park / future small-route change. |
| Depend on authority lint as semantic firewall. | Wrong. | Reject. |
| Depend on recurrence bundle as default core. | Too early and risky. | Keep as conditional side arm only. |
