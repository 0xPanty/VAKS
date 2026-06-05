---
type: real_promotion_validation
status: candidate
created_at: 2026-06-05
project: verified-action-knowledge-system
scope: v0-2-13-mainline-minimal-rule-landing
truth_boundary: validation output only; not reviewed knowledge; not release tag; not action basis for future unrelated changes
write_scope: outputs/review only
---

# v0.2.13 Real Promotion Validation

## 说人话结论

这次验证的是一个真实问题：

```text
既然 v0.2.13 的最小 warrant 规则已经按用户要求放进主架构，
它现在是该保留，还是说明我们放太早了要收回？
```

结论：

```text
keep the minimal mainline wording for now
do not expand it
do not create schema/template/new subsystem/stable workspace yet
```

更直白：

```text
这条小规则可以留。
但只留这条小规则。
```

## Action-Facing Claim

```text
VAKS should keep the v0.2.13 main architecture landing as a minimal action-support
visibility guardrail, because it only strengthens the existing Evidence-Aware Review /
Evidence Sufficiency Gate / Action Basis boundary. It should not be expanded into
a schema object, template, candidate pattern, stable project workspace, assurance-case
subsystem, or directory migration at this time.
```

## Point-Specific Anchored Evidence

### Evidence 1: Pro's recommendation allowed a future minimal rule

Anchor:

```text
outputs/review/2026-06-05-v0-2-13-pro-review-response-revise-candidate.md
```

Relevant point:

```text
Pro's verdict was revise_candidate, but it explicitly described the future acceptable
shape as a sentence-level minimal rule plus companion guardrail, not a new system,
pattern, schema object, or template family.
```

Support role:

```text
Supports keeping a very small mainline guardrail if it stays minimal.
Blocks expansion into a named subsystem or full assurance-case framework.
```

### Evidence 2: The main architecture landing is minimal

Anchors:

```text
FUSION_ARCHITECTURE_V0_2_DRAFT.md
ARCHITECTURE_PRINCIPLES.md
outputs/review/2026-06-05-v0-2-13-main-architecture-obsidian-test.md
```

Relevant point:

```text
The landing adds Action Support Visibility / non-circular warrant wording to existing
Evidence Sufficiency Gate and Evidence-Aware Review language. It did not add a new
schema object, template, pattern file, GSN diagram requirement, SACM model, or tool
adoption path.
```

Support role:

```text
Supports the claim that the change is a minimal guardrail, not a system conversion.
```

### Evidence 3: Pressure tests found the right failure modes

Anchors:

```text
outputs/review/2026-06-05-v0-2-13-revised-pressure-test-suite.md
outputs/review/2026-06-05-v0-2-13-revised-nonmeta-action-basis-trials.md
outputs/review/2026-06-05-v0-2-13-no-upgrade-validation.md
```

Relevant point:

```text
The tests catch circular warrant, source-family fake independence, tool/vendor/diagram
support smuggling, premature template change, routing-hint-to-decision jumps, and
v0.2.13 contaminating ordinary intake.
```

Support role:

```text
Supports keeping the guardrail because it improves blocking of real overreach paths.
```

### Evidence 4: Dual-project validation preserved contextualization

Anchor:

```text
outputs/review/2026-06-05-v0-2-13-dual-project-reuse-validation.md
```

Relevant point:

```text
The same candidate pattern can be adapt for VAKS and already-aligned / watch-only
for Misa without changing the candidate pattern itself.
```

Support role:

```text
Supports the larger layer boundary: reusable candidate knowledge remains separate
from project-specific borrowing and project decisions.
```

### Evidence 5: No-upgrade validation preserved light intake

Anchor:

```text
outputs/review/2026-06-05-v0-2-13-no-upgrade-validation.md
```

Relevant point:

```text
Many sources can stay searchable in source cards / routing overlays without becoming
candidate patterns, borrowing entries, or action basis.
```

Support role:

```text
Supports keeping ordinary capture/search light while reserving warrant checks for
heavy action-facing use.
```

## Non-Circular Warrant

These anchors support the action-facing claim because they address the exact promotion boundary under test:

```text
Should the minimal v0.2.13 action-support rule remain in main architecture after landing?
```

The Pro review did not say "never promote"; it said the current candidate needed narrowing and that the future acceptable shape would be a very small rule plus guardrail. The landing matches that narrow shape: it adds support-visibility wording inside existing Evidence-Aware Review / Evidence Sufficiency Gate / Action Basis boundaries, and it explicitly blocks diagrams, notation, source counts, tool counts, vendor pages, and confidence labels from becoming support.

The pressure tests then show why the rule matters: it catches cases where an evidence list looks full but does not explain why the evidence supports the action-facing claim. The no-upgrade and dual-project validations show the rule has not forced every source, pattern, or borrowing entry to become heavy.

Therefore the evidence supports:

```text
keep the minimal main architecture wording
```

It does not support:

```text
schema change
template change
candidate pattern creation
stable project workspace migration
directory rename
full assurance-case / GSN / SACM adoption
```

## Scope / Assumptions

Scope:

```text
only the minimal v0.2.13 action-support visibility wording
only action_basis / significant promotion / decision / risk-sensitive use
only current VAKS architecture wording
```

Assumptions:

```text
ordinary source capture remains governed by light / medium / heavy separation
outputs/review remains the experimental landing zone for candidate validations
future schema/template/directory changes need separate review
```

## Known Challenges / Gaps

Known challenges:

```text
the validation suite is still mostly manual
the rule's usability over repeated ordinary work is not proven long-term
"non-circular warrant" still requires reviewer judgment
```

Known gaps:

```text
no second Pro review of the exact mainline wording after landing
no stable workspace migration test
no template-level burden test
no long-run intake sample showing ordinary sources remain light over many weeks
```

These gaps do not require rolling back the minimal rule. They do block expansion.

## Current Residual Review Status

```yaml
minimal_mainline_wording: keep_for_now
expansion_to_schema: blocked
expansion_to_template: blocked
candidate_pattern_file: blocked
stable_project_workspace_migration: blocked
directory_rename: blocked
assurance_case_system_adoption: blocked
ordinary_intake_change: blocked
residual_risk: medium for expansion, low-to-medium for the minimal wording
```

## Decision For This Validation

Decision:

```text
Keep the v0.2.13 minimal main architecture landing.
```

Do not do now:

```text
do not rename Project Borrowing Ledger / Workspace directories
do not create a new stable "development area" directory
do not add schemas
do not add templates
do not create a structured assurance-case pattern
do not claim v0.2.13 is fully validated
```

Allowed next step:

```text
continue using outputs/review to test light / medium / heavy behavior on real materials
```

## What This Means Compared With Pro's Advice

Pro's advice was:

```text
reasonable direction
make it smaller
keep it late-triggered
test no-upgrade and real promotion
do not expand into a system
```

Current state after this validation:

```text
the smallest mainline rule has landed
no-upgrade validation passed
dual-project contextualization passed
real promotion validation says keep the rule but stop there
```

So the answer is:

```text
yes, Pro's core advice has been implemented in the conservative form
no, Pro's larger future workspace/naming suggestions have not been promoted yet
```
