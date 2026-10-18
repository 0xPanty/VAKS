---
type: sandbox_final_report
status: completed
created_at: 2026-06-05
project: verified-action-knowledge-system
scope: seven-project-sidecar-candidates-full-pressure-test
truth_boundary: sandbox test report only; not reviewed knowledge; not architecture decision; not action basis
---

# Seven Project-Sidecar Candidates Full Pressure Test

## 一句话

七个候选**值得继续留沙盒用**，但**不适合整套进主架构**。

它们对 Codex/agent 维护项目确实顺手，尤其是 `kp_ref`、`target_hint`、
`stance/outcome` 分离、closeout drain、tombstone 排除和默认检索顺序。

但一旦全量写进主架构，主线马上从一条轻边界膨胀成对象模型、字段契约、
生命周期协议、检索规则和清场制度。测试结论是：

```text
keep testing in outputs/review
do not mainline the object model
do not modify SCHEMA.md / REVIEW_QUEUE.md / templates
```

## What Was Built

New sandbox:

```text
outputs/review/project-sidecar-seven-candidate-pressure-test-2026-06-05/
```

Major artifacts:

```text
mainline_baseline/
mainline_with_seven_candidates/
misa_overlay/MISA.md
misa_overlay/MISA-closeout-manifest-2026-06-05.md
snapshots/landed/misa-runtime-memory-quarantine-no-effect-gate.md
snapshots/boundary/misa-retrieval-hints-not-control-authority.md
snapshots/boundary/misa-graph-carrier-not-controller.md
snapshots/boundary/retrieval-priority-wording-withdrawn.md
snapshots/boundary/default-retrieval-precedence-is-inclusion-order.md
tombstones/adaptive-retrieval-depth-duplicate-vector-priority.md
checks/
```

Obsidian copy:

```text
H:\Obsidian\资料库\outputs\review\project-sidecar-seven-candidate-pressure-test-2026-06-05
H:\Obsidian\资料库\outputs\review\project-sidecar-seven-candidate-pressure-test-2026-06-05.zip
```

## Second Project Sample

Misa / `misa-cybernetic-evolution` was suitable as the second-project sample.

Why:

```text
It has real docs, modules, schemas, tests, commands, sidecar boundaries,
runtime-thread logic, component-health diagnostics, replay gates, VPS shadow
scripts, and human-owner authority boundaries.
```

Concrete evidence:

```text
selected Misa tests run: 25
passed: 25
failed: 0
```

See:

```text
checks/misa-anchor-and-test-evidence.md
```

## Quant Results

Sandbox mainline insertion:

```text
ARCHITECTURE_PRINCIPLES.md: +131 / -0
FUSION_ARCHITECTURE_V0_2_DRAFT.md: +15 / -0
total: +146 / -0
```

Misa overlay:

```text
entries: 11
healthy anchors: 17
not_checked anchors: 9
unanchored anchors: 1
```

Pressure matrix:

```text
average_sandbox_usefulness: 2.57 / 3
average_mainline_readiness: 0.71 / 3
average_leakage_risk: 2.43 / 3
average_maintenance_gain: 2.57 / 3
```

Interpretation:

```text
High sandbox value.
Low mainline readiness.
High leakage risk if promoted too early.
```

## Seven Candidate Verdicts

| Candidate | Verdict | Why |
|---|---|---|
| Project Lens concept / naming | Keep as sandbox alias only | useful shorthand, but too object-like for mainline |
| Field design | Keep minimal sandbox fields | helps maintenance, but not schema-ready |
| `stance` state design | Keep `watch/partial/avoid/park` in sandbox | useful if outcome words are banned from live stance |
| Snapshot mechanism | Keep only as candidate experience/boundary | valuable, but high best-practice / universal-ban risk |
| Closeout drain protocol | Keep testing as sandbox policy | directly prevents zombie overlays |
| Lifecycle actions | Keep as operations, not state machine | useful, but too heavy and owner-confirmation dependent |
| Retrieval precedence / manifest | Keep with renamed wording | use `default retrieval precedence`; avoid `retrieval priority` |

## What Worked

### 1. Misa gave real anchors

The second-project test was not concept-only. Most entries point to actual files,
symbols, tests, or commands.

### 2. `kp_ref` and `target_hint` helped

As an agent, I could quickly move:

```text
overlay entry -> candidate pattern -> Misa file/module/test -> boundary check
```

That made maintenance faster and less guessy.

### 3. `stance` and outcome separation held

The live overlay could say `watch`, `partial`, `avoid`, or `park` without saying
`adopted`, `rejected`, `approved`, or `landed`.

That prevented the Misa overlay from becoming an ADR.

### 4. The action-facing escalation did the right thing

The Misa component-health scenario forced the overlay to stop at navigation.
The action-facing answer had to use v0.2.13:

```text
claim
anchored evidence
non-circular warrant
scope / assumptions
known gaps / risks
residual review status
```

See:

```text
checks/action-facing-escalation.md
```

## Obsidian Sync

The package was copied into the formal Obsidian vault sandbox path and hash
checked.

First sync:

```text
repo_file_count: 26
mismatch_count: 0
zip_match: true
```

Final sync includes `checks/obsidian-sync.md`; see that file for details.

## What Broke Or Nearly Broke

### 1. Full mainline insertion got heavy fast

`+146` lines is too much for the mainline docs. It changes the feel from
principle to operating system.

### 2. Snapshot wording is fragile

Without `candidate experience` and `candidate boundary`, snapshots read like:

```text
landed = best practice
boundary = universal ban
```

This is the highest authority-leakage risk.

### 3. Retrieval wording needed correction

`retrieval priority` should be withdrawn for this mechanism.

Use:

```text
default retrieval precedence
default search inclusion order
default read order
```

### 4. Lifecycle actions are useful but too institutional

Archive, delete+tombstone, carry-forward, and supersede worked in the manifest,
but promoting them as mainline states would make the system feel bureaucratic.

They should stay owner-confirmed operations.

### 5. Not all targets were healthy

The overlay had:

```text
healthy anchors: 17
not_checked anchors: 9
unanchored: 1
```

That is acceptable for sandbox pressure testing, but not enough for formalizing
a field contract.

## Retain / Change / Drop

### Retain In Sandbox

```text
kp_ref
stance: watch | partial | avoid | park
borrow_scope
non_borrow_scope
target_hint
outcome_ref
updated_at
closeout drain manifest
delete+tombstone audit trail
default retrieval precedence
```

### Change

```text
Project Lens -> sandbox alias only
retrieval priority -> default retrieval precedence
landed snapshot -> candidate experience snapshot
boundary snapshot -> candidate boundary snapshot
anchor_health -> prefer derived/check result, not manual required field
gate_hint -> use sparingly or drop from minimal fields
review_origin -> drop from minimal fields
```

### Do Not Mainline Now

```text
Project Lens named object
field contract
stance enum
snapshot vocabulary
closeout lifecycle protocol
lifecycle state machine
retrieval precedence policy
formal workspace directory
SCHEMA.md changes
REVIEW_QUEUE.md changes
template changes
automation / database / graph governance
```

## Final Recommendation

Keep the current mainline exactly where it is:

```text
v0.2.13 action-facing warrant gate
generic project-scoped sidecar overlay boundary principle
```

Continue the seven candidates in `outputs/review` only.

The next useful test is not more architecture insertion. It is one more
second-project or third-project live maintenance pass where a non-author tries
to use the overlay and reports confusion, speed, and boundary leakage.
