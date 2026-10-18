---
type: sandbox_design_note
status: candidate_only
created_at: 2026-06-07
scope: borrowable ideas from existing VAKS / Obsidian candidate distillations
truth_boundary: sandbox design note only; not reviewed knowledge; not architecture decision; not action basis
---

# Vault Distillation Borrowings

## Plain Takeaway

The existing VAKS / Obsidian distillations do not replace the Pro tag-routing
design.

They add the missing use layer:

```text
Pro report:
  keep tags, metadata, status, candidate points, overlay, and retrieval lanes
  separated.

Existing vault distillations:
  make that separation usable through read-first indexes, artifact receipts,
  topic entry pages, progressive context packs, and vault-health filtering.
```

In short:

```text
The previous sandbox defined safe retrieval lanes.
The vault distillations suggest the workbench that makes those lanes pleasant to
use.
```

## Sources Scanned

High-signal candidate distillations:

```text
outputs/review/2026-06-07-infiniflow-ragflow-candidate-distillation.md
outputs/review/2026-06-06-anthropic-contextual-retrieval-candidate-distillation.md
outputs/review/2026-06-06-anthropic-effective-context-engineering-agents-candidate-distillation.md
outputs/review/2026-06-06-microsoft-azure-ai-search-agentic-retrieval-candidate-distillation.md
outputs/review/2026-06-06-google-cloud-gemini-enterprise-hybrid-search-candidate-distillation.md
outputs/review/2026-06-06-rag-eval-tracing-citation-rrf-batch-candidate-distillation.md
outputs/review/2026-06-06-datachain-ai-datachain-detailed-candidate-distillation.md
outputs/review/2026-06-06-openinference-semantic-conventions-candidate-distillation.md
outputs/review/2026-06-06-x-hamza-obsidian-second-brain-candidate-distillation.md
outputs/review/2026-06-06-x-damidefi-obsidian-claude-research-stack-candidate-distillation.md
outputs/review/2026-06-06-x-damidefi-obsidian-signal-density-cleanup-candidate-distillation.md
outputs/review/2026-06-06-x-cyrilxbt-claude-obsidian-90-days-candidate-distillation.md
outputs/review/2026-06-06-x-cyrilxbt-obsidian-from-scratch-candidate-distillation.md
outputs/review/2026-06-06-x-zaimiri-hermes-obsidian-vault-ai-brain-candidate-distillation.md
```

All of these are candidate-only source comprehension artifacts.
They are not reviewed knowledge.

## Borrowing Layer

### 1. Read-First Artifact Registry

Borrow:

```text
Before raw full-text search, check whether VAKS already has processed artifacts:

source card
candidate distillation
project overlay
query-run receipt
context-pack manifest
topic retrieval pack
latest handoff / index
```

Why:

```text
This reduces repeated extraction and helps agents reuse prior work.
```

Do not borrow as:

```text
artifact exists -> artifact is true
artifact exists -> artifact is current rule
artifact exists -> artifact is action basis
```

Candidate registry shape:

```yaml
source_id:
source_card:
candidate_distillations: []
project_overlays: []
query_runs: []
context_packs: []
latest_check:
warnings: []
```

### 2. Identifier-First, Payload-Later Context

Borrow:

```text
Context packs should first show identifiers and navigation:

item_id
source_ref
path
heading
selector_or_offset
why_included
citable_status
drilldown_path
```

Then load:

```text
short snippet
contextualized snippet
full raw/source payload only on drilldown
```

Why:

```text
This keeps search results readable and prevents long raw dumps from drowning the
useful route.
```

Do not borrow as:

```text
identifier presence -> evidence support
short summary -> final support
compactness -> permission to omit source anchor
```

### 3. Query-Run Receipt Reuse

Borrow:

```text
Important query-runs should be reusable receipts.
```

Candidate fields:

```yaml
query_run_id:
query_type:
risk_type:
mode:
retrieval_profile:
hard_filters:
indexes_used:
retrievers_called:
candidate_counts_by_lane:
selected_items:
excluded_items:
warnings:
fallbacks:
pack_id:
used_anchor_refs:
feedback_ref:
```

Why:

```text
The next agent should not have to rediscover the same source/candidate/check
chain from scratch.
```

Do not borrow as:

```text
query-run receipt -> reviewed decision
trace completeness -> evidence sufficiency
retrieval score -> trust
```

### 4. Pack Item Receipt

Borrow:

```text
Every context-pack item should explain why it is present and how it may be used.
```

Candidate fields:

```yaml
item_id:
display_label:
lane:
source_ref:
selector_or_offset:
snippet:
contextualized_snippet:
citable_status: activation_only | drilldown_required | span_ready
matched_channels: []
channel_ranks: []
rrf_rank:
rerank_score:
why_included:
exclusion_or_caution_note:
```

Why:

```text
This turns retrieval output into a readable workbench instead of a mixed search
dump.
```

Do not borrow as:

```text
citation marker -> support
pack inclusion -> review
rerank score -> authority
```

### 5. Topic Entry Pages / Topic Retrieval Packs

Borrow:

```text
High-value topics should have human entry pages.
```

Useful topic packs:

```text
source-intake-routing
retrieval-workbench
candidate-distillation
project-overlay
context-pack
feedback-query-run
```

Each entry should show:

```text
current rule
candidate orientation
raw drilldown
active project overlays
audit evidence
known exclusions
last refreshed
```

Why:

```text
This upgrades "search results are separated" into "the entrance is already laid
out."
```

Do not borrow as:

```text
topic pack -> topic ontology
MOC prominence -> truth
hub page -> reviewed relation
```

### 6. Vault Health / Signal Density Filtering

Borrow:

```text
Agent synthesis degrades when low-signal, duplicated, stale, or unprocessed
material is pulled into ordinary context.
```

Use this as:

```text
default exclusions
cooling
archive-first reactivation
duplicate detection
low-signal diagnostics
```

Do not use this as:

```text
automatic deletion
raw source destruction
truth downgrade
hidden suppression of contrary evidence
```

### 7. Links And Graph As Activation Bets

Borrow:

```text
Links, backlinks, graph view, and connection-finders are useful activation
surfaces.
```

Use this as:

```text
related context suggestion
candidate relation prompt
review queue routing
topic-pack expansion
```

Do not use this as:

```text
reviewed relation
evidence support
confidence
action readiness
```

### 8. Steering / Handoff Freshness

Borrow:

```text
Read-first steering files and fresh handoffs improve recurring agent output.
```

Use this as:

```text
latest handoff first
AGENTS.md / index first
active project state first
staleness warning
```

Do not use this as:

```text
truth confidence
permission to act
substitute for source anchor
```

### 9. One Stage, One Saved Output

Borrow:

```text
Expensive or important processing should produce named, inspectable artifacts.
```

Examples:

```text
ingest-source -> source card + receipt
make-candidate -> candidate distillation + candidate points
update-index -> compiled index + freshness receipt
make-context-pack -> pack manifest + item receipts
record-feedback -> append-only feedback event
sync-obsidian -> hash check
```

Do not borrow as:

```text
compiled output -> truth source
script success -> review
agent skill output -> self-approval
```

## What This Adds To The Current Sandbox

Already covered by the sandbox:

```text
authority/status/project/path-role hard filters
separate retrieval lanes
topics/entities as recall metadata
candidate points with kp_ref
project overlay sidecar boundary
suggested vs confirmed metadata
topic retrieval pack concept
```

New useful additions from existing distillations:

```text
read-first artifact registry
identifier-first payload-later pack UX
query-run receipt reuse
pack item receipt fields
vault health / signal density diagnostics
steering and handoff freshness checks
one-stage-one-output tool contract
```

## Human Experience Target

Before:

```text
Search a phrase.
Get many raw, candidate, sandbox, audit, baseline, package, and overlay hits.
Manually decide what each hit means.
```

After:

```text
Open a topic pack or run a query mode.
See current rule first.
See candidate references separately.
See raw anchors only when needed.
See audit evidence only when asking why/how it changed.
See active project overlays only in active project mode.
Reuse prior query-run/context-pack artifacts.
Drill down only when action-facing support needs raw or reviewed anchors.
```

## Recommended Next Sandbox Additions

If this sandbox continues, add candidate-only files for:

```text
12_ARTIFACT_REGISTRY_CANDIDATE.md
13_CONTEXT_PACK_BUILDER_V0_CONTRACT.md
14_OBSIDIAN_WORKBENCH_ENTRYPOINTS.md
```

These should remain usage-layer artifacts until reviewed.

No mainline writeback should happen from this file alone.
