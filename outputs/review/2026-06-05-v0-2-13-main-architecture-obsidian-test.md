---
type: main_architecture_landing_test
status: test_ready
created_at: 2026-06-05
project: verified-action-knowledge-system
version: v0.2.13-mainline-minimal-rule-test
rule: make-action-support-visible
truth_boundary: architecture wording test; not commit, not release tag
write_scope:
  - FUSION_ARCHITECTURE_V0_2_DRAFT.md
  - ARCHITECTURE_PRINCIPLES.md
  - H:/Obsidian/资料库 sync copy
---

# v0.2.13 Main Architecture / Obsidian Test

## 说人话

这次不是把 VAKS 改成 assurance-case 系统。

主架构只落了一条最小规则：

```text
真正要拿去行动时，不能只列 evidence。
必须说清楚 evidence 为什么支撑这个 claim。
```

短句：

```text
Evidence is not enough; show the non-circular warrant.
```

## Light / Medium / Heavy View

先按这个理解看，不要先看术语：

```text
轻 = 能搜到
中 = 能参考
重 = 能拿来做决定
```

对应关系：

```text
轻：
  Source Card
  Source Routing Overlay
  candidate points
  source-bound constraints

中：
  Candidate Pattern Bank
  Project Borrowing Ledger / Project Borrowing Workspace

重：
  Evidence-Aware Review
  Evidence Sufficiency Gate
  Action Basis
  v0.2.13 non-circular warrant rule
```

健康状态：

```text
很多资料停在轻
少数点进入中
极少数进入重
```

v0.2.13 只属于“重”：

```text
它只在某个参考点要被用于 promotion / decision / action basis 时触发。
它不是 source intake 规则，也不是 Candidate Pattern Bank 规则。
```

## Mainline Landing Points

### 1. `FUSION_ARCHITECTURE_V0_2_DRAFT.md`

新增/强化位置：

```text
Current controlling interpretation
4.5 Evidence Sufficiency Gate
5.2.1 Evidence-Aware Review / Support-Challenge Review
```

测试关键词：

```text
Action Support Visibility
non-circular warrant
action-facing claim
Diagrams, notation, source counts, tool counts, vendor pages, and confidence labels
```

### 2. `ARCHITECTURE_PRINCIPLES.md`

新增/强化位置：

```text
3.3.1 Evidence Packet sharpens review input
```

测试关键词：

```text
evidence list is not action basis by itself
action-facing use must show a non-circular warrant
diagram / notation / source count / tool count / vendor claim / confidence label is not support
```

## What Did Not Change

Not changed:

```text
SCHEMA.md
README.md
IMPLEMENTATION_BLUEPRINT.md
REVIEW_QUEUE.md
templates/
```

No new:

```text
schema object
template
candidate pattern file
assurance-case module
GSN diagram requirement
SACM model
tool adoption
```

## Obsidian Test Steps

Open Obsidian vault:

```text
H:/Obsidian/资料库
```

Open:

```text
FUSION_ARCHITECTURE_V0_2_DRAFT.md
ARCHITECTURE_PRINCIPLES.md
outputs/review/2026-06-05-v0-2-13-main-architecture-obsidian-test.md
```

Search in Obsidian:

```text
non-circular warrant
Action Support Visibility
evidence list is not action basis
```

Expected effect:

```text
The rule should appear as a small action-basis guardrail inside existing review/sufficiency logic.
It should not look like a new subsystem or template family.
```

## Manual Test Cases In Obsidian

### Case 1: Good action-basis packet

Should pass candidate review:

```text
claim: retrieval should stay activation, not truth
evidence: candidate pattern + VAKS ledger + architecture boundary
warrant: all anchors address the same boundary and none promotes truth by retrieval
scope: retrieval/context-pack preparation
challenge: candidate pattern is not reviewed truth
status: candidate wording review allowed, mainline promotion blocked
```

### Case 2: Bad action-basis packet

Should fail:

```text
claim: source intake templates should change now
evidence: active candidate pattern + VAKS ledger says adapt
warrant: active + adapt means template should change
```

Failure reason:

```text
candidate pattern is not reviewed truth
ledger adapt is not architecture decision
required gates missing
ordinary capture burden risk
```

### Case 3: Tool catalogue shortcut

Should fail:

```text
claim: VAKS should adopt assurance-case tools
evidence: SCSC Tools lists many tools
warrant: many tools exist, so VAKS should adopt/build them
```

Failure reason:

```text
tool catalogue = discovery only
vendor/tool count = not support or action readiness
```

## Test Verdict

Current local verdict:

```text
main architecture minimal rule: landed for Obsidian inspection
Obsidian sync copy: expected after sync step
mainline release/commit: not done
commit/push: not done
```

If the rule feels too heavy in Obsidian, the likely fix is not schema change. It is wording trim.
