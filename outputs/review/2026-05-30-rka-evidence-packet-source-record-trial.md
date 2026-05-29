---
type: qa
status: active
created: 2026-05-30
updated: 2026-05-30
project: verified-action-knowledge-system
scope:
  - evidence-packet
  - source-record-trial
  - rka
  - v0-3
sources:
  - "raw/repos/2026-05-29-rka-source.md"
  - "FUSION_ARCHITECTURE_V0_2_DRAFT.md"
  - "SCHEMA.md"
verification_status: in-review
evidence_level: source-record-excerpt
confidence: medium
last_verified: 2026-05-30
next_review: 2026-06-03
tags:
  - evidence-discipline
  - micro-trial
  - rka
  - source-hygiene
---

# RKA Evidence Packet Source-Record Trial

Post-Pro note:
This was an earlier source-record pressure test. Its main conclusion still stands, but its packet examples preserve a draft packet shape. The canonical post-Pro packet shape now puts source anchors on `evidence_items`, uses `evidence_support.evidence_role` instead of `relation_to_point`, and uses `knowledge_state` for review output. See `outputs/review/2026-05-30-v0-3-integrated-ten-alpha-trial.md` for the patched canonical trial.

## Purpose

This is the second Evidence Packet micro-trial.

Unlike the first trial, this one uses a local repository source record rather than the broad framework research report.

It tests whether Evidence Packet can:

```text
1. use a local source record as evidence without overclaiming source-code verification
2. expose source hygiene limits when actual code snippets are not embedded
3. distinguish conceptual adoption from runtime adoption
4. turn repo-source uncertainty into minimal review actions
```

## Trial Source

```text
raw/repos/2026-05-29-rka-source.md
```

The record identifies the repo and checked commit:

```text
raw/repos/2026-05-29-rka-source.md:43-48
```

It also lists files reviewed:

```text
raw/repos/2026-05-29-rka-source.md:61-77
```

Important limitation:

```text
The local source record lists reviewed files and extracted patterns, but it does not embed exact code spans from those files.
```

Therefore this trial treats the evidence granularity as:

```text
source_record_excerpt
```

Mapped to the current enum:

```text
excerpt_or_passage
```

But with a source hygiene warning:

```text
not table_or_code_anchor
not full_source_reviewed inside this local packet
```

## Source Anchors

### RKA-A1 Source Identity

Source:

```text
raw/repos/2026-05-29-rka-source.md:43-50
```

Anchor:

```text
https://github.com/infinitywings/rka
checked commit: 7bc2d76efba61b92db5b056220f7009763003a0d
RKA is MIT-licensed. This vault should not copy the runtime, but may borrow and adapt conceptual patterns with attribution.
```

Evidence relation:

```text
supports source identity and adoption boundary
```

### RKA-A2 Files Reviewed

Source:

```text
raw/repos/2026-05-29-rka-source.md:61-77
```

Anchor:

```text
Files reviewed:
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

Evidence relation:

```text
supports that prior review was code-aware, but undercuts full code-anchor support in this packet because exact code spans are absent
```

### RKA-A3 Adopted Concepts

Source:

```text
raw/repos/2026-05-29-rka-source.md:79-115
```

Anchor:

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
...
confidence cap without full text:
  abstract/snippet-only or URL-only material cannot receive high evidence confidence

decision outcome calibration:
  record recommendation, confidence, user choice, outcome, and future recommendation impact
```

Evidence relation:

```text
supports conceptual adoption as workflow metadata
```

### RKA-A4 Do-Not-Adopt Boundary

Source:

```text
raw/repos/2026-05-29-rka-source.md:117-127
```

Anchor:

```text
full runtime
MCP surface
dashboard
workflow actions as truth changes
SQLite as the Markdown source of truth
automatic background truth mutation
Brier / ECE machinery before there is enough outcome data
```

Evidence relation:

```text
supports rejection of runtime/platform adoption
```

### RKA-A5 Fit To This Vault

Source:

```text
raw/repos/2026-05-29-rka-source.md:129-140
```

Anchor:

```text
RKA is useful as an engineering and workflow reference, not as a skeleton to fork.
...
ordinary capture remains light
ordinary query remains simple
promotion and action basis become more auditable
feedback and outcomes calibrate future recommendation, not truth
```

Evidence relation:

```text
supports scope limit and minimal adoption
```

## Candidate Points

| Point | Type | Evidence granularity | Initial judgment |
|---|---|---|---|
| RKA-P1: RKA review queue taxonomy is reasonable as optional routing metadata. | pattern | excerpt_or_passage with source_hygiene warning | standing with confidence cap |
| RKA-P2: RKA decision superseding should be absorbed as audit-preserving review_due flow. | pattern | excerpt_or_passage with source_hygiene warning | standing with scope limit |
| RKA-P3: RKA runtime / MCP / dashboard should not be adopted into the core. | risk with decision_input intended use | excerpt_or_passage | standing |

## Evidence Packet RKA-P1

```yaml
evidence_packet:
  point: "RKA review queue taxonomy is reasonable as optional routing metadata."
  point_type: pattern
  source_anchors:
    - url_or_path: raw/repos/2026-05-29-rka-source.md
      exact_quote: "review queue item types: low_confidence_claim, contradiction, missing_evidence, synthesis_needed, decision_superseded"
      prefix: "## Adopt"
      suffix: "decision superseding:"
      captured_at: 2026-05-30
    - url_or_path: raw/repos/2026-05-29-rka-source.md
      exact_quote: "Files reviewed: README.md ... rka/models/review_queue.py ... rka/services/review_queue.py"
      prefix: "Files reviewed:"
      suffix: "rka/db/migrations/018_bitemporal_and_calibration.sql"
      captured_at: 2026-05-30
  evidence_items:
    - source_anchor: RKA-A3
      evidence_granularity: excerpt_or_passage
      relation_to_point: supports
      rationale: "The local source record extracts the exact taxonomy intended for adoption."
    - source_anchor: RKA-A2
      evidence_granularity: excerpt_or_passage
      relation_to_point: undercuts
      rationale: "The record says code files were reviewed, but this packet does not include exact code spans, so it cannot claim code-anchor support."
  grounds: "The source record identifies RKA, checked commit, reviewed files, and the extracted review queue taxonomy."
  warrant: "If a source record captures reviewed files and extracted taxonomy, it can support conceptual adoption as candidate routing metadata, but not high-confidence code-level claims without exact code anchors."
  qualifier: "Adopt only as optional routing metadata, not as a new truth node type or runtime behavior."
  strongest_rebuttal: "The local source record does not embed the actual code snippets defining these item types."
  challenge_kind: source_hygiene
  risk_flags:
    - source_record_without_code_anchor
    - confidence_cap
  omission_check:
    missing_risks: "Potential mismatch between source-record extraction and actual code implementation."
    missing_scope_limits: "Does not prove the taxonomy is complete or stable across future commits."
    possible_omissions: "Exact enum definitions, validation logic, and service behavior may be absent from the source record."
    needs_full_source_read: true
  review_question: "Should the taxonomy remain optional until code anchors are captured?"
  minimal_revision_needed: refine_scope
```

Review result:

```yaml
review_result:
  knowledge_state: limited
  strongest_challenge: "No embedded exact code spans for the taxonomy."
  scope_limit: "Conceptual adoption as optional routing metadata only."
  minimal_revision_needed: refine_scope
  review_due_when:
    - source_code_anchor_needed
    - RKA_commit_changes
    - taxonomy_used_for_promotion_or_action_basis
```

## Evidence Packet RKA-P2

```yaml
evidence_packet:
  point: "RKA decision superseding should be absorbed as audit-preserving review_due flow."
  point_type: pattern
  source_anchors:
    - url_or_path: raw/repos/2026-05-29-rka-source.md
      exact_quote: "old decision is not deleted; replacement decision links back to the old decision; affected downstream claims, patterns, relations, and context packs become review_due"
      prefix: "decision superseding:"
      suffix: "intent confirmation / backbrief:"
      captured_at: 2026-05-30
    - url_or_path: raw/repos/2026-05-29-rka-source.md
      exact_quote: "RKA is useful as an engineering and workflow reference, not as a skeleton to fork."
      prefix: "## Fit To This Vault"
      suffix: "feedback and outcomes calibrate future recommendation, not truth"
      captured_at: 2026-05-30
  evidence_items:
    - source_anchor: RKA-A3
      evidence_granularity: excerpt_or_passage
      relation_to_point: supports
      rationale: "The source record states an audit-preserving superseding flow."
    - source_anchor: RKA-A5
      evidence_granularity: excerpt_or_passage
      relation_to_point: limits_scope
      rationale: "The fit section says to use RKA as workflow reference, not skeleton."
  grounds: "The RKA record describes decision replacement without deleting history and marks downstream content review_due."
  warrant: "This maps directly to the vault's existing distinction between applicability changes and truth mutation."
  qualifier: "Absorb as decision/action-basis audit metadata; do not import RKA runtime or database authority."
  strongest_rebuttal: "Without code spans, this packet cannot verify how RKA implements superseding in services/migrations."
  challenge_kind: source_hygiene
  risk_flags:
    - source_record_without_code_anchor
    - runtime_not_adopted
  omission_check:
    missing_risks: "Implementation details may contain behavior not represented in source record."
    missing_scope_limits: "No code-level proof of affected downstream traversal."
    possible_omissions: "Service functions and migration schemas are not quoted."
    needs_full_source_read: true
  review_question: "Is the source record enough for conceptual adoption, or should code anchors be captured before any further schema hardening?"
  minimal_revision_needed: keep
```

Review result:

```yaml
review_result:
  knowledge_state: standing
  strongest_challenge: "Implementation not verified inside this packet."
  scope_limit: "Conceptual review_due flow only."
  minimal_revision_needed: keep
  review_due_when:
    - decision_superseding_used_as_action_basis
    - exact_code_anchor_required
    - RKA_commit_changes
```

## Evidence Packet RKA-P3

```yaml
evidence_packet:
  point: "RKA runtime / MCP / dashboard should not be adopted into the core."
  point_type: risk
  verifiability:
    state: partially_verifiable
    reason: RKA runtime surfaces are source-checkable; rejecting them for this vault is a local architecture risk judgment.
  review_route: risk_check
  intended_use: decision_input
  source_anchors:
    - url_or_path: raw/repos/2026-05-29-rka-source.md
      exact_quote: "full runtime; MCP surface; dashboard; workflow actions as truth changes; SQLite as the Markdown source of truth; automatic background truth mutation"
      prefix: "## Do Not Adopt"
      suffix: "Brier / ECE machinery before there is enough outcome data"
      captured_at: 2026-05-30
    - url_or_path: raw/repos/2026-05-29-rka-source.md
      exact_quote: "RKA is useful as an engineering and workflow reference, not as a skeleton to fork."
      prefix: "## Fit To This Vault"
      suffix: "This vault absorbs the patterns as lazy gates and metadata"
      captured_at: 2026-05-30
  evidence_items:
    - source_anchor: RKA-A4
      evidence_granularity: excerpt_or_passage
      relation_to_point: supports
      rationale: "The source record explicitly lists runtime, MCP, dashboard, SQLite truth source, and automatic mutation as do-not-adopt."
    - source_anchor: RKA-A5
      evidence_granularity: excerpt_or_passage
      relation_to_point: supports
      rationale: "The source record scopes RKA to engineering/workflow reference."
  grounds: "The source record explicitly rejects core adoption of runtime/platform pieces."
  warrant: "The vault's public story and Truth Core remain thin only if RKA stays a reference and not an imported runtime."
  qualifier: "Future API/MCP work may borrow read-only or candidate-only access concepts, but not core write authority."
  strongest_rebuttal: "Some RKA runtime ideas may become useful later after micro-trials."
  challenge_kind: scope_limit
  risk_flags:
    - runtime_creep
    - mcp_write_surface
    - sqlite_truth_source
  omission_check:
    missing_risks: "Does not inspect whether RKA runtime has small components that could be separately useful."
    missing_scope_limits: "Future implementation stage may revisit read-only API patterns."
    possible_omissions: "No dashboard/API source files are quoted."
    needs_full_source_read: false
  review_question: "Should any runtime pieces stay watch-only rather than rejected forever?"
  minimal_revision_needed: reject
```

Review result:

```yaml
review_result:
  knowledge_state: standing
  strongest_challenge: "Future implementation might reuse small runtime ideas."
  scope_limit: "Reject core adoption now; keep runtime/API ideas parked."
  minimal_revision_needed: reject
  review_due_when:
    - agent_api_work_begins
    - mcp_write_surface_reopened
    - runtime_micro_trial_requested
```

## Context Pack Trace

```yaml
context_pack_trace:
  used_sources:
    - raw/repos/2026-05-29-rka-source.md
    - FUSION_ARCHITECTURE_V0_2_DRAFT.md
    - SCHEMA.md
  ignored_sources:
    - live GitHub repository files
    - local raw/repos/_snapshots RKA source tree
  ignored_reason: "The user requested local materials; no RKA source snapshot was found in raw/repos/_snapshots during this trial, and no live fetch was needed for source-record contract testing."
  activation_role: core
  unresolved_contradictions:
    - "Source record says files were reviewed, but this packet lacks exact code spans."
  risk_flags:
    - source_record_without_code_anchor
    - confidence_cap
    - needs_full_source_read_for_code_level_claims
```

## Logic Test Matrix

| Test | Expected | Result |
|---|---|---|
| Source record with checked commit can support conceptual adoption. | support with confidence cap | pass |
| Source record without code snippets cannot support high-confidence code-level claim. | source_hygiene warning | pass |
| Review queue taxonomy remains optional metadata, not truth node type. | refine_scope | pass |
| Decision superseding is audit flow, not truth mutation. | keep with scope limit | pass |
| Runtime / MCP / dashboard adoption is rejected for core. | reject core adoption | pass |
| Missing exact code anchors trigger next-source-read pressure. | needs_full_source_read true | pass |

## Trial Finding

This trial is strongly positive because it found a real boundary issue:

```text
The RKA source record is enough for conceptual adoption.
It is not enough for high-confidence code-level proof.
```

That is exactly the kind of distinction Evidence Packet is supposed to force.

Without Evidence Packet, the vault might over-read the source record as:

```text
RKA code proves this taxonomy and superseding flow.
```

With Evidence Packet, the narrower result is:

```text
RKA source record supports conceptual adoption as optional review / workflow metadata.
Code-level or implementation-level claims need exact source/code anchors.
```

## Decision

```yaml
decision:
  evidence_packet_passed_source_record_trial: true
  keep_rka_taxonomy_as_optional_metadata: true
  keep_decision_superseding_as_audit_flow: true
  reject_rka_runtime_core_adoption: true
  cap_code_level_confidence_until_code_anchors_exist: true
  next_revision: add_source_code_anchor_if_RKA_is_used_for_code_level_claim
```

## Stop Point

Do not fetch or clone RKA automatically.

Next useful step, only if needed:

```text
Open or fetch the exact checked commit and capture code anchors for:
- rka/models/review_queue.py
- rka/services/decisions.py
- rka/db/migrations/014_add_staleness_and_assumptions.sql
```

Until then, RKA remains:

```text
conceptual adoption: usable
workflow source: usable
code-level support source: not yet sufficient
```
