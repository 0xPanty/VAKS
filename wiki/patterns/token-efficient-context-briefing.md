---
type: pattern
status: draft
created: 2026-05-27
updated: 2026-05-27
source_libraries:
  - willynikes2/knowledge-base-server
related_concepts:
  - "[[MEMORY_TIER]]"
  - "[[DEV_CONTEXT]]"
  - "[[context-pack-evidence-envelope]]"
  - "[[agent-context-pack-budget-guardrails]]"
related_projects:
  - verified-action-knowledge-system
adoption_status: adapt
verification_status: single-source
evidence_level: secondary
evidence_count: 1
confidence: medium
negative_evidence:
  - "The source repo's context briefing is retrieval-oriented and does not by itself enforce evidence review."
extension_points:
  - memory-tier
  - dev-context
  - context-pack
  - query-run
last_verified: 2026-05-27
next_review: 2026-06-03
epistemic_type: take
gaps:
  - "Needs real query-run trial inside this vault."
evidence_timeline:
  - date: 2026-05-27
    source: "[[2026-05-27-knowledge-base-server-source]]"
    observation: "`kb_context` returns summaries and metadata before `kb_read` loads full content."
    effect: supports
    confidence: medium
relations:
  - target: "[[DEV_CONTEXT]]"
    type: refines
    strength: 5
    confidence: medium
    evidence:
      - "[[2026-05-27-knowledge-base-server-source]]"
    rationale: "A dev context pack can be built from a low-token briefing before selecting full Core/Support files."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[MEMORY_TIER]]"
    type: refines
    strength: 5
    confidence: medium
    evidence:
      - "[[2026-05-27-knowledge-base-server-source]]"
    rationale: "Memory tiers should influence what appears in the briefing and what gets full-read next."
    created: 2026-05-27
    last_verified: 2026-05-27
tags:
  - pattern
  - context-briefing
  - token-budget
  - memory-tier
---

# Token-Efficient Context Briefing

## AI-readable preamble

Before reading full notes, produce a compact briefing with summaries, metadata, tiers, and source pointers.

The briefing decides what to open next. It does not decide truth.

## One-line definition

Use a low-token context briefing before full document reads.

## Problem solved

Large vaults make agents waste context:

```text
too many full documents loaded too early
raw captures mixed with decisions
supporting notes read before Core is clear
old cold material pollutes current work
```

A context briefing gives the agent a map before it opens the files.

## Source evidence

`willynikes2/knowledge-base-server` implements this through `kb_context`.

The repo describes:

```text
kb_context:
  returns summaries and metadata without full content
  should be used before kb_read
  saves tokens compared with reading everything
```

Relevant code surfaces:

```text
src/tools.js:
  kb_context tool description and handler

src/classify/summarizer.js:
  creates summaries optimized for deciding whether an agent needs the full note

src/db.js:
  vault_files stores summary and key_topics
```

## Applicable scenarios

- Starting a dev context pack.
- Answering a broad question.
- Choosing which source to open for evidence.
- Keeping Core small.
- Letting Support remain expandable.
- Showing why something was retrieved.

## Not applicable

- Replacing source review.
- Deciding truth confidence.
- Promoting a candidate point.
- Proving a relation.
- Approving an action decision.

## Minimum implementation

For a query or task, return:

```yaml
query:
scope_key:
briefing:
  - file:
    title:
    note_type:
    memory_tier:
    activation_reason:
    summary:
    key_topics:
    source_pointer:
    why_suggested:
    suggested_layer: core_candidate | support_candidate | risk_candidate | cold_reference
```

Then:

```text
open Core candidates first
open Support only by need
open Risk before decisions/writes
open Cold References only for evidence/history/conflict
```

## Fusion suggestion

Use with `DEV_CONTEXT.md`:

```text
Discovery -> Context Briefing -> Context Pack -> Development Mode
```

Use with `FEEDBACK.md`:

```text
query-run should record which briefing items were opened, ignored, corrected, or missing
```

Use with `MEMORY_TIER.md`:

```text
hot appears early in briefing
warm appears when relevant
cold appears as evidence pointer unless explicitly needed
```

## Boundary

The briefing is a loading plan.

It is not:

```text
evidence
truth
review
decision authority
```

## Verification metrics

- Full reads per task decrease.
- Missing Core files decrease after feedback.
- Cold references stay traceable without default loading.
- The user can see why each file was suggested.
- Wrong-scope suggestions become feedback events.
