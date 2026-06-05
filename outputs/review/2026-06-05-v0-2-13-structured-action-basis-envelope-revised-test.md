---
type: candidate_patch_test
status: revise_candidate
created_at: 2026-06-05
project: verified-action-knowledge-system
version_under_test: v0.2.13
patch_under_test: v0-2-13-make-action-support-visible
test_method: revised_manual_boundary_trial
source_basis:
  - outputs/review/2026-06-05-v0-2-13-structured-action-basis-envelope-revised-candidate-patch.md
  - outputs/review/2026-06-05-v0-2-13-pro-review-response-revise-candidate.md
truth_boundary: test output only, not reviewed knowledge
write_scope: outputs/review only
---

# v0.2.13 Revised Test: Make Action Support Visible

## 测试结论

v0.2.13 revised candidate passes a stricter boundary / face-validity trial.

It does not yet pass a real VAKS action-basis validation, because no real action-basis example has been run.

What this test supports:

```text
The revised rule is narrower than the original draft.
It catches missing or non-explanatory warrant cases.
It does not intentionally burden ordinary intake.
It keeps tool/vendor/diagram/source-count material out of support.
```

What this test does not support:

```text
mainline promotion
candidate pattern creation
validated ordinary-intake non-burden
validated real-world action-basis usefulness
```

## Test Matrix

| Test | Pressure | Expected Result | Result |
| --- | --- | --- | --- |
| T1 | Ordinary source routing | Do not trigger rule | PASS |
| T2 | Action-facing claim with anchored evidence and non-circular warrant | Candidate action-basis packet can proceed to review | PASS |
| T3 | Blank warrant | Block / degrade action use | PASS |
| T4 | Circular warrant | Block / degrade action use | PASS |
| T5 | Scope jump | Block / degrade action use | PASS |
| T6 | Same source family repeated as independent support | Degrade support independence claim | PASS |
| T7 | Tool/vendor/diagram used as support | Exclude as non-support | PASS |
| T8 | Explicit "is this enough?" ordinary reviewer question | Do not trigger unless action/promotion/decision/risk-sensitive | PASS |
| T9 | Strong relation proposed for ordinary context | Do not trigger unless promotion/action-critical | PASS |
| T10 | Existing v0.2.12 flow | Preserve flow; no new ordinary stage | PASS |

## T1: Ordinary Source Routing

### Input

```text
New source arrives.
Need to create routing overlay and candidate comprehension.
No action, promotion, decision, or risk-sensitive answer is being made.
```

### Expected v0.2.13 revised behavior

```text
trigger_make_support_visible: no
reason: ordinary intake / routing
```

### Judgment

PASS.

The rule stays late and action-facing.

## T2: Good Enough Action-Facing Use

### Input

```yaml
action_facing_claim: VAKS should keep GSN / CAE borrowing candidate-only and use only a lightweight action-support visibility rule.
point_specific_anchored_evidence:
  - GSN / CAE deep-read says the useful borrowing is claim/evidence/argument/context organization, not full system conversion.
  - Pro review says the direction is valid but should stay revise_candidate and narrow.
non_circular_warrant: The evidence directly addresses the same design question: whether VAKS should borrow a lightweight evidence-to-claim argument structure without adopting a full assurance-case system. The Pro review also narrows the wording and blocks mainline promotion, which matches the claim's candidate-only scope.
scope_assumptions:
  - applies only to action_basis / significant promotion / decision / risk-sensitive use.
known_challenges_or_gaps:
  - no real VAKS action-basis example has been run.
current_residual_review_status: candidate-only; ready for one real example trial, not mainline.
```

### Expected behavior

```text
status: can_proceed_to_candidate_review
mainline_ready: no
```

### Judgment

PASS.

The warrant explains why the evidence supports the scoped claim.

## T3: Blank Warrant

### Input

```yaml
action_facing_claim: Promote the v0.2.13 rule to mainline.
point_specific_anchored_evidence:
  - GSN / CAE sources discuss claim/evidence/argument structures.
non_circular_warrant:
known_challenges_or_gaps:
  - no real action-basis example yet.
```

### Expected behavior

```text
status: insufficient
reason: missing_or_non_explanatory_warrant
blocked_next_step: mainline promotion
```

### Judgment

PASS.

This catches the easy missing-warrant case.

## T4: Circular Warrant

### Input

```yaml
action_facing_claim: Promote the v0.2.13 rule to mainline.
point_specific_anchored_evidence:
  - Pro review says the direction is valid.
non_circular_warrant: The evidence supports mainline promotion because it supports mainline promotion.
known_challenges_or_gaps:
  - Pro review said revise_candidate, not accept_candidate.
```

### Expected behavior

```text
status: insufficient
reason: circular_warrant
blocked_next_step: mainline promotion
```

### Judgment

PASS.

This is the important upgrade over a simple blank-field check.

## T5: Scope Jump

### Input

```yaml
action_facing_claim: Because GSN helps safety cases, VAKS ordinary source intake should require an action-support envelope for every source.
point_specific_anchored_evidence:
  - GSN material describes claim/evidence/context/strategy structures for assurance arguments.
non_circular_warrant: GSN uses structured arguments, so all VAKS intake should use structured arguments too.
scope_assumptions:
  - ordinary source intake is equivalent to action-basis use.
```

### Expected behavior

```text
status: insufficient
reason: scope_jump
blocked_next_step: ordinary_intake_change
```

### Judgment

PASS.

The source applies to action-facing assurance argument organization, not ordinary intake burden.

## T6: Source-Family Repetition As Fake Independence

### Input

```yaml
action_facing_claim: The v0.2.13 rule has many independent supports.
point_specific_anchored_evidence:
  - SCSC GSN overview
  - SCSC GSN nutshell
  - SCSC GSN pattern catalogue
non_circular_warrant: These are three pages, so they count as three independent supports.
```

### Expected behavior

```text
status: insufficient_for_independence_claim
reason: source_family_repetition_not_independent_support
```

### Judgment

PASS.

The revised rule keeps source-family context as a guardrail when relevant, not a mandatory field.

## T7: Tool / Vendor / Diagram Smuggled Into Support

### Input

```yaml
action_facing_claim: VAKS should implement assurance-case tooling.
point_specific_anchored_evidence:
  - SCSC Tools lists multiple assurance-case tools.
  - Vendor pages show diagram editors and collaboration features.
non_circular_warrant: Many tools exist and the diagrams look mature, so VAKS should implement this capability.
```

### Expected behavior

```text
status: insufficient
reason:
  - tool_count_not_adoption_evidence
  - vendor_claim_not_conformance_validation
  - diagram_clarity_not_support
blocked_next_step: tool adoption or mainline architecture change
```

### Judgment

PASS.

Tool ecosystem remains discovery-only.

## T8: Explicit "Is This Enough?" But Not Action-Facing

### Input

```text
Reviewer asks: Is this enough context to keep reading this source?
No promotion, decision, action-basis, or risk-sensitive answer is being made.
```

### Expected behavior

```text
trigger_make_support_visible: no
reason: explicit enough-question is not action/promotion/decision/risk-sensitive
```

### Judgment

PASS.

This narrows the original trigger wording.

## T9: Strong Relation But Not Promotion / Action-Critical

### Input

```text
A draft note says two concepts may be related.
The relation is not being promoted and not used for action.
```

### Expected behavior

```text
trigger_make_support_visible: no
reason: relation is not promotion-facing or action-critical
```

### Judgment

PASS.

This prevents action-basis-only from leaking into ordinary relation drafting.

## T10: Existing v0.2.12 Flow Compatibility

### Input

```text
Raw Source
-> Source Routing Overlay
-> Candidate Pattern Bank
-> Project Borrowing Ledger
-> Evidence-Aware Review / EtD-lite
-> Decision / Action Basis
```

### Expected behavior

```text
new_stage_added: no
late_rule_added: yes, only for triggered action-facing use
```

### Judgment

PASS.

v0.2.13 revised remains compatible with v0.2.12.

## Regression Summary

| Boundary | Result |
| --- | --- |
| Candidate-only status preserved | PASS |
| Action-basis-only wording narrowed | PASS |
| Ordinary intake not intentionally burdened | PASS |
| Missing warrant caught | PASS |
| Circular warrant caught | PASS |
| Scope jump caught | PASS |
| Source-family fake independence caught | PASS |
| Tool/vendor/diagram support smuggling caught | PASS |
| Candidate pattern not created | PASS |
| Mainline promotion not claimed | PASS |

## Remaining Risk

The revised candidate still needs a real VAKS example.

Unproven:

```text
Does this improve a real action-basis note?
Does it stay lightweight when used on real material?
Does it reduce mistaken action readiness without annoying ordinary review?
```

## Recommendation

Keep as:

```text
v0.2.13 revised candidate
```

Do not promote to mainline.

Do not create a candidate pattern file.

Next test:

```text
Pick one real VAKS action-basis / important promotion / risk-sensitive answer
and run the revised rule against it.
```
