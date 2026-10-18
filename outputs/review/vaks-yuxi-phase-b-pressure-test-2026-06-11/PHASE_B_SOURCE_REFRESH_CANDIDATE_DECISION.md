---
record_kind: sandbox_iteration_decision
status: candidate
project_id: VAKS
created_at: 2026-06-11
truth_boundary: source_refresh_candidate_not_support
action_basis_allowed: false
---

# Phase B Source Refresh Candidate Decision

## Decision

Keep the source-refresh candidate assembly as the next adapter-level sandbox
candidate.

Do not treat refreshed source hashes or refreshed source spans as semantic
support, Evidence Packets, evidence sufficiency, or action basis.

## Compared Against Previous Version

Previous version:

```text
Evidence Support Check candidate assembly
```

That version proved:

```text
Phase B can prepare Evidence Support Check work from retrieval output while
still refusing to assert semantic support.
```

It also surfaced:

```text
68 source hash mismatches
```

This step added:

```text
source hash refresh
source span refresh
refresh status per evidence item
post-refresh mismatch validation
```

It preserved:

```text
evidence support check: pass / 0 errors
evidence envelope: pass / 0 errors
context pack: pass / 0 errors
runtime feasibility: pass / 0 errors
minimal doc patch: pass / 0 errors
contract: pass / 0 errors
approved four-file doc patch only
no original Yuxi runtime claim
```

## Check Result

```text
source refresh status: pass
error count: 0
source refresh count: 90
refresh item count: 389
source_span_available_count: 389
pre_refresh_mismatch_count: 68
post_refresh_mismatch_count: 0
refreshed_item_count: 68
already_current_item_count: 321
blocked_no_source_anchor_count: 2
support_passed_count: 0
support_counts_for_promotion_count: 0
action_basis_allowed_count: 0
evidence_packet_allowed_count: 0
evidence_sufficiency_passed_count: 0
```

## Why This Is Positive

This step proves a narrow but important operational improvement:

```text
the adapter can detect stale source receipts and refresh source-span/hash
snapshots without granting evidence authority
```

The key comparison is:

```text
before refresh: 68 source hash mismatches
after refresh:  0 source hash mismatches
```

The validator checks:

```text
refresh scope is source_hash_and_span_snapshot_only
rerank_or_retrieve_changed stays false
semantic_support_reviewed stays false
every refreshed item keeps span_supports_target = unclear
every refreshed item keeps evidence_role = background_context
no refreshed item counts for promotion
no refresh record becomes action basis or Evidence Packet
support-check / envelope / context-pack / runtime / minimal-doc / contract gates stay green
```

The most important positive signals:

```text
68 stale receipt hashes were refreshed.
321 already-current items stayed current.
389 source spans remained available.
2 no-anchor checks stayed blocked instead of becoming fake evidence.
0 items became reviewed support, promotion support, Evidence Packet, sufficiency pass, or action basis.
```

## Boundary

This decision supports:

```text
use Phase B to refresh source-span/hash snapshots before support review
surface whether a support-check candidate is fresh enough to review
reduce stale-index risk before any human or formal support judgment
```

It does not approve:

```text
semantic support pass
reviewed evidence support
Evidence Packet
Evidence Sufficiency Gate pass
action basis
reviewed support
truth confidence
reviewed relation
runtime / production adoption
original Yuxi full-stack parity
C-lite
Skills
MCP writes
subagents
formal writeback
```

## Next Step

Next adapter-level step should be either:

```text
source-refresh candidate -> refreshed support-check rebuild / delta sandbox
```

or:

```text
commit the already validated four-file documentation patch
```

Do not expand mainline docs or runtime claims without a new gate.
