---
type: no_upgrade_validation
status: candidate
created_at: 2026-06-05
project: verified-action-knowledge-system
scope: source-routing-to-pattern-to-borrowing-lightweighting
truth_boundary: validation output only; not reviewed knowledge; not architecture decision; not action basis
write_scope: outputs/review only
---

# v0.2.13 No-Upgrade Validation

## 说人话结论

这个验证回答一个问题：

```text
VAKS 会不会把每份参考资料都逼成知识点、pattern、项目借鉴项，甚至行动依据？
```

结果：

```text
pass
```

健康状态不是“每份资料都升级”。健康状态是：

```text
很多资料停在轻层：可搜、可回源、有 routing hint
少数点进入中层：形成可复用候选模式或项目借鉴条目
极少数进入重层：真的要 promotion / decision / action basis 时才开 warrant gate
```

这符合现在的轻 / 中 / 重分级：

```text
轻 = 能搜到
中 = 能参考
重 = 能拿来做决定
```

## Files Checked

本次只读检查这些现有材料：

```text
outputs/review/source_cards/INDEX.md
outputs/review/source_cards/2026-06-04-external-intake-source-routing-ledger.md
outputs/review/2026-06-05-v0-2-12-reference-sweep-triage.md
outputs/review/2026-06-05-v0-2-12-intake-trial-scsc-tools.md
outputs/review/2026-06-05-v0-2-12-gsn-assurance-case-cluster-deep-read.md
outputs/review/2026-06-05-v0-2-13-light-medium-heavy-alignment.md
outputs/review/2026-06-05-v0-2-13-dual-project-reuse-validation.md
outputs/review/candidate_pattern_bank/INDEX.md
```

没有读取或盘点所有旧 intake 文件。没有写入 `SCHEMA.md`、`REVIEW_QUEUE.md`、`templates/`。

## Test Matrix

| Material / cluster | Correct stopping layer | Why it should not upgrade automatically | Still searchable? |
| --- | --- | --- | --- |
| SCSC Tools page | light | It is a tool directory / discovery source. The trial explicitly says no endorsement, no conformance validation, no new pattern from one source. | yes: source id, URL, source family, tool names, candidate points, future route hints |
| Individual assurance-case vendor tool pages | light / discovery-only | Vendor claims and tool feature lists are not independent support, adoption evidence, or VAKS architecture requirements. | yes: discoverable through the SCSC tools trial and source family |
| Reference sweep items marked already covered or support-only | light | They may repeat existing boundaries, but repetition does not create new support or new patterns. | yes: triage file preserves source names and why they were not prioritized |
| Weak search snippets / broad blogs / generic ADR or TOGAF pages | skip or light | They do not justify deep read, pattern creation, or borrowing entry without stronger anchors. | partly: names remain in triage when useful, but they are not promoted |
| External intake source-routing ledger rows | light overlay | The ledger is routing hint only. Pattern routes are not support and project routes are not project decisions. | yes: rows carry source path, family, transferable candidates, constraints, and route hints |
| Candidate Pattern Bank entries | medium only when warranted | Only recurring mechanisms with problem, mechanism, applicability, non-goals, sources, aliases, and overreach risk qualify. One-off observations stay out. | yes: bank index lists the small active/draft set |
| Project Borrowing Ledger entries | medium / project workspace | A borrowing entry is project contextualization, not ADR, not adoption, not reviewed knowledge. | yes: project workspace remains searchable without becoming truth |
| GSN / SACM / CAE cluster | exception: deep read, then heavy-rule pressure | Multiple sources converged on the missing-warrant problem, but the result is still only a minimal action-basis rule, not full assurance-case adoption. | yes: deep-read and v0.2.13 files retain source-family context |

## Stress Cases

### 1. Tool catalogue to pattern

Bad upgrade path:

```text
SCSC lists many assurance-case tools
-> create "assurance-case-tooling-for-vaks" pattern
-> infer VAKS should adopt a GSN tool workbench
```

Expected behavior:

```text
blocked
```

Reason:

```text
tool directory = discovery
vendor/tool feature claims = candidate claims
tool count = not support
catalogue membership = not conformance validation
```

Actual behavior in current files:

```text
pass
```

The SCSC tools trial keeps it in outputs/review, creates no pattern, makes no adoption judgment, and records only future pattern pressure.

### 2. Search sweep to independent support

Bad upgrade path:

```text
large reference sweep
-> many source names
-> stronger evidence because source count is high
```

Expected behavior:

```text
blocked
```

Reason:

```text
source count is not support strength
same source family is not independent support
already-covered references are support-only at most
```

Actual behavior in current files:

```text
pass
```

The sweep triage separates priority deep-read clusters from already-covered / support-only / weak sources.

### 3. Every intake source to pattern

Bad upgrade path:

```text
new video / repo / paper source
-> extract candidate point
-> create one new candidate pattern per source
```

Expected behavior:

```text
blocked
```

Reason:

```text
candidate point is not automatically a pattern
pattern needs recurring problem, mechanism, applicability, non-goals, sources, and overreach risk
```

Actual behavior in current files:

```text
pass
```

The current Candidate Pattern Bank is sparse. The source-routing ledger points many sources to existing candidate routes instead of minting a new pattern for each source.

### 4. Routing hint to project decision

Bad upgrade path:

```text
Source Routing Overlay says "VAKS: adapt / watch"
-> treat it as project decision
-> update architecture or action basis
```

Expected behavior:

```text
blocked
```

Reason:

```text
routing overlay = hint
project borrowing workspace = pre-ADR / pre-decision
promotion/action basis needs evidence-aware review
```

Actual behavior in current files:

```text
pass
```

The overlay explicitly says pattern route is not support. The light / medium / heavy alignment keeps borrowing separate from action basis.

### 5. v0.2.13 warrant rule contaminates intake

Bad upgrade path:

```text
because action basis needs non-circular warrant
-> every source card must carry a warrant
-> every routing row becomes mini assurance case
```

Expected behavior:

```text
blocked
```

Reason:

```text
v0.2.13 belongs to heavy use only
ordinary source capture and routing stay light
```

Actual behavior in current files:

```text
pass
```

The light / medium / heavy note keeps v0.2.13 as a promotion / decision / action-basis rule, not an intake rule.

## Searchability After No-Upgrade

No-upgrade does not mean lost.

停在轻层的资料仍然可以被搜到，因为它至少保留：

```text
source path / URL / source id
source family / de-dup hint when available
candidate comprehension
candidate points
transferable hints
non-generalizable constraints
candidate pattern routes when useful
optional project route hints when useful
```

也就是说：

```text
不升级 != 不存在
不升级 != 不能检索
不升级 = 不让它假装已经变成通用知识、项目决策或行动依据
```

## What This Confirms

This confirms Pro's warning in operational terms:

```text
not every source becomes a knowledge point
not every candidate point becomes a pattern
not every pattern becomes a project borrowing item
not every borrowing item becomes action basis
not every action-facing claim can pass with an evidence list only
```

The current VAKS direction is therefore compatible with the user's original idea:

```text
external reference material
-> distilled candidate points
-> small reusable candidate knowledge layer when repeated/useful
-> project borrowing workspace when current project fit matters
-> strict action-basis gate only when action/decision/promotion is at stake
```

## Validation Verdict

```text
verdict: pass
mainline_change_needed_now: no
schema_change_needed_now: no
template_change_needed_now: no
new_candidate_pattern_needed_now: no
stable_directory_migration_needed_now: no
continue_in_outputs_review: yes
```

The strongest result is simple:

```text
VAKS can keep sources searchable without forcing them to become knowledge, patterns, project decisions, or action basis.
```
