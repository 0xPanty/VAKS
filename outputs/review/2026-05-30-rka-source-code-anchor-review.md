---
type: source-code-review
status: completed
created: 2026-05-30
source_id: 2026-05-29-rka-source
source_repo: https://github.com/infinitywings/rka
checked_commit: 7bc2d76efba61b92db5b056220f7009763003a0d
review_mode: exact-commit-source-inspection
runtime_executed: false
tags:
  - rka
  - review-queue
  - decision-superseding
  - calibration
  - source-code-anchor
---

# RKA Source Code Anchor Review

## Purpose

This review checks whether the RKA ideas already absorbed into the Verified Action Knowledge System have real source-code support, and whether the source code exposes any small design point we missed.

It inspected the exact checked commit:

```text
infinitywings/rka
7bc2d76efba61b92db5b056220f7009763003a0d
```

No RKA runtime was run. No MCP, API server, dashboard, database migration, or worker was started.

## Files Inspected

```text
rka/models/review_queue.py
rka/services/review_queue.py
rka/services/decisions.py
rka/models/decision.py
rka/models/claim.py
rka/services/claims.py
rka/services/clusters.py
rka/models/decision_option.py
rka/services/decision_options.py
rka/models/calibration.py
rka/services/calibration.py
rka/services/maintenance.py
rka/services/context.py
rka/services/knowledge_pack.py
rka/db/migrations/009_v2_claims_clusters_entity_redesign.sql
rka/db/migrations/014_add_staleness_and_assumptions.sql
rka/db/migrations/018_bitemporal_and_calibration.sql
rka/skills/brain/SKILL.md
rka/skills/brain/workflows.md
```

## High-Level Result

The source code confirms the earlier conceptual adoption:

```text
RKA is useful as a workflow / review-discipline reference.
It should not be forked as this vault's runtime.
It should not become the truth source.
```

The best confirmed ideas are:

```text
review queue is attention routing, not truth
decision superseding preserves history and creates review pressure
staleness is editorial review pressure
valid_until is temporal validity boundary
decision outcomes calibrate future recommendations, not truth
maintenance checks should surface structural gaps without auto-repairing reviewed truth
```

## Code Anchors

### 1. Review Queue Is Routing Metadata

Source anchors:

- `rka/models/review_queue.py` lines 10-36
  <https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/models/review_queue.py#L10-L36>
- `rka/services/review_queue.py` lines 15-74
  <https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/services/review_queue.py#L15-L74>
- `rka/db/migrations/009_v2_claims_clusters_entity_redesign.sql` lines 208-227
  <https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/db/migrations/009_v2_claims_clusters_entity_redesign.sql#L208-L227>

What the code shows:

```text
review_queue has item_type, item_id, flag, context, priority, status, raised_by, resolved_by, resolution.
flags include low_confidence_cluster, potential_contradiction, complex_synthesis_needed, re_distill_review, cross_topic_link, stale_theme.
statuses include pending, acknowledged, resolved, dismissed.
```

Fit to our framework:

```text
Keep review_queue_item optional.
Keep it as routing / attention pressure.
Do not require every candidate point to have a queue item.
Do not treat queue resolution as a truth update.
```

Small useful nuance:

```text
RKA separates acknowledged from resolved.
Our open / in-review / resolved / rejected / parked shape already covers the same workflow.
No schema change is required now.
```

### 2. Decision Superseding Preserves History

Source anchors:

- `rka/services/decisions.py` lines 217-333
  <https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/services/decisions.py#L217-L333>
- `rka/db/migrations/009_v2_claims_clusters_entity_redesign.sql` lines 84-88
  <https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/db/migrations/009_v2_claims_clusters_entity_redesign.sql#L84-L88>

What the code shows:

```text
supersede_decision creates a new decision, increments scope_version, marks the old decision superseded, links new -> old with supersedes, marks affected claims stale, marks affected clusters needs_reprocessing, and creates a review queue item.
```

Fit to our framework:

```text
This strongly supports our decision superseding rule.
Old decisions should remain queryable.
New decisions should link back.
Affected downstream material should become review_due / stale, not silently rewritten.
```

One exact RKA detail we should not copy:

```text
RKA marks claims stale and clusters needs_reprocessing inside its database runtime.
Our Markdown vault should record review_due / stale pressure in records and maintenance manifests, not run automatic database mutation as truth.
```

### 3. Contradiction Creates Reprocessing Pressure

Source anchors:

- `rka/services/claims.py` lines 159-201
  <https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/services/claims.py#L159-L201>
- `rka/services/clusters.py` lines 272-293
  <https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/services/clusters.py#L272-L293>
- `rka/services/clusters.py` lines 321-336
  <https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/services/clusters.py#L321-L336>

What the code shows:

```text
contradicts edges mark clusters as needs_reprocessing.
large or contested synthesis creates review_queue flags.
existing contradiction edges create potential_contradiction review items.
```

Fit to our framework:

```text
This supports challenge taxonomy and review_due triggers.
Contradiction is not automatic truth resolution.
It creates review pressure and asks for human/Brain review.
```

Small useful nuance:

```text
RKA treats contested synthesis and many-claim synthesis as separate queue pressure.
Our challenge taxonomy already has rebuttal / undercut / scope_limit / source_hygiene / stale_assumption / action_failure.
No need to add many more challenge types.
```

### 4. Source Anchors Exist As Offsets, But Are Not Enough

Source anchors:

- `rka/db/migrations/009_v2_claims_clusters_entity_redesign.sql` lines 102-116
  <https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/db/migrations/009_v2_claims_clusters_entity_redesign.sql#L102-L116>
- `rka/models/claim.py` lines 17-35
  <https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/models/claim.py#L17-L35>

What the code shows:

```text
claims can store source_offset_start and source_offset_end.
claims also track source_entry_id, confidence, verified, stale.
```

Fit to our framework:

```text
This supports source_anchor mini-profile.
Our source_anchor is stronger for Markdown review because it keeps exact_quote, prefix, suffix, and optional content_hash.
Offset-only anchors are useful, but brittle if source text changes.
```

### 5. Staleness And Validity Are Different Signals

Source anchors:

- `rka/db/migrations/014_add_staleness_and_assumptions.sql` lines 1-16
  <https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/db/migrations/014_add_staleness_and_assumptions.sql#L1-L16>
- `rka/db/migrations/018_bitemporal_and_calibration.sql` lines 1-24
  <https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/db/migrations/018_bitemporal_and_calibration.sql#L1-L24>
- `rka/skills/brain/SKILL.md` lines 194-200
  <https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/skills/brain/SKILL.md#L194-L200>
- `rka/skills/brain/workflows.md` lines 361-364
  <https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/skills/brain/workflows.md#L361-L364>

What the code and repo docs show:

```text
staleness / stale_reason / valid_from are separate from valid_until.
valid_until is added later as a temporal validity boundary.
RKA explicitly says staleness is editorial overlay, while valid_until is temporal end-of-validity.
```

Fit to our framework:

```text
This directly confirms our Graphiti / Zep-inspired temporal applicability boundary.
empty valid_until means no reviewed expiry boundary yet, not permanent truth.
stale / review_due means review pressure, not automatic invalidity.
```

### 6. Decision Outcome Requires User Resolution

Source anchors:

- `rka/models/decision_option.py` lines 121-130
  <https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/models/decision_option.py#L121-L130>
- `rka/services/decision_options.py` lines 234-280
  <https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/services/decision_options.py#L234-L280>
- `rka/api/routes/decisions.py` lines 227-243
  <https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/api/routes/decisions.py#L227-L243>

What the code shows:

```text
PI selection is recorded separately from recommendation.
At least one of selected_option_id or override_rationale is required.
Outcome recording is rejected if there is no recorded PI selection or override.
```

Fit to our framework:

```text
This is a real improvement for our Use Ledger wording.
decision_outcome should require user_choice or explicit override before outcome is recorded.
Otherwise there is no clear recommendation-to-choice-to-outcome chain.
```

Adopted as a small wording hardening in:

```text
SCHEMA.md
FEEDBACK.md
FUSION_ARCHITECTURE_V0_2_DRAFT.md
```

### 7. Evidence Strength Is Split Between Pointer And Aggregate

Source anchors:

- `rka/models/decision_option.py` lines 21-48
  <https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/models/decision_option.py#L21-L48>
- `rka/models/decision_option.py` lines 51-75
  <https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/models/decision_option.py#L51-L75>

What the code shows:

```text
Each evidence pointer has strength_tier: direct / indirect / weak.
The option also has aggregate confidence_evidence_strength: weak / moderate / strong.
```

Fit to our framework:

```text
This supports our Evidence Packet distinction:
evidence_item support is not the same as overall evidence_sufficiency.
Direct evidence refs can still produce only moderate aggregate strength.
```

No new field is needed because our current split already exists:

```text
evidence_support
evidence_granularity
evidence_sufficiency
coverage_overview
```

### 8. Calibration Metrics Have Sample-Size Guards

Source anchors:

- `rka/models/calibration.py` lines 16-26
  <https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/models/calibration.py#L16-L26>
- `rka/models/calibration.py` lines 54-89
  <https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/models/calibration.py#L54-L89>
- `rka/services/calibration.py` lines 237-306
  <https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/services/calibration.py#L237-L306>
- `rka/services/calibration.py` lines 311-378
  <https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/services/calibration.py#L311-L378>

What the code shows:

```text
outcomes are succeeded / failed / mixed / unresolved.
unresolved is excluded from calibration.
mixed counts as half-success in RKA.
metrics are marked unavailable under a minimum sample threshold.
override_rate, escape_hatch_rate, and near_miss_rate use a separate denominator from outcome-based Brier / ECE.
```

Fit to our framework:

```text
This confirms our existing stance:
record outcomes first
do not compute heavy metrics too early
outcomes improve future recommendation behavior, not truth
```

Small useful nuance:

```text
Keep near_miss as a feedback / recommendation-quality signal, not a truth signal.
Keep sample-size guard if we ever compute calibration metrics.
```

### 9. Maintenance Manifest Is Structural Hygiene

Source anchors:

- `rka/services/maintenance.py` lines 14-18
  <https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/services/maintenance.py#L14-L18>
- `rka/services/maintenance.py` lines 240-266
  <https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/services/maintenance.py#L240-L266>
- `rka/services/maintenance.py` lines 367-394
  <https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/services/maintenance.py#L367-L394>
- `rka/services/knowledge_pack.py` lines 14-30 and 860-891
  <https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/services/knowledge_pack.py#L14-L30>
  <https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/services/knowledge_pack.py#L860-L891>

What the code shows:

```text
maintenance checks are SQL structural checks.
RKA separates critical integrity errors from warnings in knowledge pack import.
stale claims and stale clusters are surfaced as maintenance items.
```

Fit to our framework:

```text
This supports maintenance_manifest as lint pressure.
It can surface missing anchors, missing evidence packets, stale dependencies, and orphan review items.
It must not auto-repair reviewed knowledge.
```

Small useful nuance:

```text
For future import / pack / migration flows, severity may need critical / warning / advisory.
For current Markdown lint, low / medium / high is enough.
```

### 10. Context Ranking Is Activation, Not Truth

Source anchors:

- `rka/models/context.py` lines 31-53
  <https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/models/context.py#L31-L53>
- `rka/services/context.py` lines 326-420
  <https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/services/context.py#L326-L420>

What the code shows:

```text
context packages carry ranked entries, sources, narrative, note, and token_estimate.
ranking uses search relevance / importance / centrality / recency / anchor-aware extras.
```

Fit to our framework:

```text
This supports our context_pack_trace and activation-tier boundary.
Ranking explains why context was surfaced.
Ranking does not create support, confidence, reviewed relation, or action readiness.
```

RKA does not fully implement our desired selected / ignored / ignored_reason trace. Our context_pack_trace remains a stronger audit shape.

## What We Were Missing

The source code exposed one concrete improvement worth adopting now:

```text
decision_outcome needs a precondition:
do not record an outcome unless the recommendation had a recorded user_choice or explicit override.
```

Reason:

```text
Without user_choice / override, an outcome cannot tell whether the recommendation worked.
It would mix "what the system recommended" with "what the user actually did."
```

This strengthens Use Ledger and feedback calibration without expanding Truth Core.

## What We Should Not Copy

Do not copy:

```text
RKA runtime
SQLite truth source
MCP write surface
dashboard
automatic database mutation as reviewed truth
heavy Brier / ECE workflow before enough outcome data exists
context ranker as trust signal
claim_edge confidence as reviewed relation confidence
```

## Final Judgment

The RKA source-code review is strongly positive for the already-adopted ideas.

It confirms the important boundary:

```text
signals create review pressure
review pressure is not truth
outcome feedback calibrates future recommendations
context ranking activates material
source/code anchors raise evidence quality
```

No large architecture change is needed. The only immediate hardening is the decision-outcome precondition.
