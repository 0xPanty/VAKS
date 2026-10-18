---
record_type: feedback-log
status: captured
created: 2026-06-06
updated: 2026-06-06
feedback_id: feedback-2026-06-06-retrieval-source-intake-operational
created_by: Codex
feedback_source: explicit-user-and-operator-run
query_intent: research
query_scope:
  project: verified-action-knowledge-system
  domain: retrieval-query-contract
  version: v0.2.13-candidate-extension
  time_range: 2026-06-06
scope_key: vaks/retrieval-query-contract/source-intake-run
target_type: route
target_id: retrieval-source-intake-flow
feedback_type: useful
event_type: answer_helpful
signal_type: explicit_positive
polarity: mixed-positive
signal_strength: 2
signal_confidence: 0.85
severity: medium
affects:
  usefulness: true
  scope_fit: true
  activation_ranking: true
  review_due: false
  future_recommendation: true
  risk_calibration: true
  option_framing: true
never_affects_directly:
  - truth_confidence
  - verification_status
  - source_reliability
requires_review: false
review_status: pending
tags:
  - feedback-log
  - retrieval
  - source-intake
  - toolchain
  - codex-skill
  - obsidian-sync
  - candidate-only
---

# Retrieval Source Intake Operational Feedback

## What Happened

During the VAKS retrieval/query design补齐 run, the operator processed a batch
of external retrieval references into candidate-only records:

```text
official engineering docs:
  Anthropic Contextual Retrieval
  Anthropic Effective Context Engineering for AI Agents
  Azure AI Search Agentic Retrieval
  Google Cloud Gemini Enterprise Hybrid Search

papers / publication pages:
  Lost in the Middle
  ARES
  Self-RAG
  RAPTOR
  Adaptive-RAG
  LongCite
  RAG vs. GraphRAG
  Microsoft Research GraphRAG Query-Focused Summarization
```

The run used the current VAKS path:

```text
external source
-> raw source card
-> candidate distillation
-> reusable candidate point
-> candidate knowledge index
-> Obsidian sync
-> SHA256 verification
```

No reviewed knowledge, decision, action basis, schema, template, or mainline
architecture file was edited.

## What Felt Good

### 1. Layer Boundaries Were Easy To Follow

The path itself helped keep the operator honest:

```text
raw source = provenance
candidate distillation = comprehension / extraction
candidate index = navigation
Obsidian sync = durable visibility
none of these = truth
```

This reduced the chance of accidentally treating Pro's recommendation or a
paper abstract as adopted architecture.

### 2. Duplicate Handling Worked Naturally

ARES appeared twice in the user-provided list. The flow encouraged one source
record and one candidate extraction rather than duplicate source cards.

Self-RAG already existed as:

```text
raw/papers/2026-05-29-self-rag-source.md
```

The new batch reused that existing record instead of creating a second
provenance object.

### 3. Source Type Routing Was Mostly Clear

The operator could distinguish:

```text
raw/articles:
  official engineering docs / web articles

raw/papers:
  arXiv papers / Microsoft Research paper page

raw/repos:
  repository documentation or code source records
```

This helped avoid mixing the Microsoft GraphRAG repo/docs card with the
Microsoft Research paper-page card.

### 4. Candidate Tags Became Useful Without Becoming Authority

The candidate index made the new ideas findable:

```text
query-complexity-router
position-aware-context-pack-ordering
sentence-level-citation-binding
global-question-as-qfs-mode
community-summary-as-global-briefing
```

The tag/index layer felt useful as a workbench map while still being clearly
non-authoritative.

### 5. Light / Medium Intake Started To Mean Something

The run naturally separated:

```text
medium:
  official docs, current-design-critical papers/pages, or sources already used
  as architecture references

light:
  abstract/metadata-level arXiv intake used only for candidate extraction
```

This is a good sign: VAKS can keep ordinary source intake light while making
important design references more visible.

### 6. Obsidian Sync Plus Hash Verification Felt Reassuring

Copying candidate artifacts to:

```text
H:\Obsidian\资料库
```

and checking SHA256 made the work feel durable without requiring a commit or
mainline write.

## What Felt Uncomfortable

### 1. Source Card Writing Is Too Manual

Several fields are repetitive and easy to forget:

```text
raw_location
source_family
confidence_cap_reason
processing_mode
processing_level
candidate_relation_suggestions
topics
tags
```

Observed issue:

```text
raw_location had to be patched back into several paper source cards.
```

Likely fix:

```text
new-source-intake script should generate the frontmatter from URL, title,
source type, date, and target folder.
```

### 2. Processing Level Rubric Is Still Too Implicit

The operator can explain why something is `light` or `medium`, but the rule is
not yet machine-checkable.

Current working intuition:

```text
light:
  abstract/metadata/read-once intake, source-only, candidate extraction only

medium:
  official documentation, design-critical source, or source used to shape a
  candidate module

heavy:
  full PDF/code/repo deep read, line/code anchors, or source used for promotion,
  decision, action basis, or mainline writeback
```

Risk:

```text
abstract-level source cards may later look stronger than they are.
```

Likely fix:

```text
lint should require confidence_cap_reason and processing_mode for all light
sources; candidate index should optionally surface review depth.
```

### 3. Candidate Slug Naming Is Hand-Rolled

Manual slugging worked in a small batch, but future collisions are likely:

```text
selective-graphrag-branch
local-to-global-graph-summarization-branch
summary-tree-as-selective-structure-branch
```

These are related but not identical. A future reviewer needs to know whether
they are duplicates, refinements, or sibling patterns.

Likely fix:

```text
candidate-index-lint should detect similar slugs, repeated source refs, and
near-duplicate borrow scopes.
```

### 4. Ledger Files Are Becoming Too Long

The main extraction ledger is useful, but it is now accumulating many source
sections:

```text
outputs/review/2026-06-06-vaks-retrieval-external-source-extractions.md
```

Risk:

```text
one file may become too long to scan, diff, or hand to a reviewer.
```

Likely fix:

```text
keep the current ledger as a manifest/index, then split long extraction details
by module or source batch.
```

### 5. Obsidian Sync Is Too Manual

The operator repeatedly ran:

```text
copy project file to H:\Obsidian\资料库
hash local copy
hash Obsidian copy
check staged empty
```

This is reliable but boring and error-prone.

Likely fix:

```text
sync-and-hash script:
  input: list of project-relative paths
  output: copy report, hash match report, missing path report
```

### 6. Git Safety Requires Repeated Manual Checks

The current discipline is good:

```text
do not git add .
do not commit
do not push
check git diff --cached is empty
```

But it is repeated manually after every intake block.

Likely fix:

```text
post-intake sanity script should report:
  staged files
  touched files matching mainline paths
  untracked candidate artifacts
  Obsidian hash matches
```

### 7. Abstract-Level Sources Need A More Visible Badge

The arXiv batch was intentionally abstract/metadata-level. That was recorded in
source cards, but the candidate index only shows `candidate_only`.

Risk:

```text
future readers may not notice that a point came from an abstract-level pass,
not a full PDF review.
```

Likely fix:

```text
candidate index could add `review_depth` or `source_depth` later:
  abstract_only
  official_doc_section
  full_pdf_read
  repo_code_read
```

Do not add this to mainline schema yet; treat it as a tool/workbench candidate.

## Optimization Candidates

### OC-001: new-source-intake

Purpose:

```text
Create a raw source card from a URL/source type with safe defaults.
```

Inputs:

```text
url
source_type
title
published_or_updated_at
processing_level
target_folder
topics
```

Outputs:

```text
raw/articles/<date>-<slug>-source.md
raw/papers/<date>-<slug>-source.md
or raw/repos/<date>-<slug>-source.md
```

Safety:

```text
never create reviewed knowledge
never infer truth confidence
warn on duplicate source_uri / title / arXiv id
```

### OC-002: batch-candidate-distill

Purpose:

```text
Turn a set of source cards into one candidate-only batch distillation.
```

Must preserve:

```text
source_ref
source_anchor
evidence_granularity
promotion_readiness: not_ready
non-borrow scope
truth boundary
```

### OC-003: candidate-index-lint

Purpose:

```text
Check candidate index hygiene.
```

Checks:

```text
slug uniqueness
source file exists
distillation file exists
status is candidate_only
tags are navigation-only
similar slug warning
abstract-only source warning
```

### OC-004: sync-and-hash

Purpose:

```text
Copy selected candidate artifacts to the formal Obsidian vault and verify hash.
```

Inputs:

```text
project-relative file list
vault root: H:\Obsidian\资料库
```

Outputs:

```text
copied files
SHA256 match table
missing file errors
```

Safety:

```text
copy only named files
do not delete
do not stage
do not modify mainline
```

### OC-005: retrieval-intake-postflight

Purpose:

```text
One command to summarize safety state after a retrieval-intake run.
```

Report:

```text
new raw source cards
new candidate distillations
updated indexes/ledgers
mainline files touched: yes/no
staged files: yes/no
Obsidian hashes matched: yes/no
```

## Suggested Priority

```text
1. sync-and-hash
2. new-source-intake
3. candidate-index-lint
4. batch-candidate-distill
5. retrieval-intake-postflight
```

Reason:

```text
sync-and-hash removes the most repetitive manual step immediately.
new-source-intake removes the highest risk of missing source-card fields.
candidate-index-lint reduces future duplicate/collision drift.
batch-candidate-distill and postflight make the full flow smoother after the
first three are stable.
```

## Boundary

This feedback can affect:

```text
future toolchain design
Codex skill operating rules
source intake ergonomics
candidate index hygiene
Obsidian sync workflow
```

This feedback must not directly affect:

```text
truth confidence
verification_status
source reliability
reviewed relations
architecture decisions
action basis
```

## One-Line Takeaway

VAKS is already usable as an operating system for source intake and candidate
design extraction; the next discomfort is not conceptual architecture, but
small compiler/toolchain ergonomics.
