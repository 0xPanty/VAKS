---
type: validation-report
status: completed
created: 2026-05-30
project: verified-action-knowledge-system
scope:
  - v0-3
  - evidence-discipline
  - ten-alpha
  - pro-review
tags:
  - evidence-packet
  - warrant
  - challenge-taxonomy
  - context-pack-trace
  - review-due
---

# v0.3 Ten Alpha Validation

## Purpose

This report validates whether the 10 adopted v0.3 evidence-discipline alpha points have been actually landed, not merely discussed.

The validation standard is:

```text
each alpha must have:
1. a clear improvement over v0.2
2. an explicit location in docs or templates
3. a trigger boundary
4. a truth-authority boundary
5. at least one local trial or contract check
```

This is not a runtime implementation report. The current vault is still a Markdown-first architecture vault.

## Summary Judgment

```text
All 10 alpha points are landed at architecture / schema / template level.
They remain lazy gates.
They do not expand Truth Core.
They are ready for Pro review as v0.3 Evidence and Review Discipline.
```

Current strongest proof:

```text
Evidence Packet micro-trial:
outputs/review/2026-05-30-evidence-packet-micro-trial.md

RKA source-record trial:
outputs/review/2026-05-30-rka-evidence-packet-source-record-trial.md

RKA source-code anchor review:
outputs/review/2026-05-30-rka-source-code-anchor-review.md

Integrated 10-alpha local trial:
outputs/review/2026-05-30-v0-3-integrated-ten-alpha-trial.md
```

## Validation Matrix

### 1. Evidence Packet

Improvement over v0.2:

```text
Before: source provenance and review existed, but the handoff from source span to reviewed point could still be loose.
After: important review uses a smaller packet: point + source anchor + evidence item + grounds + warrant + challenge + scope + minimal revision.
```

Landed in:

```text
SCHEMA.md
REVIEW_QUEUE.md
templates/review-candidate.md
FUSION_ARCHITECTURE_V0_2_DRAFT.md
ARCHITECTURE_PRINCIPLES.md
```

Trigger:

```text
promotion
decision
strong reviewed relation
context pack / action basis
risk-sensitive answer
stale or contested point
explicit reviewer challenge
```

Boundary:

```text
Evidence Packet is review input.
It does not create truth, confidence, reviewed relation, or action readiness by itself.
```

Validation result:

```text
PASS
```

Why:

```text
Micro-trial showed the packet prevented URL-only provenance from being treated as support.
RKA source-record trial showed source records without code anchors get a confidence cap.
RKA source-code review upgraded specific points to code-anchor support without adopting runtime.
```

### 2. Warrant Separation

Improvement over v0.2:

```text
Before: evidence-aware review could still blur "we have a source" with "the source actually supports this point."
After: grounds and warrant are separated.
```

Human question:

```text
grounds = what evidence do we have?
warrant = why does that evidence support or weaken this point?
```

Landed in:

```text
SCHEMA.md
REVIEW_QUEUE.md
templates/review-candidate.md
FUSION_ARCHITECTURE_V0_2_DRAFT.md
ARCHITECTURE_PRINCIPLES.md
```

Trigger:

```text
high-impact claim
architecture decision
pattern adoption
risk-sensitive action basis
strong reviewed relation
```

Boundary:

```text
Warrant is reviewer reasoning, not automatic entailment.
It does not make the source true.
It does not replace evidence support check.
```

Validation result:

```text
PASS
```

Why:

```text
Integrated trial uses RKA code as grounds, then states the warrant separately:
RKA rejects outcome recording without user resolution, therefore our decision_outcome must require recommendation + user_choice / explicit override.
```

### 3. Challenge Taxonomy

Improvement over v0.2:

```text
Before: challenge was mostly "support / contradict / risk."
After: review can say what kind of problem exists.
```

Landed challenge kinds:

```text
rebuttal
undercut
scope_limit
source_hygiene
stale_assumption
action_failure
```

Landed in:

```text
SCHEMA.md
REVIEW_QUEUE.md
templates/review-candidate.md
FUSION_ARCHITECTURE_V0_2_DRAFT.md
```

Trigger:

```text
point collision
evidence packet review
review queue item
feedback event
context pack contradiction
action failure
```

Boundary:

```text
challenge_kind names the problem.
It does not automatically reject, supersede, or edit a point.
```

Validation result:

```text
PASS
```

Why:

```text
Integrated trial exercises all six challenge kinds:
rebuttal, undercut, scope_limit, source_hygiene, stale_assumption, action_failure.
```

### 4. Minimal Revision Needed

Improvement over v0.2:

```text
Before: point collision could surface conflict, but the next review move was less standardized.
After: reviewers ask for the smallest safe revision instead of automatic conflict resolution.
```

Allowed values:

```text
keep
refine_scope
mark_contested
mark_stale
supersede
reject
```

Landed in:

```text
SCHEMA.md
REVIEW_QUEUE.md
templates/review-candidate.md
FUSION_ARCHITECTURE_V0_2_DRAFT.md
```

Trigger:

```text
evidence packet review
point collision
decision superseding
source hygiene problem
action failure
```

Boundary:

```text
minimal_revision_needed is a recommendation.
It does not edit reviewed knowledge automatically.
```

Validation result:

```text
PASS
```

Why:

```text
RKA source-code review found one small revision:
refine_scope decision_outcome by requiring user_choice / explicit override before final outcome.
It did not trigger a broad redesign.
```

### 5. Source Anchor Mini-Profile

Improvement over v0.2:

```text
Before: source provenance told where material came from.
After: source anchor tells where the specific evidence lives.
```

Landed shape:

```text
source_anchor:
  url_or_path:
  exact_quote:
  prefix:
  suffix:
  captured_at:

heavy optional:
  position:
  content_hash:
  archived_url:
  checked_latest_at:
  source_changed:
```

Landed in:

```text
SCHEMA.md
SOURCE_INTAKE.md
REVIEW_QUEUE.md
templates/review-candidate.md
FUSION_ARCHITECTURE_V0_2_DRAFT.md
```

Trigger:

```text
medium / heavy source
repo source review
paper source review
promotion
decision
action basis
high-impact point
```

Boundary:

```text
source anchor is provenance.
It is not support by itself.
```

Validation result:

```text
PASS
```

Why:

```text
RKA source-code review uses exact GitHub commit URLs and line anchors.
The trial treats code anchors as stronger evidence than source-record summary, but still not automatic truth.
```

### 6. Evidence Granularity / Escalation

Improvement over v0.2:

```text
Before: a source summary and a full source could be accidentally used with the same force.
After: evidence has a granularity level that caps how far it can be used.
```

Landed values:

```text
metadata_only
abstract_or_summary
excerpt_or_passage
table_or_code_anchor
full_source_reviewed
```

Landed in:

```text
SCHEMA.md
SOURCE_INTAKE.md
REVIEW_QUEUE.md
templates/review-candidate.md
FUSION_ARCHITECTURE_V0_2_DRAFT.md
```

Trigger:

```text
any evidence item in an evidence packet
promotion attempt
action basis
strong relation
confidence cap check
```

Boundary:

```text
low granularity can support triage or candidate review.
It cannot support high-impact promotion or action readiness without escalation.
```

Validation result:

```text
PASS
```

Why:

```text
RKA source-record trial correctly blocked high-confidence code-level proof because it lacked exact code spans.
RKA source-code review escalated the same claim to table_or_code_anchor evidence.
```

### 7. Omission Check

Improvement over v0.2:

```text
Before: digest risk focused on whether the summary was wrong.
After: digest review also checks what may have been omitted: risks, scope limits, facts, and need for full source read.
```

Landed shape:

```text
omission_check:
  missing_risks:
  missing_scope_limits:
  possible_omissions:
  omission_questions:
  needs_full_source_read:
```

Landed in:

```text
SCHEMA.md
REVIEW_QUEUE.md
templates/review-candidate.md
FUSION_ARCHITECTURE_V0_2_DRAFT.md
```

Trigger:

```text
heavy source digest
important repo
long paper
high-impact decision
reviewer request
compiled wiki / generated digest
```

Boundary:

```text
omission_check creates review pressure.
It does not prove the omitted fact exists.
```

Validation result:

```text
PASS
```

Why:

```text
RKA source-record trial caught a real omission: source record listed reviewed files but lacked exact code spans.
Integrated trial records missing runtime evidence as an omission without requiring runtime adoption.
```

### 8. Context Pack Trace

Improvement over v0.2:

```text
Before: context pack could explain coverage, but not always why material was selected or ignored.
After: context_pack_trace records used, ignored, reasons, activation roles, contradictions, and risk flags.
```

Landed shape:

```text
context_pack_trace:
  used_sources:
  ignored_sources:
  ignored_reason:
  activation_role:
  unresolved_contradictions:
  risk_flags:
```

Landed in:

```text
SCHEMA.md
DEV_CONTEXT.md
templates/dev-context-pack.md
FUSION_ARCHITECTURE_V0_2_DRAFT.md
```

Trigger:

```text
context pack
action basis
dev context pack
Pro review package
important answer audit
```

Boundary:

```text
context_pack_trace is trace / use-ledger surface.
It is not truth.
retrieved or selected does not mean believed.
ignored does not mean false.
```

Validation result:

```text
PASS
```

Why:

```text
Integrated trial traces used RKA code anchors and ignored RKA runtime/dashboard material.
This makes the "borrow design, not runtime" boundary auditable.
```

### 9. Agent Memory Quarantine

Improvement over v0.2:

```text
Before: feedback boundary existed, but future agent memory writes needed a sharper quarantine rule.
After: agent memory writes are candidate-only or feedback-event-only by default.
```

Landed shape:

```text
agent_memory_write:
  status: candidate_only
  source:
  scope:
  review_due:
  allowed_effect:
    - activation
    - usefulness
    - scope_fit
  forbidden_effect:
    - truth_confidence
    - reviewed_relation
    - promotion
```

Landed in:

```text
FUSION_ARCHITECTURE_V0_2_DRAFT.md
ARCHITECTURE_PRINCIPLES.md
FEEDBACK.md
templates/maintenance-manifest.md
```

Trigger:

```text
future agent / MCP / Codex / Claude Code memory write
feedback import
conversation-derived memory
action result memory
```

Boundary:

```text
agent memory cannot write reviewed truth.
agent memory cannot change confidence.
agent memory cannot create reviewed relations.
agent memory cannot promote knowledge.
```

Validation result:

```text
PASS
```

Why:

```text
Contract simulation already confirmed agent memory cannot change confidence.
Integrated trial includes an agent_memory_write quarantine case.
```

### 10. Review Due Triggers

Improvement over v0.2:

```text
Before: review_due existed, but trigger families were spread across feedback, staleness, and decision superseding.
After: review_due_when is explicit and can be attached to evidence packets and review results.
```

Landed trigger families:

```text
new_primary_source
contradiction
correction_or_retraction
source_version_change
dependency_release_change
action_failure
missed_feedback
stale_assumption
```

Landed in:

```text
SCHEMA.md
REVIEW_QUEUE.md
FEEDBACK.md
FUSION_ARCHITECTURE_V0_2_DRAFT.md
templates/review-candidate.md
templates/dev-context-pack.md
templates/feedback-event.md
```

Trigger:

```text
new source
explicit correction
decision superseded
action failure
source changed
validity window mismatch
feedback exposes missing evidence
```

Boundary:

```text
review_due is pressure to recheck.
It is not proof that the old claim is false.
```

Validation result:

```text
PASS
```

Why:

```text
RKA code confirms superseding and contradiction create review pressure.
Feedback rules confirm action failure and explicit correction create review_due without truth mutation.
```

## Cross-Alpha Contract Checks

These are the core invariants that must hold when the 10 alpha points run together:

```text
source_anchor without evidence item cannot support promotion
evidence_packet without warrant cannot support high-impact action basis
metadata_only or abstract_or_summary cannot make high-impact action ready
challenge_kind names pressure but does not auto-reject
minimal_revision_needed recommends but does not edit
omission_check can demand full source read without proving the missing fact
context_pack_trace can explain selection without becoming trust
agent_memory_write can create candidate / feedback pressure only
review_due does not equal invalid
decision_outcome requires recommendation + user choice / explicit override
```

Conceptually passed; schema conformance and evidence-support pressure tests were patched after Pro review.

## Pro Review Position

Suggested Pro-facing position:

```text
v0.3 does not add a new module.
It adds a lightweight evidence discipline across existing layers.

The 10 alpha points are not a feature roadmap.
They are lazy review gates and audit fields.

Evidence Packet is the center.
Warrant, challenge, minimal revision, source anchors, evidence granularity, omission check, context trace, agent quarantine, and review_due triggers are supporting discipline around it.
```

## Remaining Risks

```text
Risk 1: overusing Evidence Packet on ordinary capture.
Mitigation: docs repeatedly state ordinary capture and ordinary query stay light.

Risk 2: treating context trace or graph activation as trust.
Mitigation: context_pack_trace is explicitly trace/use-ledger surface, not truth.

Risk 3: letting review_due imply invalidity.
Mitigation: stale/review_due is review pressure; valid_until/supersession define applicability boundaries.

Risk 4: turning outcome calibration into truth mutation.
Mitigation: decision_outcome affects future recommendation, risk calibration, scope fit, and option framing only.
```

## Final Result

```text
The 10 alpha points are complete enough for v0.3 architecture review.
They should still be kept as review discipline, not expanded into a runtime platform.
```
