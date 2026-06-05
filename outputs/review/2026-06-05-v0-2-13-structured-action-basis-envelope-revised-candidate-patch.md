---
type: candidate_patch
status: revise_candidate
created_at: 2026-06-05
project: verified-action-knowledge-system
version: v0.2.13
revision: revised_after_pro_review
patch_id: v0-2-13-make-action-support-visible
previous_patch_id: v0-2-13-structured-action-basis-envelope
source_basis:
  - outputs/review/2026-06-05-v0-2-13-pro-review-response-revise-candidate.md
  - outputs/review/2026-06-05-v0-2-13-structured-action-basis-envelope-candidate-patch.md
  - outputs/review/2026-06-05-v0-2-12-gsn-assurance-case-cluster-deep-read.md
formalization_status: candidate-only
truth_boundary: not reviewed knowledge, not architecture decision, not action basis
write_scope: outputs/review only
---

# v0.2.13 Revised Candidate Patch: Make Action Support Visible

## 说人话结论

v0.2.13 继续保留，但按 Pro 反馈降级成更窄的 `revise_candidate`。

这次修订把重点从一个名词化的对象：

```text
Structured Action-Basis Envelope
```

收回到一个动作要求：

```text
真正要拿去行动时，把 support 摊开。
```

核心句仍然成立，但要更严格：

```text
Evidence is not enough; show the non-circular warrant.
```

这不是新层，不是新模板，不是新系统，也不是 assurance-case adoption。

## Current Candidate State

Mainline remains:

```text
Fusion Architecture v0.2 Draft
```

Candidate workflow version:

```text
VAKS external-source borrowing workflow v0.2.13 revised candidate
```

Disposition:

```text
status: revise_candidate
mainline_promotion: no
candidate_pattern_file: no
next_required_test: one real VAKS action-basis / important promotion / risk-sensitive answer
```

## Revised Rule

For action_basis and significant promotion/decision use, when an answer or claim will be relied on for action or risk-sensitive judgment, make the support visible:

```text
state the action-facing claim,
the point-specific anchored evidence,
the non-circular warrant connecting that evidence to the claim,
the relevant scope/assumptions,
the known challenges or gaps,
and the current residual review status.
```

Companion guardrail:

```text
Diagrams, notation, source counts, tool counts, vendor pages, and confidence labels
do not increase support, independence, or action readiness.
```

This is the candidate rule. It should not be promoted to mainline without a real VAKS action-basis trial.

## Minimal Core

The revised core is intentionally smaller than the previous draft.

Required only when triggered:

```yaml
action_facing_claim: what claim will be relied on
point_specific_anchored_evidence: evidence items with source/text anchors, not bare URLs
non_circular_warrant: why this evidence supports this claim
scope_assumptions: where the claim applies and what premises it depends on
known_challenges_or_gaps: counterpressure, omissions, conflicts, or missing support
current_residual_review_status: the remaining review/risk disposition in plain language
```

Not core fields:

```yaml
source_family_context: guardrail note only when repetition could be mistaken for independent support
excluded_non_support: lint / reviewer note only when tool/vendor/diagram/source-count material appears
review_status_state_machine: not introduced
```

## Narrowed Trigger Rules

Trigger the rule only when the claim is action-facing or promotion-facing:

- action_basis use.
- significant promotion toward reviewed knowledge.
- significant project decision.
- risk-sensitive answer that may guide action.
- explicit "is this enough?" question, only when the "enough" refers to action, promotion, decision, or risk-sensitive use.
- strong relation judgment, only when it is being promoted or used as an action-critical relation.

Do not trigger it for:

- ordinary light capture.
- ordinary source routing.
- ordinary search.
- simple summaries.
- tool-directory triage.
- candidate-only scratch notes.
- reviewer questions that are not action-facing, promotion-facing, decision-facing, or risk-sensitive.

## Warrant Quality Rule

The failure condition is now:

```text
missing_or_non_explanatory_warrant
```

This includes:

```text
blank warrant
circular warrant
scope jump
source-family repetition treated as independent support
vendor claim treated as support
diagram clarity treated as support
tool count treated as adoption evidence
confidence label treated as truth confidence
```

Examples:

```text
Bad: This evidence supports the claim because it supports the claim.
Bad: Three pages in the same GSN source family say similar things, so support is stronger.
Bad: A vendor tool supports this feature, so the architectural claim is validated.
Bad: The diagram is clean, so the conclusion is action-ready.
```

Good enough:

```text
The evidence supports this action-facing claim because it describes the same
mechanism under the same scope, the source anchor directly supports the specific
point being used, and the known challenges do not break that scoped claim.
```

If the non-circular warrant cannot be written, the claim must stay:

```text
candidate-only | insufficient | blocked for action use
```

## Source-Family And Non-Support Guardrails

These are guardrails, not mandatory fields.

Use a source-family note only when repetition might be mistaken for independent support:

```text
GSN overview + GSN nutshell + GSN pattern catalogue
= source-family clarification
!= three independent supports
```

Use an excluded-non-support note only when non-support material is present:

```text
tool page = discovery
vendor claim = product claim
diagram = communication aid
confidence notation = source/notation claim
source count = not support count
```

## Relationship To v0.2.12

v0.2.12 still provides the core borrowing spine:

```text
Raw Source
-> Source Routing Overlay
-> Candidate Pattern Bank
-> Project Borrowing Ledger
-> Evidence-Aware Review / EtD-lite
-> Decision / Action Basis
```

v0.2.13 revised does not add a new stage.

It tightens the final action-facing use:

```text
If you will rely on it for action, show the anchored evidence and the non-circular warrant.
```

Preserved boundaries:

```text
URL/source = provenance
raw text = source text
AI summary = candidate comprehension
candidate point = review unit
retrieval/context pack = activation/context preparation
feedback = usefulness/scope-fit pressure, not truth mutation
promotion/action basis = evidence-aware review only
```

## Candidate Pattern Decision

Do not create a candidate pattern file now.

Current disposition:

```text
qualified_for_discussion: yes
create_pattern_file_now: no
reason: more like a tiny terminal rule than an independent reusable pattern
```

Avoid:

```text
gsn-lite
sacm-lite
assurance-case-system-for-vaks
structured-action-basis-envelope as a new schema object
```

## Testing Status

Current tests show:

```text
boundary / face-validity trial: passed after revision
real VAKS action-basis example: not yet tested
ordinary intake unaffected: intended, not proven
```

Do not claim:

```text
accepted_candidate
validated
ready_for_mainline
ordinary intake proven unaffected
```

## Promotion Boundary

Before any mainline promotion, require:

- one real VAKS action-basis / important promotion / risk-sensitive answer trial.
- evidence that the rule catches missing or non-explanatory warrant better than v0.2.12.
- evidence that ordinary source intake/routing is not pulled into this rule.
- second-pass review of the exact sentence-level wording.

Likely future mainline shape, if accepted later:

```text
one minimal rule
one companion guardrail
no new schema object
no mandatory template
no GSN/SACM/tool adoption
```

## Files / Claims That Must Stay outputs/review

Keep candidate-only:

- GSN / SACM / CAE deep-read and source-family grouping.
- tool ecosystem notes and discovery-only claims.
- SCSC page / fetched PDF version caveat.
- original v0.2.13 patch and manual trial.
- this revised candidate patch.
- any statement that this has passed only boundary / face-validity testing.
- candidate pattern discussion.
- any claim about ordinary intake not being proven yet.
