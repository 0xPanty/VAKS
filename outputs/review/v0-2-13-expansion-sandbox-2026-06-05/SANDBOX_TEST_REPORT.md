---
type: expansion_sandbox_test_report
status: completed
created_at: 2026-06-05
project: verified-action-knowledge-system
scope: v0.2.13-not-landed-expansion-options
truth_boundary: sandbox test only; not reviewed knowledge; not architecture decision; not action basis
write_scope: outputs/review only
---

# v0.2.13 Expansion Sandbox Test Report

## 说人话结论

这 7 个东西已经放进沙盒测了。

测试结果：

```text
全部不适合现在落地。
```

不是说它们永远没用，而是：

```text
现在落地会太早、太重、太容易误导 agent。
```

当前最稳状态仍然是：

```text
主架构只保留 v0.2.13 最小规则。
这 7 个扩展项继续留在 outputs/review 沙盒。
```

## Test Method

对每个扩展项问 5 个问题：

```text
1. 它是否解决当前真实痛点？
2. 它是否会污染 light / medium / heavy 分层？
3. 它是否会让 candidate / borrowing / routing 冒充 truth 或 decision？
4. 它是否会让 ordinary intake 变重？
5. 它是否已有足够真实使用证据？
```

判定：

```text
pass_to_mainline
keep_sandboxed
reject_for_now
```

## Candidate 1: New Schema

Verdict:

```text
reject_for_now
```

Why:

```text
The useful part is already captured by the minimal mainline rule.
A schema object would make the final warrant check look like a new formal data layer.
That increases compliance pressure before we have long-run proof it helps.
```

Failure mode:

```text
agent starts asking for action_support_envelope everywhere
ordinary action notes become schema filling
review status becomes mini state machine
```

Current disposition:

```text
do not modify SCHEMA.md
```

## Candidate 2: New Template

Verdict:

```text
keep_sandboxed
```

Why:

```text
A tiny checklist may become useful later, but a reusable template now would be too tempting.
Agents may apply it to ordinary intake, summaries, and routing notes.
```

Failure mode:

```text
source card becomes mini action basis
simple reviewer question becomes full warrant packet
template completeness replaces real judgment
```

Current disposition:

```text
no template change now
possible future tiny checklist only after repeated inconsistency
```

## Candidate 3: Formal Project Development Workspace Directory

Verdict:

```text
keep_sandboxed
```

Why:

```text
The idea is directionally useful because the user does want a development / borrowing area.
But naming and semantics are still not stable enough to make a formal directory.
If it lands too early, it may look like reviewed knowledge, ADR, or official architecture area.
```

Failure mode:

```text
project borrowing workspace becomes hidden decision folder
watch / adapt / reject looks official
cross-project candidate points get polluted by VAKS-specific disposition
```

Current disposition:

```text
continue using outputs/review/project_borrowing_ledgers as sandbox
do not create formal stable directory yet
```

## Candidate 4: New Pattern

Verdict:

```text
reject_for_now
```

Why:

```text
v0.2.13 is a final gate rule, not a reusable design pattern.
Turning it into a named pattern would invite overuse and abstraction drift.
```

Failure mode:

```text
structured-action-support-envelope becomes a pretty-name object
agents route ordinary sources into it
pattern bank fills with process wrappers instead of reusable mechanisms
```

Current disposition:

```text
do not create candidate pattern file
```

## Candidate 5: GSN / SACM System

Verdict:

```text
reject_for_now
```

Why:

```text
GSN / SACM / assurance-case materials helped identify the missing-warrant problem.
But VAKS only needs the small insight: action-facing support must expose claim, evidence,
warrant, scope, challenges, and status.
It does not need diagram notation, metamodels, confidence notation, or assurance-case tooling.
```

Failure mode:

```text
VAKS becomes an assurance-case system
diagrams or notation get mistaken for support
confidence notation gets mistaken for truth confidence
ordinary review becomes model maintenance
```

Current disposition:

```text
do not adopt GSN / SACM system
keep source cluster in outputs/review
```

## Candidate 6: Tool Adoption

Verdict:

```text
reject_for_now
```

Why:

```text
Tool pages are discovery-only.
They do not prove fit, conformance, maturity, adoption value, or VAKS need.
No current VAKS bottleneck requires a GSN / assurance-case tool.
```

Failure mode:

```text
catalogue membership becomes endorsement
vendor claim becomes support
tool count becomes maturity proof
tool workflow dictates VAKS architecture
```

Current disposition:

```text
no tool adoption
no tool evaluation project
tool pages remain discovery-only
```

## Candidate 7: Make All Intake Heavier

Verdict:

```text
reject_for_now
```

Why:

```text
This directly violates the light / medium / heavy design.
It would make agents produce fake rigor for ordinary source capture.
The correct default is still light intake, with v0.2.13 only at promotion / decision / action basis.
```

Failure mode:

```text
ordinary source card becomes heavy review
candidate comprehension pretends to be evidence-aware review
agents fabricate non-circular-looking warrants too early
users stop using the workflow because capture cost is too high
```

Current disposition:

```text
ordinary intake stays light
v0.2.13 remains heavy-only
```

## Summary Matrix

| Expansion | Sandbox verdict | Why not land now |
| --- | --- | --- |
| New schema | reject_for_now | Turns sentence-level guardrail into formal object too early |
| New template | keep_sandboxed | May become useful later, but likely to over-trigger now |
| Formal development workspace directory | keep_sandboxed | Direction useful, naming/semantics not stable enough |
| New pattern | reject_for_now | v0.2.13 is a gate rule, not a reusable pattern |
| GSN / SACM system | reject_for_now | Would convert VAKS into assurance-case system |
| Tool adoption | reject_for_now | Tool pages are discovery, not fit/adoption evidence |
| All intake heavier | reject_for_now | Breaks light / medium / heavy design |

## Final Sandbox Verdict

```yaml
new_schema: reject_for_now
new_template: keep_sandboxed
formal_development_workspace_directory: keep_sandboxed
new_pattern: reject_for_now
gsn_sacm_system: reject_for_now
tool_adoption: reject_for_now
all_intake_heavier: reject_for_now
mainline_change_needed: no
schema_change_needed: no
template_change_needed: no
directory_change_needed: no
keep_outputs_review_sandbox: yes
```

## What This Means

The sandbox confirms:

```text
The only thing that deserved mainline landing was the minimal v0.2.13 rule.
The bigger structures are either premature or actively harmful right now.
```

Good future path:

```text
Keep using outputs/review/project_borrowing_ledgers as the sandbox development area.
Let real use prove whether a stable directory or tiny checklist is needed.
Do not pre-build the system.
```
