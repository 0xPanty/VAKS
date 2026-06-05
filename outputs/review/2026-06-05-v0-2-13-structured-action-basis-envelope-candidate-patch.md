---
type: candidate_patch
status: candidate
created_at: 2026-06-05
project: verified-action-knowledge-system
version: v0.2.13
supersedes_candidate: v0.2.12
patch_id: v0-2-13-structured-action-basis-envelope
source_basis:
  - outputs/review/2026-06-05-v0-2-12-gsn-assurance-case-cluster-deep-read.md
  - outputs/review/2026-06-05-v0-2-12-next-window-memory-alignment.md
  - outputs/review/2026-06-05-cross-project-borrowing-v0-2-12-delta-test.md
formalization_status: candidate-only
truth_boundary: not reviewed knowledge, not architecture decision, not action basis
write_scope: outputs/review only
---

# v0.2.13 Candidate Patch: Structured Action-Basis Envelope

## 说人话升级说明

v0.2.13 不把 VAKS 改成 assurance-case 系统。

它只做一个小升级：当 VAKS 要把某个判断拿去支撑重要 action / decision / promotion 时，不能只说“这里有证据”。它还要把证据怎么支撑 claim 说清楚。

也就是从：

```text
claim + evidence list
```

升级为：

```text
claim
-> evidence anchors
-> argument / warrant
-> context / scope / assumptions
-> challenges / known gaps
-> residual risk / review status
```

这借鉴的是 GSN / CAE / assurance case 的最小组织方法，不借完整 GSN 图形标准，不借完整 SACM 模型，不借工具链。

## Version Bump

Current candidate workflow version:

```text
VAKS external-source borrowing workflow v0.2.13 candidate
```

v0.2.12 core stayed:

```text
Raw Source
-> Source Routing Overlay
-> Candidate Pattern Bank
-> Project Borrowing Ledger
-> Evidence-Aware Review / EtD-lite
-> Decision / Action Basis
```

v0.2.13 adds a lazy internal envelope inside the final review/action area:

```text
Decision / Action Basis
-> Structured Action-Basis Envelope, only when triggered
```

This is not a new truth layer and not a new ordinary intake step.

## Patch Rule

For promotion, significant decisions, action-basis use, risk-sensitive answers, strong reviewed relations, or an explicit "is this enough?" question, VAKS should expose a lightweight structured action-basis envelope.

Minimum envelope:

```yaml
action_or_decision_claim: the claim being used for action
source_family_context: source family grouping and duplicate-support warning
evidence_items_with_anchors: source-backed evidence items, not bare URLs
argument_or_warrant: why these evidence items support this claim
context_scope_assumptions: where the claim applies and what premises it depends on
challenges_counterevidence_known_gaps: known pressure against the claim
applicability_window: time/version/project/environment limits when relevant
residual_risk: remaining risk after review
review_status: candidate | review_ready | reviewed | blocked | insufficient
excluded_non_support: tool pages, vendor claims, diagrams, source counts, confidence labels, or background citations that do not support the specific point
```

Short version:

```text
Evidence is not enough; show the warrant.
```

## Trigger Rules

Use the envelope when one of these is true:

- a candidate point is being promoted toward reviewed knowledge.
- a decision or action basis depends on the point.
- the user asks whether evidence is enough.
- the answer is risk-sensitive or high-impact.
- a strong reviewed relation is proposed.
- a conclusion depends on contested, stale, version-bound, or scope-bound material.

Do not use the envelope for ordinary light capture, ordinary search, routine source routing, simple summaries, tool-directory triage, or candidate-only scratch notes.

## Warrant Rule

The `argument_or_warrant` field must not merely restate the claim.

Good enough:

```text
The evidence supports the claim because it directly describes the same mechanism,
under the same scope, and no known challenge in this packet breaks that scope.
```

Not good enough:

```text
The evidence supports the claim because it supports the claim.
```

If the warrant cannot be written, the envelope should degrade the result:

```text
status: blocked | insufficient | candidate-only
reason: missing_argument_or_warrant
```

## Source-Family Rule

Multiple pages from the same source family may clarify a mechanism, but they do not automatically count as independent support.

For this patch:

```text
GSN overview + GSN nutshell + GSN pattern catalogue
= source_family support
!= three independent truth supports
```

The same applies to tool pages and vendor pages. Tool count is not evidence count.

## Anti-Overreach Guardrails

The envelope must not imply any of the following:

- GSN diagrams are required.
- SACM modeling is required.
- VAKS should adopt assurance-case tooling.
- source count creates truth confidence.
- tool count creates adoption evidence.
- vendor claim creates conformance validation.
- confidence notation creates truth confidence.
- a complete-looking envelope creates action readiness.

Correct reading:

```text
structured envelope = easier to inspect support, challenge, scope, and residual risk
```

Wrong reading:

```text
structured envelope = true / safe / ready / approved
```

## Relationship To Existing v0.2.12 Boundaries

This patch preserves:

```text
URL/source = provenance
raw text = source text
summary = candidate comprehension
candidate point = review unit
retrieval/context pack = activation/context preparation
feedback = usefulness/scope-fit pressure, not truth mutation
promotion/action basis = evidence-aware review only
```

v0.2.13 only tightens the last step:

```text
action use requires explicit evidence-to-claim warrant when the risk justifies it
```

## Candidate Pattern Decision

Candidate pattern qualification:

```text
qualified_for_discussion: yes
create_pattern_file_now: no
suggested_slug: structured-action-basis-envelope
```

Reason:

- GSN supplies claim / evidence / context / strategy organization.
- SACM supplies vocabulary pressure for separating claim, argument, evidence, artifact, and assessment.
- CAE / assurance-case materials support the action-before-trust framing.
- tool pages are discovery-only and are not counted as pattern support.

Do not create `gsn-lite`, `sacm-lite`, or `assurance-case-system-for-vaks`.

## Promotion Boundary

This file is a candidate patch, not a mainline change.

Before promotion, it needs:

- Pro review or equivalent second-pass review.
- at least one real VAKS action-basis example.
- confirmation that the envelope does not burden ordinary intake.
- confirmation that it catches missing-warrant cases better than v0.2.12.

## Minimal Mainline Patch Candidate, Later

If promoted later, the likely mainline rule should be only this:

```text
For action_basis and significant promotion/decision use, include a lightweight
claim-argument-evidence-context envelope when the answer depends on reviewed support:
the action-facing claim, source-anchored evidence, the warrant connecting evidence
to claim, scope/context/assumptions, known challenges or gaps, and residual
review status. GSN/SACM diagrams and assurance-case tools are optional communication
aids, not required schema or truth evidence.
```

Companion guardrail:

```text
GSN/SACM/CAE notation, diagrams, source count, tool count, vendor pages,
confidence labels, and catalogue membership do not create truth confidence,
conformance validation, or action readiness.
```
