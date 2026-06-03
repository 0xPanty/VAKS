---
type: implementation-note
status: active
created: 2026-05-28
updated: 2026-06-03
project: verified-action-knowledge-system
scope:
  - source-intake
  - processing-tier
  - ux
  - provenance
related_files:
  - "[[SCHEMA]]"
  - "[[IMPLEMENTATION_BLUEPRINT]]"
  - "[[DEV_CONTEXT]]"
  - "[[MEMORY_TIER]]"
  - "[[REFERENCE_REVIEW_PROTOCOL]]"
  - "[[templates/video-source]]"
verification_status: active
evidence_level: synthetic
confidence: high
last_verified: 2026-05-28
next_review: 2026-06-04
tags:
  - source-intake
  - processing-tier
  - karpathy-simple
  - source-provenance
  - video-intake
---

# SOURCE_INTAKE.md v0.1

## AI-readable preamble

This file defines how incoming material should be handled without making everyday use heavy.

The rule is:

```text
Karpathy for normal intake.
Dusk-style dashboard for project use.
Verified-action strictness only for strong sources and action-bearing knowledge.
```

Do not run the full verified-action process on every note.

## 1. Core Judgment

Not all material deserves the same processing depth.

Use three levels:

```text
light:
  capture and keep findable.

medium:
  summarize and route.

heavy:
  preserve provenance, extract points, compare, review, and write durable patterns/decisions/risks.
```

The goal is to avoid both extremes:

```text
too light:
  AI summaries become untraceable and unreliable.

too heavy:
  every ordinary note becomes paperwork.
```

## 2. Processing Levels

### Light Processing

Use for:

```text
ordinary articles
interesting but unproven ideas
temporary references
small notes
low-impact links
material saved for possible future lookup
```

Minimum record:

```text
source link or file path
title
author/publisher if obvious
captured_at
why saved
short note or summary
current status
```

Do not require:

```text
confidence
evidence_level
relations
negative_evidence
formal review
pattern extraction
```

### Medium Processing

Use for:

```text
material likely to be reused
project background
useful references for a current question
docs that may enter a dev context
sources with clear but not architecture-changing ideas
```

Add:

```text
structured summary
tags/topics
source status
possible related files
candidate points
open questions
whether it belongs in a scope dashboard or dev context
```

Medium processing can feed:

```text
index
scope dashboard
context briefing
DEV_CONTEXT support or cold references
```

It still does not create truth.

### Heavy Processing

Use only for strong sources:

```text
papers
valuable repositories
official specs/docs
high-signal technical articles
important design discussions
materials that can validate or falsify our architecture
sources that affect project direction
risks, anti-patterns, failure reports
sources likely to become action basis
```

Add:

```text
full provenance
PROV-inspired trace when the source is medium/heavy
author / organization
published_at / updated_at
captured_at
version / commit / DOI / release
source_status: active | legacy | deprecated | unknown
timeline notes
files or sections reviewed
source/code anchors
candidate points
supports / contradicts / refines / risk_of / derived_from relations
what we adopt
what we reject
risk and anti-pattern extraction
fit with current branch
fit with whole architecture
```

Heavy processing can create:

```text
source record
architecture review
pattern
anti-pattern
decision
review queue item
maintenance manifest
decision outcome record
implementation-note
index update
handoff update
```

### Video Source Intake

Video is a source format, not a truth format.

Use `raw/videos/` and `templates/video-source.md` for useful Bilibili, YouTube, course, lecture, interview, podcast-with-video, demo, or walkthrough material.

The borrowed product/workflow ideas are narrow:

```text
batch links instead of one-by-one manual handling
platform-aware source identity
public subtitles first
local ASR when subtitles are missing
timestamped transcript / segment ledger
key-entity confidence
anti-omission extraction pass
user visual check for unclear names, URLs, commands, numbers, or UI text
delete downloaded media scratch after transcript by default
route useful ideas into candidate points before review
```

Default processing:

```text
light:
  save source card, metadata, why saved, one-sentence summary, and uncertainty.

medium:
  add transcript or subtitle, timestamp segments, key-entity confidence,
  anti-omission extraction, candidate points, borrow / do-not-borrow notes,
  and related VAKS layer.

heavy:
  only when the video affects architecture, decision, action basis,
  strong reviewed relation, important adoption, or explicit review.
```

Allowed direct conclusion:

```text
This video says X.
```

Not allowed without later review:

```text
X is true.
We should adopt X.
X supports a reviewed claim.
X changes confidence.
```

When upgrading video material to heavy, verify important entities and claims against stronger anchors such as official docs, project repositories, source code, release notes, screenshots / key frames, or independent sources. Then route the extracted point through `REVIEW_QUEUE.md`.

Anti-omission pass:

```text
pain point:
  What real user problem is the source solving?

workflow:
  What is the full input -> process -> output path?

tools / plugins:
  Which Obsidian plugins, AI tools, platforms, commands, or services appear?

information structure:
  How are notes, files, tags, links, databases, cards, folders, or dashboards organized?

judgment mechanism:
  How does the source decide what is useful, reliable, worth keeping, or worth acting on?

user experience:
  What becomes easier or harder than our current workflow?

automation boundary:
  Which steps are automatic, which stay manual, and where can automation mislead?

risk:
  What can pollute knowledge, create false authority, lose context, or become a junk pile?

fit for us:
  What can replace self-built design, reduce scope, or fill a gap?

challenge to us:
  Does this show our framework is too heavy, too slow, missing UI/workflow, or solving the wrong problem?
```

If a video / post digest only says "what it is about" but does not cover pain point, workflow, tools / plugins, risks, and VAKS comparison, the digest is incomplete.

## 3. What "Preserve Source" Means

Preserving source means giving important knowledge an identity card.
For strong sources, it can also record a small handling trail:

```text
source identity:
  what the source is

capture / extraction:
  who or what captured and extracted it

agent:
  simple human/model/tool strings
```

This does not make capture heavy. Light sources keep the minimal identity fields; medium/heavy sources may add extraction and optional provenance details.

Review, promotion, and context-pack usage are not stored as source main fields. They belong to reviewed nodes, promotion records, context packs, or the use ledger.

For a repository:

```yaml
source_id:
source_uri:
source_url:
owner:
repo:
checked_commit:
commit_time:
captured_at:
captured_by:
extracted_by:
extracted_at:
extraction_tool:
extraction_model:
source_status: active | legacy | deprecated | unknown
files_reviewed:
source_anchor_matrix:
why_captured:
extracted_points:
not_adopted:
timeline_notes:
```

For user directives, explicit corrections, preferences, decisions, or action instructions that affect durable knowledge or action:

```yaml
verbatim_input:
model_interpretation:
intent_confirmation:
  restated_intent:
  assumptions:
  scope_in:
  scope_out:
  success_criteria:
```

Do not require `verbatim_input` / `model_interpretation` for ordinary article, repository, paper, or source capture.

For evidence that may support promotion, strong reviewed relations, decisions, or action basis, preserve a source anchor rather than only a source link:

```yaml
source_anchor:
  url_or_path:
  exact_quote:
  prefix:
  suffix:
  captured_at:
```

For heavy, high-drift, or action-relevant sources, add optional stability fields:

```yaml
source_anchor:
  position:
  content_hash:
  archived_url:
  checked_latest_at:
  source_changed: unknown | yes | no
```

Track how far the evidence was actually inspected:

```yaml
evidence_granularity: metadata_only | abstract_or_summary | excerpt_or_passage | table_or_code_anchor | full_source_reviewed
```

Rule:

```text
Source provenance tells where material came from.
Source anchor tells where the specific evidence lives.
Neither proves support by itself.
```

For a paper:

```yaml
source_id:
source_uri:
title:
authors:
published_at:
venue:
doi_or_arxiv:
version:
captured_at:
captured_by:
extracted_by:
extracted_at:
extraction_tool:
extraction_model:
key_sections_reviewed:
main_claims:
limitations:
later_updates:
fit_to_our_architecture:
```

Plain rule:

```text
Do not let an AI summary become detached from who said it, when, where, and in what version.
Do not let an AI paraphrase replace the user's original words.
```

## 4. User Experience Modes

### Normal Question Mode

Use:

```text
Karpathy-simple
```

Flow:

```text
search/read enough
answer
optionally save light note if valuable
```

Do not create:

```text
dev context pack
full review
pattern/anti-pattern
feedback-event
```

unless the material proves important.

### Project Development Mode

Use:

```text
Dusk-style scope dashboard + DEV_CONTEXT
```

Flow:

```text
project goal
-> scope dashboard / related-material briefing
-> DEV_CONTEXT Core / Support / Risk / Cold References
-> development
-> closeout
```

The dashboard is a workbench.

It is not truth.

### Strong Source / Decision Mode

Use:

```text
verified-action strictness
```

Flow:

```text
source record
-> candidate points
-> collision / comparison
-> review
-> pattern / anti-pattern / decision
-> index / handoff
```

Use this mode when the source may affect future action.

## 5. When To Upgrade Processing

Upgrade light to medium when:

```text
the source is reused
the user asks about it again
it becomes relevant to a project
it appears in search/context briefing repeatedly
```

Upgrade medium to heavy when:

```text
it changes architecture
it validates or contradicts a design
it becomes a development constraint
it exposes a risk or failure mode
it should be cited as action basis
```

Downgrade or cool after use when:

```text
it was one-off evidence
it no longer fits the active project
its value is only historical
it has been superseded
```

## 6. Non-negotiable Boundaries

```text
Capture must stay easy.
Strong sources must remain traceable.
Important evidence should carry a source anchor, not just a URL.
Evidence granularity must stay visible: metadata-only or summary-only material cannot silently become high-confidence support.
Heavy source digests should include an omission check for missing risks, missing scope limits, likely dropped facts, and whether full source read is needed.
Dashboard state is not truth.
Retrieval rank is not trust.
Repeated appearance is a signal, not proof.
Heavy review is for promotion and action, not ordinary saving.
Evidence support and evidence sufficiency checks are lazy gates: use them for promotion, decision, strong relation, action basis, or explicitly challenged points, not for ordinary capture.
Association neighborhood activation is also lazy: use it for query/context-pack preparation, promotion review, action basis, or explicit contradiction/risk checks, not for ordinary source capture.
Graph traversal, PPR, similarity, and association score can suggest what to inspect next; they cannot create support, confidence, reviewed relations, or action readiness.
Graph retrieval strata can organize context-pack preparation: low-level source/text-unit/claim/entity recall, high-level pattern/theme/community recall, and relation-neighborhood recall. TextUnit anchors are provenance, community reports are briefings, and graph rank is not trust.
Temporal applicability is checked when a point is promoted, used in a decision/action basis, or appears stale/superseded/out-of-scope; ordinary capture can leave validity windows blank rather than inventing dates.
Confidence caps are checked when a candidate is promoted or used for action: abstract/snippet/URL-only material cannot become high-confidence support without a direct source span or full-text anchor.
Intent confirmation is checked only before significant action, high-impact decision, implementation, deployment, or hard-to-rollback work.
```

## 7. First Implementation

Do not write automation first.

First prove this manually with real material:

```text
1 light source
1 medium project reference
1 heavy repo/paper review
1 scope dashboard or dev context pack
1 closeout update
```

Only after the manual loop works should scripts or CLI commands be written.
