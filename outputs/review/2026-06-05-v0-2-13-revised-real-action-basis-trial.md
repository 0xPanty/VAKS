---
type: real_action_basis_trial
status: candidate
created_at: 2026-06-05
project: verified-action-knowledge-system
version_under_test: v0.2.13 revised candidate
rule_under_test: v0-2-13-make-action-support-visible
trial_question: should_v0_2_13_revised_remain_current_candidate_working_posture
truth_boundary: trial output only, not reviewed knowledge, not architecture decision
write_scope: outputs/review only
---

# v0.2.13 Revised Real Action-Basis Trial

## 试跑问题

这不是概念测试，而是一个真实的候选行动依据问题：

```text
VAKS 现在是否应该把 v0.2.13 revised 作为当前 candidate working posture 继续使用，
同时明确不进主线、不建 pattern、下一步只做真实案例继续试跑？
```

## Action-Facing Claim

```text
VAKS should keep v0.2.13 revised as the current candidate-only working posture
for action-basis / significant-promotion / risk-sensitive review experiments,
but should not promote it to mainline or create a candidate pattern file yet.
```

## Point-Specific Anchored Evidence

### Evidence 1: Pro verdict was `revise_candidate`, not reject

Anchor:

```text
outputs/review/2026-06-05-v0-2-13-pro-review-response-revise-candidate.md
```

Relevant point:

```text
Pro accepted the direction but asked to narrow trigger, reduce fields,
make warrant non-circular, and keep candidate-only.
```

Support role:

```text
Supports continuing the direction, but blocks accept/mainline promotion.
```

### Evidence 2: Revised patch incorporated Pro constraints

Anchor:

```text
outputs/review/2026-06-05-v0-2-13-structured-action-basis-envelope-revised-candidate-patch.md
```

Relevant point:

```text
The patch now frames the rule as "make action support visible",
not as a new schema object or assurance-case subsystem.
```

Support role:

```text
Supports keeping the revised candidate because the overreach risk was reduced.
```

### Evidence 3: Revised pressure test found no blocking design failure

Anchor:

```text
outputs/review/2026-06-05-v0-2-13-revised-pressure-test-suite.md
```

Relevant point:

```text
The rule survived adversarial tests around trigger creep, circular warrant,
scope jump, source-family fake independence, tool/vendor/diagram support smuggling,
candidate pattern overreach, and premature mainline promotion.
```

Support role:

```text
Supports using it as current candidate posture for further real trials.
```

### Evidence 4: The rule remains aligned with v0.2.12 boundaries

Anchor:

```text
outputs/review/2026-06-05-v0-2-13-revised-next-window-memory-alignment.md
outputs/review/2026-06-05-v0-2-12-next-window-memory-alignment.md
```

Relevant point:

```text
URL/source remains provenance; raw text remains source text; candidate point remains review unit;
retrieval/context pack remains activation/context preparation; action basis still requires review.
```

Support role:

```text
Supports compatibility with the existing candidate workflow.
```

## Non-Circular Warrant

These evidence anchors support the action-facing claim because they address the same decision:

```text
Should v0.2.13 revised continue as the current candidate posture, and how far may it go?
```

The Pro review establishes the direction is worth keeping but not yet accepting. The revised patch shows the main overreach concerns were narrowed: fewer core fields, narrower triggers, non-circular warrant, no pattern file, no mainline. The pressure suite then tried to break those changes across trigger, evidence, warrant, source-family, tool/vendor, pattern, and promotion dimensions and found no blocking design failure. Together, these support continued candidate-only use.

They do not support mainline promotion because the same evidence also says:

```text
real VAKS action-basis usefulness is not fully proven
ordinary intake non-burden is intended but not proven over time
second-pass wording review would still be required before mainline
```

Therefore the correct action is:

```text
continue candidate-only use and real-case trials
not mainline promotion
not pattern creation
```

## Scope / Assumptions

Scope:

```text
applies only to v0.2.13 revised candidate workflow under outputs/review
applies only to action-basis / significant promotion / decision / risk-sensitive review experiments
does not apply to ordinary source intake, routing, search, or simple summaries
```

Assumptions:

```text
the Pro review text was accurately transcribed by the user
current local files are the durable state
no mainline docs are being modified in this trial
```

## Known Challenges / Gaps

Challenges:

```text
The pressure suite is still manual.
The real trial is meta-level: it tests the current candidate-posture decision,
not a future unrelated high-stakes operational answer.
Warrant quality remains reviewer-judgment-dependent.
```

Gaps:

```text
No long-run usability evidence.
No proof that ordinary intake stays light under repeated use.
No second Pro review of the exact revised wording.
```

## Current Residual Review Status

```yaml
status: candidate_only_continue
mainline_promotion: blocked
candidate_pattern_file: blocked
ordinary_intake_change: blocked
next_allowed_step: run another real, non-meta VAKS action-basis or important promotion example
residual_risk: medium-low for candidate use, high for mainline promotion
```

## Decision For This Trial

Decision:

```text
Keep v0.2.13 revised as the current candidate working posture.
```

Do not:

```text
promote to mainline
create pattern file
modify templates
claim validation is complete
claim ordinary intake is proven unaffected
```

## What This Trial Proved

It proved enough for:

```text
continued candidate-only use
using the revised rule in future action-basis experiments
calling v0.2.13 revised the current candidate posture
```

It did not prove enough for:

```text
mainline patch
pattern-bank entry
template update
schema update
ordinary-intake non-burden as a proven fact
```

## Follow-Up Trial Needed

The next trial should be less meta.

Good candidates:

```text
Should `retrieval-is-activation-not-truth` receive a tiny mainline wording patch?
Should `source-structure-first-rag` change any source intake guidance?
Should a risk-sensitive answer use a specific candidate point as action basis?
```

The rule has earned that next test. It has not earned mainline promotion.
