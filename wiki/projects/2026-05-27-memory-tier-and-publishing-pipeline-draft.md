---
type: implementation-note
status: draft
created: 2026-05-27
updated: 2026-05-27
project: verified-action-knowledge-system
related_patterns:
  - "[[source-to-publish-content-pipeline]]"
  - "[[published-performance-feedback-loop]]"
  - "[[conversation-derived-feedback-routing]]"
related_files:
  - "[[FEEDBACK]]"
  - "[[IMPLEMENTATION_BLUEPRINT]]"
verification_status: draft
evidence_level: synthetic
confidence: medium
last_verified: 2026-05-27
next_review: 2026-06-03
tags:
  - draft-direction
  - memory-tier
  - publishing-pipeline
  - activation
  - output
---

# Memory Tier + Publishing Pipeline Draft Direction

## AI-readable preamble

This is a draft direction, not an implemented spec.

Memory tiering and the publishing pipeline should be designed together, but implemented as separate modules.

Memory tier controls activation priority. Publishing pipeline controls output progress.

## Core Judgment

Do not merge the two concepts into one system.

Use this rule:

```text
memory_tier:
  controls what should be activated first

workflow_stage:
  controls where an item is in a workflow
```

They are related, but not the same.

## Module 1: Memory Tier

Purpose:

```text
Decide what should be surfaced first for the user or agent.
```

It answers:

```text
What is currently active?
What should be shown on the dashboard?
What should an agent read first?
What can stay in the background unless queried?
```

Draft fields:

```yaml
memory_tier: hot | warm | cold
activation_status: active | dormant | archived
last_activated:
activation_reason:
next_action:
scope_key:
```

Meaning:

```text
hot:
  current work, active route, active project, current draft, current trial

warm:
  reviewed patterns, common decisions, stable point clusters, frequently reused context

cold:
  raw sources, old query runs, historical feedback, archived references
```

Hard boundary:

```text
hot does not mean true
warm does not mean verified
cold does not mean useless
```

Temperature is only activation priority.

It must stay separate from:

```text
truth confidence
verification_status
source reliability
decision authority
```

## Module 2: Publishing Pipeline

Purpose:

```text
Move useful knowledge from idea to publishable output.
```

It answers:

```text
What can this idea become?
What stage is this output in?
What is the next push needed?
What feedback came back after publishing?
```

Draft workflow:

```text
capture
-> triage
-> theme
-> draft
-> publish
-> feedback
```

Draft fields:

```yaml
workflow_lane: knowledge | publishing | action
workflow_stage: captured | triaged | themed | drafted | published | feedback
audience:
claim:
structure:
source_materials: []
publish_channel:
next_action:
feedback_path:
```

Meaning:

```text
captured:
  idea/link/excerpt enters inbox

triaged:
  decide whether it becomes knowledge, project, draft, or archive

themed:
  connect it to topics, point clusters, claims, and questions

drafted:
  turn it into a publishable artifact with audience, claim, structure, materials, channel, and next action

published:
  shipped to an external channel or product surface

feedback:
  comments, objections, metrics, new questions, and missing points return to the vault
```

## How They Connect

A note can have both:

```yaml
workflow_stage: drafted
memory_tier: hot
```

This means:

```text
It is currently a draft and should be activated first.
```

Another note can be:

```yaml
workflow_stage: published
memory_tier: cold
```

This means:

```text
The artifact is done and archived unless feedback reactivates it.
```

Feedback can reheat old material:

```text
published artifact receives strong comment / contradiction / missing question
-> create feedback-event
-> create missing-point or route candidate
-> set related item memory_tier: hot or warm
```

## Recommended Implementation Order

Next window should not build a UI first.

Recommended order:

```text
1. MEMORY_TIER.md
   Define hot/warm/cold and the activation rules.

2. PUBLISHING_PIPELINE.md
   Define capture -> triage -> theme -> draft -> publish -> feedback.

3. templates/publish-draft.md
   Add audience, claim, structure, source materials, channel, next action, feedback path.

4. SCHEMA.md update
   Add optional fields:
     memory_tier
     activation_status
     workflow_lane
     workflow_stage
     next_action

5. README / handoff update
   Explain that memory tier is an activation layer and publishing pipeline is an output module.
```

## What Not To Do

Do not create top-level folders first:

```text
01-Hot/
02-Warm/
03-Cold/
```

Reason:

```text
Manual file moving will become busywork.
Temperature should be metadata and dashboard logic first.
Folders can come later only if they clearly reduce friction.
```

Do not let publishing workflow own truth:

```text
draft-friendly does not mean verified
popular post does not mean true
published content does not become a claim automatically
```

Published feedback can create:

```text
feedback-event
missing-point candidate
wrong-scope signal
contradiction warning
new source to ingest
```

It cannot directly change:

```text
truth confidence
verification_status
source reliability
decision outcome
```

## Stop Point

This file is a direction-setting draft.

No schema implementation has happened yet.

## Not Yet Done

These items are intentionally not implemented in this draft:

```text
MEMORY_TIER.md
PUBLISHING_PIPELINE.md
templates/publish-draft.md
SCHEMA.md optional fields for memory_tier / workflow_stage
hot / warm / cold dashboard
real publishing workflow trial
real query-run / feedback-event trial
```

Do not treat this draft as an active workflow.

Next concrete action:

```text
Create MEMORY_TIER.md, then PUBLISHING_PIPELINE.md.
```
