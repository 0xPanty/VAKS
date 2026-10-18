---
type: source
record_kind: source_card
status: source-captured
title: "RKA research knowledge assistant"
source_id: 2026-05-29-rka-source
source_uri: https://github.com/infinitywings/rka
source_url: https://github.com/infinitywings/rka
source_type: repository
version_or_commit: 7bc2d76efba61b92db5b056220f7009763003a0d
captured_at: 2026-05-29
captured_by: Codex
review_priority: high
review_owner: Codex
formalization_status: candidate-generated
topics:
  - review-queue
  - contradiction-queue
  - decision-superseding
  - intent-confirmation
  - backbrief
  - verbatim-input
  - maintenance-manifest
  - confidence-cap
  - decision-outcome-calibration
  - rka
projects:
  - verified-action-knowledge-system
verification_status: primary-source-captured
candidate_relation_suggestions: []
tags:
  - rka
  - review-queue
  - decision-superseding
  - outcome-calibration
knowledge_status: raw
processing_tier: light
why_saved: see_body_or_legacy_record
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
---

# RKA Source Record

## Source Status

The exact GitHub repository is now identified:

```text
https://github.com/infinitywings/rka
checked commit: 7bc2d76efba61b92db5b056220f7009763003a0d
```

RKA is MIT-licensed. This vault should not copy the runtime, but may borrow and adapt conceptual patterns with attribution.

## Source Identity

```text
Repository: infinitywings/rka
Purpose: AI-assisted research orchestration runtime
Runtime shape: SQLite, MCP, REST API, React dashboard, Claude skills
Main actors: PI, Brain, Executor
```

Files reviewed:

```text
README.md
rka/skills/brain/SKILL.md
rka/skills/executor/SKILL.md
rka/models/review_queue.py
rka/models/claim.py
rka/services/review_queue.py
rka/services/decisions.py
rka/services/context.py
rka/services/calibration.py
rka/models/calibration.py
rka/db/migrations/009_v2_claims_clusters_entity_redesign.sql
rka/db/migrations/014_add_staleness_and_assumptions.sql
rka/db/migrations/018_bitemporal_and_calibration.sql
```

## Adopt

```text
review queue item types:
  low_confidence_claim
  contradiction
  missing_evidence
  synthesis_needed
  decision_superseded

decision superseding:
  old decision is not deleted
  replacement decision links back to the old decision
  affected downstream claims, patterns, relations, and context packs become review_due

intent confirmation / backbrief:
  restated intent
  assumptions
  scope in/out
  success criteria

verbatim input separation:
  preserve user / PI exact words separately from model interpretation

maintenance manifest:
  lint-style queue for missing links, provenance gaps, stale dependencies, orphaned review items

staleness vs validity distinction:
  valid_until / valid_from express applicability windows
  stale / review_due express editorial review pressure

confidence cap without full text:
  abstract/snippet-only or URL-only material cannot receive high evidence confidence

decision outcome calibration:
  record recommendation, confidence, user choice, outcome, and future recommendation impact
```

## Do Not Adopt

```text
full runtime
MCP surface
dashboard
workflow actions as truth changes
SQLite as the Markdown source of truth
automatic background truth mutation
Brier / ECE machinery before there is enough outcome data
```

## Fit To This Vault

RKA is useful as an engineering and workflow reference, not as a skeleton to fork.

This vault absorbs the patterns as lazy gates and metadata:

```text
ordinary capture remains light
ordinary query remains simple
promotion and action basis become more auditable
feedback and outcomes calibrate future recommendation, not truth
```
