---
type: pattern
status: draft
created: 2026-05-27
updated: 2026-05-27
source_libraries:
  - willynikes2/knowledge-base-server
related_concepts:
  - "[[FEEDBACK]]"
  - "[[MEMORY_TIER]]"
  - "[[DEV_CONTEXT]]"
related_projects:
  - verified-action-knowledge-system
adoption_status: adapt
verification_status: single-source
evidence_level: secondary
evidence_count: 1
confidence: medium
negative_evidence:
  - "Captured sessions can be noisy and must not automatically become lessons or decisions."
extension_points:
  - feedback-event
  - query-run
  - project-closeout
  - risk-layer
last_verified: 2026-05-27
next_review: 2026-06-03
epistemic_type: take
gaps:
  - "Needs real feedback-event/query-run trial in this vault."
evidence_timeline:
  - date: 2026-05-27
    source: "[[2026-05-27-knowledge-base-server-source]]"
    observation: "The repo provides kb_capture_session and kb_capture_fix tools for saving operational learning."
    effect: supports
    confidence: medium
relations:
  - target: "[[FEEDBACK]]"
    type: refines
    strength: 5
    confidence: medium
    evidence:
      - "[[2026-05-27-knowledge-base-server-source]]"
    rationale: "Session/fix capture can feed feedback events, missing-point records, and operational lessons."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[DEV_CONTEXT]]"
    type: refines
    strength: 4
    confidence: medium
    evidence:
      - "[[2026-05-27-knowledge-base-server-source]]"
    rationale: "Closeout capture can decide what remains hot, warms, cools, or becomes Risk."
    created: 2026-05-27
    last_verified: 2026-05-27
tags:
  - pattern
  - feedback
  - operational-memory
  - session-capture
---

# Operational Session Capture Loop

## AI-readable preamble

Capture what happened during work so the vault learns from actual operations.

Session capture creates candidates and feedback. It does not create verified truth by itself.

## One-line definition

Record significant sessions and fixes as structured operational memory.

## Problem solved

The most valuable knowledge often lives in:

```text
commands that failed
commands that worked
root causes
fixes
mistakes
scope corrections
user preferences
hidden project constraints
```

If this stays only in chat or terminal scrollback, the next agent repeats the same work.

## Source evidence

`willynikes2/knowledge-base-server` exposes:

```text
kb_capture_session:
  records goal, failed commands, working commands, root causes, fixes, lessons

kb_capture_fix:
  records symptom, cause, resolution, commands, project
```

Relevant implementation surfaces:

```text
src/tools.js
src/capture/terminal.js
docs/workflow/SELF-LEARNING.md
```

## Applicable scenarios

- End of a dev context pack.
- After a failed or successful implementation.
- After a user correction.
- After discovering a missing point.
- After a safety/risk issue.
- After a repeated bug fix.

## Not applicable

- Treating every session note as a lesson.
- Auto-promoting fixes into runbooks.
- Auto-changing truth confidence.
- Replacing human review of decisions.

## Minimum implementation

At project closeout, write or queue:

```yaml
record_type: session-capture
project:
scope_key:
goal:
commands_failed:
commands_worked:
root_causes:
fixes:
lessons_candidate:
risk_candidate:
missing_point_candidate:
writeback_targets:
review_needed:
```

## Fusion suggestion

Use with `DEV_CONTEXT.md` exit:

```text
What changed?
What should stay hot?
What cools to warm?
What returns to cold?
What new risk or anti-pattern appeared?
```

Use with `FEEDBACK.md`:

```text
session capture can generate feedback-event and query-run evidence
```

Use with `MEMORY_TIER.md`:

```text
repeatedly reused fixes warm up
one-off session logs cool down
new active blockers can become scoped hot
```

## Boundary

Operational capture is the memory of work.

Review decides what becomes knowledge.
